from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, Document
from aiogram.utils.keyboard import InlineKeyboardBuilder
from callbacks import LeaderPick, DraftOption, DraftAction, MapPick
from keyboard import leaders_keyboard, players_keyboard, civs_per_player_keyboard, maps_keyboard
from storage.leaders_config import save_leaders_config
from storage.maps_config import save_maps_config
from draft_generator import generate_leader_draft, pick_random_map
import json
router = Router()

user_players: dict[int, int] = {}           # user_id -> players
user_civs_per_player: dict[int, int] = {}   # user_id -> civs_per_player

@router.message(F.text == "/draft")  # или /start, или твоя команда
async def start_draft(message: Message):
    await message.answer(
        "Выбери количество игроков (1–12):",
        reply_markup=players_keyboard().as_markup(),
    )

@router.callback_query(DraftOption.filter(F.option == "players"))
async def choose_players(callback: CallbackQuery, callback_data: DraftOption):
    players = callback_data.value
    user_id = callback.from_user.id
    # на будущее сохранить players в твоё состояние (FSM или свой стор)
    # Пример: fsm_context.update_data(players=players)
    user_players[user_id] = int(players)
    await callback.answer(f"Выбрано игроков: {players}", show_alert=False)

    # После выбора — предлагаем следующий шаг: выбор цивилизаций по игроку
    await callback.message.edit_text(
        f"Игроков: {players}\nТеперь выбери, сколько цивилизаций на игрока (1–5):",
        reply_markup=civs_per_player_keyboard().as_markup(),
    )

@router.callback_query(DraftOption.filter(F.option == "civs_per_player"))
async def choose_civs_per_player(callback: CallbackQuery, callback_data: DraftOption):
    civs_per_player = callback_data.value
    user_id = callback.from_user.id

    # на будущее сохранить civs_per_player в состояние
    await callback.answer(
        f"Цивилизаций на игрока: {civs_per_player}", show_alert=False
    )
    user_civs_per_player[user_id] = int(civs_per_player)
    # Инициализируем пустой выбор лидеров для пользователя
    user_leader_selection[user_id] = set()
    await callback.message.edit_text(
        "Теперь выбери, какие лидеры будут участвовать в драфте.\n",
        reply_markup=leaders_keyboard(selected_keys=set()).as_markup(),
    )



user_leader_selection: dict[int, set[str]] = {}  # user_id -> set of leader keys
user_map_selection: dict[int, set[str]] = {}


@router.callback_query(LeaderPick.filter())
async def pick_leader(callback: CallbackQuery, callback_data: LeaderPick):
    user_id = callback.from_user.id
    leader_key = callback_data.key

    selected = user_leader_selection.get(user_id, set())
    if leader_key in selected:
        selected.remove(leader_key)
    else:
        selected.add(leader_key)
    user_leader_selection[user_id] = selected

    #await callback.answer("Выбор лидеров обновлен.", show_alert=False)

    await callback.message.edit_text(
        "Выбери лидеров, которые будут участвовать в драфте.\n\n"
        "Можно выбрать несколько. Можешь сохранить/загрузить сет, или нажать «Готово».",
        reply_markup=leaders_keyboard(selected_keys=selected).as_markup(),
    )

@router.callback_query(DraftAction.filter(F.action == "leaders_save"))
async def leaders_save(callback: CallbackQuery, callback_data: DraftAction, bot: Bot):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    selected_leaders = list(user_leader_selection.get(user_id, set()))
    if not selected_leaders:
        await callback.answer(
            "Нечего экспортировать: выбери хотя бы одного лидера.", show_alert=True
        )
        return

    await save_leaders_config(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        leader_keys=selected_leaders,
    )

    await callback.answer("Файл с конфигурацией лидеров отправлен. Сохрани его у себя.", show_alert=False)

waiting_leaders_json: dict[int, bool] = {}

