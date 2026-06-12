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

def load_gold_reviews(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_gold_audit():
    gold_file = os.path.join(root_dir, "gold_reviews.json")
    if not os.path.exists(gold_file):
        print(f"Error: {gold_file} does not exist.")
        sys.exit(1)

    print("=" * 70)
    print(" VERISIGHT AI — GOLD STANDARD CALIBRATION AUDIT RUNNER")
    print("=" * 70)
    print(f"Loading human-curated benchmark dataset from: {gold_file}")
    
    test_cases = load_gold_reviews(gold_file)
    print(f"Loaded {len(test_cases)} benchmark cases.")
    print("Running audit pipeline...\n")

    failures = []
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
            }
            
        stats = category_stats[category]
        stats["count"] += 1
        total_run += 1
        
        # Run analysis
        try:
            analysis = trust_analysis_service.analyze(review_text)
        except Exception as e:
            print(f"ERROR running case {case_id} [{category}]: {e}")
            failures.append({
                "id": case_id,
                "category": category,
                "review": review_text,
                "expected": expected,
                "actual": None,
                "reasons": [f"Exception thrown: {str(e)}"]
            })
            continue

        # Accumulate metrics
        stats["total_trust"] += analysis.trust_score
        stats["total_confidence"] += analysis.confidence
        
        # Validation checks
        mismatch_reasons = []
        
        # 1. Risk Level check
        if analysis.risk_level != expected["risk_level"]:
            mismatch_reasons.append(f"Risk level mismatch: expected '{expected['risk_level']}', got '{analysis.risk_level}'")
            
        # 2. Evidence Strength check
        if analysis.evidence_strength != expected["evidence_strength"]:
            mismatch_reasons.append(f"Evidence strength mismatch: expected '{expected['evidence_strength']}', got '{analysis.evidence_strength}'")
            
        # 3. Trust Score range check
        min_trust = expected["min_trust_score"]
        max_trust = expected["max_trust_score"]
        if not (min_trust <= analysis.trust_score <= max_trust):
            mismatch_reasons.append(f"Trust score {analysis.trust_score} outside [{min_trust}, {max_trust}]")
            
        # 4. Confidence range check (if present)
        if "min_confidence" in expected and "max_confidence" in expected:
            min_conf = expected["min_confidence"]
            max_conf = expected["max_confidence"]
            if not (min_conf <= analysis.confidence <= max_conf):
                mismatch_reasons.append(f"Confidence {analysis.confidence} outside [{min_conf}, {max_conf}]")

        if not mismatch_reasons:
            stats["passed"] += 1
            total_passed += 1
        else:
            failures.append({
                "id": case_id,
                "category": category,
                "review": review_text,
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
    print(f"{'Category':<25} | {'Count':<5} | {'Pass Rate':<9} | {'Avg Trust':<9} | {'Avg Conf':<8}")
    print("-" * 70)
    
    formatted_category_stats = {}
    for cat, stat in category_stats.items():
        cat_count = stat["count"]
        cat_passed = stat["passed"]
        cat_pass_rate = (cat_passed / cat_count) * 100 if cat_count else 0.0
        avg_trust = stat["total_trust"] / cat_count if cat_count else 0.0
        avg_conf = stat["total_confidence"] / cat_count if cat_count else 0.0
        
        print(f"{cat:<25} | {cat_count:<5} | {cat_pass_rate:>7.2f}% | {avg_trust:>9.2f} | {avg_conf:>8.2f}")
        
        formatted_category_stats[cat] = {
            "count": cat_count,
            "passed": cat_passed,
            "failed": cat_count - cat_passed,
            "pass_rate": round(cat_pass_rate, 2),
            "avg_trust": round(avg_trust, 2),
            "avg_confidence": round(avg_conf, 2),
        }

    print("=" * 70)
    print(f"GOLD AUDIT COMPLETED in {duration:.2f} seconds.")
    print(f"Overall Pass Rate: {total_passed}/{total_run} ({pass_rate:.2f}%)")
    print("=" * 70)
    
    if failures:
        print(f"\n[!] Detected {len(failures)} calibration mismatches / violations:")
        for idx, m in enumerate(failures[:15]):
            print(f"\n{idx+1}. Case {m['id']} [{m['category']}]")
            print(f"   Review  : {m['review'][:100]}...")
            print(f"   Expected: {m['expected']}")
            print(f"   Actual  : {m['actual']}")
            print(f"   Failures: {m['reasons']}")
        if len(failures) > 15:
            print(f"... and {len(failures) - 15} more failures omitted.")
    else:
        print("\n[+] SUCCESS! All gold benchmark cases calibrated within human expectations.")

    # Export results (JSON)
    outputs_dir = os.path.join(root_dir, "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    
    results_export_path = os.path.join(outputs_dir, "gold_evaluation_results.json")
    export_payload = {
        "timestamp": time.time(),
        "total_reviews": total_run,
        "pass_count": total_passed,
        "fail_count": len(failures),
        "pass_rate": round(pass_rate, 2),
        "duration_seconds": round(duration, 3),
        "category_stats": formatted_category_stats,
        "failures": failures
    }
    
    with open(results_export_path, "w", encoding="utf-8") as f:
        json.dump(export_payload, f, indent=2, ensure_ascii=False)
    print(f"\nJSON metrics exported to: {results_export_path}")

    # Export report (Markdown)
    report_export_path = os.path.join(outputs_dir, "gold_evaluation_report.md")
    with open(report_export_path, "w", encoding="utf-8") as f:
        f.write("# VeriSight AI — Gold Standard Calibration Audit Report\n\n")
        f.write(f"**Generated**: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}  \n")
        f.write(f"**Source Dataset**: `gold_reviews.json` (Human-curated Ground Truth)  \n\n")
        
        f.write("## 1. Summary Metrics\n\n")
        f.write("| Metric | Value |\n")
        f.write("| :--- | :--- |\n")
        f.write(f"| **Total Reviews** | {total_run} |\n")
        f.write(f"| **Pass Count** | {total_passed} |\n")
        f.write(f"| **Fail Count** | {len(failures)} |\n")
        f.write(f"| **Overall Pass Rate** | **{pass_rate:.2f}%** |\n")
        f.write(f"| **Execution Duration** | {duration:.3f} seconds |\n\n")
        
        f.write("## 2. Per-Category Breakdown\n\n")
        f.write("| Category | Total Count | Passed | Failed | Pass Rate | Avg Trust | Avg Conf |\n")
        f.write("| :--- | :---: | :---: | :---: | :---: | :---: | :---: |\n")
        for cat, stats in formatted_category_stats.items():
            f.write(f"| {cat} | {stats['count']} | {stats['passed']} | {stats['failed']} | {stats['pass_rate']}% | {stats['avg_trust']} | {stats['avg_confidence']}% |\n")
        f.write("\n")
        
        f.write("## 3. Failure Diagnostics\n\n")
        if failures:
            f.write(f"The evaluation detected **{len(failures)}** calibration mismatches against manual human expectations. Below are the details of each failure:\n\n")
            for idx, fail in enumerate(failures):
                f.write(f"### {idx+1}. Case `{fail['id']}` ({fail['category']})\n")
                f.write(f"- **Review Text**: *\"{fail['review']}\"*\n")
                f.write("- **Expected Values**:\n")
                f.write(f"  - Risk Level: `{fail['expected']['risk_level']}`\n")
                f.write(f"  - Evidence Strength: `{fail['expected']['evidence_strength']}`\n")
                f.write(f"  - Trust Score Range: `[{fail['expected']['min_trust_score']}, {fail['expected']['max_trust_score']}]`\n")
                f.write(f"  - Reasoning: *{fail['expected']['reasoning']}*\n")
                if fail["actual"]:
                    f.write("- **Actual Engine Values**:\n")
                    f.write(f"  - Risk Level: `{fail['actual']['risk_level']}`\n")
                    f.write(f"  - Evidence Strength: `{fail['actual']['evidence_strength']}`\n")
                    f.write(f"  - Trust Score: `{fail['actual']['trust_score']}`\n")
                    f.write(f"  - Confidence: `{fail['actual']['confidence']}%`\n")
                f.write("- **Mismatches Detected**:\n")
                for r in fail["reasons"]:
                    f.write(f"  - ❌ {r}\n")
                f.write("\n---\n\n")
        else:
            f.write("> [!NOTE]\n")
            f.write("> **SUCCESS**: All 50 gold standard cases matched manual expectations perfectly. No calibration failures detected.\n\n")
            
    print(f"Markdown report exported to: {report_export_path}")
    return len(failures) == 0

if __name__ == "__main__":
    success = run_gold_audit()
    sys.exit(0 if success else 1)
