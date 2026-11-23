# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib==3.10.8"]
# ///
"""Plot the final aggregate counts from one completed comparison."""

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
STRATEGIES = (
    ("original_feedback", "Original feedback", "#24519b"),
    ("simplified_feedback", "Simplified feedback", "#a4551e"),
    ("random_search", "Random search", "#535b69"),
)


def main():
    with (ROOT / "data/search-results.csv").open(newline="") as source:
        rows = list(csv.DictReader(source))
    if len(rows) != 3 or {row["strategy"] for row in rows} != {
        item[0] for item in STRATEGIES
    }:
        raise ValueError("Expected one endpoint for each of the three strategies.")
    protocols = {
        (row["experiment"], row["completion_date_cst"], row["model_family"])
        for row in rows
    }
    if len(protocols) != 1:
        raise ValueError("The rows must belong to one comparison.")
    _, date, model = protocols.pop()
    results = {}
    for row in rows:
        actions = int(row["actions"])
        verified = int(row["distinct_verified_failures"])
        unresolved = int(row["unresolved_actions"])
        if actions != 800 or verified < 0 or not 0 <= unresolved <= actions:
            raise ValueError("Invalid budget or outcome counts.")
        results[row["strategy"]] = verified, unresolved

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11})
    fig, ax = plt.subplots(figsize=(10.4, 4.5), dpi=180)
    fig.subplots_adjust(left=0.24, right=0.93, bottom=0.24, top=0.69)
    fig.text(0.06, 0.9, "First full evaluation on the frozen candidate pool",
             fontsize=17, weight="bold", color="#17243d")
    fig.text(0.06, 0.81,
             f"{model}-family endpoint  ·  {date}  ·  800 actions per strategy",
             fontsize=10.5, color="#50617a")
    print("Strategy                  Actions  Verified  Unresolved")
    for index, (strategy, label, color) in enumerate(STRATEGIES):
        verified, unresolved = results[strategy]
        ax.barh(index, verified, height=0.52, color=color)
        ax.text(verified + 3, index, str(verified), va="center",
                color="#17243d", weight="bold", fontsize=12)
        print(f"{label:<25} {800:>7} {verified:>9} {unresolved:>11}")
    ax.set(xlim=(0, 200), yticks=range(3),
           yticklabels=[item[1] for item in STRATEGIES],
           xticks=range(0, 201, 50))
    ax.invert_yaxis()
    ax.set_xlabel("Distinct verified API/release-pair failures",
                  labelpad=10, color="#50617a")
    ax.set_axisbelow(True)
    ax.grid(axis="x", color="#dce3ec", linewidth=0.8)
    ax.tick_params(axis="both", length=0, pad=9, colors="#50617a")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color("#b4bfce")
    fig.text(0.06, 0.065,
             "All three strategies from one completed comparison. "
             "One run per configuration; unresolved actions consume budget.",
             fontsize=8.5, color="#50617a")
    output = ROOT / "figures/comparison.png"
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, facecolor="white")
    plt.close(fig)
    print(f"Wrote {output.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
