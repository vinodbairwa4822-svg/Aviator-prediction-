import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

# ===== Graph Styling + Animation =====
def animate_airplane(results, multiplier, pattern, warning):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_facecolor("#f5f5f5")  # background color

    # Smooth trend line
    ax.plot(results, marker='o', linestyle='-', linewidth=2.5, color='#1f77b4', label="Game Results")
    ax.fill_between(range(len(results)), results, color="#d0e7ff", alpha=0.3)  # area under line

    # Prediction line
    ax.axhline(multiplier, color='#ff4c4c', linestyle='--', linewidth=2, label=f"Prediction: {multiplier:.2f}×")

    # Warning message
    if warning:
        ax.text(len(results)//2, max(results)+0.2, warning, fontsize=14, color='#ff8800', weight='bold')

    # Labels and grid
    ax.set_title("📈 Smart Trend Prediction Chart", fontsize=18, weight='bold')
    ax.set_xlabel("Round", fontsize=14)
    ax.set_ylabel("Multiplier", fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend(fontsize=12)

    # Airplane marker
    airplane, = ax.plot([], [], marker=">", color="green", markersize=14)

    def init():
        airplane.set_data([], [])
        return airplane,

    def animate(i):
        if i < len(results):
            airplane.set_data(i, results[i])
            airplane.set_color("cyan" if pattern[i-1] == "small" else "green")
        return airplane,

    ani = animation.FuncAnimation(fig, animate, frames=len(results)+10, init_func=init,
                                  interval=500, blit=True, repeat=False)
    plt.show()

# ===== Main =====
pattern = detect_trend(results)
multiplier = np.mean(results)  # simple prediction
warning = detect_warning(pattern)

print(f"Pattern Detected: {pattern}")
print(f"Warning: {warning}")
print(f"Predicted Multiplier: {multiplier:.2f}×")

animate_airplane(results, multiplier, pattern, warning)
