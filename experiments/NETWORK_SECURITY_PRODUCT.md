This is a high-value proposition. In an era of ubiquitous TLS 1.3 encryption, payload inspection is increasingly blinded. Moving the detection logic from **Content (what is said)** to **Context (when it is said)** is the correct strategic pivot.

Here is a blueprint for the MVP and a technical integration roadmap.

---

### 1. The MVP Strategy: "The Sidecar Approach"
An MVP should not attempt to ingest all raw PCAP (too expensive/heavy). Instead, the MVP should focus on **NetFlow/IPFIX or VPC Flow Logs**. These are metadata-only, low-volume, and already indexed in the SIEM.

**MVP Core Features:**
*   **Scope:** Focus on a single "Critical Subnet" or "High-Value Asset" list (rather than the whole enterprise).
*   **The Engine:** A Python-based microservice that uses **Lomb-Scargle Periodograms** (better than FFT for unevenly sampled network data) to identify periodicities in inter-arrival times (IAT).
*   **Detection Logic:** Identify peaks in the frequency domain that correlate with a "heartbeat" pattern.
*   **Output:** A "Beaconing Score" (0–100) and a "Periodicity Estimate" (e.g., "Detected signal every 300 seconds with 10% jitter").
*   **Alerting:** Push a single, high-fidelity alert back to the SIEM dashboard.

**What the MVP is NOT:**
*   It is not a packet capture tool.
*   It does not do deep packet inspection (DPI).
*   It does not attempt to identify the *type* of malware (it only identifies the *behavior*).

---

### 2. Technical Architecture (The "Sidecar" Model)
To ensure low friction for the customer, the product should act as a **"Compute Sidecar."** It queries the existing SIEM data, processes it externally, and writes results back.

1.  **Ingestion Layer:** Pulls Flow Logs via API from Splunk/Elastic.
2.  **Feature Engineering Layer:** Calculates Inter-Arrival Time (IAT) and packet size variance for specific (SrcIP, DwellIP, DstPort) tuples.
3.  **Spectral Engine:** Applies the Lomb-Scargle algorithm to the IAT series.
4.  **Thresholding:** Uses an adaptive threshold (e.g., Median Absolute Deviation) to distinguish between "natural" periodic traffic (NTP, Windows Updates) and "anomalous" traffic (C2).
5.  **Feedback Loop:** Writes the anomaly metadata back to the SIEM as a new index/lookup table.

---

### 3. SIEM Integration Map

To achieve the $K–$10K/month pricing, you must integrate natively so the SOC analyst never has to leave their primary interface.

#### **A. Splunk Integration**
*   **Data Retrieval:** Use the **Splunk Search API (`search/jobs`)**. Your plugin will submit a SPL (Splunk Processing Language) query to extract `_time`, `src_ip`, `dest_ip`, and `bytes`.
*   **Implementation:** Develop a **Splunk Add-on (TA - Technology Add-on)**.
*   **Output/Visualization:** 
    *   **Custom Dashboard:** Use Splunk Dashboard Studio to visualize the "Frequency Spectrum" (the power spectral density).
    *   **Alerting:** Use the **Splunk Alert Actions API** to trigger native Splunk alerts when your sidecar detects a spike.
*   **The "Hook":** Use a **Splunk Modular Input**. This allows your Python engine to run as a scheduled task within the Splunk environment.

#### **B. Elastic (ELK) Integration**
*   **Data Retrieval:** Use the **Elasticsearch Query DSL** via the Python `elasticsearch` client. You will query the `packetbeat-*` or `flow-*` indices.
*   **Implementation:** A **Logstash Filter Plugin** or a standalone **Kibana App**.
*   **Output/Visualization:**
    *   **Kibana Lens:** Create custom visualizations showing the "Periodicity Score" over time.
    *   **Elasticsearch Watcher:** Use the Watcher API to trigger alerts in the Elastic Stack when the sidecar detects a new frequency peak.
*   **The "Hook":** Leverage **Kibana Canvas** to create high-level executive "Threat Heatmaps" based on your spectral findings.

---

### 4. The "Moat": How to scale to $10K/month
To justify the premium price, you must move from "Detecting a beat" to "Contextual Intelligence."

*   **Jitter Analysis:** Advanced C2 (like Cobalt Strike) uses "jitter" to break periodicity. Your product must be able to detect "broken" periodicity (e.g., a signal that is 30s $\pm$ 25%).
*   **Baseline Auto-Tuning:** The system should automatically learn the "normal" heartbeat of enterprise services (like NTP or OS telemetry) so it doesn't create false positives.
*   **Graph Integration:** Don't just report an IP; report a **connection chain**. "This periodic signal from Host A is communicating with an IP that was recently seen in a DNS tunneling event."

### Summary Table for Pitch Deck

| Feature | MVP (The Hook) | Enterprise (The $10K/mo) |
| :--- | :--- | :--- |
| **Data Source** | NetFlow / VPC Flow Logs | Full Packet Metadata / PCAP |
| **Algorithm** | Basic FFT (Fast Fourier) | Lomb-Scargle + Jitter Modeling |
| **Detection** | Fixed-interval heartbeats | Adaptive, high-jitter C2 detection |
| **UI** | Simple Alerting | Interactive Spectral Dashboards |
| **Integration** | API Polling (Pull) | Native Splunk/Elastic Sidecar (Push/Pull) |
