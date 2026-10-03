"""Shared chart helpers."""

import matplotlib.pyplot as plt


def plot_horizontal_bar(
    data: list[tuple[str, int]],
    title: str,
    xlabel: str,
    ylabel: str,
) -> None:
    """Show a horizontal bar chart of (label, value) pairs.

    Pairs are drawn top to bottom in the order given, so pass them
    sorted from highest to lowest.
    """
    # barh draws the first item at the bottom, so reverse to put it on top
    labels = [label for label, _ in reversed(data)]
    values = [value for _, value in reversed(data)]

    fig, ax = plt.subplots(figsize=(14, 9))
    bars = ax.barh(labels, values, edgecolor="black", linewidth=0.7)

    label_offset = max(values) * 0.01
    for bar, value in zip(bars, values, strict=True):
        ax.text(
            bar.get_width() + label_offset,
            bar.get_y() + bar.get_height() / 2,
            f"{value:,}",
            va="center",
            fontsize=10,
            fontweight="bold",
        )

    ax.set_title(title, fontsize=20, fontweight="bold", pad=20)
    ax.set_xlabel(xlabel, fontsize=12, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=12, fontweight="bold")

    ax.grid(axis="x", linestyle="--", alpha=0.3)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)

    fig.tight_layout()
    plt.show()
