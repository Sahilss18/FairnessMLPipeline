"""
Comprehensive Flask API test suite.
Tests health, baseline analysis, Groq autoregressive reasoning, batch analysis, and audit chain endpoints.
"""
import requests
import json
import sys

if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

API_BASE = "http://localhost:5000"

def run_tests():
    print("\n" + "=" * 80)
    print("FAIRNESS & BIAS DETECTION API TEST SUITE")
    print("=" * 80)

    # 1. Health check
    try:
        r = requests.get(f"{API_BASE}/api/health", timeout=5)
        print(f"\n[1] GET /api/health -> Status: {r.status_code}")
        print("    Payload:", r.json())
        assert r.status_code == 200, "Health check failed"
    except Exception as e:
        print(f"[FAIL] Could not connect to API server at {API_BASE}: {e}")
        print("Please ensure the Flask API is running on port 5000.")
        return False

    # 2. Examples endpoint
    try:
        r = requests.get(f"{API_BASE}/api/examples", timeout=5)
        print(f"\n[2] GET /api/examples -> Status: {r.status_code}")
        data = r.json()
        print(f"    Loaded {len(data.get('examples', []))} example comments.")
    except Exception as e:
        print(f"[FAIL] /api/examples failed: {e}")

    # 3. Analyze single comment with Groq reasoning
    test_comment = "Women belong in the kitchen."
    try:
        r = requests.post(
            f"{API_BASE}/api/analyze",
            json={"comment": test_comment, "use_groq": True},
            timeout=15
        )
        print(f"\n[3] POST /api/analyze (with Groq) -> Status: {r.status_code}")
        res = r.json()
        print(f"    Comment: '{test_comment}'")
        print(f"    Baseline Prediction: {res.get('prediction')} (Confidence: {res.get('confidence', 0):.2%})")
        
        if 'groq_reasoning' in res:
            groq = res['groq_reasoning']
            print(f"    Groq Model: {groq.get('model')}")
            print(f"    Groq Explanation: {groq.get('explanation')}")
            print(f"    Groq Prediction: {'biased' if groq.get('groq_prediction') == 1 else 'fair'}")
        
        if 'audit' in res:
            print(f"    Audit Logged: {res['audit'].get('logged')} (ID: {res['audit'].get('audit_id')})")
            
    except Exception as e:
        print(f"[FAIL] /api/analyze with Groq failed: {e}")

    # 4. Batch analyze
    batch_comments = [
        "Everyone deserves equal treatment under the law.",
        "That person is completely incompetent because of their race."
    ]
    try:
        r = requests.post(
            f"{API_BASE}/api/batch-analyze",
            json={"comments": batch_comments},
            timeout=10
        )
        print(f"\n[4] POST /api/batch-analyze -> Status: {r.status_code}")
        b_res = r.json()
        print(f"    Analyzed {b_res.get('total_analyzed')} comments. Biased: {b_res.get('biased_count')}, Fair: {b_res.get('fair_count')}")
    except Exception as e:
        print(f"[FAIL] /api/batch-analyze failed: {e}")

    # 5. Audit endpoints
    try:
        r_ver = requests.get(f"{API_BASE}/api/audit/verify", timeout=5)
        print(f"\n[5] GET /api/audit/verify -> Status: {r_ver.status_code}")
        print(f"    Chain valid: {r_ver.json().get('verified')} ({r_ver.json().get('valid_entries')}/{r_ver.json().get('total_entries')} valid)")

        r_exp = requests.get(f"{API_BASE}/api/audit/export?limit=5", timeout=5)
        print(f"\n[6] GET /api/audit/export -> Status: {r_exp.status_code}")
        print(f"    Recent entries exported: {r_exp.json().get('count')}")

        r_stat = requests.get(f"{API_BASE}/api/audit/stats", timeout=5)
        print(f"\n[7] GET /api/audit/stats -> Status: {r_stat.status_code}")
        print(f"    Audit Stats: {r_stat.json()}")
    except Exception as e:
        print(f"[FAIL] Audit endpoints failed: {e}")

    print("\n" + "=" * 80)
    print("[SUCCESS] API TEST SUITE FINISHED")
    print("=" * 80 + "\n")
    return True

if __name__ == "__main__":
    run_tests()
