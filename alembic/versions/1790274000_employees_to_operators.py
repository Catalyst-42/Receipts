"""Rename employees database objects to operators.

Revision ID: 1790274000
Revises: eb2b310dfb4f

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "1790274000"
down_revision: Union[str, Sequence[str], None] = "eb2b310dfb4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _rename_constraint(table: str, old_name: str, new_name: str) -> None:
    op.execute(
        sa.text(f'ALTER TABLE "{table}" RENAME CONSTRAINT "{old_name}" TO "{new_name}"')
    )


def _rename_index(old_name: str, new_name: str) -> None:
    op.execute(sa.text(f'ALTER INDEX "{old_name}" RENAME TO "{new_name}"'))


def upgrade() -> None:
    op.rename_table("employees", "operators")
    op.alter_column(
        "receipts",
        "employee_id",
        new_column_name="operator_id",
        existing_type=sa.UUID(),
    )

    _rename_constraint("operators", "pk_employees", "pk_operators")
    _rename_constraint("operators", "uq_employees_shop_id", "uq_operators_shop_id")
    _rename_constraint(
        "operators",
        "fk_employees_retailer_id_retailers",
        "fk_operators_retailer_id_retailers",
    )
    _rename_constraint(
        "operators",
        "fk_employees_shop_id_shops",
        "fk_operators_shop_id_shops",
    )
    _rename_constraint(
        "receipts",
        "fk_receipts_employee_id_employees",
        "fk_receipts_operator_id_operators",
    )

    _rename_index("ix_employees_retailer_id", "ix_operators_retailer_id")
    _rename_index("ix_employees_shop_id", "ix_operators_shop_id")
    _rename_index(
        "ix_employees_retailer_name_null_shop",
        "ix_operators_retailer_name_null_shop",
    )
    _rename_index("ix_receipts_employee_id", "ix_receipts_operator_id")


def downgrade() -> None:
    _rename_index("ix_receipts_operator_id", "ix_receipts_employee_id")
    _rename_index(
        "ix_operators_retailer_name_null_shop",
        "ix_employees_retailer_name_null_shop",
    )
    _rename_index("ix_operators_shop_id", "ix_employees_shop_id")
    _rename_index("ix_operators_retailer_id", "ix_employees_retailer_id")

    _rename_constraint(
        "receipts",
        "fk_receipts_operator_id_operators",
        "fk_receipts_employee_id_employees",
    )
    _rename_constraint(
        "operators",
        "fk_operators_shop_id_shops",
        "fk_employees_shop_id_shops",
    )
    _rename_constraint(
        "operators",
        "fk_operators_retailer_id_retailers",
        "fk_employees_retailer_id_retailers",
    )
    _rename_constraint("operators", "uq_operators_shop_id", "uq_employees_shop_id")
    _rename_constraint("operators", "pk_operators", "pk_employees")

    op.alter_column(
        "receipts",
        "operator_id",
        new_column_name="employee_id",
        existing_type=sa.UUID(),
    )
    op.rename_table("operators", "employees")
