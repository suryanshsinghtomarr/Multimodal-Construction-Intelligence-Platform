"""
Module: Daily Site Assistant & Weather-Aware Advisory (Epic 5)
Provides dynamic weather-triggered safety advisories (crane shutdown, dewatering, curing protocols)
and an interactive multi-turn Construction Engineering Chatbot grounded in OSHA and IS standards.
"""

import streamlit as st
from modules.ui_components import render_severity_badge

WEATHER_PROFILES = {
    "High Wind (> 45 km/h / Gale Force)": {
        "severity": "Critical",
        "icon": "💨",
        "crane_protocol": "MANDATORY SUSPENSION: Discontinue all tower crane, mobile crawler, and hoist operations. Release tower crane slewing brake into free-weathervaning mode (IS 875 Part 3 & OSHA 1926.1431). Lower all suspended loads immediately.",
        "heights_protocol": "STRICT BAN: Prohibit all work on external scaffolding, mast climbing work platforms (MCWP), and suspended cradles above 10m elevation.",
        "concreting_protocol": "High evaporation risk: Avoid high-elevation boom placer pours. Apply plastic sheeting or aliphatic moisture retaining spray to prevent plastic shrinkage cracking.",
        "housekeeping": "Lash down all loose perimeter formwork shutters, CGI zinc sheets, insulation boards, and rebar cages. Clear loose debris from slab edges."
    },
    "Heavy Monsoonal Rain / Storm Alert": {
        "severity": "Critical",
        "icon": "⛈️",
        "crane_protocol": "CAUTION: Halt hoisting in zero-visibility conditions; secure crane hook blocks in uppermost retracted position with electrical breakers locked out.",
        "heights_protocol": "SLIP & FALL HAZARD: Metal scaffolding decks become slick. Suspend all steel erection and structural bolting. Verify fall arrest lanyards are dry and unfrayed.",
        "concreting_protocol": "RAIN STOP-ORDER: Halt ongoing slab casting immediately if rain penetrates fresh mix to prevent dilution of water-cement ratio and cement paste washout. If unpreventable, create emergency bulkhead construction joint with shear dowels and cover with tarpaulins.",
        "housekeeping": "ELECTRICAL & TRENCH HAZARD: Inspect all 415V distribution boxes and ensure 30mA RCCB/ELCB tripping sensitivity. Station submersible dewatering slurry pumps in basement excavations to avert soil slide collapse (OSHA 1926.651)."
    },
    "Extreme Heatwave (> 42°C / 108°F)": {
        "severity": "High",
        "icon": "☀️",
        "crane_protocol": "Hydraulic oil temperature monitoring: Inspect mobile crane hydraulic fluid viscosity and boom cylinder seals against thermal degradation.",
        "heights_protocol": "THERMAL STRESS: Schedule elevated steel deck works prior to 10:30 AM or post 4:00 PM. Metal surfaces reach > 60°C; mandatory thermal-insulated gloves.",
        "concreting_protocol": "HOT WEATHER CONCRETING (IS 7861 Part 1): Concrete mix temperature at placement must NOT exceed 32°C. Substitute batching water with crushed ice flakes (up to 75%). Add retarder admixtures to extend initial setting time. Initiate continuous wet burlap ponding curing immediately after finishing.",
        "housekeeping": "WORKER WELFARE (OSHA Heat Illness Prevention): Provide chilled electrolyte hydration stations within 50 feet of active zones. Enforce mandatory 15-minute shaded rest breaks every 60 minutes for high-exertion trades."
    },
    "Normal / Clear Weather Conditions": {
        "severity": "Low",
        "icon": "🌤️",
        "crane_protocol": "NORMAL OPERATIONS: Standard pre-shift crane daily inspection checklist (limit switches, load moment indicator LMI, wire rope reeving).",
        "heights_protocol": "STANDARD SAFETY: Enforce 100% tie-off on scaffolding above 1.8m (6ft) with certified dorsal D-ring harness (IS 3521).",
        "concreting_protocol": "NOMINAL CONCRETING: Proceed according to design mix proportions (IS 10262). Maintain water-cement ratio <= 0.45. Ensure standard 7-day wet ponding curing (IS 456 Cl. 13.5).",
        "housekeeping": "Maintain standard housekeeping, clear accessways, and conduct daily morning toolbox safety briefing."
    },
    "Dense Fog & Low Temperature (< 8°C / Cold Snap)": {
        "severity": "Medium",
        "icon": "🌫️",
        "crane_protocol": "POOR VISIBILITY: Deploy illuminated flashing beacons on jib and counterweight. Hoist movements permitted ONLY with designated two-way radio communication between banksman and operator.",
        "heights_protocol": "Condensation slip hazard: Inspect icy or dewy scaffolding transoms before shift commencement.",
        "concreting_protocol": "COLD WEATHER CONCRETING (IS 7861 Part 2): Concrete temperature at placement must not drop below 5°C. Extend formwork striking times by 30-50% per IS 456 Table 11 due to retarded hydration kinetics.",
        "housekeeping": "Maintain high-visibility outerwear (IS 15809 Class 3) and install auxiliary floodlighting along internal transit routes."
    }
}

ENGINEERING_ASSISTANT_SYSTEM_PROMPT = """
You are "Aura Civil-AI", an elite Chief Structural & Construction Safety Consultant.
You possess encyclopedic mastery of:
- Indian Standard IS 456:2000 (Plain and Reinforced Concrete Code of Practice)
- IS 875 (Parts 1-5: Design Loads, Wind, Snow, Seismic)
- IS 1893:2016 (Criteria for Earthquake Resistant Design of Structures)
- IS 13920:2016 (Ductile Detailing of Reinforced Concrete Structures)
- IS 7861 (Hot & Cold Weather Concreting)
- National Building Code of India (NBC 2016)
- OSHA 1926 Safety and Health Regulations for Construction (Fall protection, Crane safety, Excavation shoring)
- CPWD Civil Specifications & FIDIC contract administration.

Always provide concise, authoritative, deeply technical civil engineering guidance.
Format your responses with clear markdown headers, bold citations of specific clauses/tables, and actionable execution checklists.
"""


def render_weather_advisor_tab(gemini_client):
    """Render Tab 4: Daily Site Assistant & Weather-Aware Advisory."""
    st.markdown("### 🌦️ Daily Site Assistant & Weather-Aware Environmental Advisory")
    st.markdown(
        "Real-time site meteorological risk engine dynamically cross-referencing field conditions against "
        "**IS 875**, **IS 7861 (Hot/Cold Concreting)**, and **OSHA 1926**. Includes interactive conversational engineering advisory."
    )

    # Weather Condition Selector Panel
    w_col1, w_col2 = st.columns([1.2, 1.8], gap="large")

    with w_col1:
        st.markdown("#### 🌡️ Environmental Field Conditions")
        selected_weather = st.selectbox(
            "Current On-Site Meteorological Status",
            list(WEATHER_PROFILES.keys()),
            index=0,
            key="weather_selector"
        )
        profile = WEATHER_PROFILES[selected_weather]
        
        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 8px; padding: 14px; margin-top: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                    <span style="font-size: 1.5rem;">{profile['icon']}</span>
                    {render_severity_badge(profile['severity'])}
                </div>
                <div style="font-weight: 700; color: #F8FAFC; font-size: 1rem;">{selected_weather}</div>
                <div style="color: #94A3B8; font-size: 0.82rem; margin-top: 4px;">Dynamic protocols active across site zones</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with w_col2:
        st.markdown("#### 🚨 Dynamic Site Safety & Operational Directives")
        
        # Accordion of directives
        with st.expander("🏗️ Crane & Heavy Lifting Directives", expanded=True):
            st.markdown(profile["crane_protocol"])
        with st.expander("🧗 Working at Heights & Scaffolding Protocol", expanded=True):
            st.markdown(profile["heights_protocol"])
        with st.expander("🧱 Concrete Batching, Placement & Curing Protocol", expanded=True):
            st.markdown(profile["concreting_protocol"])
        with st.expander("🧹 Housekeeping, Dewatering & Worker Welfare", expanded=False):
            st.markdown(profile["housekeeping"])

    st.markdown("---")

    # Multi-turn Construction Engineering Assistant Chatbot
    st.markdown("#### 💬 Senior Structural & Site Engineering Assistant")
    st.markdown(
        "Consult your autonomous engineering co-pilot on design codes, curing tables, formwork striking times, "
        "rebar detailing, and OSHA field safety protocols."
    )

    # Pre-loaded prompt chips for quick 1-click evaluation
    st.markdown("**⚡ Recommended Inquiries (1-Click Prompt Chips):**")
    chip_col1, chip_col2, chip_col3, chip_col4 = st.columns(4)

    prompt_to_send = None
    with chip_col1:
        if st.button("⏱️ IS 456 Stripping Times", use_container_width=True, key="chip1"):
            prompt_to_send = "What are the minimum formwork striking periods for props under beams > 6m according to IS 456:2000 Table 11?"
    with chip_col2:
        if st.button("💨 High Wind Crane Limits", use_container_width=True, key="chip2"):
            prompt_to_send = "What are the permissible wind speed thresholds for crane lifting and weathervaning under IS 875 and OSHA?"
    with chip_col3:
        if st.button("🔬 Repair Shear Cracks", use_container_width=True, key="chip3"):
            prompt_to_send = "How should a forensic structural engineer remediate 45-degree diagonal shear cracks near RCC beam-column joints?"
    with chip_col4:
        if st.button("💧 Hot Weather Curing", use_container_width=True, key="chip4"):
            prompt_to_send = "What is the recommended curing protocol and temperature limit for fresh concrete placed in extreme heat (>42°C) under IS 7861?"

    # Chat session state initialization
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [
            {
                "role": "assistant",
                "content": (
                    "👋 **Greetings Engineer!** I am your Senior Structural & Construction Safety AI Co-Pilot.\n\n"
                    "I am calibrated to **IS 456:2000**, **IS 875**, **IS 13920**, **NBC 2016**, and **OSHA 1926** standards. "
                    "Ask me anything regarding structural load calculations, concrete curing, crack remediation, or site safety protocols!"
                )
            }
        ]

    # Render Conversation History
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state["chat_history"]:
            with st.chat_message(msg["role"], avatar=("👷‍♂️" if msg["role"] == "user" else "🏗️")):
                st.markdown(msg["content"])

    # User Input Handling
    user_input = st.chat_input("Type your civil engineering or site safety question here...")
    
    if prompt_to_send:
        user_input = prompt_to_send

    if user_input:
        # Append User Message
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="👷‍♂️"):
            st.markdown(user_input)

        # Generate Assistant Response
        with st.chat_message("assistant", avatar="🏗️"):
            with st.spinner("🧠 Consulting IS codes & engineering standards..."):
                response_text = gemini_client.chat_response(
                    conversation_history=st.session_state["chat_history"],
                    system_instruction=ENGINEERING_ASSISTANT_SYSTEM_PROMPT,
                    weather_context=f"{selected_weather}: {profile['crane_protocol']} {profile['concreting_protocol']}"
                )
                st.markdown(response_text)
                st.session_state["chat_history"].append({"role": "assistant", "content": response_text})

    # Clear Chat or Export Conversation
    c_btn1, c_btn2, _ = st.columns([1, 1, 2])
    with c_btn1:
        if st.button("🗑️ Reset Chat History", use_container_width=True):
            st.session_state["chat_history"] = [
                {
                    "role": "assistant",
                    "content": "Conversation reset. How can I assist your construction engineering workflow today?"
                }
            ]
            st.rerun()
    with c_btn2:
        transcript = "\n\n".join([f"[{m['role'].upper()}]: {m['content']}" for m in st.session_state["chat_history"]])
        st.download_button(
            label="📄 Export Chat Transcript",
            data=transcript,
            file_name="site_assistant_consultation_log.txt",
            mime="text/plain",
            use_container_width=True
        )
