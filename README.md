# Cisco IOS-XE Automated S2S Policy-Based VPN Data Collector

## 🎯 Project Overview
This project was developed as a hands-on training exercise to demonstrate modern **NetDevOps** and network automation capabilities. The goal of the utility is to programmatically connect to multiple Cisco IOS-XE enterprise routers, parse complex running configurations, and consolidate Site-to-Site (S2S) Policy-Based VPN parameters into a standardized format for documentation and compliance auditing.

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
