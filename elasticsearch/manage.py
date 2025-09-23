#!/usr/bin/env python3
"""
ThIRU demo traffic simulator for OpenWISP
- Exposes Prometheus metrics on :9100
- Simulates clients, rx/tx counters, and avg RSSI per device
- Device list is auto-loaded from /opt/openwisp2/demo_devices.txt (one name per line)
  or falls back to ThIRU-AP-1..8 if file not found.
"""

from prometheus_client import start_http_server, Gauge, Counter
import time, random, os, itertools

PORT = int(os.getenv("THIRU_METRICS_PORT", "9100"))
DEVLIST_FILE = os.getenv("THIRU_DEVLIST_FILE", "/opt/openwisp2/demo_devices.txt")

def load_devices():
    if os.path.exists(DEVLIST_FILE):
        with open(DEVLIST_FILE, "r") as f:
            names = [ln.strip() for ln in f if ln.strip()]
            if names:
                return names
    return [f"ThIRU-AP-{i}" for i in range(1, 9)]

devices = load_devices()

# Metrics
clients_g = Gauge('thiru_device_clients', 'Connected clients per AP', ['device'])
rssi_g    = Gauge('thiru_device_avg_rssi_dbm', 'Average RSSI (dBm) per AP', ['device'])
online_g  = Gauge('thiru_device_online', 'Device online status (1=online,0=offline)', ['device'])
rx_c      = Counter('thiru_device_rx_bytes_total', 'RX bytes total per AP', ['device'])
tx_c      = Counter('thiru_device_tx_bytes_total', 'TX bytes total per AP', ['device'])

# Initialize
for d in devices:
    clients_g.labels(d).set(0)
    rssi_g.labels(d).set(-60)
    online_g.labels(d).set(1)
    # Counters start at 0 automatically

# A simple cycle so some APs flap occasionally
flap_cycle = itertools.cycle([0]*60 + [1] + [0]*120 + [1])

def step():
    flap = next(flap_cycle)
    for d in devices:
        # Occasionally mark one AP offline for a few cycles (looks realistic)
        offline = (flap == 1 and hash(d) % 5 == 0)
        online_g.labels(d).set(0 if offline else 1)

        if offline:
            # When offline, keep counters flat and clients 0
            clients_g.labels(d).set(0)
            continue

        # Simulate clients 0..35
        nclients = max(0, int(random.gauss(mu=12, sigma=6)))
        clients_g.labels(d).set(nclients)

        # Simulate avg RSSI around -65 dBm (lower is worse)
        rssi = -60 - abs(random.gauss(0, 7))
        rssi_g.labels(d).set(rssi)

        # Simulate byte increments proportional to clients
        # Between ~50 KB/s and ~3 MB/s total, scaled by clients
        base = random.randint(50_000, 3_000_000)
        factor = 0.5 + (nclients / 30.0)
        incr_rx = int(base * factor * random.uniform(0.7, 1.3))
        incr_tx = int(base * factor * random.uniform(0.5, 1.1))

        rx_c.labels(d).inc(incr_rx)
        tx_c.labels(d).inc(incr_tx)

if __name__ == "__main__":
    start_http_server(PORT)
    print(f"[ThIRU] Fake metrics serving on 0.0.0.0:{PORT} for devices: {', '.join(devices)}")
    while True:
        step()
        time.sleep(5)
