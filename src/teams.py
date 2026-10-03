"""Team groups shared by the per-team, per-season charts."""

# The eight franchises that played most IPL seasons. They are listed in a fixed
# order so each team keeps the same color in every chart.
MAIN_TEAMS = [
    "Chennai Super Kings",
    "Delhi Daredevils",
    "Kings XI Punjab",
    "Kolkata Knight Riders",
    "Mumbai Indians",
    "Rajasthan Royals",
    "Royal Challengers Bangalore",
    "Sunrisers Hyderabad",
]

# Short-lived franchises (Deccan Chargers, Kochi Tuskers Kerala, Pune Warriors,
# Gujarat Lions, Rising Pune Supergiant/s) are grouped under this name, because
# more than 8 colors in one chart become hard to tell apart.
OTHER_TEAMS = "Other teams"

TEAM_GROUPS = MAIN_TEAMS + [OTHER_TEAMS]


def team_group(team: str) -> str:
    """Return the team's own name if it is a main team, else "Other teams"."""
    if team in MAIN_TEAMS:
        return team
    return OTHER_TEAMS
