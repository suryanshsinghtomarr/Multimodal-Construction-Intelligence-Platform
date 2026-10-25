"""
Automated Unit & Smoke Test Suite for Multimodal Construction Intelligence Platform.
"""

import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from modules.gemini_client import ConstructionGeminiClient
from sample_data.samples import (
    generate_sample_ppe_image,
    generate_sample_crack_image,
    DEMO_PPE_AUDIT_DATA,
    DEMO_CRACK_DATA
)
from modules.valuation_planner import (
    TIER_COST_BENCHMARKS,
    STRUCTURE_TYPE_PARAMS,
    FINISH_GRADE_MULTIPLIER,
    format_inr
)

def run_tests():
    print(">>> Testing Gemini Client Fallback Mode...")
    client = ConstructionGeminiClient(api_key="")
    assert not client.is_live, "Client should be in demonstration/offline mode when no key is supplied."
    
    # Test multimodal fallback
    res = client.analyze_multimodal(
        image_bytes=b"dummy",
        mime_type="image/jpeg",
        prompt="Audit PPE",
        system_instruction="Safety Auditor",
        fallback_data=DEMO_PPE_AUDIT_DATA,
        is_json=True
    )
    assert res["safety_score"] == 62, f"Expected safety score 62, got {res.get('safety_score')}"
    print("[OK] Multimodal fallback verified.")

    # Test Chat Fallback
    chat_reply = client.chat_response(
        conversation_history=[{"role": "user", "content": "What is the IS 456 curing period?"}],
        system_instruction="Senior Engineer",
        weather_context="Normal"
    )
    assert "IS 456:2000" in chat_reply, "Chat reply did not contain IS 456 standard."
    print("[OK] Engineering chat fallback verified.")

    # Test Sample Image Generation
    print(">>> Testing Synthetic Visual Generators...")
    ppe_bytes = generate_sample_ppe_image("violation")
    assert len(ppe_bytes) > 1000, "PPE image bytes too small."
    
    crack_bytes = generate_sample_crack_image("shear")
    assert len(crack_bytes) > 1000, "Crack image bytes too small."
    print("[OK] Synthetic Visual Generators verified.")

    # Test Valuation & Quantities Calculations
    print(">>> Testing Valuation & Material Estimation Math...")
    sqft = 50000
    tier = list(TIER_COST_BENCHMARKS.keys())[0]
    struct = list(STRUCTURE_TYPE_PARAMS.keys())[0]
    grade = list(FINISH_GRADE_MULTIPLIER.keys())[0]

    cost_sqft = TIER_COST_BENCHMARKS[tier]["base_cost_sqft"] * STRUCTURE_TYPE_PARAMS[struct]["cost_multiplier"] * FINISH_GRADE_MULTIPLIER[grade]
    total_budget = sqft * cost_sqft
    assert total_budget > 0, "Total budget must be greater than zero."
    formatted = format_inr(total_budget)
    assert "Cr" in formatted or "Lakhs" in formatted, f"Formatted amount error: {formatted}"
    print(f"[OK] Valuation for 50,000 sqft: {formatted}")

    print("\n==========================================")
    print("ALL PLATFORM TESTS PASSED SUCCESSFULLY!")
    print("==========================================")

if __name__ == "__main__":
    run_tests()
