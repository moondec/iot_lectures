# IoT Lecture Presentations - Slide Descriptions

## Lecture 1: Internet of Things - From Concept to Industry 4.0
### From Automation to Ubiquity (Lecture 1)

---

### Slide 1: Title Slide
**Introduction: Technology and Reality**
Opening slide introducing the first lecture on IoT fundamentals. Sets the stage for understanding how IoT transforms from a technical concept to ubiquitous technology in Industry 4.0.

---

### Slide 2: Technology Will Set You Free?
**Critical perspective on technological buzzwords**
This slide presents a cautionary quote from Yuval Noah Harari's "21 Lessons for the 21st Century" about how ordinary people feel disconnected from concepts like globalization, blockchain, AI, and IoT. It challenges the audience to recognize that these technologies affect everyone, even when they seem abstract.

---

### Slide 3: The Bright Side: IoT Benefits
**Five key benefits of IoT technology**
Presents the positive aspects of IoT: (1) expanded environmental knowledge, (2) improved medical care through self-tracking, (3) sustainable resource management, (4) Industry 4.0 production optimization, and (5) instant vector communication. Emphasizes data-driven optimization as the core of 21st-century engineering.

---

### Slide 4: IoT in Agriculture: Crop and Ecosystem Monitoring
**Precision agriculture applications**
Shows how IoT replaces traditional farming intuition with integrated monitoring systems. Covers microclimate analysis in leaf canopies, AI-driven pesticide minimization, and soil sensors for NPK and pH monitoring to prevent groundwater contamination.

---

### Slide 5: Medicine – Know Yourself (Smart Wearables)
**Quantified Self movement and health tracking**
Discusses smart wearables like fitness bands and rings (featuring the Oura Ring) that perform continuous health monitoring including HRV and oxygen saturation. Explains how these devices build population-scale AI diagnosis databases through continuous biological data collection.

---

### Slide 6: Industry 4.0: Process Monitoring
**Industrial IoT (IIoT) applications**
Focuses on predictive maintenance in manufacturing, showing how vibration sensors detect equipment failures before they occur. Discusses digital twins of production facilities and automation that minimizes downtime in global supply chains.

---

### Slide 7: IoT & AI Cycle – The Future, and Now?
**Four generations of data processing evolution**
Presents the historical progression: Generation 1.0 (manual labor), Generation 2.0 (mechanical machines), Generation 3.0 (mathematical prediction and ERP systems), and Generation 4.0 (IoT + AI/ML integration). Explains how modern systems use edge computing and natural language interfaces.

---

### Slide 8: Prologue: The Desire that Began the Digital Ecosystem
**Historical context: Evolution of communication**
Traces the history of data transmission from the 1832 electromagnetic telegraph through Morse code (1844), telephone (1876), first wearable computer (1955), to ARPANET (1969). Shows how the need for remote data transmission drove IoT development.

---

### Slide 9: Founding Myth: Desire
**The Coca-Cola machine story (Carnegie Mellon, 1982)**
Tells the origin story of IoT: CMU students connected a vending machine to the local network to check drink availability remotely. This proof-of-concept demonstrated that machines could communicate status without human intermediaries.

---

### Slide 10: Kevin Ashton and the Toaster (1990s)
**Birth of the term "Internet of Things"**
Covers two milestones: (1) John Romkey's 1990 TCP/IP-controlled toaster demonstration, and (2) Kevin Ashton's 1999 Procter & Gamble presentation where he coined "Internet of Things" while analyzing RFID supply chain solutions for Olay lipstick distribution.

---

### Slide 11: Turning Point: Scale of the Phenomenon
**When devices exceeded human population (2008-2009)**
Defines IoT as networks of devices with unique identifiers exchanging data autonomously. Distinguishes between digital-first devices (laptops, smartphones) and physical-first devices (gates, bulbs, washing machines). Shows exponential growth chart from Cisco's analysis.

