"""
Modelos de banco de dados relacionados
aos experimentos de Chaos Engineering.
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.core.database import Base


class ChaosExperiment(Base):
    """
    Representa um experimento de caos.

    Cada experimento registra:

    - qual falha foi executada;
    - qual serviço foi afetado;
    - quando começou;
    - quando terminou;
    - impacto;
    - tempo de recuperação;
    - resultado.
    """

    __tablename__ = "chaos_experiments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    experiment_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    target_service: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="created",
    )

    started_at: Mapped[datetime | None] = (
        mapped_column(
            DateTime,
            nullable=True,
        )
    )

    finished_at: Mapped[datetime | None] = (
        mapped_column(
            DateTime,
            nullable=True,
        )
    )

    recovery_time: Mapped[float | None] = (
        mapped_column(
            Float,
            nullable=True,
        )
    )

    impact_score: Mapped[float | None] = (
        mapped_column(
            Float,
            nullable=True,
        )
    )

    blast_radius: Mapped[float | None] = (
        mapped_column(
            Float,
            nullable=True,
        )
    )

    result: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )