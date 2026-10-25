"""
Module: Crack Diagnostics & Structural Integrity (Epic 2)
Multimodal classification of concrete surface defects, crack width estimation, root cause analysis,
and structural repair protocols per IS 456:2000, ACI 224R, and IS 13920.
"""

import streamlit as st
import pandas as pd
from PIL import Image
import io
import json
from modules.ui_components import (
    render_metric_card,
    render_severity_badge,
    render_status_badge,
    render_risk_gauge,
    render_json_download
)
from sample_data.samples import (
    generate_sample_crack_image,
    DEMO_CRACK_DATA
)

CRACK_SYSTEM_PROMPT = """
You are a Senior Forensic Structural Engineer specialized in Reinforced Cement Concrete (RCC) damage assessment,
crack propagation analysis, and rehabilitation under IS 456:2000, IS 13920:2016 (Ductile Detailing),
ACI 224R-01 (Control of Cracking in Concrete Structures), and BS 8110.

Inspect the concrete surface defect image and provide forensic diagnostic intelligence:
1. Classify the defect into one of the following primary types:
   - "Hairline" (< 0.3mm non-structural plastic/drying shrinkage)
   - "Settlement" (differential foundation settlement, diagonal step masonry or base shear cracks)
   - "Structural Shear" (critical 45-degree diagonal web shear crack near beam-column joints)
   - "Thermal Expansion" (cyclic expansion/contraction, lack of expansion joints)
   - "Spalling" (concrete cover delamination with corroded rebar exposure)
2. Estimate the crack width in millimeters (mm) and compare it against IS 456 Cl. 35.3.2 permissible crack width limits (0.3mm for mild, 0.2mm for moderate, 0.1mm for severe marine environments).
3. Determine:
   - structural_risk_level: "Low" | "Moderate" | "High" | "Critical"
   - urgency: "Monitor Only" | "Scheduled Maintenance (30 Days)" | "Urgent Action (48-72 Hours)" | "Immediate Shoring / Evacuation"
   - structural_health_score: integer from 0 (total failure imminent) to 100 (pristine sound concrete)
4. List comprehensive civil engineering root causes.
5. Provide step-by-step engineering repair methods (e.g. low-viscosity epoxy resin injection, polyurethane chemical grouting, CFRP external jacket wrapping, polymer-modified mortar stitching, anti-carbonation coatings).

Return STRICT JSON adhering to this schema:
{
  "defect_type": "Hairline" | "Settlement" | "Structural Shear" | "Thermal Expansion" | "Spalling",
  "defect_category": "Descriptive civil category",
  "estimated_crack_width_mm": "Estimated width with measurement (e.g. 2.8 mm)",
  "structural_risk_level": "Low" | "Moderate" | "High" | "Critical",
  "urgency": "Monitor Only" | "Scheduled Maintenance (30 Days)" | "Urgent Action (48-72 Hours)" | "Immediate Shoring / Evacuation",
  "structural_health_score": 45,
  "applicable_codes": ["IS 456:2000 Cl. 35.3.2", "ACI 224R-01"],
  "root_causes": ["Cause 1", "Cause 2", "Cause 3"],
  "recommended_repairs": [
    {
      "method": "Repair Technique Name",
      "material_spec": "Chemical / Structural Material Spec",
      "procedure": "Detailed step-by-step method statement",
      "standard_reference": "Code / Standard"
    }
  ],
  "structural_impact": "Impact on load-bearing capacity",
  "monitoring_protocol": "Sensor or optical gauge monitoring protocol"
}
"""

