import os
import time
import random
import threading
import psutil
from datetime import datetime
from flask import Flask, render_template_string
from flask_socketio import SocketIO, emit

# --- INITIALIZATION ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'noc_secret_2024'
socketio = SocketIO(app, cors_allowed_origins="*")

# --- GLOBAL DATA STATE ---
class NetworkState:
    def __init__(self):
        self.health_score = 98
        self.packet_loss = 0.2
        self.active_threats = 0
        self.prev_io = psutil.net_io_counters()
        self.ai_logs = []
        self.devices = [
            {"name": "Master-Router", "ip": "192.168.1.1", "mac": "00:1A:2B:3C:4D:5E", "status": "Stable", "usage": "2.5MB/s"},
            {"name": "Admin-PC", "ip": "192.168.1.15", "mac": "AA:BB:CC:DD:EE:FF", "status": "Stable", "usage": "1.2MB/s"},
            {"name": "Unknown-Device", "ip": "10.0.0.55", "mac": "FF:EE:DD:CC:BB:AA", "status": "Suspicious", "usage": "45.8MB/s"},
        ]

state = NetworkState()

# --- AI SELF-HEALING & MONITORING LOGIC ---
def background_monitor():
    while True:
        # 1. Get Real Hardware Stats
        curr_io = psutil.net_io_counters()
        download_speed = (curr_io.bytes_recv - state.prev_io.bytes_recv) / 1024 / 1024
        upload_speed = (curr_io.bytes_sent - state.prev_io.bytes_sent) / 1024 / 1024
        state.prev_io = curr_io
        
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent

        # 2. Simulate AI "Detection"
        packet_loss = round(random.uniform(0.1, 0.5), 2)
        if random.random() > 0.9: packet_loss = round(random.uniform(2.5, 5.0), 2) # Random spike

        # 3. AI Self-Healing Actions
        ai_msg = None
        if packet_loss > 2.0:
            ai_msg = f"⚠️ CRITICAL: High Packet Loss ({packet_loss}%). AI Re-routing traffic to Node-X..."
            state.health_score = max(70, state.health_score - 5)
        elif download_speed > 50:
            ai_msg = "🚀 CONGESTION: High Bandwidth usage. AI Throttling Unassigned Devices..."
        elif cpu > 80:
            ai_msg = "🔥 OVERLOAD: CPU spike detected. AI optimizing background processes..."
        
        if ai_msg:
            log_entry = {"time": datetime.now().strftime("%H:%M:%S"), "msg": ai_msg}
            state.ai_logs.insert(0, log_entry)
            if len(state.ai_logs) > 10: state.ai_logs.pop()

        # 4. Push to Frontend
        socketio.emit('update_data', {
            'download': round(download_speed, 2),
            'upload': round(upload_speed, 2),
            'cpu': cpu,
            'ram': ram,
            'health': state.health_score,
            'packet_loss': packet_loss,
            'threats': state.active_threats,
            'logs': state.ai_logs,
            'time': datetime.now().strftime("%H:%M:%S")
        })
        time.sleep(1)

# --- ROUTES ---
@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE, devices=state.devices)

