import numpy as np

# ===== Sample Data =====
results = [1.8, 1.9, 2.0, 3.2, 1.7, 1.8, 1.9, 2.1, 3.3, 1.6, 1.7, 1.8, 2.2, 3.1]

# ===== Trend Detection =====
def detect_trend(results):
    pattern = []
    for i in range(1, len(results)):
        if results[i] > results[i-1]:
            pattern.append("big")
        else:
            pattern.append("small")
    return pattern

# ===== Smart Pattern Detection =====
def detect_warning(pattern):
    warning = ""
    if len(pattern) >= 7:
        last7 = pattern[-7:]
        if last7[:3] == ["big", "big", "big"] and last7[3] == "small" and last7[4:] == ["big", "big", "big"]:
            warning = "⚠️ Pattern Detected: 3 big → 1 small → 3 big"
    return warning

# ===== Trend Break Detection =====
def is_trend_break(pattern):
    if len(pattern) < 2:
        return False
    return pattern[-1] != pattern[-2]

# ===== Next Number Prediction =====
def predict_next(results, pattern):
    avg = round(np.mean(results), 2)
    if is_trend_break(pattern):
        next_trend = "small" if pattern[-1] == "big" else "big"
    else:
        next_trend = pattern[-1]

    if next_trend == "small":
        next_num = avg - 0.2
    else:
        next_num = avg + 0.2

    return round(next_num, 2), next_trend

# ===== Main =====
pattern = detect_trend(results)
warning = detect_warning(pattern)
prediction, predicted_trend = predict_next(results, pattern)

print(f"Results: {results}")
print(f"Pattern Detected: {pattern}")
print(f"Warning: {warning}")
print(f"Trend Break: {is_trend_break(pattern)}")
print(f"Next Number Prediction: {prediction}× ({predicted_trend})")
