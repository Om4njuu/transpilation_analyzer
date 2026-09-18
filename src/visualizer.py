#visualization engine for transpilation benchmark results

import matplotlib.pyplot as plt
import pandas as pd

#generates line plots comparing depth and 2-qubit gate counts across optimization levels
def plot_transpilation_results(df_ghz: pd.DataFrame, df_qft: pd.DataFrame, output_filename: str = "transpilation_metrics.png") -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True)

    #plot 1 - Circuit Depth vs Optimization Level
    axes[0].plot(df_ghz["optimization_level"], df_ghz["depth"], marker='o', label="GHZ (5q)", linewidth=2)
    axes[0].plot(df_qft["optimization_level"], df_qft["depth"], marker='s', label="QFT (5q)", linewidth=2)
    axes[0].set_title("Circuit Depth vs Optimization Level")
    axes[0].set_xlabel("Optimization Level")
    axes[0].set_ylabel("Circuit Depth")
    axes[0].set_xticks([0, 1, 2, 3])
    axes[0].grid(True, linestyle="--", alpha=0.6)
    axes[0].legend()

    #plot 2 - Two-Qubit Gates vs Optimization Level
    axes[1].plot(df_ghz["optimization_level"], df_ghz["two_qubit_gates"], marker='o', label="GHZ (5q)", linewidth=2)
    axes[1].plot(df_qft["optimization_level"], df_qft["two_qubit_gates"], marker='s', label="QFT (5q)", linewidth=2)
    axes[1].set_title("Two-Qubit Gate Count vs Optimization Level")
    axes[1].set_xlabel("Optimization Level")
    axes[1].set_ylabel("2-Qubit Gates (CX/ECR/CZ)")
    axes[1].set_xticks([0, 1, 2, 3])
    axes[1].grid(True, linestyle="--", alpha=0.6)
    axes[1].legend()

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300)
    print(f"Chart saved successfully as '{output_filename}'")