from typing import Any

from football.data.sleeper import get_draft, get_draft_picks, get_league


class Draft:
    def __init__(self, draft_id: str):
        # Set metadata
        self.draft_id = draft_id
        draft = get_draft(draft_id)
        self.league_size = draft["league_size"]
        self.rounds = draft["rounds"]
        self.order = draft["order"]
        self.type = draft["type"]

        # Set picks
        self.picks: list[dict[str, Any]] = []
        self.update_picks()

    def update_picks(self):
        self.picks = get_draft_picks(self.draft_id)

    def get_next_pick(self) -> int | None:
        # Get team with next pick
        num_picks = len(self.picks)
        if num_picks >= len(self.order):  # draft over
            return None
        else:
            return self.order[num_picks]

    def get_rosters(self) -> dict[int, list[dict[str, Any]]]:
        # Build map of team index -> picks
        picks = self.picks
        rosters: dict[int, list[dict[str, Any]]] = {i + 1: [] for i in range(self.league_size)}
        for i, team in enumerate(self.order):
            if i >= len(picks):
                break
            else:
                rosters[team].append(picks[i])

        return rosters


class League:
    def __init__(self, league_id: str):
        # Set metadata
        self.league_id = league_id
        league = get_league(league_id)
        self.draft_id = league["draft_id"]
        self.roster_positions = league["roster_positions"]
        self.users = league["users"]
        self.roster_size = league["roster_size"]
        self.league_size = league["league_size"]

    def get_draft(self) -> Draft:
        return Draft(self.draft_id)
