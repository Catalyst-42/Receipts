"""Remove _orm postfix from database object names.

Revision ID: eb2b310dfb4f
Revises: d0ec47c86e3d
Create Date: 2026-09-24 21:13:36.263657

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "eb2b310dfb4f"
down_revision: Union[str, Sequence[str], None] = "d0ec47c86e3d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLES = (
    ("crpt_orm", "crpt"),
    ("measures_orm", "measures"),
    ("nds_orm", "nds"),
    ("payments_orm", "payments"),
    ("products_orm", "products"),
    ("retailers_orm", "retailers"),
    ("users_orm", "users"),
    ("shops_orm", "shops"),
    ("employees_orm", "employees"),
    ("receipts_orm", "receipts"),
    ("items_orm", "items"),
)

CONSTRAINTS = (
    ("retailers_orm", "pk_retailers_orm", "pk_retailers"),
    ("retailers_orm", "uq_retailers_orm_inn", "uq_retailers_inn"),
    ("users_orm", "pk_users_orm", "pk_users"),
    ("users_orm", "uq_users_orm_username", "uq_users_username"),
    ("shops_orm", "pk_shops_orm", "pk_shops"),
    ("shops_orm", "uq_shops_orm_retailer_id", "uq_shops_retailer_id"),
    (
        "shops_orm",
        "fk_shops_orm_retailer_id_retailers_orm",
        "fk_shops_retailer_id_retailers",
    ),
    ("employees_orm", "pk_employees_orm", "pk_employees"),
    ("employees_orm", "uq_employees_orm_shop_id", "uq_employees_shop_id"),
    (
        "employees_orm",
        "fk_employees_orm_retailer_id_retailers_orm",
        "fk_employees_retailer_id_retailers",
    ),
    (
        "employees_orm",
        "fk_employees_orm_shop_id_shops_orm",
        "fk_employees_shop_id_shops",
    ),
    ("receipts_orm", "pk_receipts_orm", "pk_receipts"),
    ("receipts_orm", "uq_receipts_orm_crpt_id", "uq_receipts_crpt_id"),
    ("receipts_orm", "uq_receipts_orm_t", "uq_receipts_t"),
    ("receipts_orm", "fk_receipts_orm_crpt_id_crpt_orm", "fk_receipts_crpt_id_crpt"),
    (
        "receipts_orm",
        "fk_receipts_orm_employee_id_employees_orm",
        "fk_receipts_employee_id_employees",
    ),
    (
        "receipts_orm",
        "fk_receipts_orm_owner_id_users_orm",
        "fk_receipts_owner_id_users",
    ),
    (
        "receipts_orm",
        "fk_receipts_orm_retailer_id_retailers_orm",
        "fk_receipts_retailer_id_retailers",
    ),
    ("receipts_orm", "fk_receipts_orm_shop_id_shops_orm", "fk_receipts_shop_id_shops"),
    ("items_orm", "pk_items_orm", "pk_items"),
    ("items_orm", "fk_items_orm_measure_measures_orm", "fk_items_measure_measures"),
    ("items_orm", "fk_items_orm_nds_nds_orm", "fk_items_nds_nds"),
    ("items_orm", "fk_items_orm_payment_payments_orm", "fk_items_payment_payments"),
    ("items_orm", "fk_items_orm_product_products_orm", "fk_items_product_products"),
    (
        "items_orm",
        "fk_items_orm_receipt_id_receipts_orm",
        "fk_items_receipt_id_receipts",
    ),
    ("measures_orm", "pk_measures_orm", "pk_measures"),
    ("nds_orm", "pk_nds_orm", "pk_nds"),
    ("payments_orm", "pk_payments_orm", "pk_payments"),
    ("products_orm", "pk_products_orm", "pk_products"),
    ("crpt_orm", "pk_crpt_orm", "pk_crpt"),
)

INDEXES = (
    ("ix_shops_orm_retailer_id", "ix_shops_retailer_id"),
    ("ix_employees_orm_retailer_id", "ix_employees_retailer_id"),
    ("ix_employees_orm_shop_id", "ix_employees_shop_id"),
    ("ix_receipts_orm_employee_id", "ix_receipts_employee_id"),
    ("ix_receipts_orm_owner_id", "ix_receipts_owner_id"),
    ("ix_receipts_orm_retailer_id", "ix_receipts_retailer_id"),
    ("ix_receipts_orm_shop_id", "ix_receipts_shop_id"),
    ("ix_items_orm_measure", "ix_items_measure"),
    ("ix_items_orm_nds", "ix_items_nds"),
    ("ix_items_orm_payment", "ix_items_payment"),
    ("ix_items_orm_product", "ix_items_product"),
    ("ix_items_orm_receipt_id", "ix_items_receipt_id"),
)

SEQUENCES = (
    ("measures_orm_id_seq", "measures_id_seq"),
    ("nds_orm_id_seq", "nds_id_seq"),
    ("payments_orm_id_seq", "payments_id_seq"),
    ("products_orm_id_seq", "products_id_seq"),
)


def _rename_constraint(table: str, old_name: str, new_name: str) -> None:
    op.execute(
        sa.text(f'ALTER TABLE "{table}" RENAME CONSTRAINT "{old_name}" TO "{new_name}"')
    )


def _rename_index(old_name: str, new_name: str) -> None:
    op.execute(sa.text(f'ALTER INDEX IF EXISTS "{old_name}" RENAME TO "{new_name}"'))


def _rename_sequence(old_name: str, new_name: str) -> None:
    op.execute(sa.text(f'ALTER SEQUENCE IF EXISTS "{old_name}" RENAME TO "{new_name}"'))


def upgrade() -> None:
    for old_name, new_name in TABLES:
        op.rename_table(old_name, new_name)

    for table, old_name, new_name in CONSTRAINTS:
        _rename_constraint(table.removesuffix("_orm"), old_name, new_name)

    for old_name, new_name in INDEXES:
        _rename_index(old_name, new_name)

    for old_name, new_name in SEQUENCES:
        _rename_sequence(old_name, new_name)


def downgrade() -> None:
    for new_name, old_name in reversed(SEQUENCES):
        _rename_sequence(new_name, old_name)

    for new_name, old_name in reversed(INDEXES):
        _rename_index(new_name, old_name)

    for table, old_name, new_name in reversed(CONSTRAINTS):
        _rename_constraint(table.removesuffix("_orm"), new_name, old_name)

    for old_name, new_name in reversed(TABLES):
        op.rename_table(new_name, old_name)
