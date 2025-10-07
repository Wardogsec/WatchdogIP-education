# 🛡️ Valkry – IP Detection

Valkry is a lightweight Python tool designed for **endpoint IP visibility** on Linux systems.  
It allows defenders, researchers, and penetration testers to quickly **analyze inbound network activity** over a user-defined time frame using Suricata's `eve.json` logs.

By default, Valkry scans the **last 24 hours** and displays **all IPs that have accessed the target endpoint**, providing clean, color-coded output directly in your terminal.

---

## ✨ Features

- 📅 **Custom Time Window** – Search inbound IP activity over any number of hours (default: 24h).  
- 🌐 **Inbound IP Detection** – Identifies which external/local IPs accessed your target endpoint.  
- 🧠 **IP Labeling Engine** – Auto-labels IPs (e.g., Router, VPN, Local, Unknown).  
- 🎨 **Rich Terminal UI** – Uses [Rich](https://github.com/Textualize/rich) for beautiful, colorized tables.  
- 🧪 **Standalone Script** – No agent or daemon required. Run it and get results immediately.

---

## 🧰 Requirements

- **Python**: `>=3.8`  
- **Suricata** installed and actively logging to `/var/log/suricata/eve.json`  
- **Dependencies**:  
  ```bash
  pip install rich
🚀 Installation
Clone the repository and make the script executable:

bash
Copy code
git clone https://github.com/yourusername/valkry.git
cd valkry
chmod +x beelink_security.py
(Optional) Install dependencies globally or inside a virtual environment:

bash
Copy code
pip install -r requirements.txt
📝 requirements.txt should contain at least:

nginx
Copy code
rich
🧠 Usage
🔸 Basic Scan (24h by default)
Detect all inbound IPs hitting the endpoint in the past 24 hours:

bash
Copy code
sudo python3 beelink_security.py
🔸 Custom Time Frame
Search inbound IPs over the past 6 hours:

bash
Copy code
sudo python3 beelink_security.py --hours 6
🔸 Custom Destination IP
If your target endpoint has a different IP:

bash
Copy code
sudo python3 beelink_security.py --dest-ip 192.168.1.50 --hours 12
🔸 Limit Output
Limit to the last 20 events:

bash
Copy code
sudo python3 beelink_security.py --count 20
📊 Example Output
text
Copy code
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━┳━━━━━━┓
┃ Timestamp           ┃ IP           ┃ Label        ┃ Proto ┃ Port ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━╇━━━━━━┩
│ 2025-10-07 11:45:22 │ 37.19.221.247│ ProtonVPN    │ TCP   │ 443  │
│ 2025-10-07 10:12:03 │ 192.168.0.29 │ Mac-Local    │ UDP   │ 137  │
│ 2025-10-07 09:48:51 │ 192.168.64.12│ Kali-Local   │ TCP   │ 22   │
│ 2025-10-07 08:15:30 │ 8.8.8.8      │ Unknown      │ ICMP  │      │
└─────────────────────┴──────────────┴──────────────┴───────┴──────┘
🧭 How It Works
Valkry reads the Suricata eve.json log file line by line and:

Parses JSON flow events.

Filters traffic inbound to the specified target IP.

Checks whether each event falls within the user-specified time frame.

Labels the IP (if it matches known sets) or marks as Unknown.

Displays results in a rich table with timestamps, protocol, and port.

🧱 File Structure
bash
Copy code
valkry/
├── beelink_security.py      # Main Valkry script
├── requirements.txt         # Python dependencies
└── README.md                # This file
⚠️ Legal Disclaimer
This project is intended for defensive security, research, and authorized testing only.
Running Valkry against systems you do not own or have explicit permission to monitor may violate laws.

📌 Always ensure you comply with local regulations and have proper authorization before use.

🧑‍💻 Contributing
Contributions are welcome!

🐛 Report issues in the Issues tab

💡 Submit enhancements via pull requests

Please follow standard GitHub contribution etiquette.

📜 License
This project is licensed under the MIT License – see LICENSE for details.

⭐ Acknowledgments
Suricata for powerful network visibility.

Rich for terminal formatting.

Inspired by modern red team/blue team workflows.

Made with 🛡️ by BlackInferno

