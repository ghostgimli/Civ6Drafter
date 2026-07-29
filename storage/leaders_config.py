import json
import tempfile
from datetime import datetime
from pathlib import Path

from aiogram.types import FSInputFile
from aiogram import Bot

CONFIG_DIR = Path("configs")
CONFIG_DIR.mkdir(exist_ok=True)


def leaders_config_path(user_id: int) -> Path:
    return CONFIG_DIR / f"leaders_{user_id}.json"


async def save_leaders_config(bot: Bot, chat_id: int, user_id: int, leader_keys: list[str]) -> None:
    data = {
        "user_id": user_id,
        "leaders": leader_keys,
        "created_at": datetime.utcnow().isoformat(),
        "version": 1,
    }
    # path = leaders_config_path(user_id)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".json") as tmp:
        json.dump(data, tmp, ensure_ascii=False, indent=4)  # читаемый JSON[web:60][web:94]
        tmp_path = Path(tmp.name)
        filename = "draft_" + str(datetime.now().strftime("%d-%m-%Y_%H%M%S")) + ".json"
    document = FSInputFile(tmp_path,filename = filename)
    await bot.send_document(
        chat_id,
        document,
        caption="Конфигурация драфта лидеров (сохрани этот файл у себя).",
    )

    # По желанию: удалить временный файл после отправки
    tmp_path.unlink(missing_ok=True)


# def load_leaders_config(user_id: int) -> list[str] | None:
#     # path = maps_config_path(user_id)
#     if filepath == "":
#         return None
#     try:
#         with open(filepath, "r", encoding="utf-8") as f:
#             data = json.load(f)
#         leaders = data.get("leaders")
#         if isinstance(leaders, list):
#             # минимальная валидация
#             return [str(k) for k in leaders]
#         return None
#     except json.JSONDecodeError:
#         # битый файл — можно залогировать, вернуть None
#         return None