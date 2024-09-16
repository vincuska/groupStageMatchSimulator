from itertools import combinations
from copy import deepcopy

def guess_matches(group):
    num_teams = len(group)
    matchups = {}

    for team_a in range(num_teams):
        for team_b in range(team_a + 1, num_teams):
            matchups[(team_a, team_b)] = [0, 0]

    matches = list(combinations(range(num_teams), 2))

    def can_distribute_goals(remaining_goals, remaining_goals_against, match_index, blacklist):
        if match_index >= len(matches):
            if all(goals == 0 for goals in remaining_goals) and all(goals == 0 for goals in remaining_goals_against):
                results = [[0, 0, 0] for _ in range(num_teams)]
                for (team_a, team_b), (goals_a, goals_b) in matchups.items():
                    if goals_a > goals_b:
                        results[team_a][0] += 1 # team_a wins
                        results[team_b][2] += 1 # team_b loses
                    elif goals_a < goals_b:
                        results[team_a][2] += 1 # team_b wins
                        results[team_b][0] += 1 # team_a loses
                    else:
                        results[team_a][1] += 1 # draw for both
                        results[team_b][1] += 1

                for team_idx, (_, wins, draws, losses, _, _) in enumerate(group):
                    if results[team_idx] != [wins, draws, losses]:
                        return False

                return matchups not in blacklist
            return False

        team_a, team_b = matches[match_index]
        for goals_a in range(min(remaining_goals[team_a], remaining_goals_against[team_b]) + 1):
            for goals_b in range(min(remaining_goals[team_b], remaining_goals_against[team_a]) + 1):
                matchups[(team_a, team_b)] = [goals_a, goals_b]
                remaining_goals[team_a] -= goals_a
                remaining_goals[team_b] -= goals_b
                remaining_goals_against[team_a] -= goals_b
                remaining_goals_against[team_b] -= goals_a

                if can_distribute_goals(remaining_goals, remaining_goals_against, match_index + 1, blacklist):
                    return True

                remaining_goals[team_a] += goals_a
                remaining_goals[team_b] += goals_b
                remaining_goals_against[team_a] += goals_b
                remaining_goals_against[team_b] += goals_a

        return False

    initial_goals = [team[4] for team in group]
    initial_goals_against = [team[5] for team in group]

    blacklist = []
    while True:
        if can_distribute_goals(initial_goals.copy(), initial_goals_against.copy(), 0, blacklist):
            blacklist.append(deepcopy(matchups))
        else:
            break

    print(f"Found {len(blacklist)} valid distributions:")
    for team_idx, distribution in enumerate(blacklist, 1):
        print(f"\nDistribution {team_idx}:")
        for (team_a, team_b), goals in distribution.items():
            print(f"{group[team_a][0]} vs {group[team_b][0]}: {goals[0]} - {goals[1]}")

group = [ # Country, Wins, Draws, Losses, Goals For, Goals Against
    ["Germany", 2, 1, 0, 8, 2],
    ["Switzerland", 1, 2, 0, 5, 3],
    ["Hungary", 1, 0, 2, 2, 5],
    ["Scotland", 0, 1, 2, 2, 7]
]

guess_matches(group)
