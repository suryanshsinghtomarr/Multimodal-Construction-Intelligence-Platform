# 🏗️ Multimodal Construction Intelligence Platform
> **Skill Wallet Capstone Project 1** • Enterprise Civil Engineering & Autonomous Construction Site Intelligence Platform  
> Powered by **Google Gemini Multimodal Vision & Deep Reasoning (gemini-2.5-flash)** • Built with **Streamlit** & **Python**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![Google Gemini API](https://img.shields.io/badge/Google%20GenAI-gemini--2.5--flash-orange.svg)](https://ai.google.dev/)
[![OSHA & IS 456 Standards](https://img.shields.io/badge/Compliance-OSHA%201926%20%7C%20IS%20456%3A2000-green.svg)](#standards--regulatory-framework)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Executive Summary

The **Multimodal Construction Intelligence Platform** is a full-stack, production-grade civil engineering and construction management application. It bridges the gap between field safety enforcement, structural forensic diagnostics, financial progress forecasting, and meteorological risk mitigation using state-of-the-art multimodal AI.

Engineered with **zero external database dependencies**, the platform is completely self-contained and pre-configured for seamless **1-click deployment on Streamlit Community Cloud**.

---

## 🏛️ System Architecture & Core Modules

```
Multimodal Construction Intelligence Platform/
├── .streamlit/
│   └── config.toml                  # Streamlit dark/amber theme & server configuration
├── modules/
│   ├── __init__.py
│   ├── gemini_client.py             # Google GenAI SDK wrapper with graceful Demo Fallback
│   ├── site_safety.py               # Epic 2: Site Safety & PPE Audit (OSHA 1926 / IS 456)
│   ├── crack_diagnostics.py         # Epic 2: Structural Crack Integrity & Forensic Analysis
│   ├── valuation_planner.py         # Epic 3: CapEx Valuation, IS 456 BOQ & Pollinations 3D Render
│   ├── weather_advisor.py           # Epic 5: Dynamic Meteorological Directives & Engineering Chatbot
│   └── ui_components.py             # Reusable UI cards, gauges, badges, and custom CSS
├── sample_data/
│   ├── __init__.py
│   └── samples.py                   # Synthetic image generators & calibrated demo simulation datasets
├── app.py                           # Main Streamlit application entry point
├── test_app.py                      # Automated unit and smoke test suite
├── requirements.txt                 # Production package dependencies
└── README.md                        # Documentation and deployment guide
```

---

## 🚀 Module Breakdown by Epic

### 1. 🔑 Sidebar & Security Control Center
- **Secure Gemini API Authentication:** Masked API key input with automatic validation and session memory.
- **Graceful Demonstration Fallback:** If no API key is supplied, the platform instantly engages **Demonstration Mode (Simulation Engine)**. Evaluators can test every visual and analytical feature immediately without supplying credentials.
- **Engine Status Indicator:** Real-time visual pill (`🟢 Gemini 2.5 Live Engine` vs `🟡 Demonstration Mode`).
- **Architecture Overview & Reference Standards:** Quick navigation and citation of relevant design codes.

---

### 2. 🛡️ Tab 1 - Site Safety & PPE Audit (Epic 2)
- **High-Resolution Visual Uploader:** Accepts JPG/PNG site photos, drone captures, or CCTV frames.
- **1-Click Test Presets:** Built-in synthetic visual generator creating realistic elevated scaffolding violation scenes and fully compliant crew scenes.
- **Autonomous PPE Inspection Checklist:**
  - 🪖 **Hard Hats / Safety Helmets** (*OSHA 1926.100* / *IS 2925:1984*)
  - 🦺 **High-Visibility Retroreflective Vests** (*OSHA 1926.201* / *IS 15809:2017 Class 2*)
  - 🧗 **Fall Arrest Harness & Anchorage** (*OSHA 1926.501* / *IS 3521:1999*)
  - 🥾 **Steel-Toe Protective Footwear** (*OSHA 1926.96* / *IS 15298:2016 Part 2*)
- **Hazard Identification Engine:** Catalogues site hazards with severity tags (`Critical`, `High`, `Medium`, `Low`) and actionable engineering/administrative remedies.
- **Telemetry Dash:** Safety score gauge (0-100), workers detected, critical violations counter, and audit status badge.
- **Dossier Exports:** One-click download of structured JSON report (`construction_site_safety_audit.json`) and formatted TXT field report.

---

### 3. 🔬 Tab 2 - Crack Diagnostics & Structural Integrity (Epic 2)
- **Defect Classification Engine:** Multimodal classification of concrete fractures:
  - **Structural Shear Cracks:** Critical 45° diagonal web fractures near beam-column joints.
  - **Concrete Spalling & Corrosion:** Cover delamination, carbonation depth, and corroded rebar exposure.
  - **Foundation Settlement Cracks:** Differential movement and diagonal step masonry shear.
  - **Thermal Expansion Cracks:** Joint failure and cyclic thermal stresses.
  - **Hairline Shrinkage Cracks:** Non-structural plastic and drying shrinkage fissures.
- **Quantitative Crack Width Estimation:** Compares crack aperture against **IS 456:2000 Clause 35.3.2** permissible crack limits (0.3mm mild, 0.2mm moderate, 0.1mm severe marine).
- **Structural Health Index (Plotly Gauge):** Interactive dial visualizing load-path integrity.
- **Forensic Action Plan:** Specific civil engineering remediation protocols (low-viscosity epoxy resin injection per ASTM C881 / IS 15809, CFRP external U-jacket wraps per ACI 440.2R, zinc-rich rebar passivation, structural propping).
- **Downloadable Dossier:** Export comprehensive JSON and TXT forensic reports.

---

### 4. 📐 Tab 3 - Planning & Real Estate Valuation (Epic 3)
- **Dynamic Project Modeling:**
  - **Structure Typologies:** Residential High-Rise (RCC Framed), Commercial Grade-A Office Complex, Industrial PEB Warehouse, Luxury Villa Community, Infrastructure Elevated Viaduct/Bridge.
  - **Location Municipal Tiers:**
    - *Tier 1:* Mumbai, Delhi-NCR, Bengaluru, Hyderabad, Chennai
    - *Tier 2:* Pune, Ahmedabad, Jaipur, Lucknow, Chandigarh, Kochi
    - *Tier 3:* Indore, Coimbatore, Bhubaneswar, Nagpur, Surat
  - **Built-up Area:** Configurable from 2,000 to 1,000,000 sq.ft.
  - **Milestone Completion Slider:** Physical execution progress from 0% to 100%.
- **Financial Intelligence:**
  - Total Project Budget (INR Lakhs / Crores)
  - CapEx Incurred to Date & Balance Capital Outlay Required
  - Current Fair Market Asset Valuation (incorporates land capitalization, progress discount, and developer margin)
- **IS 456 Bill of Quantities (Material Estimates):**
  - High-yield strength deformed steel rebar (TMT Fe 500D / Fe 550D) in Metric Tons.
  - Cement consumption in Bags and Metric Tons (OPC 53 / PPC).
  - Ready-Mix Concrete (RMC) M25-M40 volume in cubic meters ($m^3$).
  - Coarse aggregates and M-Sand requirements.
- **Interactive Visualizations:** Plotly component cost allocation bar charts and capital disbursement ratio donut.
- **Conceptual 3D Architectural Rendering (Pollinations AI):**
  - Neural prompt synthesizer generating photorealistic 3D architectural renders matching structure type, facade materials, landscape, and lighting atmosphere.
  - Interactive "Regenerate 3D Perspective" control with random seed generation.

---

### 5. 🌦️ Tab 4 - Daily Site Assistant & Weather Advisory (Epic 5)
- **Meteorological Condition Selector:**
  - 💨 **High Wind (> 45 km/h):** Tower crane suspension, slewing brake weathervaning protocol (*IS 875 Part 3* / *OSHA 1926.1431*), elevation work bans.
  - ⛈️ **Heavy Monsoonal Rain:** Concrete pour stop-orders to prevent water-cement ratio dilution, 30mA RCCB/ELCB electrical trip verifications, basement excavation slurry dewatering.
  - ☀️ **Extreme Heatwave (> 42°C):** Hot weather concreting (*IS 7861 Part 1*), batching with ice flakes, retarder admixtures, wet burlap curing, OSHA heat stress hydration rotations.
  - 🌤️ **Normal / Clear Weather:** Standard toolbox briefing and 7-day wet ponding curing.
  - 🌫️ **Dense Fog / Low Temp (< 8°C):** Formwork striking extension under *IS 456 Table 11*, crane radio signaling.
- **Interactive Multi-Turn Civil Engineering Chatbot ("Aura Civil-AI"):**
  - Powered by Gemini 2.5 (or civil engineering fallback engine in Demo mode).
  - Context-aware of current on-site weather advisories.
  - Pre-loaded 1-click prompt chips for rapid testing (Formwork stripping times, crane wind speed limits, shear crack remediation, hot weather curing).
  - Chat history persistence and one-click TXT transcript export.

---

## 📚 Standards & Regulatory Framework

| Standard Code | Domain / Scope | Implementation in Platform |
|---|---|---|
| **OSHA 1926** | Safety and Health Regulations for Construction | Hard hat (1926.100), Vest (1926.201), Fall protection (1926.501), Excavations (1926.651), Cranes (1926.1431) |
| **IS 456:2000** | Plain and Reinforced Concrete - Code of Practice | Cl. 35.3.2 (Crack width limits), Cl. 13.5 (Curing periods), Table 11 (Striking of formwork), Cl. 40 (Safety) |
| **IS 875 (Part 3)** | Code of Practice for Design Loads (Wind Loads) | High-wind crane shutdown thresholds (> 38 km/h alert, > 45 km/h stop-work) |
| **IS 13920:2016** | Ductile Design and Detailing of Reinforced Concrete | Beam-column shear stirrup spacing and shear failure remediation |
| **IS 7861 (P1 & P2)**| Hot and Cold Weather Concreting | Temperature control at placement (< 32°C hot, > 5°C cold), ice flaking, curing compound specs |
| **NBC 2016** | National Building Code of India | Construction practices, site management, fire & occupational safety |

---

## 💻 Local Setup & Execution Guide

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/multimodal-construction-intelligence-platform.git
cd "multimodal-construction-intelligence-platform"
```

### 2. Create and Activate Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Unit & Smoke Test Suite
```bash
python test_app.py
```
*Expected output:* `ALL PLATFORM TESTS PASSED SUCCESSFULLY!`

### 5. Launch the Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ 1-Click Deployment to Streamlit Community Cloud

The platform is 100% cloud-ready with zero database or local driver dependencies:

1. Push this repository to your **GitHub** account.
2. Sign in to [share.streamlit.io](https://share.streamlit.io/).
3. Click **"New app"** and select:
   - **Repository:** `your-username/multimodal-construction-intelligence-platform`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. *(Optional)* Add your Gemini API key under **Advanced settings -> Secrets**:
   ```toml
   GEMINI_API_KEY = "AIzaSyYourGeminiApiKeyHere"
   ```
5. Click **"Deploy!"** Your application will be live globally in under 2 minutes.

---

## 📄 License
Distributed under the **MIT License**. See `LICENSE` for details. Built for **Skill Wallet Capstone Project 1**.
