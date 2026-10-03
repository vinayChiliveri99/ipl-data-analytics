""" Extra runs conceded per team in the year 2016. Plot a bar chart """

import matplotlib.pyplot as plt

def plot_extra_runs_conceded_2016(deliveries: list[dict[str, str]], matches: list[dict[str, str]]) -> None:
    """Plot a bar chart of extra runs conceded per team in the year 2016."""
    # Count extra runs conceded by team in 2016
    counts = {}
    for ball in deliveries:
        match_id = ball["match_id"]
        # using this match_id find the season of the match from matches data
        match = next((m for m in matches if m["id"] == match_id), None)
        if match and match["season"] == "2016":
            bowling_team = ball["bowling_team"]
            if bowling_team not in counts:
                counts[bowling_team] = 0
            counts[bowling_team] += int(ball["extra_runs"])

    # Sort by team
    sorted_counts = sorted(counts.items(), key=lambda item: item[0])

    # Prepare data for plotting
    teams = [item[0] for item in sorted_counts]
    values = [item[1] for item in sorted_counts]

    # Plot the bar chart
    plt.bar(teams, values)
    plt.xlabel("Team")
    plt.ylabel("Extra Runs Conceded")
    plt.title("Extra Runs Conceded Per Team in 2016 IPL Season")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
