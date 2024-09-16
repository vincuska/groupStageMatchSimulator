from itertools import combinations
from copy import deepcopy

def guess_matches(group):
    num_teams = len(group)
    matchups = {}

    for i in range(num_teams):
        for j in range(i + 1, num_teams):
            matchups[(i, j)] = [0, 0]

    matches = list(combinations(range(num_teams), 2))

    def can_distribute_goals(remaining_goals, remaining_goals_against, match_index, blacklist):
        if match_index >= len(matches):
            if all(goals == 0 for goals in remaining_goals) and all(goals == 0 for goals in remaining_goals_against):
                results = [[0, 0, 0] for _ in range(num_teams)]
                for (i, j), (goals_i, goals_j) in matchups.items():
                    if goals_i > goals_j:
                        results[i][0] += 1
                        results[j][2] += 1
                    elif goals_i < goals_j:
                        results[i][2] += 1
                        results[j][0] += 1
                    else:
                        results[i][1] += 1
                        results[j][1] += 1

                for idx, (_, wins, draws, losses, _, _) in enumerate(group):
                    if results[idx] != [wins, draws, losses]:
                        return False

                return matchups not in blacklist
            return False

        i, j = matches[match_index]
        for goals_i in range(min(remaining_goals[i], remaining_goals_against[j]) + 1):
            for goals_j in range(min(remaining_goals[j], remaining_goals_against[i]) + 1):
                matchups[(i, j)] = [goals_i, goals_j]
                remaining_goals[i] -= goals_i
                remaining_goals[j] -= goals_j
                remaining_goals_against[i] -= goals_j
                remaining_goals_against[j] -= goals_i

                if can_distribute_goals(remaining_goals, remaining_goals_against, match_index + 1, blacklist):
                    return True

                remaining_goals[i] += goals_i
                remaining_goals[j] += goals_j
                remaining_goals_against[i] += goals_j
                remaining_goals_against[j] += goals_i

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
    for idx, distribution in enumerate(blacklist, 1):
        print(f"\nDistribution {idx}:")
        for (i, j), goals in distribution.items():
            print(f"{group[i][0]} vs {group[j][0]}: {goals[0]} - {goals[1]}")

group = [ # Country, Wins, Draws, Losses, Goals For, Goals Against
    ["Germany", 2, 1, 0, 8, 2],
    ["Switzerland", 1, 2, 0, 5, 3],
    ["Hungary", 1, 0, 2, 2, 5],
    ["Scotland", 0, 1, 2, 2, 7]
]

guess_matches(group)