@router.callback_query(DraftAction.filter(F.action == "leaders_load_external"))
async def leaders_load_external(callback: CallbackQuery, callback_data: DraftAction):
    user_id = callback.from_user.id

    # Включаем режим ожидания JSON‑файла для этого пользователя
    waiting_leaders_json[user_id] = True

    await callback.answer("Теперь пришли JSON‑файл с конфигурацией лидеров.", show_alert=False)

    await callback.message.edit_text(
        "📂 Загрузка конфигурации лидеров\n\n"
        "Отправь сюда JSON‑файл с конфигурацией драфта лидеров.\n"
        "После загрузки я применю его и верну тебя в меню выбора.",
    )

@router.message(F.document)
async def handle_config_document(message: Message, bot: Bot):
    user_id = message.from_user.id
    # Проверяем, активен ли режим загрузки конфигурации лидеров
    if waiting_leaders_json.get(user_id):
        document: Document = message.document

        if not document.file_name.endswith(".json"):
            await message.answer("Ожидаю JSON‑файл (расширение .json).")
            return

        # Скачиваем файл в память[web:95]
        file = await bot.download(document)
        file.seek(0)

        try:
            data = json.load(file)  # парсим JSON в dict[web:64][web:94]
        except json.JSONDecodeError:
            await message.answer("Не удалось прочитать JSON. Проверь формат файла.")
            return

        leaders = data.get("leaders")
        if not isinstance(leaders, list):
            await message.answer("В файле не найдены корректные поля 'leaders'.")
            return

        # Применяем конфигурацию
        selected_leaders = set(str(k) for k in leaders)
        user_leader_selection[user_id] = selected_leaders

        # Выключаем режим ожидания
        waiting_leaders_json[user_id] = False
        await message.answer(
            "Конфигурация лидеров успешно загружена из файла.\n",
            reply_markup=leaders_keyboard(selected_keys=selected_leaders).as_markup(),
        )
    elif waiting_maps_json.get(user_id):
        document: Document = message.document

        if not document.file_name.endswith(".json"):
            await message.answer("Ожидаю JSON‑файл с конфигурацией карт (расширение .json).")
            return

        # Скачиваем файл в память[web:105][web:106]
        file = await bot.download(document)
        file.seek(0)

        try:
            data = json.load(file)  # парсим JSON в dict[web:64][web:94]
        except json.JSONDecodeError:
            await message.answer("Не удалось прочитать JSON. Проверь формат файла.")
            return

        maps = data.get("maps")
        if not isinstance(maps, list):
            await message.answer("В файле не найдены корректные поля 'maps'.")
            return

        # Применяем конфиг
        selected_maps = set(str(k) for k in maps)
        user_map_selection[user_id] = selected_maps

        # Выключаем режим ожидания
        waiting_maps_json[user_id] = False

        await message.answer(
            "Конфигурация карт успешно загружена из файла.\n",
            reply_markup=maps_keyboard(selected_keys=selected_maps).as_markup(),
        )
    else:
        return
# ✅ Нажатие на «Готово» после выбора лидеров — переход к выбору карты
@router.callback_query(DraftAction.filter(F.action == "leaders_done"))
async def leaders_done(callback: CallbackQuery, callback_data: DraftAction):
    user_id = callback.from_user.id
    selected_leaders = user_leader_selection.get(user_id, set())

    if not selected_leaders:
        await callback.answer(
            "Сначала выбери хотя бы одного лидера.", show_alert=True
        )
        return

    await callback.answer("Лидеры зафиксированы.", show_alert=False)

    user_map_selection[user_id] = set()

    await callback.message.edit_text(
        "Теперь выбери карты для драфта.\n\n"
        "Можно выбрать несколько карт, затем нажать «Готово».",
        reply_markup=maps_keyboard(selected_keys=set()).as_markup(),
    )



@router.callback_query(MapPick.filter())
async def pick_map(callback: CallbackQuery, callback_data: MapPick):
    user_id = callback.from_user.id
    map_key = callback_data.key

    selected = user_map_selection.get(user_id, set())
    if map_key in selected:
        selected.remove(map_key)
    else:
        selected.add(map_key)
    user_map_selection[user_id] = selected

    await callback.answer("Выбор карт обновлен.", show_alert=False)

    await callback.message.edit_text(
        "Выбери карты, которые будут участвовать в драфте.\n\n"
        "Можешь сохранить или загрузить свою конфигурацию. После чего жми «Готово».",
        reply_markup=maps_keyboard(selected_keys=selected).as_markup(),
    )


