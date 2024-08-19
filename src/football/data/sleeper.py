from typing import Any

import polars as pl
from sleeper_wrapper.drafts import Drafts
from sleeper_wrapper.league import League
from sleeper_wrapper.players import Players
from sleeper_wrapper.stats import Stats


def get_players() -> pl.DataFrame:
    # Get players
    players = Players()
    players_json = players.get_all_players("nfl")

    # Convert to dataframe
    out = pl.DataFrame(list(players_json.values()), infer_schema_length=None)
    out = out.select(pl.col(pl.Int64), pl.col(pl.String), pl.col(pl.Boolean), pl.col(pl.List(pl.String)))

    return out


def get_weekly_projections(season: int, week: int) -> pl.DataFrame:
    # Get projections
    stats = Stats()
    proj_json = stats.get_week_projections("regular", season, str(week))

    # Convert to dataframe
    out = pl.DataFrame(list(proj_json.values()), infer_schema_length=None)
    out = out.with_columns(player_id=pl.Series(proj_json.keys()), season=season, week=week)

    return out


def get_league(league_id: str) -> dict[str, Any]:
    # Get league
    league = League(league_id)
    meta = league.get_league()
    users = league.get_users()

    # Build output
    out = {
        "league_id": league_id,
        "draft_id": meta["draft_id"],
        "roster_positions": meta["roster_positions"],
        "users": [
            {
                "user_id": u["user_id"],
                "display_name": u["display_name"],
                "team_name": u["metadata"]["team_name"] if "team_name" in u["metadata"] else None,
            }
            for u in users
        ],
    }
    out["roster_size"] = len(out["roster_positions"])
    out["league_size"] = len(out["users"])

    return out


def get_draft(draft_id: str) -> dict[str, Any]:
    # Get draft
    draft = Drafts(draft_id)
    meta = draft.get_specific_draft()

    # Build draft order using team index
    slots = meta["slot_to_roster_id"]
    num_teams = len(slots)
    num_rounds = meta["settings"]["rounds"]
    one_round = [slots[str(i + 1)] for i in range(num_teams)]
    draft_order = []
    for r in range(num_rounds):  # default snake
        if r % 2 == 0:
            draft_order += one_round
        else:
            draft_order += one_round[::-1]

    # Handle traded picks
    # trades = draft.get_traded_picks()  # TODO

    # Build output
    out = {
        "draft_id": draft_id,
        "league_size": num_teams,
        "rounds": num_rounds,
        "order": draft_order,
        "type": meta["type"],
        "slots": meta["draft_order"],
    }

    return out


def get_draft_picks(draft_id: str) -> list[dict[str, Any]]:
    # Get draft
    draft = Drafts(draft_id)
    picks = draft.get_all_picks()

    return [
        {
            "round": p["round"],
            "slot": p["draft_slot"],
            "pick": p["pick_no"],
            "player_id": p["player_id"],
            "user_id": p["picked_by"] if p["picked_by"] != "" else None,
        }
        for p in picks
    ]