def render_crack_diagnostics_tab(gemini_client):
    """Render Tab 2: Crack Diagnostics & Structural Integrity."""
    st.markdown("### 🔬 Crack Diagnostics & Structural Integrity Assessment")
    st.markdown(
        "Deploy multimodal computer vision to classify concrete fissures, evaluate structural shear risks, "
        "estimate crack width against **IS 456:2000 Clause 35.3.2**, and formulate remedial engineering repair protocols."
    )

    col_input, col_view = st.columns([1.1, 1.2], gap="large")

    crack_bytes = None
    crack_mime = "image/jpeg"
    crack_label = ""

    with col_input:
        st.markdown("#### 📤 Input Structural Surface Image")
        crack_file = st.file_uploader(
            "Upload concrete/wall inspection image (JPG/PNG)",
            type=["jpg", "jpeg", "png"],
            key="crack_uploader",
            help="High-contrast macro photographs of concrete beams, slabs, shear walls, or foundation piers."
        )

        st.markdown("##### ⚡ Quick Demonstration Presets:")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⚡ Shear Crack", use_container_width=True, key="btn_shear_preset"):
                st.session_state["crack_preset_type"] = "shear"
                st.session_state["crack_bytes_cache"] = generate_sample_crack_image("shear")
                st.session_state["crack_label_cache"] = "Preset: 45° Beam Shear Crack"
        with c2:
            if st.button("🧱 Spalling & Rust", use_container_width=True, key="btn_spall_preset"):
                st.session_state["crack_preset_type"] = "spalling"
                st.session_state["crack_bytes_cache"] = generate_sample_crack_image("spalling")
                st.session_state["crack_label_cache"] = "Preset: Delaminated Spalling with Exposed Rebar"
        with c3:
            if st.button("〰️ Hairline", use_container_width=True, key="btn_hair_preset"):
                st.session_state["crack_preset_type"] = "hairline"
                st.session_state["crack_bytes_cache"] = generate_sample_crack_image("hairline")
                st.session_state["crack_label_cache"] = "Preset: Plastic Shrinkage Hairline Fissures"

        # Determine which image to feed
        if crack_file is not None:
            crack_bytes = crack_file.getvalue()
            crack_mime = crack_file.type
            crack_label = f"Uploaded File: {crack_file.name}"
        elif "crack_bytes_cache" in st.session_state:
            crack_bytes = st.session_state["crack_bytes_cache"]
            crack_label = st.session_state.get("crack_label_cache", "Synthetic Defect Sample")

        analyze_crack_btn = st.button("🧪 Execute Structural Diagnostic Analysis", type="primary", use_container_width=True, disabled=(crack_bytes is None))

    with col_view:
        st.markdown("#### 🖼️ Inspected Structural Element")
        if crack_bytes:
            st.image(crack_bytes, caption=crack_label, use_container_width=True)
        else:
            st.info("👈 Upload a concrete defect photo or select a structural preset above to trigger diagnostic telemetry.")

    st.markdown("---")

    # Execution Trigger
    if analyze_crack_btn and crack_bytes:
        with st.spinner("🔍 Forensic AI examining crack geometry, fracture depth, and load-path distress..."):
            prompt = (
                "Perform an in-depth forensic structural integrity audit on this concrete surface. "
                "Classify defect type (Hairline, Settlement, Structural Shear, Thermal Expansion, Spalling). "
                "Estimate crack width in mm, assess risk level, root causes, and recommended engineering repairs with specs. Return strict JSON."
            )

            # Choose realistic preset if running demo
            preset_type = st.session_state.get("crack_preset_type", "shear")
            if preset_type == "spalling":
                fallback = {
                    "defect_type": "Spalling",
                    "defect_category": "Concrete Cover Delamination & Chloride/Carbonation Rebar Corrosion",
                    "estimated_crack_width_mm": "Spall depth 35-50 mm, crater width ~250 mm",
                    "structural_risk_level": "High",
                    "urgency": "Urgent Action (48-72 Hours)",
                    "structural_health_score": 48,
                    "applicable_codes": ["IS 456:2000 Cl. 26.4 (Cover Requirements)", "IS 9077 (Rust Protection)", "EN 1504 (Concrete Repair)"],
                    "root_causes": [
                        "Carbonation front reaching rebar level, depleting alkaline passivation layer (pH dropped below 9.0).",
                        "Volumetric expansion of ferric oxide (rust expands 300-600%), exerting internal bursting pressures exceeding concrete tensile strength.",
                        "Inadequate clear cover during casting (< 20mm observed vs mandatory 40-50mm for moderate/severe environments)."
                    ],
                    "recommended_repairs": [
                        {
                            "method": "Mechanical Chipping & Rebar De-Rusting",
                            "material_spec": "Pneumatic needle scalers / wire brushes to Swedish Standard Sa 2.5",
                            "procedure": "Chip out cracked concrete 20mm behind corroded rebar perimeter. Mechanically remove all rust scale.",
                            "standard_reference": "BS EN ISO 8501-1"
                        },
                        {
                            "method": "Zinc-Rich Epoxy Primer & Passivation",
                            "material_spec": "Two-component zinc phosphate / epoxy active primer",
                            "procedure": "Coat exposed cleaned rebar with sacrificial zinc-rich primer within 4 hours of cleaning to inhibit galvanic corrosion cells.",
                            "standard_reference": "ASTM A775"
                        },
                        {
                            "method": "Polymer Modified Structural Mortar Build-up",
                            "material_spec": "Class R4 structural repair mortar (compressive strength > 45 MPa at 28 days)",
                            "procedure": "Apply epoxy bonding agent and build back cross-section in 25mm passes. Finish with elastomeric anti-carbonation protective coating.",
                            "standard_reference": "EN 1504-3 / IS 516"
                        }
                    ],
                    "structural_impact": "Loss of cross-sectional steel area (~15-20%) reducing moment carrying capacity; ongoing moisture ingress will accelerate adjacent rebar pitting.",
                    "monitoring_protocol": "Conduct Half-Cell Potential mapping (ASTM C876) to identify un-spalled active corrosion zones."
                }
            elif preset_type == "hairline":
                fallback = {
                    "defect_type": "Hairline",
                    "defect_category": "Non-Structural Plastic Shrinkage & Micro-Drying Fissures",
                    "estimated_crack_width_mm": "0.15 - 0.25 mm (Within IS 456 permissible threshold)",
                    "structural_risk_level": "Low",
                    "urgency": "Monitor Only",
                    "structural_health_score": 88,
                    "applicable_codes": ["IS 456:2000 Cl. 35.3.2", "ACI 224R-01 Cl. 4"],
                    "root_causes": [
                        "Rapid surface moisture evaporation exceeding bleed water ascent during initial setting (wind speed > 15 km/h, RH < 40%).",
                        "Lack of immediate mist curing or delayed application of aluminized curing membrane."
                    ],
                    "recommended_repairs": [
                        {
                            "method": "Surface Penetrating Hydrophobic Silane/Siloxane Sealer",
                            "material_spec": "Monomeric Alkyltrialkoxysilane penetrating water-repellent sealer",
                            "procedure": "Clean surface with high-pressure air jet. Flood surface with silane impregnant to seal pores against moisture without altering vapor breathability.",
                            "standard_reference": "EN 1504-2"
                        }
                    ],
                    "structural_impact": "Negligible structural load risk; superficial aesthetic defect, though sealing is recommended to avert future carbonation ingress.",
                    "monitoring_protocol": "Place reference demec points and inspect quarterly for active elongation."
                }
            else:
                fallback = DEMO_CRACK_DATA
                fallback["structural_health_score"] = 42

            diag_result = gemini_client.analyze_multimodal(
                image_bytes=crack_bytes,
                mime_type=crack_mime,
                prompt=prompt,
                system_instruction=CRACK_SYSTEM_PROMPT,
                fallback_data=fallback,
                is_json=True
            )

            st.session_state["crack_diag_result"] = diag_result

    # Display Diagnostic Output
    if "crack_diag_result" in st.session_state:
        res = st.session_state["crack_diag_result"]
        st.markdown("### 📊 Forensic Structural Assessment Report")

        defect_type = res.get("defect_type", "Structural Shear")
        width = res.get("estimated_crack_width_mm", "2.5 mm")
        risk = res.get("structural_risk_level", "High")
        urgency = res.get("urgency", "Urgent Action")
        health_score = res.get("structural_health_score", 50)

        # Top Metric Dash
        m1, m2, m3, m4 = st.columns([1.2, 1.1, 1.1, 1.1])
        with m1:
            render_metric_card("Defect Classification", defect_type, res.get("defect_category", ""), "🧱", "#F59E0B")
        with m2:
            render_metric_card("Estimated Crack Width", width, "IS 456 Max Limit: 0.3mm", "📏", "#38BDF8")
        with m3:
            urg_color = "#EF4444" if "Immediate" in urgency or "Urgent" in urgency else "#F59E0B"
            render_metric_card("Action Urgency", urgency, "Field Remediation Timeline", "⏱️", urg_color)
        with m4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-card-label">Structural Risk Rating</div>
                    <div style="margin-top: 0.6rem;">{render_severity_badge(risk)}</div>
                    <div class="metric-card-subtext" style="margin-top: 0.75rem;">Forensic Risk Matrix</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # Health Gauge & Structural Impact Summary
        g_col, impact_col = st.columns([1.1, 1.4], gap="large")
        with g_col:
            st.plotly_chart(render_risk_gauge(health_score, title="Structural Health Index"), use_container_width=True)
        with impact_col:
            st.markdown(
                f"""
                <div class="engineering-callout" style="border-left-color: #EF4444; margin-top: 15px;">
                    <h4 style="color: #F87171;">⚠️ Structural Impact & Load-Bearing Hazard</h4>
                    <p style="margin-bottom: 8px;">{res.get('structural_impact', 'Detailed evaluation underway.')}</p>
                    <p><strong>Monitoring Protocol:</strong> <em>{res.get('monitoring_protocol', 'Periodic crack gauge telemetry.')}</em></p>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Applicable Codes
            codes = res.get("applicable_codes", ["IS 456:2000", "ACI 224R"])
            code_badges = " ".join([f"<code>{c}</code>" for c in codes])
            st.markdown(f"**Regulatory & Design Standards:** {code_badges}", unsafe_allow_html=True)

        st.markdown("---")

        # Root Causes & Recommended Engineering Repairs
        rc_col, rep_col = st.columns([1, 1.4], gap="large")

        with rc_col:
            st.markdown("#### 🔬 Root Cause Analysis")
            roots = res.get("root_causes", [])
            for r_idx, root in enumerate(roots, 1):
                st.markdown(
                    f"""
                    <div style="background: rgba(15, 23, 42, 0.7); border-left: 3px solid #38BDF8; padding: 10px; margin-bottom: 8px; border-radius: 4px;">
                        <strong style="color: #38BDF8;">Point {r_idx}:</strong> <span style="color: #E2E8F0; font-size: 0.9rem;">{root}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        with rep_col:
            st.markdown("#### 🛠️ Recommended Engineering Repair Plan")
            repairs = res.get("recommended_repairs", [])
            for rep_idx, rep in enumerate(repairs, 1):
                with st.expander(f"Phase {rep_idx}: {rep.get('method', 'Remediation Step')}", expanded=True):
                    st.markdown(
                        f"""
                        <div style="margin-bottom: 6px;">
                            <strong>Material Specification:</strong> <code style="color: #10B981;">{rep.get('material_spec', 'Engineering Grade')}</code>
                        </div>
                        <div style="margin-bottom: 6px; font-size: 0.88rem; color: #CBD5E1;">
                            <strong>Execution Procedure:</strong><br/>{rep.get('procedure', '')}
                        </div>
                        <div style="font-size: 0.8rem; color: #94A3B8;">
                            <strong>Standard Reference:</strong> <code>{rep.get('standard_reference', 'IS / ACI')}</code>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        # Download Dossier
        st.markdown("---")
        st.markdown("#### 📥 Export Forensic Structural Report")
        d1, d2 = st.columns([1, 1])
        with d1:
            render_json_download(
                res,
                filename="forensic_structural_defect_report.json",
                label="📥 Download Structured JSON Diagnostics Dossier"
            )
        with d2:
            txt_report = f"""MULTIMODAL CONSTRUCTION INTELLIGENCE PLATFORM
FORENSIC STRUCTURAL INTEGRITY & DEFECT DIAGNOSTIC REPORT
=========================================================
Defect Classification: {defect_type} ({res.get('defect_category', '')})
Estimated Crack Width: {width}
Structural Risk Level: {risk}
Action Urgency: {urgency}
Structural Health Index: {health_score}/100

STRUCTURAL IMPACT:
{res.get('structural_impact', '')}

ROOT CAUSE ANALYSIS:
"""
            for r in roots:
                txt_report += f"- {r}\n"

            txt_report += "\nRECOMMENDED REPAIR PROTOCOLS:\n"
            for rep in repairs:
                txt_report += f"- {rep.get('method')}\n"
                txt_report += f"  Spec: {rep.get('material_spec')}\n"
                txt_report += f"  Procedure: {rep.get('procedure')}\n"
                txt_report += f"  Reference: {rep.get('standard_reference')}\n\n"

            st.download_button(
                label="📄 Download Formatted TXT Engineering Report",
                data=txt_report,
                file_name="structural_defect_diagnostic_report.txt",
                mime="text/plain",
                use_container_width=True
            )
