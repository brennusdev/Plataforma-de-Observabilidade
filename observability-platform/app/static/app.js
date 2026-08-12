async function loadApplicationMetrics() {

    try {

        const metrics =
            await fetchJSON(
                "/api/application/metrics?minutes=60"
            );

        const requestCount =
            document.getElementById(
                "requestCount"
            );

        const errorRate =
            document.getElementById(
                "errorRate"
            );

        const avgLatency =
            document.getElementById(
                "avgLatency"
            );

        const p95Latency =
            document.getElementById(
                "p95Latency"
            );

        const p99Latency =
            document.getElementById(
                "p99Latency"
            );


        if (requestCount) {

            requestCount.textContent =
                metrics.request_count;

        }


        if (errorRate) {

            errorRate.textContent =
                `${metrics.error_rate}%`;

        }


        if (avgLatency) {

            avgLatency.textContent =
                `${metrics.average_latency_ms} ms`;

        }


        if (p95Latency) {

            p95Latency.textContent =
                `${metrics.p95_latency_ms} ms`;

        }


        if (p99Latency) {

            p99Latency.textContent =
                `${metrics.p99_latency_ms} ms`;

        }

    } catch (error) {

        console.error(
            "Application metrics error:",
            error
        );
    }
}