@router.callback_query(DraftAction.filter(F.action == "maps_done"))
async def maps_done(callback: CallbackQuery, callback_data: DraftAction):
    user_id = callback.from_user.id
    selected_maps = user_map_selection.get(user_id, set())

    if not selected_maps:
        await callback.answer(
            "Выбери хотя бы одну карту.", show_alert=True
        )
        return

    # await callback.answer("Карты зафиксированы.", show_alert=False)

    # Показать кнопку «Сгенерировать драфт»
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🎲 Сгенерировать драфт",
        callback_data=DraftAction(action="draft_generate"),
    )

    await callback.message.edit_text(
        "Лидеры и карты выбраны.\n"
        "Нажми «Сгенерировать драфт» и готовься побеждать",
        reply_markup=builder.as_markup(),
    )

@router.callback_query(DraftAction.filter(F.action == "maps_save"))
async def maps_save(callback: CallbackQuery, callback_data: DraftAction, bot: Bot):
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id

    selected_maps = list(user_map_selection.get(user_id, set()))
    if not selected_maps:
        await callback.answer(
            "Нечего экспортировать: выбери хотя бы одну карту.", show_alert=True
        )
        return

    await save_maps_config(
        bot=bot,
        chat_id=chat_id,
        user_id=user_id,
        map_keys=selected_maps,
    )

    await callback.answer("Файл с конфигурацией карт отправлен. Сохрани его у себя.", show_alert=False)

waiting_maps_json: dict[int, bool] = {}

@router.callback_query(DraftAction.filter(F.action == "maps_load_external"))
async def maps_load_external(callback: CallbackQuery, callback_data: DraftAction):
    user_id = callback.from_user.id

    waiting_maps_json[user_id] = True

    await callback.answer("Теперь пришли JSON‑файл с конфигурацией карт.", show_alert=False)

    await callback.message.edit_text(
        "📂 Загрузка конфигурации карт\n\n"
        "Отправь сюда JSON‑файл с конфигурацией драфта карт.\n"
        "После загрузки я применю его и верну тебя в меню выбора карт.",
    )

@router.callback_query(DraftAction.filter(F.action == "draft_generate"))
async def draft_generate(callback: CallbackQuery, callback_data: DraftAction):
    user_id = callback.from_user.id

    players = user_players.get(user_id)
    civs_per_player = user_civs_per_player.get(user_id)
    selected_leader_keys = list(user_leader_selection.get(user_id, set()))
    selected_map_keys = list(user_map_selection.get(user_id, set()))

    # Простые проверки
    if not players or not civs_per_player:
        await callback.answer(
            f"Сначала выбери количество игроков и цивилизаций на игрока. {players} and {civs_per_player}", show_alert=True
        )
        return
    if not selected_leader_keys:
        await callback.answer(
            "Сначала выбери лидеров для драфта.", show_alert=True
        )
        return
    if not selected_map_keys:
        await callback.answer(
            "Сначала выбери карты для драфта.", show_alert=True
        )
        return

    try:
        draft = generate_leader_draft(
            players=players,
            civs_per_player=civs_per_player,
            selected_leader_keys=selected_leader_keys,
        )
        game_map = pick_random_map(selected_map_keys)
    except ValueError as e:
        await callback.answer(str(e), show_alert=True)
        return

    # Формируем человекочитаемый текст
    lines: list[str] = ["🎲 Результаты драфта:\n"]

    for player_index, leaders in draft.items():
        leader_desc = ", ".join(
            f"{leader.name} ({leader.civilization})" for leader in leaders
        )
        lines.append(f"Игрок {player_index}: {leader_desc}")

    lines.append("")
    lines.append(f"🗺 Карта: {game_map.name}")

    text = "\n".join(lines)

    try:
        del user_players[user_id]
        del user_civs_per_player[user_id]
        del user_leader_selection[user_id]
        del user_map_selection[user_id]
        del waiting_maps_json[user_id]
        del waiting_leaders_json[user_id]
    except:
        print('xто-то делалось вручную')

    await callback.answer("Драфт сгенерирован.", show_alert=False)
    await callback.message.edit_text(text)