---

### Slide 12: IoT System Architecture
**Three-layer hierarchical model**
Introduces the IEEE-standardized architecture: (1) Perception Layer (sensors and actuators), (2) Network Layer (gateways and routing), and (3) Application Layer (interfaces and analytics). Compares the system to the human nervous system.

---

### Slide 13: Flow Diagram
**Information flow between layers**
Visual Mermaid diagram showing the three-layer architecture with progressive revelation: first the Perception Layer alone, then adding the Network Layer, finally completing with the Application Layer. Demonstrates how information flows vertically through the system.

---

### Slide 14: Perception Layer: Machine Senses
**Sensors and their characteristics**
Explains how physical quantities become digital signals through sensors measuring temperature, humidity, light, gases, pressure, motion, vibrations, and GPS. Distinguishes passive sensors from active sensors and discusses calibration challenges.

---

### Slide 15: Perception Layer: Actuators
**Executive elements that influence the physical world**
Describes actuators as the system's means of affecting change: electric actuators (relays, servos, motors), liquid/gas actuators (solenoid valves). Explains the control loop: measurement → decision → actuator action, and warns about false sensor readings creating safety risks.

---

### Slide 16: Network Edge Gateway (Edge Gateway)
**Edge Computing and latency reduction**
Explains the shift from transmitting all data to the cloud toward intelligent filtering at the network edge. Gateways aggregate data (e.g., sending "Bearing Status: Stable" instead of millions of vibration packets). Discusses critical latency requirements for applications like autonomous vehicles.

---

### Slide 17: From Idea to Deployment
**Rapid prototyping revolution**
Describes how modern IoT development has shifted from months of PCB design to using ready-made development platforms. Discusses standardized GPIO pins, power supplies, and how this democratization enables faster time-to-market.

---

### Slide 18: Hardware Platforms as the Cornerstone
**Arduino vs ESP32 vs Raspberry Pi comparison**
Compares three platform categories: Microcontrollers (Arduino for education, ESP32 for professional IoT with Wi-Fi/Bluetooth), and Single Board Computers (Raspberry Pi for running full operating systems and local MQTT servers).

---

### Slide 19: "Deep Sleep" - the Power Compromise
**Power management in battery-powered devices**
Explains how IoT devices achieve multi-year battery life through aggressive sleep modes. Describes the wake-up → measure → transmit → sleep paradigm and Ultra Low Power (ULP) techniques that enable operation on small batteries for years.

---

### Slide 20: Digital Twins
**Virtual representations of physical systems**
Introduces Digital Twins as virtual copies of connected systems used for simulation and failure prediction. Explains how industrial machines undergo stochastic simulations ("what if" scenarios) before implementing changes in physical systems.

---

### Slide 21: Comparison: Arduino vs ESP vs Raspberry Pi
**Technical specification table**
Detailed comparison table covering: chip type, operating system, power consumption, built-in radio capabilities, and main use cases. ESP32 dominates commercial applications due to integrated Wi-Fi/BT with minimal power consumption.

---

### Slide 22: Summary
**Lecture 1 key takeaways**
Recaps: understanding how physical objects receive identity (UID) and senses, the role of edge gateways, and how errors at the perception layer cascade through the entire system. Emphasizes that poor hardware connections cannot be fixed by software.

---

## Lecture 2: Language of Things
### How Machines Talk to Each Other (Lecture 2)

---

### Slide 1: Title Slide
**Prologue: Physics, Energy, and the Tower of Babel**
Opening slide for the second lecture focusing on communication protocols that enable machine-to-machine (M2M) interaction.

---

### Slide 2: M2M Communication Problem
**The IoT Impossible Triangle**
Presents the fundamental constraint: engineers must choose only two of three parameters - Range (kilometers), Throughput (MB/s), or Battery life (years). Shows the triangle diagram illustrating this trade-off with a scatter plot of various technologies.

---

