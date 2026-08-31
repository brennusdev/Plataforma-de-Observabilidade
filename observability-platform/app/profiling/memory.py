"""
Memory Profiler.

Utiliza tracemalloc para identificar
alocações de memória.
"""

import tracemalloc


def start_memory_profiling() -> None:
    """
    Inicia a coleta de informações
    de memória.
    """

    if not tracemalloc.is_tracing():

        tracemalloc.start()


def stop_memory_profiling() -> None:
    """
    Interrompe a coleta.
    """

    if tracemalloc.is_tracing():

        tracemalloc.stop()


def take_memory_snapshot():
    """
    Cria um snapshot da memória atual.
    """

    if not tracemalloc.is_tracing():

        tracemalloc.start()

    return tracemalloc.take_snapshot()


def compare_memory_snapshots(
    previous_snapshot,
    current_snapshot,
    limit: int = 10,
) -> list[dict]:
    """
    Compara dois snapshots de memória.

    Retorna as maiores diferenças
    encontradas.
    """

    differences = current_snapshot.compare_to(
        previous_snapshot,
        "lineno",
    )

    result = []

    for difference in differences[
        :limit
    ]:

        result.append(
            {
                "file": str(
                    difference.traceback
                ),
                "size_diff": difference.size_diff,
                "count_diff": difference.count_diff,
                "size": difference.size,
                "count": difference.count,
            }
        )

    return result