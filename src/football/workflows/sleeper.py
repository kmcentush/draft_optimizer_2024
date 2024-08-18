import polars as pl
from prefect import flow, task
from prefect.task_runners import ConcurrentTaskRunner

from football.data import sleeper, write_parquet


@task(retries=2)
def get_players():
    players = sleeper.get_players()
    write_parquet(players, "players.parquet")


@task(retries=2)
def _get_weekly_projections(season: int, week: int) -> pl.DataFrame:
    proj = sleeper.get_weekly_projections(season, week)
    return proj


def get_weekly_projections(season: int, weeks: list[int]):
    futures = []
    for week in weeks:
        future = _get_weekly_projections.submit(season, week)
        futures.append(future)
    projs = [f.result() for f in futures]
    proj = pl.concat(projs, how="diagonal")
    write_parquet(proj, "weekly_projections.parquet")


@flow(name="Sleeper - Get Data", task_runner=ConcurrentTaskRunner())
def main(season: int, weeks: list[int]):
    get_players()
    get_weekly_projections(season, weeks)


if __name__ == "__main__":
    main(season=2024, weeks=list(range(1, 19)))