### Slide 3: Wi-Fi (IEEE 802.11): Curse and Blessing
**Wi-Fi's role in IoT**
Discusses Wi-Fi's advantages (ubiquity, high throughput, native IP) and disadvantages (power-hungry, complex connection handshake). Explains why Wi-Fi is suitable only for constantly-powered devices like smart TVs, not battery sensors.

---

### Slide 4: Bluetooth and BLE (Low Energy) Revolution
**From Classic Bluetooth to BLE**
Contrasts Classic Bluetooth (continuous audio streaming, always-on radio) with Bluetooth Low Energy (sleep mode with millisecond data bursts). Explains how BLE achieves 100x power reduction, enabling CR2032 batteries to last years in wearables.

---

### Slide 5: Zigbee and Z-Wave: Swarm Engineering (Mesh)
**Mesh network topology**
Explains how mesh networks solve range limitations: mains-powered devices act as routers, forwarding packets from weak battery sensors. Shows self-healing capability where the network automatically reroutes around failed nodes. Notes Z-Wave's superior wall penetration at 868 MHz.

---

### Slide 6: LPWAN: Telemetry Over Kilometers
**Low Power Wide Area Network technologies**
Introduces LPWAN for long-range, low-power applications: 5-10 year battery life, 15-20 km range, but only bytes/second throughput. Used exclusively for telemetry (sensor readings), not video or large files.

---

### Slide 7: Comparison of Radio Technologies
**Protocol comparison chart**
Visual bubble chart showing: x-axis (distance), y-axis (throughput, logarithmic), bubble size (power consumption). Helps designers choose appropriate technology based on application requirements.

---

### Slide 8: LoRaWAN vs NB-IoT: Private Network or Subscription?
**Two approaches to long-range connectivity**
Compares LoRaWAN (open protocol, free 868 MHz band, community networks like TTN) with NB-IoT/LTE-M (operator-based, subscription fees, excellent basement penetration). Provides decision framework: LoRaWAN for rural areas, NB-IoT for urban deployments.

---

### Slide 9: Sigfox: Ultra-Light Messages as a Service
**Network-as-a-Service model**
Describes Sigfox's extreme constraints: maximum 140 messages/day, 12 bytes payload, limited downlink. Suitable only for simple status confirmations, completely inadequate for control applications.

---

### Slide 10: Why HTTP Protocol Doesn't Fit IoT?
**HTTP limitations for resource-constrained devices**
Explains three problems: header overhead (headers larger than data), synchronous request-response model (keeps radio on), and lack of broadcast support. Shows visual comparison: HTTP packet (~500 bytes) vs MQTT packet (~40 bytes).

---

### Slide 11: MQTT: Lightweight, Binary IoT Standard
**Publish/Subscribe architecture**
Introduces MQTT's broker-based model where sensors publish to topics and subscribers receive pushed data. Clients don't know each other, only the broker. Emphasizes asynchronous operation and 2-byte header efficiency.

---

### Slide 12: MQTT: Topics, QoS, and "Last Will"
**Advanced MQTT features**
Explains topic hierarchies (e.g., `prod/hall_B/press_3/temperature`), three Quality of Service levels (QoS 0: fire-and-forget, QoS 1: confirmed delivery, QoS 2: guaranteed delivery), and Last Will Testament for failure notifications.

---

### Slide 13: MQTT QoS Diagram
**Quality of Service sequence diagram**
Mermaid sequence diagram showing message exchange patterns for QoS 0 (single PUBLISH), QoS 1 (PUBLISH + PUBACK), and QoS 2 (four-message handshake: PUBREC/PUBREL/PUBCOMP).

---

### Slide 14: CoAP and AMQP: Alternatives for Specific Scenarios
**Protocol alternatives**
CoAP: UDP-based HTTP equivalent for simple request-response on microcontrollers. AMQP: Heavy-duty enterprise messaging (RabbitMQ) for server-to-server communication, too complex for sensors.

