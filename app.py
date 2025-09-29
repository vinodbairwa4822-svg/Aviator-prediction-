   import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys  # For stopping program

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

# ===== Smart Pattern Alert Detection =====
def detect_warning(pattern):
    warning = ""
    if len(pattern) >= 7:
        last7 = pattern[-7:]
        if last7[:3] == ["big", "big", "big"] and last7[3] == "small" and last7[4:] == ["big", "big", "big"]:
            warning = "⚠️ Pattern Detected: 3 big → 1 small → 3 big"
    return warning

# ===== Trend Break Detection =====
def trend_break(pattern):
    last = pattern[-1]
    for i in reversed(range(len(pattern) - 1)):
        if pattern[i] != last:
            return True
    return False

# ===== Dynamic Multiplier Prediction =====
def predict_multiplier(results, pattern):
    avg = np.mean(results)
    trend_factor = len(set(pattern)) / len(pattern)
    if trend_break(pattern):
        return avg * (1 + trend_factor) * 1.2
    else:
        return avg * (1 + trend_factor)

# ===== Graph with Plane Crash Animation =====
def animate_airplane(results, multiplier, pattern, warning):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(results, marker='o', linestyle='-', color='blue', label="Game Results")
    ax.axhline(multiplier, color='red', linestyle='--', label=f"Prediction: {multiplier:.2f}×")

    if warning:
        ax.text(len(results)//2, max(results)+0.2, warning, fontsize=14, color='orange', weight='bold')

    ax.set_title("Smart Trend Prediction with Plane Crash ✈️💥", fontsize=16)
    ax.set_xlabel("Round", fontsize=14)
    ax.set_ylabel("Multiplier", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    airplane, = ax.plot([], [], marker=">", color="green", markersize=12)

    def init():
        airplane.set_data([], [])
        return airplane,

    def animate(i):
        if i < len(results):
            airplane.set_data(i, results[i])
        if warning and i == len(results) - 1:
            airplane.set_marker("X")  # Plane crash marker
            airplane.set_color("red")
            airplane.set_markevery([i])
            ax.text(i, results[i] + 0.2, "💥 CRASH!", fontsize=14, color="red", weight='bold')
        return airplane,

    ani = animation.FuncAnimation(fig, animate, frames=len(results)+5, init_func=init,
                                  interval=500, blit=True, repeat=False)
    plt.show()

# ===== Main =====
pattern = detect_trend(results)
multiplier = predict_multiplier(results, pattern)
warning = detect_warning(pattern)

print(f"Pattern Detected: {pattern}")
print(f"Trend Break: {trend_break(pattern)}")
print(f"Warning: {warning}")
print(f"Predicted Multiplier: {multiplier:.2f}×")

animate_airplane(results, multiplier, pattern, warning)

if warning:
    raise SystemExit("🚨 Game stopped due to detected pattern and plane crash!")             
