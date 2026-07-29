# keyboards.py (добавление)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks import LeaderPick, DraftOption, DraftAction, MapPick
from data.leaders import LEADERS, Leader, DLC
from data.maps import MAP_TYPES

def players_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for value in range(1, 13):  # 1..12
        builder.button(
            text=str(value),
            callback_data=DraftOption(option="players", value=value),
        )
    builder.adjust(4)
    return builder

def civs_per_player_keyboard() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    for value in range(1, 6):  # 1..5
        builder.button(
            text=str(value),
            callback_data=DraftOption(option="civs_per_player", value=value),
        )
    builder.adjust(5)  # одна строка из 5 кнопок
    return builder

def color_emoji(hex_color: str) -> str:
    hex_color = hex_color.lower()
    if "ff0000" in hex_color or "aa151b" in hex_color or "b22222" in hex_color:
        return "🟥"
    if "008c45" in hex_color or "006b3f" in hex_color or "009e60" in hex_color:
        return "🟩"
    if "0033a0" in hex_color or "004b87" in hex_color or "0d5eaf" in hex_color:
        return "🟦"
    if "ffd700" in hex_color or "f4c300" in hex_color or "fcd116" in hex_color:
        return "🟨"
    if "ffffff" in hex_color:
        return "⬜️"
    if "000000" in hex_color:
        return "⬛️"
    return "🟫"

def maps_keyboard(selected_keys: set[str] | None = None) -> InlineKeyboardBuilder:
    if selected_keys is None:
        selected_keys = set()
    builder = InlineKeyboardBuilder()

    for m in MAP_TYPES:
        is_selected = m.key in selected_keys
        mark = "✅" if is_selected else " "
        text = f"{m.name} {mark}"
        builder.button(
            text=text,
            callback_data=MapPick(key=m.key),
        )


    # Кнопка «Готово» — завершить выбор карт
    builder.button(
        text="✅ Готово",
        callback_data=DraftAction(action="maps_done"),
    )
    builder.adjust(1)
    # Сохранить сет карт
    builder.button(
        text="💾 Сохранить конфигурацию",
        callback_data=DraftAction(action="maps_save"),
    )
    # Загрузить сохранённый сет
    builder.button(
        text="📂 Загрузить конфигурацию из файла",
        callback_data=DraftAction(action="maps_load_external"),
    )
    return builder

def leaders_keyboard(
    selected_keys: set[str] | None = None,
    dlc_filter: set[DLC] | None = None,
    add_action_buttons: bool = True,
) -> InlineKeyboardBuilder:
    if selected_keys is None:
        selected_keys = set()
    builder = InlineKeyboardBuilder()

    leaders: list[Leader] = LEADERS
    if dlc_filter:
        leaders = [l for l in leaders if l.dlc in dlc_filter]

    for leader in leaders:
        emoji = color_emoji(leader.primary_color)
        is_selected = leader.key in selected_keys
        mark = "✅" if is_selected else " "
        text = f"{emoji} {leader.name} ({leader.civilization}) {mark}"

        builder.button(
            text=text,
            callback_data=LeaderPick(key=leader.key),
        )

    builder.button(
        text="✅ Готово",
        callback_data=DraftAction(action="leaders_done"),
    )
    # Сохранить конфиг лидеров
    builder.button(
        text="💾 Сохранить сет лидеров",
        callback_data=DraftAction(action="leaders_save"),
    )
    # Загрузить сохранённый конфиг
    builder.button(
        text="📂 Загрузить конфигурацию из файла",
        callback_data=DraftAction(action="leaders_load_external"),
    )
    builder.adjust(1)
    return builder

