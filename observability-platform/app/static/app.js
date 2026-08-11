const cpu = document.getElementById("cpu");
const memory = document.getElementById("memory");
const disk = document.getElementById("disk");
const uptime = document.getElementById("uptime");
const health = document.getElementById("health");
const services = document.getElementById("services");
const alerts = document.getElementById("alerts");
const history = document.getElementById("history");
const canvas = document.getElementById("metricsChart");
const ctx = canvas.getContext("2d");

let historyData = [];

function formatUptime(seconds) {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    return `${days}d ${hours}h`;
}

function drawChart(data) {
    const width = canvas.clientWidth * devicePixelRatio;
    const height = 235 * devicePixelRatio;

    canvas.width = width;
    canvas.height = height;

    ctx.clearRect(0, 0, width, height);

    if (!data.length) return;

    const values = data.map(item => item.cpu_percent);
    const max = Math.max(100, ...values);
    const min = 0;
    const padding = 20 * devicePixelRatio;

    ctx.strokeStyle = "#1a2b44";
    ctx.lineWidth = 1;

    for (let i = 0; i < 5; i++) {
        const y = padding + ((height - padding * 2) / 4) * i;
        ctx.beginPath();
        ctx.moveTo(padding, y);
        ctx.lineTo(width - padding, y);
        ctx.stroke();
    }

    ctx.strokeStyle = "#318cff";
    ctx.lineWidth = 2 * devicePixelRatio;
    ctx.beginPath();

    values.reverse().forEach((value, index) => {
        const x = padding + (index / Math.max(values.length - 1, 1)) * (width - padding * 2);
        const y = height - padding - ((value - min) / (max - min)) * (height - padding * 2);

        if (index === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });

    ctx.stroke();
}

async function fetchJSON(url) {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return response.json();
}

async function refresh() {
    try {
        const [latest, historyDataResponse, servicesData, alertsData] = await Promise.all([
            fetchJSON("/api/metrics/latest"),
            fetchJSON("/api/metrics/history?limit=30"),
            fetchJSON("/api/services"),
            fetchJSON("/api/alerts")
        ]);

        cpu.textContent = `${latest.cpu_percent.toFixed(1)}%`;
        memory.textContent = `${latest.memory_percent.toFixed(1)}%`;
        disk.textContent = `${latest.disk_percent.toFixed(1)}%`;
        uptime.textContent = formatUptime(latest.uptime_seconds);

        const score = Math.round(
            100 - (
                latest.cpu_percent * 0.35 +
                latest.memory_percent * 0.35 +
                latest.disk_percent * 0.30
            )
        );

        health.textContent = `${Math.max(0, score)}/100`;

        history.innerHTML = historyDataResponse.map(item => `
            <tr>
                <td>${new Date(item.created_at).toLocaleTimeString("pt-BR")}</td>
                <td>${item.cpu_percent.toFixed(1)}%</td>
                <td>${item.memory_percent.toFixed(1)}%</td>
                <td>${item.disk_percent.toFixed(1)}%</td>
            </tr>
        `).join("");

        services.innerHTML = servicesData.map(service => `
            <div class="service">
                <div class="service-name">
                    <span class="online"></span>
                    ${service.service_name}
                </div>
                <span>${service.uptime_percent.toFixed(2)}%</span>
            </div>
        `).join("");

        alerts.innerHTML = alertsData.length
            ? alertsData.map(alert => `
                <div class="alert">
                    <div>
                        <div class="alert-title">${alert.title}</div>
                        <div class="alert-meta">${alert.source}</div>
                    </div>
                    <span class="badge ${alert.severity === "critical" ? "critical" : "warning"}">
                        ${alert.severity}
                    </span>
                </div>
            `).join("")
            : `<div class="alert"><span>✓ No active alerts</span></div>`;

        historyData = historyDataResponse;
        drawChart(historyData);

        document.getElementById("connection").textContent = "● Live";
    } catch (error) {
        console.error(error);
        document.getElementById("connection").textContent = "● Offline";
    }
}

refresh();
setInterval(refresh, 15000);
window.addEventListener("resize", () => drawChart(historyData));
