import json
from typing import Any
from dataclasses import dataclass

@dataclass
class Field:
    count: int
    types: set[type]
    values: set[Any]

    nullable: bool = False
    unique: bool = False
    minimum: int | None = None
    maximum: int | None = None
    length: int | None = None
    min_len: int | None = None
    max_len: int | None = None
    shortest: Any | None = None
    longest: Any | None = None

    def __repr__(self):
        return {
            "count": self.count,
            "types": self.types,
            # "values": self.values,
            "nullable": self.nullable,
            "unique": self.unique,
            "minimum": self.minimum,
            "maximum": self.maximum,
            "length": self.length,
            "min_len": self.min_len,
            "max_len": self.max_len,
            "shortest": self.shortest,
            "longest": self.longest,
        }.__repr__()

    def __ior__(self, other: Field):
        self.count += other.count
        self.types.update(other.types)
        self.values.update(other.values)

        return self

    def bake(self, total: int):
        self.nullable = total != self.count
        self.unique = len(self.values) == self.count

        if all(hasattr(i, "__lt__") for i in self.values):
            self.minimum = min(self.values)
            self.maximum = max(self.values)

        if all(hasattr(i, "__len__") for i in self.values):
            self.min_len = min(len(v) for v in self.values)
            self.max_len = max(len(v) for v in self.values)

            if self.min_len == self.max_len:
                self.length = self.min_len

            self.shortest = min(self.values, key=len)
            self.longest = max(self.values, key=len)

        return self


@dataclass
class Structure:
    name: str
    fields: dict[str, Field | Structure]

    def __repr__(self):
        return {
            "name": self.name,
            "fields": self.fields,
        }.__repr__()

    def __ior__(self, other: Structure):
        for key, value in other.fields.items():
            if key in self.fields:
                self.fields[key] |= value
            else:
                self.fields[key] = value
        return self

    def bake(self, total: int):
        for field in self.fields:
            self.fields[field].bake(total)

        return self


def fields(item: dict, name: str = "") -> Structure:
    structure = Structure(name, dict())

    for key, value in item.items():
        if isinstance(value, dict):
            structure.fields[key] = fields(value, key)
        elif isinstance(value, list):
            structure.fields[key] = Structure(key, dict())
            for subitem in value:
                structure.fields[key] |= fields(subitem, key)
        elif key not in structure.fields:
            structure.fields[key] = Field(1, set([type(value)]), set([value]))
        else:
            structure.fields[key] |= Field(1, set([type(value)]), set([value]))

    return structure

# Analyze
receipts: list[dict] = json.load(open("test/receipts.json"))
scan = Structure("receipt", dict())
total = len(receipts)

for receipt in receipts:
    scan |= fields(receipt)

scan.bake(total)
out = scan.fields["data"].fields["fiscalData"].fields["receipt"].fields["items"]

print(out)
