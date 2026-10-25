"""
Module: Planning & Real Estate Valuation (Epic 3)
Calculates capital expenditures (CapEx), total project budget, market asset valuation in INR (Lakhs/Crores),
and IS 456 material requirement metrics (Steel, Cement, Aggregates, RMC).
Integrates Conceptual 3D Architectural Rendering via Pollinations AI prompt generation.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import urllib.parse
import random
from modules.ui_components import render_metric_card

# Construction cost and valuation benchmarks for Indian Cities (INR / sqft)
TIER_COST_BENCHMARKS = {
    "Tier 1 (Mumbai, Delhi-NCR, Bengaluru, Hyderabad, Chennai)": {
        "base_cost_sqft": 3800,
        "land_weight_factor": 2.2,
        "market_rate_sqft": 12500,
        "multiplier": 1.25
    },
    "Tier 2 (Pune, Ahmedabad, Jaipur, Lucknow, Chandigarh, Kochi)": {
        "base_cost_sqft": 2800,
        "land_weight_factor": 1.5,
        "market_rate_sqft": 7500,
        "multiplier": 1.0
    },
    "Tier 3 (Indore, Coimbatore, Bhubaneswar, Nagpur, Surat, Patna)": {
        "base_cost_sqft": 2200,
        "land_weight_factor": 1.2,
        "market_rate_sqft": 4800,
        "multiplier": 0.85
    }
}

STRUCTURE_TYPE_PARAMS = {
    "Residential High-Rise (RCC Framed)": {
        "cost_multiplier": 1.15,
        "steel_kg_sqft": 4.5,
        "cement_bags_sqft": 0.42,
        "rmc_cum_sqft": 0.042,
        "render_desc": "photorealistic luxury residential high-rise condominium tower with cantilevered glass balconies, ambient evening warm lighting, lush podium landscaping"
    },
    "Commercial Grade-A Office Complex": {
        "cost_multiplier": 1.35,
        "steel_kg_sqft": 5.2,
        "cement_bags_sqft": 0.46,
        "rmc_cum_sqft": 0.048,
        "render_desc": "award-winning modernist commercial corporate headquarters building with high-performance double-glazed curtain wall facade, landscaped atrium plaza, golden hour architectural photography"
    },
    "Industrial Pre-Engineered Building (PEB)": {
        "cost_multiplier": 0.85,
        "steel_kg_sqft": 3.8,
        "cement_bags_sqft": 0.30,
        "rmc_cum_sqft": 0.032,
        "render_desc": "cutting-edge smart logistics hub and advanced manufacturing warehouse facility with wide-span steel trusses, solar rooftop array, truck docking bays, photorealistic daytime rendering"
    },
    "Luxury Villa Community / Gated Enclave": {
        "cost_multiplier": 1.45,
        "steel_kg_sqft": 4.0,
        "cement_bags_sqft": 0.45,
        "rmc_cum_sqft": 0.040,
        "render_desc": "ultra-luxury tropical minimalist architectural villa with exposed stone accents, infinity plunge pool, floor-to-ceiling glass pavilions, lush manicured gardens, dusk atmospheric render"
    },
    "Infrastructure Elevated Viaduct / Bridge": {
        "cost_multiplier": 1.60,
        "steel_kg_sqft": 6.8,
        "cement_bags_sqft": 0.55,
        "rmc_cum_sqft": 0.060,
        "render_desc": "monumental cable-stayed concrete highway bridge spanning a river, prestressed box girders, sleek pylons, dramatic sunset lighting, high detail civil infrastructure engineering render"
    }
}

FINISH_GRADE_MULTIPLIER = {
    "Standard Economy": 0.90,
    "Executive Premium": 1.10,
    "Ultra-Luxury High-Spec": 1.35
}


def format_inr(amount: float) -> str:
    """Format numeric INR value into Indian Lakhs or Crores."""
    if amount >= 10000000:  # 1 Crore = 10,000,000
        crores = amount / 10000000
        return f"₹ {crores:,.2f} Cr"
    elif amount >= 100000:  # 1 Lakh = 100,000
        lakhs = amount / 100000
        return f"₹ {lakhs:,.2f} Lakhs"
    else:
        return f"₹ {amount:,.0f}"


def render_valuation_planner_tab():
    """Render Tab 3: Planning & Real Estate Valuation."""
    st.markdown("### 📐 Planning, CapEx Estimator & Real Estate Asset Valuation")
    st.markdown(
        "Accurately model project budgets, capital expenditure curves, and current market valuations across Indian municipal tiers. "
        "Calculates exact **IS 456** bill-of-quantities (Steel, Cement, Concrete) and synthesizes conceptual 3D architectural renders via **Pollinations AI**."
    )

    # Input Control Panel
    st.markdown("#### ⚙️ Project Parameters & Structural Specification")
    c1, c2, c3 = st.columns([1.2, 1, 1], gap="medium")

    with c1:
        structure_type = st.selectbox(
            "Structure Typology",
            list(STRUCTURE_TYPE_PARAMS.keys()),
            index=0,
            key="val_structure_type"
        )
        location_tier = st.selectbox(
            "Location City Tier",
            list(TIER_COST_BENCHMARKS.keys()),
            index=0,
            key="val_location_tier"
        )

    with c2:
        builtup_sqft = st.number_input(
            "Total Built-up Area (Sq.ft)",
            min_value=2000,
            max_value=1000000,
            value=75000,
            step=5000,
            key="val_builtup_sqft",
            help="Total gross construction floor area including basements and common areas."
        )
        quality_grade = st.selectbox(
            "Finishing & Specification Grade",
            list(FINISH_GRADE_MULTIPLIER.keys()),
            index=1,
            key="val_quality_grade"
        )

    with c3:
        st.markdown("**Construction Milestone Completion (%)**")
        completion_pct = st.slider(
            "Physical Execution Progress",
            min_value=0,
            max_value=100,
            value=45,
            step=1,
            key="val_completion_slider"
        )
        
        # Determine current stage label
        if completion_pct <= 20:
            stage_label = "Substructure & Foundation Pier Casting"
        elif completion_pct <= 55:
            stage_label = "Superstructure RCC Framing & Slabs"
        elif completion_pct <= 75:
            stage_label = "Masonry Infill & Internal MEP Services"
        elif completion_pct <= 95:
            stage_label = "Facade Cladding, Flooring & Finishes"
        else:
            stage_label = "Testing, Commissioning & Handover"
        st.caption(f"Current Phase: **{stage_label}**")

    # Perform Civil & Financial Calculations
    tier_info = TIER_COST_BENCHMARKS[location_tier]
    struct_info = STRUCTURE_TYPE_PARAMS[structure_type]
    quality_mult = FINISH_GRADE_MULTIPLIER[quality_grade]

    # Effective cost per sqft
    effective_cost_sqft = tier_info["base_cost_sqft"] * struct_info["cost_multiplier"] * quality_mult
    total_budget = builtup_sqft * effective_cost_sqft
    capex_incurred = total_budget * (completion_pct / 100.0)
    budget_remaining = total_budget - capex_incurred

    # Real Estate Asset Valuation (Market Value)
    # Market value accounts for land value + completed construction + developer margin
    base_market_rate_sqft = tier_info["market_rate_sqft"] * quality_mult
    # Discount uncompleted portion by a risk premium factor
    completion_factor = 0.35 + (0.65 * (completion_pct / 100.0))
    current_asset_valuation = builtup_sqft * base_market_rate_sqft * completion_factor

    # IS 456 Material Quantities
    steel_tons = (builtup_sqft * struct_info["steel_kg_sqft"]) / 1000.0
    cement_bags = builtup_sqft * struct_info["cement_bags_sqft"]
    cement_tons = (cement_bags * 50) / 1000.0  # 1 bag = 50 kg
    rmc_cum = builtup_sqft * struct_info["rmc_cum_sqft"]
    coarse_agg_tons = rmc_cum * 1.25  # ~1.25 tons per cum concrete
    sand_cft = rmc_cum * 16.5  # ~16.5 cu.ft per cum concrete

    st.markdown("---")

    # Financial & Valuation KPIs
    st.markdown("#### 💰 Financial Valuation & CapEx Matrix")
    k1, k2, k3, k4 = st.columns([1.1, 1.1, 1.1, 1.2])

    with k1:
        render_metric_card("Total Project Budget", format_inr(total_budget), f"Cost: ₹{effective_cost_sqft:,.0f}/sqft", "💼", "#F8FAFC")
    with k2:
        render_metric_card("CapEx Incurred", format_inr(capex_incurred), f"{completion_pct}% Progress Disbursed", "📉", "#38BDF8")
    with k3:
        render_metric_card("Remaining Outlay", format_inr(budget_remaining), "Required to Handover", "⏳", "#F59E0B")
    with k4:
        render_metric_card("Current Asset Valuation", format_inr(current_asset_valuation), "Fair Market Capitalization", "🏷️", "#10B981")

    # Progress Bar & Milestone Roadmap
    st.markdown("#### 🚩 Milestone Progress & Civil Phasing")
    st.progress(completion_pct / 100.0, text=f"Overall Structural Completion: {completion_pct}% ({stage_label})")

    # Visual Breakdown: Cost Distribution & CapEx Donut
    chart_col1, chart_col2 = st.columns([1.2, 1], gap="large")

    with chart_col1:
        # Cost distribution breakdown
        categories = ["RCC Substructure & Superstructure", "Reinforcement Steel (Fe 500D)", "Cement & Concrete Ready-Mix", "MEP & Electrical HVAC", "Finishes, Facade & Glazing", "Contingency & Approvals"]
        allocations = [
            total_budget * 0.28,
            total_budget * 0.22,
            total_budget * 0.16,
            total_budget * 0.14,
            total_budget * 0.14,
            total_budget * 0.06
        ]
        fig_bar = go.Figure(
            go.Bar(
                x=[format_inr(a) for a in allocations],
                y=categories,
                orientation='h',
                marker=dict(
                    color=["#F59E0B", "#38BDF8", "#10B981", "#818CF8", "#F472B6", "#94A3B8"],
                    line=dict(color="#1E293B", width=1)
                ),
                text=[format_inr(a) for a in allocations],
                textposition='auto',
            )
        )
        fig_bar.update_layout(
            title={"text": "Cost Component Allocation", "font": {"color": "#F8FAFC", "size": 14}},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#94A3B8"},
            height=280,
            margin=dict(l=10, r=10, t=35, b=10),
            xaxis=dict(showgrid=False, showticklabels=False),
            yaxis=dict(tickfont=dict(size=11, color="#CBD5E1"))
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        # CapEx Incurred vs Remaining Donut
        fig_donut = go.Figure(
            go.Pie(
                labels=["CapEx Incurred", "Balance CapEx Remaining"],
                values=[capex_incurred, budget_remaining],
                hole=0.6,
                marker=dict(colors=["#38BDF8", "#334155"]),
                textinfo="percent+label",
                textfont=dict(color="#F8FAFC", size=12),
            )
        )
        fig_donut.update_layout(
            title={"text": "Capital Disbursement Ratio", "font": {"color": "#F8FAFC", "size": 14}},
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={"color": "#94A3B8"},
            height=280,
            margin=dict(l=10, r=10, t=35, b=10),
            showlegend=False
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")

    # IS 456 Material Estimation Table
    st.markdown("#### 🏗️ IS 456 Bill of Quantities (Material Estimates)")
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        render_metric_card("Structural Steel (TMT)", f"{steel_tons:,.1f} MT", f"{(steel_tons * 1000) / builtup_sqft:.1f} kg/sqft (Fe 500D)", "🔩", "#38BDF8")
    with m_col2:
        render_metric_card("Cement Consumption", f"{cement_bags:,.0f} Bags", f"{cement_tons:,.1f} MT (OPC 53/PPC)", "🧱", "#F59E0B")
    with m_col3:
        render_metric_card("Ready-Mix Concrete", f"{rmc_cum:,.0f} m³", "Grade M25 to M40", "🚚", "#10B981")
    with m_col4:
        render_metric_card("Coarse Aggregates", f"{coarse_agg_tons:,.0f} MT", f"Sand: {sand_cft:,.0f} cu.ft", "🪨", "#E2E8F0")

    st.markdown("---")

    # 3D Architectural Conceptual Visualization via Pollinations AI
    st.markdown("#### 🎨 Conceptual 3D Architectural Rendering (Pollinations AI Integration)")
    st.markdown(
        "Synthesize high-fidelity conceptual architectural visualizations reflecting your structure typology, "
        "exterior facade materials, and ambient lighting directly via neural prompt synthesis."
    )

    r_col1, r_col2 = st.columns([1, 1.4], gap="large")

    with r_col1:
        render_style = st.selectbox(
            "Architectural Visual Style",
            [
                "Ultra-Modern Glass Curtain Wall & Terraces",
                "Sustainable Biophilic Timber & Vertical Greenery",
                "Monolithic Architectural Exposed Concrete",
                "Futuristic Parametric Aerodynamic Facade",
                "Neo-Classical Luxury Heritage Stone"
            ],
            index=0,
            key="render_style_selector"
        )
        lighting_mood = st.selectbox(
            "Lighting & Atmosphere",
            ["Dramatic Dusk Golden Hour", "Crisp Architectural Midday Sun", "Sleek Blue Hour with Accent LEDs", "Atmospheric Foggy Morning"],
            index=0,
            key="render_lighting_selector"
        )
        
        # User seed control
        seed_btn = st.button("🎲 Regenerate New 3D Perspective", use_container_width=True)
        if seed_btn:
            st.session_state["render_seed"] = random.randint(1000, 999999)
        
        active_seed = st.session_state.get("render_seed", 42891)

        # Build Pollinations Prompt
        city_short = location_tier.split("(")[1].split(",")[0].strip()
        base_desc = struct_info["render_desc"]
        full_prompt = (
            f"masterpiece, architectural photography, 8k render, {base_desc}, "
            f"style of {render_style}, set in urban {city_short} skyline, "
            f"{lighting_mood}, highly detailed, ray tracing reflections, cinematic composition, photorealistic civil engineering model"
        )

        encoded_prompt = urllib.parse.quote(full_prompt)
        pollinations_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1280&height=720&nologo=true&seed={active_seed}&model=flux"

        st.caption(f"**Synthesized Prompt:** `{full_prompt[:140]}...`")

    with r_col2:
        with st.container():
            st.image(
                pollinations_url,
                caption=f"Conceptual 3D Visualization ({structure_type} - {render_style}) [Seed: {active_seed}]",
                use_container_width=True
            )
            st.caption("Powered by Pollinations.ai Neural Image Generator")
