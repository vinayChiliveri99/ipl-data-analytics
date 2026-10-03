"""Top 10 economical bowlers in the year 2015. Plot a bar chart."""

import matplotlib.pyplot as plt

def plot_top_economical_bowlers(deliveries: list[dict[str, str]], matches: list[dict[str, str]], top_n: int = 10, year: str = "2015") -> None:
    """Plot a bar chart of top `top_n` economical bowlers in the year `year`."""
    # Calculate total runs conceded and total balls bowled by each bowler in the specified year
    bowler_stats = {}
    for ball in deliveries:
        # using this match_id find the season of the match from matches data
        match = next((m for m in matches if m["id"] == ball["match_id"]), None)
        if match and match["season"] == year:
            bowler = ball["bowler"]
            runs_conceded = int(ball["total_runs"])
            if bowler not in bowler_stats:
                bowler_stats[bowler] = {"runs": 0, "balls": 0}
            bowler_stats[bowler]["runs"] += runs_conceded
            bowler_stats[bowler]["balls"] += 1

    # Calculate economy rate for each bowler
    economy_rates = {}
    for bowler, stats in bowler_stats.items():
        if stats["balls"] > 0:
            overs_bowled = stats["balls"] / 6
            economy_rate = stats["runs"] / overs_bowled
            economy_rates[bowler] = economy_rate

    # Sort bowlers by economy rate and get the top `top_n`
    top_bowlers = sorted(economy_rates.items(), key=lambda item: item[1])[:top_n]

    # Prepare data for plotting
    bowlers = [item[0] for item in top_bowlers]
    economy_values = [item[1] for item in top_bowlers]

    # Plot the bar chart
    plt.bar(bowlers, economy_values)
    plt.xlabel("Bowler")
    plt.ylabel("Economy Rate")
    plt.title(f"Top {top_n} Economical Bowlers in {year} IPL Season")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