# --- FUTURISTIC HTML/CSS/JS TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Self-Healing NOC</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500;700&display=swap');
        
        body {
            background-color: #050505;
            color: #e2e8f0;
            font-family: 'Rajdhani', sans-serif;
            overflow-x: hidden;
        }

        .glass {
            background: rgba(15, 15, 15, 0.8);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 102, 0, 0.15);
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
        }

        .orange-glow {
            box-shadow: 0 0 15px rgba(255, 102, 0, 0.3);
            border: 1px solid #ff6600;
        }

        .sidebar-item:hover {
            background: linear-gradient(90deg, rgba(255, 102, 0, 0.2) 0%, transparent 100%);
            border-left: 4px solid #ff6600;
            color: #ff6600;
        }

        .stat-value {
            font-family: 'Orbitron', sans-serif;
            text-shadow: 0 0 10px rgba(255, 102, 0, 0.5);
        }

        .terminal-text {
            font-family: 'Courier New', Courier, monospace;
            color: #ffaa00;
        }

        ::-webkit-scrollbar { width: 5px; }
        ::-webkit-scrollbar-thumb { background: #ff6600; border-radius: 10px; }
    </style>
</head>
<body class="flex h-screen">

    <!-- SIDEBAR -->
    <aside class="w-64 glass h-full flex flex-col border-r border-orange-900/30">
        <div class="p-6 text-center">
            <h1 class="text-2xl font-bold text-orange-500 tracking-widest">NOC_AI <span class="text-xs block text-gray-500">v4.0.2-STABLE</span></h1>
        </div>
        <nav class="flex-1 mt-4">
            <a href="#" class="sidebar-item flex items-center p-4 transition-all text-orange-500 bg-orange-950/10 border-l-4 border-orange-500">
                <i class="fas fa-chart-line mr-3"></i> DASHBOARD
            </a>
            <a href="#" class="sidebar-item flex items-center p-4 transition-all text-gray-400">
                <i class="fas fa-microchip mr-3"></i> AI HEALING ENGINE
            </a>
            <a href="#" class="sidebar-item flex items-center p-4 transition-all text-gray-400">
                <i class="fas fa-network-wired mr-3"></i> TOPOLOGY
            </a>
            <a href="#" class="sidebar-item flex items-center p-4 transition-all text-gray-400">
                <i class="fas fa-shield-virus mr-3"></i> THREAT DETECTION
            </a>
            <a href="#" class="sidebar-item flex items-center p-4 transition-all text-gray-400">
                <i class="fas fa-cog mr-3"></i> SETTINGS
            </a>
        </nav>
        <div class="p-6">
            <div class="p-3 rounded bg-orange-950/20 border border-orange-500/30 text-xs text-orange-400">
                <i class="fas fa-shield-alt mr-2"></i> SYSTEM ENCRYPTED
            </div>
        </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="flex-1 flex flex-col overflow-hidden">
        
        <!-- TOP NAVBAR -->
        <header class="h-16 glass flex items-center justify-between px-8 border-b border-orange-900/30">
            <div class="flex items-center space-x-4">
                <span class="text-green-500 animate-pulse"><i class="fas fa-circle text-[10px] mr-2"></i> LIVE MONITORING</span>
            </div>
            <div class="flex items-center space-x-6">
                <i class="fas fa-search text-gray-500 cursor-pointer"></i>
                <i class="fas fa-bell text-gray-500 cursor-pointer relative">
                    <span class="absolute -top-1 -right-1 bg-red-600 w-2 h-2 rounded-full"></span>
                </i>
                <div class="flex items-center space-x-2 border-l border-gray-800 pl-6">
                    <span class="text-sm font-bold">ADMIN_SYS</span>
                    <img src="https://ui-avatars.com/api/?name=Admin&background=ff6600&color=fff" class="w-8 h-8 rounded-full border border-orange-500">
                </div>
            </div>
        </header>

        <div class="p-8 overflow-y-auto space-y-8">
            
            <!-- TOP STATS CARDS -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div class="glass p-6 rounded-xl hover:scale-105 transition-transform cursor-pointer orange-glow">
                    <p class="text-xs text-gray-500 uppercase tracking-tighter">Download Speed</p>
                    <h2 class="text-3xl font-bold stat-value text-orange-500 mt-2" id="stat-download">0.00</h2>
                    <p class="text-xs text-orange-900 mt-1 font-bold">MBPS / SEC</p>
                </div>
                <div class="glass p-6 rounded-xl hover:scale-105 transition-transform cursor-pointer">
                    <p class="text-xs text-gray-500 uppercase tracking-tighter">Network Health</p>
                    <h2 class="text-3xl font-bold stat-value text-green-500 mt-2" id="stat-health">98%</h2>
                    <p class="text-xs text-green-900 mt-1 font-bold">OPTIMIZED</p>
                </div>
                <div class="glass p-6 rounded-xl hover:scale-105 transition-transform cursor-pointer">
                    <p class="text-xs text-gray-500 uppercase tracking-tighter">Packet Loss</p>
                    <h2 class="text-3xl font-bold stat-value text-red-500 mt-2" id="stat-loss">0.1%</h2>
                    <p class="text-xs text-red-900 mt-1 font-bold">STABLE</p>
                </div>
                <div class="glass p-6 rounded-xl hover:scale-105 transition-transform cursor-pointer">
                    <p class="text-xs text-gray-500 uppercase tracking-tighter">CPU Load</p>
                    <h2 class="text-3xl font-bold stat-value text-blue-500 mt-2" id="stat-cpu">12%</h2>
                    <p class="text-xs text-blue-900 mt-1 font-bold">RESOURCES</p>
                </div>
            </div>

            <!-- GRAPHS & AI LOGS -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div class="lg:col-span-2 glass p-6 rounded-xl">
                    <h3 class="text-lg font-bold mb-4 text-orange-500"><i class="fas fa-wave-square mr-2"></i> REAL-TIME TRAFFIC FLOW</h3>
                    <canvas id="trafficChart" height="120"></canvas>
                </div>
                <div class="glass p-6 rounded-xl flex flex-col">
                    <h3 class="text-lg font-bold mb-4 text-orange-500"><i class="fas fa-brain mr-2"></i> AI ENGINE LOGS</h3>
                    <div id="ai-logs" class="flex-1 space-y-3 overflow-y-auto terminal-text text-xs p-4 bg-black/50 rounded-lg border border-orange-900/20">
                        <p>> System Initialization Successful...</p>
                        <p>> AI Core Monitoring Active...</p>
                    </div>
                </div>
            </div>

            <!-- DEVICE TABLE -->
            <div class="glass p-6 rounded-xl">
                <h3 class="text-lg font-bold mb-4 text-orange-500"><i class="fas fa-laptop-code mr-2"></i> CONNECTED DEVICES MONITOR</h3>
                <table class="w-full text-left">
                    <thead>
                        <tr class="text-gray-500 border-b border-gray-800 text-sm">
                            <th class="pb-3">DEVICE NAME</th>
                            <th class="pb-3">IP ADDRESS</th>
                            <th class="pb-3">MAC ADDRESS</th>
                            <th class="pb-3">TRAFFIC</th>
                            <th class="pb-3">STATUS</th>
                        </tr>
                    </thead>
                    <tbody class="text-sm">
                        {% for device in devices %}
                        <tr class="border-b border-gray-900/50 hover:bg-white/5 transition-colors">
                            <td class="py-4">{{ device.name }}</td>
                            <td class="py-4">{{ device.ip }}</td>
                            <td class="py-4 font-mono text-gray-400">{{ device.mac }}</td>
                            <td class="py-4 text-orange-500">{{ device.usage }}</td>
                            <td class="py-4">
                                <span class="px-2 py-1 rounded text-[10px] uppercase font-bold 
                                    {{ 'bg-green-950 text-green-500' if device.status == 'Stable' else 'bg-red-950 text-red-500 animate-pulse' }}">
                                    {{ device.status }}
                                </span>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>

        </div>
    </main>

    <script>
        const socket = io();
        const ctx = document.getElementById('trafficChart').getContext('2d');

        // CHART CONFIG
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Bandwidth (MB/s)',
                    borderColor: '#ff6600',
                    backgroundColor: 'rgba(255, 102, 0, 0.1)',
                    borderWidth: 2,
                    data: [],
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0
                }]
            },
            options: {
                responsive: true,
                scales: {
                    x: { display: false },
                    y: { grid: { color: '#1a1a1a' }, ticks: { color: '#555' } }
                },
                plugins: { legend: { display: false } }
            }
        });

        // SOCKET UPDATES
        socket.on('update_data', function(data) {
            // Update Stats
            document.getElementById('stat-download').innerText = data.download;
            document.getElementById('stat-health').innerText = data.health + "%";
            document.getElementById('stat-loss').innerText = data.packet_loss + "%";
            document.getElementById('stat-cpu').innerText = data.cpu + "%";

            // Update Chart
            chart.data.labels.push(data.time);
            chart.data.datasets[0].data.push(data.download);
            if (chart.data.labels.length > 20) {
                chart.data.labels.shift();
                chart.data.datasets[0].data.shift();
            }
            chart.update('none');

            // Update Logs
            const logContainer = document.getElementById('ai-logs');
            logContainer.innerHTML = '';
            data.logs.forEach(log => {
                const p = document.createElement('p');
                p.innerHTML = `<span class="text-gray-600">[${log.time}]</span> <span class="text-orange-400">> ${log.msg}</span>`;
                logContainer.appendChild(p);
            });
        });
    </script>
</body>
</html>
"""

# --- START APP ---
if __name__ == '__main__':
    # Start the monitoring thread
    monitor_thread = threading.Thread(target=background_monitor, daemon=True)
    monitor_thread.start()
    
    # Run Flask
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