---

### Slide 15: From Gigabytes to Knowledge
**Big Data challenge and Cloud Computing**
Discusses the scale problem: 10,000 sensors generating minute-by-minute logs create Big Data. Shows flow diagram: raw high-frequency data → Edge Computing (aggregation) → Cloud Computing (storage and analytics).

---

### Slide 16: Corporate Platforms (PaaS)
**AWS IoT Core and Azure IoT Hub**
Compares major cloud platforms: AWS (market leader, DynamoDB integration), Azure (industrial focus, Active Directory integration). Both support OTA firmware updates. Warns about vendor lock-in risk using Google Cloud IoT Core discontinuation as example.

---

### Slide 17: Open-Source Tools: Creator Independence
**Self-hosted alternatives**
Introduces ThingsBoard (professional dashboards), Home Assistant (local smart home integration), and Node-RED (visual programming). Shows screenshot of typical IoT dashboard. Emphasizes data privacy and independence from cloud providers.

---

### Slide 18: Barcelona: Pioneers of "City as a Computer"
**Smart City case study**
Documents Barcelona's IoT implementations: intelligent street lighting (30% energy savings), waste collection optimization (28% fewer empty runs), park irrigation based on soil moisture. Raises privacy question about who controls citizen movement data.

---

### Slide 19: Smart City and Industry 4.0 (IIoT)
**Dual applications of IoT**
Smart Cities: traffic optimization, air quality monitoring, adaptive lighting. Industry 4.0: predictive maintenance through vibration analysis, supply chain transparency. References Poznań's integrated telematic systems.

---

### Slide 20: Digital Twins
**Real-time virtual representations**
Explains Digital Twins as more than 3D visualization - they're powered by real-time sensor data streams. Enables "What If" simulations (e.g., valve failure during events). Shows nature applications (forest gas exchange modeling).

---

### Slide 21: When "Things" Become DDoS Weapons
**Security vulnerabilities**
Discusses IoT security challenges: limited computing power for cryptography, physical accessibility for hardware attacks, lack of updates (default passwords). Presents Mirai botnet case study (2016) that hijacked IP cameras for massive DDoS attacks.

---

### Slide 22: Good Security Practices (Defence in Depth)
**Multi-layer protection strategy**
Four key practices: (1) X.509 asymmetric encryption for TLS/DTLS, (2) OTA updates for vulnerability patching, (3) VLAN segmentation to isolate IoT from main networks, (4) Secure Boot to prevent unauthorized code. Shows network isolation diagram.

---

### Slide 23: Privacy in the Era of Always-On Microphones
**Ethical considerations**
Explores privacy threats: smart meters revealing daily routines through consumption patterns, IoT toys recording children's voices, fitness bands potentially affecting insurance premiums. Introduces Privacy by Design concept.

---

### Slide 24: Balance of Benefits and Challenges for the New Decade
**Promising gains vs challenges**
Benefits: precision agriculture (50% water reduction), predictive maintenance, Edge AI. Challenges: e-waste from single-use devices, energy harvesting needs, data ownership ethics. Presents the sustainability paradox.

---

### Slide 25: Future: 6G and New Paradigms
**Emerging technologies**
Discusses 6G integration (sub-millisecond latency, gigabit throughput), AI+IoT convergence (autonomous edge decisions), and EU Cyber Resilience Act imposing lifecycle security update obligations.

---

### Slide 26: End of the Lecture Cycle
**Closing thoughts**
Returns to the Coca-Cola machine origin story, emphasizing how the same philosophy now controls cities, factories, and life-saving systems. Ends with a call to action: "What smart thing will you design and build?"

---

**Generated:** 2026-05-18
**Source Files:** 
- `lectures_en/lecture_01_fundamentals.qmd` (24 slides)
- `lectures_en/lecture_02_communication.qmd` (26 slides)
**Total Slides:** 50 slides across two lectures
