"""
Correlation Engine.

Relaciona diferentes sinais que ocorreram
aproximadamente no mesmo período.
"""

from datetime import timedelta

from app.intelligence.incident import (
    IncidentSignal,
)


def are_signals_related(
    first: IncidentSignal,
    second: IncidentSignal,
    window_seconds: int = 300,
) -> bool:
    """
    Verifica se dois sinais podem estar
    relacionados temporalmente.

    O padrão é uma janela de 5 minutos.
    """

    difference = abs(
        first.timestamp
        - second.timestamp
    )

    return (
        difference
        <= timedelta(
            seconds=window_seconds
        )
    )


def correlate_signals(
    signals: list[IncidentSignal],
) -> list[list[IncidentSignal]]:
    """
    Agrupa sinais temporalmente relacionados.

    Esta é uma implementação inicial.

    Em versões posteriores poderemos utilizar:

    - dependency graphs;
    - causal inference;
    - statistical correlation;
    - embeddings;
    - machine learning.
    """

    groups = []

    for signal in signals:

        added = False

        for group in groups:

            if any(
                are_signals_related(
                    signal,
                    existing,
                )
                for existing in group
            ):

                group.append(signal)

                added = True

                break

        if not added:

            groups.append(
                [signal]
            )

    return groups