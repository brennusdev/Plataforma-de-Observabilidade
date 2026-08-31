"""
CPU Profiler.

Utiliza cProfile, ferramenta nativa do Python,
para identificar onde o programa está gastando
tempo de execução.
"""

import cProfile
import io
import pstats
from typing import Callable


def profile_function(
    function: Callable,
    *args,
    **kwargs,
) -> list[dict]:
    """
    Executa uma função através do profiler
    e retorna os principais hotspots.

    Parameters
    ----------
    function:
        Função que será analisada.

    *args:
        Argumentos posicionais.

    **kwargs:
        Argumentos nomeados.
    """

    profiler = cProfile.Profile()

    profiler.enable()

    try:
        function(
            *args,
            **kwargs,
        )

    finally:
        profiler.disable()

    stream = io.StringIO()

    stats = pstats.Stats(
        profiler,
        stream=stream,
    )

    stats.sort_stats(
        "cumulative"
    )

    hotspots = []

    for (
        filename,
        line_number,
        function_name,
    ), (
        primitive_calls,
        total_calls,
        total_time,
        cumulative_time,
        callers,
    ) in stats.stats.items():

        hotspots.append(
            {
                "filename": filename,
                "line": line_number,
                "function": function_name,
                "primitive_calls": primitive_calls,
                "total_calls": total_calls,
                "total_time": round(
                    total_time,
                    6,
                ),
                "cumulative_time": round(
                    cumulative_time,
                    6,
                ),
            }
        )

    return sorted(
        hotspots,
        key=lambda item:
        item["cumulative_time"],
        reverse=True,
    )