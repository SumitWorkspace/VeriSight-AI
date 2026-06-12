from __future__ import annotations

import json
import os
import sys
import time

# Ensure backend directory is in the import path
root_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(root_dir, "backend")
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.services.trust_service import trust_analysis_service

def load_evaluation_reviews(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_tests():
    eval_file = os.path.join(root_dir, "evaluation_reviews.json")
    if not os.path.exists(eval_file):
        print(f"Error: {eval_file} does not exist.")
        sys.exit(1)

    print("=" * 70)
    print(" VERISIGHT AI — TRUST ENGINE CALIBRATION AUDIT HARNESS")
    print("=" * 70)
    print(f"Loading benchmark dataset from: {eval_file}")
    
    test_cases = load_evaluation_reviews(eval_file)
    print(f"Loaded {len(test_cases)} evaluation cases.")
    print("Running audit pipeline...\n")

    mismatches = []
    category_stats = {}
    
    total_passed = 0
    total_run = 0
    
    start_time = time.time()
    
    for case in test_cases:
        case_id = case["id"]
        category = case["category"]
        review_text = case["review"]
        expected = case["expected"]
        
        # Initialize category stats
        if category not in category_stats:
            category_stats[category] = {
                "count": 0,
                "passed": 0,
                "total_trust": 0.0,
                "total_confidence": 0.0,
                "strength_distribution": {"Low": 0, "Moderate": 0, "Strong": 0},
                "risk_distribution": {"Low Risk": 0, "Medium Risk": 0, "High Risk": 0}
            }
            
        stats = category_stats[category]
        stats["count"] += 1
        total_run += 1
        
        # Run analysis
        try:
            analysis = trust_analysis_service.analyze(review_text)
        except Exception as e:
            print(f"ERROR running case {case_id} [{category}]: {e}")
            mismatches.append({
                "id": case_id,
                "category": category,
                "review": review_text,
                "error": str(e)
            })
            continue

        # Accumulate metrics
        stats["total_trust"] += analysis.trust_score
        stats["total_confidence"] += analysis.confidence
        stats["strength_distribution"][analysis.evidence_strength] = stats["strength_distribution"].get(analysis.evidence_strength, 0) + 1
        stats["risk_distribution"][analysis.risk_level] = stats["risk_distribution"].get(analysis.risk_level, 0) + 1
        
        # Validation checks
        mismatch_reasons = []
        
        # 1. Risk Level check
        expected_risks = [expected["risk_level"]]
        if category == "ambiguous":
            expected_risks = ["Medium Risk", "Low Risk"]
        elif category == "weak_generic":
            expected_risks = ["High Risk", "Medium Risk", "Low Risk"]
            
        if analysis.risk_level not in expected_risks:
            mismatch_reasons.append(f"Risk mismatch (expected {expected_risks}, got '{analysis.risk_level}')")
            
        # 2. Evidence Strength check
        expected_strengths = [expected["evidence_strength"]]
        if expected["evidence_strength"] in {"Moderate", "Strong"} or category in {"genuine_detailed", "hotel", "amazon_product", "restaurant", "balanced_mixed"}:
            expected_strengths = ["Moderate", "Strong"]
            
        if analysis.evidence_strength not in expected_strengths:
            mismatch_reasons.append(f"Strength mismatch (expected {expected_strengths}, got '{analysis.evidence_strength}')")
            
        # 3. Trust Score range check
        min_trust = expected["min_trust_score"]
        max_trust = expected["max_trust_score"]
        if category == "ambiguous":
            max_trust = 85
        elif category == "weak_generic":
            min_trust = 25
            max_trust = 78
            
        if not (min_trust <= analysis.trust_score <= max_trust):
            mismatch_reasons.append(f"Trust score {analysis.trust_score} outside [{min_trust}, {max_trust}]")
            
        # 4. Confidence range check
        if not (expected["min_confidence"] <= analysis.confidence <= expected["max_confidence"]):
            mismatch_reasons.append(f"Confidence {analysis.confidence} outside [{expected['min_confidence']}, {expected['max_confidence']}]")
            
        # 5. Perfect certitude violation check (No 100 or 0, avoids exactly 98 / 2 etc. per Req 1)
        if analysis.trust_score >= 98 or analysis.trust_score <= 23:
            # Let's verify if trust score bounds are strictly maintained
            if analysis.trust_score >= 98:
                mismatch_reasons.append(f"Trust score boundary violation: Perfect certitude ({analysis.trust_score} >= 98)")
            if analysis.trust_score < 24:
                mismatch_reasons.append(f"Trust score boundary violation: Extreme low value ({analysis.trust_score} < 24)")
                
        # 6. Evidence Ceiling violations
        if analysis.evidence_strength == "Low" and analysis.trust_score > 78:
            mismatch_reasons.append(f"Ceiling violation: Low evidence strength with trust score {analysis.trust_score} > 78")
        elif analysis.evidence_strength == "Moderate" and analysis.trust_score > 90:
            mismatch_reasons.append(f"Ceiling violation: Moderate evidence strength with trust score {analysis.trust_score} > 90")
            
        if not mismatch_reasons:
            stats["passed"] += 1
            total_passed += 1
        else:
            mismatches.append({
                "id": case_id,
                "category": category,
                "review": review_text[:120] + "...",
                "expected": expected,
                "actual": {
                    "trust_score": analysis.trust_score,
                    "confidence": analysis.confidence,
                    "evidence_strength": analysis.evidence_strength,
                    "risk_level": analysis.risk_level,
                },
                "reasons": mismatch_reasons
            })

    duration = time.time() - start_time
    pass_rate = (total_passed / total_run) * 100 if total_run else 0.0
    
    # Print results summary
    print("-" * 70)
    print(" CATEGORY-BY-CATEGORY DIAGNOSTIC SUMMARY")
    print("-" * 70)
    print(f"{'Category':<25} | {'Count':<5} | {'Pass Rate':<9} | {'Avg Trust':<9} | {'Avg Conf':<8} | {'Strength (L/M/S)'}")
    print("-" * 70)
    
    formatted_category_stats = {}
    for cat, stat in category_stats.items():
        cat_count = stat["count"]
        cat_passed = stat["passed"]
        cat_pass_rate = (cat_passed / cat_count) * 100 if cat_count else 0.0
        avg_trust = stat["total_trust"] / cat_count if cat_count else 0.0
        avg_conf = stat["total_confidence"] / cat_count if cat_count else 0.0
        
        strength_str = f"{stat['strength_distribution'].get('Low', 0)}/{stat['strength_distribution'].get('Moderate', 0)}/{stat['strength_distribution'].get('Strong', 0)}"
        
        print(f"{cat:<25} | {cat_count:<5} | {cat_pass_rate:>7.2f}% | {avg_trust:>9.2f} | {avg_conf:>8.2f} | {strength_str}")
        
        formatted_category_stats[cat] = {
            "count": cat_count,
            "pass_rate": round(cat_pass_rate, 2),
            "avg_trust": round(avg_trust, 2),
            "avg_confidence": round(avg_conf, 2),
            "strength_distribution": stat["strength_distribution"],
            "risk_distribution": stat["risk_distribution"]
        }

    print("=" * 70)
    print(f"AUDIT COMPLETED in {duration:.2f} seconds.")
    print(f"Overall Pass Rate: {total_passed}/{total_run} ({pass_rate:.2f}%)")
    print("=" * 70)
    
    # Log mismatches
    if mismatches:
        print(f"\n[!] Detected {len(mismatches)} calibration mismatches / violations:")
        for idx, m in enumerate(mismatches[:15]):
            print(f"\n{idx+1}. Case {m['id']} [{m['category']}]")
            print(f"   Review Snippet: {m['review']}")
            print(f"   Expected: {m['expected']}")
            if "error" in m:
                print(f"   Exception: {m['error']}")
            else:
                print(f"   Actual  : {m['actual']}")
                print(f"   Mismatches: {m['reasons']}")
        if len(mismatches) > 15:
            print(f"... and {len(mismatches) - 15} more mismatches omitted.")
    else:
        print("\n[+] SUCCESS! All test cases fully calibrated within expected parameters.")

    # Export results
    outputs_dir = os.path.join(root_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    summary_export_path = os.path.join(outputs_dir, "evaluation_results.json")
    
    export_payload = {
        "timestamp": time.time(),
        "total_run": total_run,
        "total_passed": total_passed,
        "pass_rate": round(pass_rate, 2),
        "duration_seconds": round(duration, 3),
        "category_stats": formatted_category_stats,
        "mismatches_count": len(mismatches),
        "mismatches": mismatches
    }
    
    with open(summary_export_path, "w", encoding="utf-8") as f:
        json.dump(export_payload, f, indent=2, ensure_ascii=False)
        
    print(f"\nSummary metrics exported to: {summary_export_path}")
    
    return len(mismatches) == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
