# Fantasy Football Draft Optimizer - 2024

Features:
- Data Scraping
  - Player metadata and weekly point projections from Sleeper
- Draft Recommendations
  - Sync draft state from Sleeper leagues
  - Use convex optimization to recommend an optimal roster
    - Obj*ective function: maximize the minimum points your team will score each week

Version bumping:
- Edit `__version__` in `src/football/__init__.py`
