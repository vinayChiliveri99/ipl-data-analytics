"""Shared chart helpers, so every chart has the same clean look."""

import matplotlib.pyplot as plt

# Background, text and axis colors
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

# Color for single-series bar charts
BAR_COLOR = "#2a78d6"

# Colors for multi-series (stacked) charts, always used in this order.
# The order was checked so neighbouring colors stay distinct for color-blind
# readers. Up to 8 series get a color; the last slot is gray for "Other".
SERIES_COLORS = [
    "#2a78d6",  # blue
    "#eb6834",  # orange
    "#1baf7a",  # aqua
    "#eda100",  # yellow
    "#e87ba4",  # magenta
    "#008300",  # green
    "#4a3aa7",  # violet
    "#e34948",  # red
    "#b4b2a9",  # gray, for "Other"
]


def create_chart(
    width: float, height: float, title: str, subtitle: str, horizontal: bool
):
    """Create a styled figure and axes with a left-aligned title and subtitle.

    `horizontal` is True for bars that grow left to right, False for columns
    that grow bottom to top. It decides which axis gets the gridlines.
    """
    fig, ax = plt.subplots(figsize=(width, height), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)

    # Keep only the baseline the bars grow from, as a light gray line
    for side in ("top", "right", "left", "bottom"):
        ax.spines[side].set_visible(False)
    baseline_side = "left" if horizontal else "bottom"
    ax.spines[baseline_side].set_visible(True)
    ax.spines[baseline_side].set_color(BASELINE)

    # Faint solid gridlines along the value axis, drawn behind the bars
    ax.grid(axis="x" if horizontal else "y", color=GRIDLINE, linewidth=0.8)
    ax.set_axisbelow(True)

    # Value axis numbers with thousands separators: 25,000 instead of 25000
    value_axis = ax.xaxis if horizontal else ax.yaxis
    value_axis.set_major_formatter("{x:,g}")
    ax.tick_params(colors=TEXT_SECONDARY, labelsize=10, length=0, pad=6)

    ax.set_title(
        title,
        loc="left",
        fontsize=16,
        fontweight="bold",
        color=TEXT_PRIMARY,
        pad=30,
    )
    ax.text(
        0,
        1.02,
        subtitle,
        transform=ax.transAxes,
        fontsize=11,
        color=TEXT_SECONDARY,
    )
    return fig, ax


def style_axis_labels(ax, xlabel: str, ylabel: str) -> None:
    """Set both axis titles in the secondary text color."""
    ax.set_xlabel(xlabel, fontsize=11, color=TEXT_SECONDARY, labelpad=10)
    ax.set_ylabel(ylabel, fontsize=11, color=TEXT_SECONDARY, labelpad=10)


def plot_horizontal_bar(
    data: list[tuple[str, float]],
    title: str,
    subtitle: str,
    xlabel: str,
    ylabel: str,
    value_format: str = "{:,}",
) -> None:
    """Show a horizontal bar chart of (label, value) pairs.

    Pairs are drawn top to bottom in the order given, so pass them already
    sorted. `value_format` controls the number printed at each bar's tip,
    e.g. "{:,}" for 4,423 or "{:.2f}" for 6.25.
    """
    # barh draws the first item at the bottom, so reverse to put it on top
    labels = [label for label, _ in reversed(data)]
    values = [value for _, value in reversed(data)]

    fig, ax = create_chart(
        width=12,
        height=0.45 * len(data) + 2.5,
        title=title,
        subtitle=subtitle,
        horizontal=True,
    )
    bars = ax.barh(labels, values, height=0.6, color=BAR_COLOR)

    value_labels = [value_format.format(value) for value in values]
    ax.bar_label(bars, labels=value_labels, padding=6, color=TEXT_PRIMARY)
    ax.margins(x=0.08)  # leave room on the right for the value labels

    style_axis_labels(ax, xlabel, ylabel)
    fig.tight_layout()
    plt.show()


def plot_column_chart(
    data: list[tuple[str, int]],
    title: str,
    subtitle: str,
    xlabel: str,
    ylabel: str,
) -> None:
    """Show a vertical bar chart of (label, value) pairs, left to right."""
    labels = [label for label, _ in data]
    values = [value for _, value in data]

    fig, ax = create_chart(
        width=11, height=6.5, title=title, subtitle=subtitle, horizontal=False
    )
    bars = ax.bar(labels, values, width=0.6, color=BAR_COLOR)
    ax.bar_label(bars, padding=4, color=TEXT_PRIMARY)
    ax.margins(y=0.1)  # leave room above the tallest bar for its label

    style_axis_labels(ax, xlabel, ylabel)
    fig.tight_layout()
    plt.show()


def plot_stacked_bar(
    counts_by_season: dict[str, dict[str, int]],
    groups: list[str],
    title: str,
    subtitle: str,
    xlabel: str,
    ylabel: str,
) -> None:
    """Show a stacked column per season, one colored segment per group.

    `counts_by_season` looks like {"2008": {"Mumbai Indians": 7, ...}, ...}.
    Groups are stacked bottom to top in the order given and each keeps the
    same color in every chart.
    """
    if len(groups) > len(SERIES_COLORS):
        raise ValueError(f"At most {len(SERIES_COLORS)} groups can get a color")

    seasons = sorted(counts_by_season)

    fig, ax = create_chart(
        width=13, height=7.5, title=title, subtitle=subtitle, horizontal=False
    )

    bottoms = [0] * len(seasons)
    for group, color in zip(groups, SERIES_COLORS):
        heights = []
        for season in seasons:
            heights.append(counts_by_season[season].get(group, 0))

        # A thin edge in the background color leaves a small gap between
        # segments, so neighbouring colors don't run into each other
        ax.bar(
            seasons,
            heights,
            bottom=bottoms,
            width=0.6,
            color=color,
            edgecolor=SURFACE,
            linewidth=1.5,
            label=group,
        )
        bottoms = [bottom + height for bottom, height in zip(bottoms, heights)]

    # Season total on top of each column
    for position, total in enumerate(bottoms):
        ax.text(
            position,
            total + 1,
            f"{total}",
            ha="center",
            va="bottom",
            fontsize=10,
            color=TEXT_PRIMARY,
        )
    ax.margins(y=0.08)

    # Reverse the legend so it reads in the same order as the stack, top first
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(
        handles[::-1],
        labels[::-1],
        loc="upper left",
        bbox_to_anchor=(1.01, 1),
        frameon=False,
        fontsize=10,
        labelcolor=TEXT_PRIMARY,
    )

    style_axis_labels(ax, xlabel, ylabel)
    fig.tight_layout()
    plt.show()
