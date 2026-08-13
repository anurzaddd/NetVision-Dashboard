// Dashboard.js - Real-time update

// نمودار سرعت
const ctx = document.getElementById('speedChart').getContext('2d');
const speedChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [],
        datasets: [
            {
                label: 'ورودی (Mbps)',
                data: [],
                borderColor: '#3498db',
                backgroundColor: 'rgba(52,152,219,0.1)',
                fill: true,
                tension: 0.3,
                pointRadius: 2
            },
            {
                label: 'خروجی (Mbps)',
                data: [],
                borderColor: '#2ecc71',
                backgroundColor: 'rgba(46,204,113,0.1)',
                fill: true,
                tension: 0.3,
                pointRadius: 2
            }
        ]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: true, position: 'top' }
        },
        scales: {
            x: { display: false },
            y: { beginAtZero: true }
        }
    }
});

// نگهداری تاریخچه برای نمودار (حداکثر ۱۰۰ نقطه)
const MAX_POINTS = 60; // 60 * 3s = 3 دقیقه

function updateDashboard() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            // به‌روزرسانی هر سوئیچ
            for (const [ip, info] of Object.entries(data)) {
                // اطلاعات پایه
                document.getElementById(`sysName-${ip}`).textContent = info.sys_name || 'N/A';
                document.getElementById(`sysDesc-${ip}`).textContent = info.sys_desc || 'N/A';
                document.getElementById(`inSpeed-${ip}`).textContent = info.in_speed || 0;
                document.getElementById(`outSpeed-${ip}`).textContent = info.out_speed || 0;

                // پورت‌ها
                const portContainer = document.getElementById(`ports-${ip}`);
                if (portContainer) {
                    portContainer.innerHTML = '';
                    const ports = info.ports || [];
                    ports.forEach(port => {
                        const div = document.createElement('div');
                        div.className = `port-item ${port.status ? 'up' : 'down'} vlan-${port.vlan || 1}`;
                        div.setAttribute('data-index', port.index);
                        div.innerHTML = `<span class="port-label">${port.index}</span>`;
                        portContainer.appendChild(div);
                    });
                }

                // آپلینک‌ها
                const uplinkSpan = document.getElementById(`uplinks-${ip}`);
                if (uplinkSpan) {
                    const uplinks = info.uplinks || [];
                    uplinkSpan.innerHTML = uplinks.map(u => 
                        `<span class="uplink-badge ${u.status ? 'up' : 'down'}">${u.name} (${u.status ? 'فعال' : 'غیرفعال'})</span>`
                    ).join(' ');
                }
            }

            // به‌روزرسانی نمودار سرعت (از اولین سوئیچ)
            const firstSwitch = Object.values(data)[0];
            if (firstSwitch) {
                const inSpeed = firstSwitch.in_speed || 0;
                const outSpeed = firstSwitch.out_speed || 0;
                const now = new Date().toLocaleTimeString();

                speedChart.data.labels.push(now);
                speedChart.data.datasets[0].data.push(inSpeed);
                speedChart.data.datasets[1].data.push(outSpeed);

                if (speedChart.data.labels.length > MAX_POINTS) {
                    speedChart.data.labels.shift();
                    speedChart.data.datasets[0].data.shift();
                    speedChart.data.datasets[1].data.shift();
                }
                speedChart.update();
            }
        })
        .catch(err => console.error('Error fetching data:', err));
}

// به‌روزرسانی هر ۳ ثانیه
setInterval(updateDashboard, 3000);
// اجرای اولیه
updateDashboard();
