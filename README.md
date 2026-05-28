# Cisco IOS-XE Automated S2S Policy-Based VPN Data Collector

## 🎯 Project Overview
This project was developed as a hands-on training exercise to demonstrate modern **NetDevOps** and network automation capabilities. The goal of the utility is to programmatically connect to multiple Cisco IOS-XE enterprise routers, parse complex running configurations, and consolidate Site-to-Site (S2S) Policy-Based VPN IKEv2/IPSec parameters into a standardized format for documentation and compliance auditing.

By moving away from legacy CLI "screen-scraping," this script leverages structured APIs and programmatic data models to interact with network infrastructure.

## 🛠️ Technologies & Skills Demonstrated
* **Network Protocols & APIs:** NETCONF (Port 830), YANG Data Models (`Cisco-IOS-XE-crypto`)
* **Automation Libraries:** `ncclient` (Python NETCONF client), `xml.etree.ElementTree`
* **Data Science & Analytics:** `pandas` (DataFrames, relational left-joins)
* **Data Structures:** Parsing hierarchical XML configuration trees using specific **XPath** expressions.
* **Defensive Coding:** Fail-safe exception handling for common network issues (SSH drops, authentication failures) and automated error logging (`logging`).

## 📋 Prerequisites & Setup
1. **Network Device Requirement:** NETCONF must be enabled on the target Cisco IOS-XE devices:
   netconf-yang
2. In root directory 'devices.csv' file should be created detailing network topology (example of such file you can find in repository)

## 💻 How to Run the Script
1. install all required Python modules
2. run script from terminal:
   - [user@machine]$ python vpn_data_collector.py

## 📊 Standardized Output
```text
VPN_NAME        LOCAL_IP_ADDR  3rdParty_REMOTE_ADDRESS  IKE_LIFETIME  IKE_AUTH_TYPE  CRYPTO_MAP_PFS_GROUP  IPSEC_TRANSFORM_SET      IPSEC_LIFETIME
S2S_Branch1     192.168.1.1    172.16.0.1               28800         pre-share      group20               AES_CBC_256_HMAC_SHA256  28800
S2S_Branch2     192.168.1.1    10.10.10.10              28800         pre-share      group14               AES_CBC_256_HMAC_SHA256  14400
AZURE_Transit   192.168.0.1    1.2.3.4                  86400         pre-share      group10               AES_CBC_256_HMAC_SHA256  None



## Disclaimer
Script **might not** work for every possible S2S Tunnel configuration, might crash by oversight, it collects only portion of data from the configuration, and eventually might be extended with more featues by anyone.
Script should be tested in staging/lab environment first before using it on production systems.
