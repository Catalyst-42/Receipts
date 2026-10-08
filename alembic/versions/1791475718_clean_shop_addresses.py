"""Clean shop addresses

Revision ID: 411cbb41f600
Revises: c678dad1cf28
Create Date: 2026-10-08 19:08:38.455564

"""

import logging
from typing import Sequence, Union

import httpx
import sqlalchemy as sa

from alembic import op

from src.config import settings

# revision identifiers, used by Alembic.
revision: str = "411cbb41f600"
down_revision: Union[str, Sequence[str], None] = "c678dad1cf28"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def clean_address(client: httpx.Client, address: str) -> tuple[str, float, float]:
    response = client.post(
        "https://cleaner.dadata.ru/api/v1/clean/address", 
        json=[address],
    )
    response.raise_for_status()
    first = response.json()[0]
    return first["result"], float(first["geo_lat"]), float(first["geo_lon"])


def dadata_client() -> httpx.Client:
    return httpx.Client(
        timeout=10,
        headers={
            "content-type": "application/json",
            "accept": "application/json",
            "Authorization": f"Token {settings.dadata_token}",
            "X-Secret": settings.dadata_secret,
        },
    )


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("shops", sa.Column("latitude", sa.Float(), nullable=True))
    op.add_column("shops", sa.Column("longitude", sa.Float(), nullable=True))

    conn = op.get_bind()
    rows = conn.execute(sa.text("SELECT id, address FROM shops")).fetchall()

    with dadata_client() as client:
        for row in rows:
            try:
                cleaned, lat, lon = clean_address(client, row.address)
            except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as e:
                raise RuntimeError(f"Could not clean shop {row.id}: {e}") from e

            conn.execute(
                sa.text(
                    "UPDATE shops "
                    "SET address = :address, latitude = :lat, longitude = :lon "
                    "WHERE id = :id"
                ),
                {"address": cleaned, "lat": lat, "lon": lon, "id": row.id},
            )

    op.alter_column("shops", "latitude", nullable=False)
    op.alter_column("shops", "longitude", nullable=False)
    op.create_check_constraint(
        "ck_shops_latitude_range", "shops", "latitude BETWEEN -90 AND 90"
    )
    op.create_check_constraint(
        "ck_shops_longitude_range", "shops", "longitude BETWEEN -180 AND 180"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("shops", "longitude")
    op.drop_column("shops", "latitude")
