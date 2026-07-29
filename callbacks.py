# callbacks.py
from aiogram.filters.callback_data import CallbackData

class LeaderPick(CallbackData, prefix="leader"):
    key: str  # Leader.key

class DraftOption(CallbackData, prefix="draft"):
    option: str  # "players" или "civs_per_player"
    value: int

class DraftAction(CallbackData, prefix="draft"):
    action: str  # "leaders_done", "leaders_save", "leaders_load"

class MapPick(CallbackData, prefix="map"):
    key: str  # MapType.key