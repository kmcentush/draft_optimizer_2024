from typing import Any

import cvxpy as cp
import numpy as np
import polars as pl


class Optimizer:
    def __init__(
        self,
        pos_col: str,
        week_cols: list[str],
        roster_size: int,
        min_pos_const: dict[str, int],
        max_pos_const: dict[str, int],
    ):
        self.pos_col = pos_col
        self.week_cols = week_cols
        self.roster_size = roster_size
        self.min_pos_const = min_pos_const
        self.max_pos_const = max_pos_const

    def optimal_roster(
        self, data: "pl.DataFrame", team_picks_idx: set[int], all_picks_idx: set[int], verbose: bool = False
    ) -> set[int]:
        # Get available players
        all_idx = set(range(data.shape[0]))
        available_idx = all_idx - all_picks_idx

        # Get data
        sorted_available_idx = sorted(available_idx)
        sorted_team_picks_idx = sorted(team_picks_idx)
        points_vals = data[sorted_available_idx, self.week_cols].to_numpy()
        pos_vals = data[sorted_available_idx, self.pos_col].to_numpy()
        team_weekly_points = data[sorted_team_picks_idx, self.week_cols].sum().to_numpy().ravel()
        team_pos_counts = dict(data[sorted_team_picks_idx, self.pos_col].value_counts().iter_rows())

        # The variable we are solving for. We define our output variable as a bool
        # since we have to make a binary decision on each player (pick or don't pick)
        roster = cp.Variable(len(available_idx), boolean=True)

        # Save constraints
        constraints = []

        # Our roster must be composed of exactly `roster_size` players
        constraints.append(cp.sum(roster) == self.roster_size - len(team_picks_idx))

        # Define position constraints
        for pos in self.min_pos_const.keys():
            is_pos = pos_vals == pos
            pos_sum = cp.sum(is_pos @ roster)
            min_num = self.min_pos_const[pos]
            max_num = self.max_pos_const[pos]
            already_picked = team_pos_counts[pos] if pos in team_pos_counts.keys() else 0
            constraints.append(pos_sum >= min_num - already_picked)
            constraints.append(pos_sum <= max_num - already_picked)

        # Define the objective
        # TODO: refine primary objective to only reflect players that are playing each week, not the entire roster
        # TODO: secondary objective to maximize the minimum weekly points on the bench, i.e. have quality back-ups
        weekly_points = (roster @ points_vals) + team_weekly_points
        min_weekly_points = cp.min(weekly_points)
        objective = cp.Maximize(min_weekly_points)

        # Try to solve
        try:
            # Solve
            problem = cp.Problem(objective, constraints)
            problem.solve(verbose=verbose)

            # Get result
            roster_idx = roster.value
            if roster_idx is not None:
                # Note: rounding is needed due to precision errors
                opt_picks = np.array(sorted_available_idx)[roster_idx.round(0).astype(bool)]  # re-align indices
                result = set(opt_picks.tolist())
            else:
                print("No solution found. No exception raised.")
                result = set()
        except Exception as e:
            print(f"No solution found. Exception raised: {e}")
            result = set()

        # Combine with existing picks
        result |= team_picks_idx

        return result


def roster_to_team_picks_idx_map(data: pl.DataFrame, roster: dict[int, list[dict[str, Any]]]) -> dict[int, set[int]]:
    # Loop over rosters
    team_picks_idx_map = {}
    for team, picks in roster.items():
        player_ids = {p["player_id"] for p in picks}
        team_data = data.filter(pl.col("player_id").is_in(player_ids))
        team_picks_idx_map[team] = set(team_data["index"].unique())

    return team_picks_idx_map
