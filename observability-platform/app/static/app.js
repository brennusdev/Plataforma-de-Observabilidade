async function loadAlertEngine() {

    const container =
        document.getElementById(
            "alertEngine"
        );

    if (!container) {
        return;
    }

    try {

        const alerts =
            await fetchJSON(
                "/api/alerts/active"
            );

        if (!alerts.length) {

            container.innerHTML = `
                <div class="alert">
                    <span>
                        ✓ System operating normally
                    </span>
                </div>
            `;

            return;
        }

        container.innerHTML =
            alerts.map(
                alert => `
                    <div class="alert">

                        <div>

                            <div class="alert-title">
                                ${alert.title}
                            </div>

                            <div class="alert-meta">
                                ${alert.metric}
                                =
                                ${alert.value.toFixed(1)}
                                /
                                threshold:
                                ${alert.threshold}
                            </div>

                        </div>

                        <span class="badge ${
                            alert.severity === "critical"
                                ? "critical"
                                : "warning"
                        }">
                            ${alert.severity}
                        </span>

                    </div>
                `
            ).join("");

    } catch (error) {

        console.error(
            "Alert Engine error:",
            error
        );

        container.innerHTML = `
            <div class="alert">
                Unable to load alert engine.
            </div>
        `;
    }
}

async function refresh() {

    await loadAlertEngine();

}