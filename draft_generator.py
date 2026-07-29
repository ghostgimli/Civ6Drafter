
import random
from typing import Dict
from data.leaders import LEADERS, Leader
from data.maps import MAP_TYPES, MapType

def leaders_by_key() -> Dict[str, Leader]:
    return {l.key: l for l in LEADERS}

def maps_by_key() -> Dict[str, MapType]:
    return {m.key: m for m in MAP_TYPES}

def generate_leader_draft(
    players: int,
    civs_per_player: int,
    selected_leader_keys: list[str],
) -> dict[int, list[Leader]]:
    """
    Возвращает словарь: player_index -> список лидеров.
    Без повторяющихся цивилизаций и лидеров.
    """
    if players <= 0 or civs_per_player <= 0:
        raise ValueError("players и civs_per_player должны быть > 0")

    total_needed = players * civs_per_player

    # Словари лидеров и уникальный список (по ключам)
    by_key = leaders_by_key()
    unique_leaders: list[Leader] = []
    used_civs: set[str] = set()

    # Перебираем выбранных лидеров, исключая повтор цивилизаций
    # Можно перемешать сначала, чтобы порядок выбора был случайным.
    shuffled_keys = list(selected_leader_keys)
    random.shuffle(shuffled_keys)

    for key in shuffled_keys:
        leader = by_key.get(key)
        if leader is None:
            continue
        if leader.civilization in used_civs:
            # Цива уже участвует в драфте — пропускаем
            continue
        unique_leaders.append(leader)
        used_civs.add(leader.civilization)
        if len(unique_leaders) >= total_needed:
            break

    if len(unique_leaders) < total_needed:
        raise ValueError(
            f"Недостаточно уникальных цивилизаций/лидеров для драфта: "
            f"нужно {total_needed}, доступно {len(unique_leaders)}."
        )

    # Теперь у нас есть уникальные лидеры, раскидываем по игрокам
    random.shuffle(unique_leaders)
    draft: dict[int, list[Leader]] = {}
    idx = 0
    for player in range(1, players + 1):
        player_leaders = unique_leaders[idx:idx + civs_per_player]
        draft[player] = player_leaders
        idx += civs_per_player

    return draft


def pick_random_map(selected_map_keys: list[str]) -> MapType:
    if not selected_map_keys:
        raise ValueError("Нет выбранных карт для драфта.")
    by_key = maps_by_key()
    # фильтруем только те карты, которые реально существуют
    candidates = [by_key[k] for k in selected_map_keys if k in by_key]
    if not candidates:
        raise ValueError("Выбранные ключи карт не совпадают с датасетом.")
    return random.choice(candidates)  # случайная карта из пула[web:77][web:81][web:82]