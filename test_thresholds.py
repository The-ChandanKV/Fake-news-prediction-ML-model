import urllib.request
import json

def test(label, text):
    payload = json.dumps({"text": text}).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:5000/api/predict",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    print(f"\n[{label}]")
    print(f"  Verdict    : {data['prediction']}")
    print(f"  Confidence : {data['confidence']}%")
    print(f"  Prob Real  : {data['prob_real']}%")
    print(f"  Prob Fake  : {data['prob_fake']}%")
    if data.get("warning"):
        print(f"  Warning    : {data['warning']}")

# Test 1: Genuine Indian news
test(
    "INDIAN REAL - PM Modi address",
    "Prime Minister Narendra Modi addressed the nation on economic reforms, stating India GDP growth rate has reached 7.2 percent this fiscal year according to Ministry of Finance data released today from New Delhi."
)

# Test 2: Clear fake news
test(
    "FAKE NEWS",
    "SHOCKING: Scientists claim bleach cures cancer! Globalists hiding the truth! Share before deleted! Deep state exposed by whistleblower! 100% real information!"
)

# Test 3: Borderline Indian news
test(
    "BORDERLINE",
    "Some sources suggest the government may or may not have changed the policy on petrol prices, though officials have not confirmed this report circulating on social media today."
)
