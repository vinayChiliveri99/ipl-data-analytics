"""Top 10 economical bowlers in the year 2015, as a bar chart.

Economy rate = runs conceded by the bowler / overs bowled.

- Runs conceded by the bowler are batsman runs + wides + no-balls. Byes and
  leg-byes are not counted, since they are not the bowler's fault.
- Only legal balls count toward overs: wides and no-balls are bowled again.
"""

from src.data_loader import season_by_match_id
from src.plotting import plot_horizontal_bar


def bowler_stats_for_year(
    deliveries: list[dict[str, str]], matches: list[dict[str, str]], year: str
) -> dict[str, dict[str, int]]:
    """Return {bowler: {"runs": runs conceded, "balls": legal balls}} for `year`."""
    seasons = season_by_match_id(matches)

    stats = {}
    for ball in deliveries:
        if seasons[ball["match_id"]] != year:
            continue

        bowler = ball["bowler"]
        if bowler not in stats:
            stats[bowler] = {"runs": 0, "balls": 0}

        wide_runs = int(ball["wide_runs"])
        noball_runs = int(ball["noball_runs"])
        stats[bowler]["runs"] += int(ball["batsman_runs"]) + wide_runs + noball_runs

        is_legal_ball = wide_runs == 0 and noball_runs == 0
        if is_legal_ball:
            stats[bowler]["balls"] += 1
    return stats


def economy_rates(
    stats: dict[str, dict[str, int]], min_balls: int
) -> dict[str, float]:
    """Return {bowler: economy rate} for bowlers with at least `min_balls`."""
    rates = {}
    for bowler, bowler_stats in stats.items():
        if bowler_stats["balls"] < min_balls:
            continue
        overs_bowled = bowler_stats["balls"] / 6
        rates[bowler] = bowler_stats["runs"] / overs_bowled
    return rates


def plot_top_economical_bowlers(
    deliveries: list[dict[str, str]],
    matches: list[dict[str, str]],
    top_n: int = 10,
    year: str = "2015",
    min_balls: int = 60,
) -> None:
    """Plot the `top_n` bowlers with the lowest economy rate in `year`.

    Bowlers need at least `min_balls` legal balls (60 = 10 overs) to qualify,
    so part-time bowlers with only a few balls don't top the list by chance.
    """
    stats = bowler_stats_for_year(deliveries, matches, year)
    rates = economy_rates(stats, min_balls)
    top_bowlers = sorted(rates.items(), key=lambda item: item[1])[:top_n]

    plot_horizontal_bar(
        top_bowlers,
        title=f"Top {top_n} Economical Bowlers, IPL {year}",
        subtitle=(
            f"Runs conceded per over (lower is better) · "
            f"minimum {min_balls // 6} overs bowled"
        ),
        xlabel="Economy rate (runs per over)",
        ylabel="Bowler",
        value_format="{:.2f}",
    )
