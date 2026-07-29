# data/leaders.py

from dataclasses import dataclass
from enum import Enum


class DLC(Enum):
    BASE = "Base"
    RISE_AND_FALL = "Rise and Fall"
    GATHERING_STORM = "Gathering Storm"
    OTHER = "Other"


@dataclass
class Leader:
    key: str              # уникальный внутренний ключ
    name: str             # имя лидера (отображаемое)
    civilization: str     # название цивилизации (отображаемое)
    dlc: DLC
    primary_color: str    # основной цвет по джерси-системе Civ6
    secondary_color: str  # вторичный цвет


LEADERS: list[Leader] = [
    Leader("trajan", "Траян", "Рим", DLC.BASE, "#800000", "#FFD700"),
    Leader("cleopatra", "Клеопатра", "Египет", DLC.BASE, "#DAA520", "#1F4E79"),
    Leader("victoria", "Виктория (Эпоха Империи)", "Англия", DLC.BASE, "#B22222", "#FFFFFF"),
    Leader("gorgo", "Горго", "Греция", DLC.BASE, "#0D5EAF", "#FFFFFF"),
    Leader("pericles", "Перикл", "Греция", DLC.BASE, "#0D5EAF", "#FFFFFF"),
    Leader("hojo", "Ходзё Токимунэ", "Япония", DLC.BASE, "#BC002D", "#FFFFFF"),
    Leader("mvemba", "Мвемба а Нзинга", "Конго", DLC.BASE, "#009E60", "#FCD116"),
    Leader("pedro", "Педру II", "Бразилия", DLC.BASE, "#008C45", "#F4C300"),
    Leader("frederick", "Фридрих Барбаросса", "Германия", DLC.BASE, "#000000", "#FFCE00"),
    Leader("gandhi", "Ганди", "Индия", DLC.BASE, "#FF9933", "#138808"),
    Leader("saladin", "Саладин (Султан)", "Арабия", DLC.BASE, "#006B3F", "#FFFFFF"),
    Leader("qin", "Цинь Шихуанди (Мандат Неба)", "Китай", DLC.BASE, "#BA0000", "#FFD700"),
    Leader("tomyris", "Томирис", "Скифы", DLC.BASE, "#FFD700", "#808000"),
    Leader("harald", "Харальд Суровый (Конунг)", "Норвегия", DLC.BASE, "#EF2B2D", "#FFFFFF"),
    Leader("gilgamesh", "Гильгамеш", "Шумер", DLC.BASE, "#654321", "#C0A878"),
    Leader("catherine", "Екатерина Медичи", "Франция", DLC.BASE, "#0055A4", "#FFFFFF"),
    Leader("peter", "Пётр I", "Россия", DLC.BASE, "#0033A0", "#FFFFFF"),
    Leader("philip", "Филипп II", "Испания", DLC.BASE, "#AA151B", "#F1BF00"),

    Leader("chandragupta", "Чандрагупта", "Индия", DLC.RISE_AND_FALL, "#FF9933", "#138808"),
    Leader("genghis", "Чингисхан", "Монголия", DLC.RISE_AND_FALL, "#006AA7", "#FFCD00"),
    Leader("lautaro", "Лаутаро", "Мапуче", DLC.RISE_AND_FALL, "#00693E", "#FFD700"),
    Leader("poundmaker", "Паундмейкер", "Кри", DLC.RISE_AND_FALL, "#006341", "#FCD116"),
    Leader("robert", "Роберт Брюс", "Шотландия", DLC.RISE_AND_FALL, "#004B8D", "#FFFFFF"),
    Leader("seondeok", "Сондок", "Корея", DLC.RISE_AND_FALL, "#003478", "#FFFFFF"),
    Leader("shaka", "Шака", "Зулу", DLC.RISE_AND_FALL, "#006B3F", "#FCD116"),
    Leader("tamar", "Тамара", "Грузия", DLC.RISE_AND_FALL, "#9B1C31", "#FFFFFF"),
    Leader("wilhelmina", "Вильгельмина", "Нидерланды", DLC.RISE_AND_FALL, "#FF8000", "#0033A0"),

    Leader("dido", "Дидона", "Финикия", DLC.GATHERING_STORM, "#6A0DAD", "#FFD700"),
    Leader("eleanor_eng", "Элеонора Аквитанская", "Англия", DLC.GATHERING_STORM, "#B22222", "#FFFFFF"),
    Leader("eleanor_fr", "Элеонора Аквитанская", "Франция", DLC.GATHERING_STORM, "#0055A4", "#FFFFFF"),
    Leader("kristina", "Кристина", "Швеция", DLC.GATHERING_STORM, "#004B87", "#FFCD00"),
    Leader("kupe", "Купе", "Маори", DLC.GATHERING_STORM, "#00696F", "#FFFFFF"),
    Leader("mansa", "Манса Муса", "Мали", DLC.GATHERING_STORM, "#FFD700", "#8B4513"),
    Leader("matthias", "Матьяш Корвин", "Венгрия", DLC.GATHERING_STORM, "#436F4D", "#FFFFFF"),
    Leader("pachacuti", "Пачакути", "Инки", DLC.GATHERING_STORM, "#C68642", "#4B5320"),
    Leader("suleiman", "Сулейман (Кануни)", "Османы", DLC.GATHERING_STORM, "#006633", "#FFFFFF"),
    Leader("laurier", "Уилфрид Лорье", "Канада", DLC.GATHERING_STORM, "#FF0000", "#FFFFFF"),

    Leader("montezuma", "Монтесума", "Ацтеки", DLC.OTHER, "#8A2A2B", "#F1E6B2"),
    Leader("jadwiga", "Ядвига", "Польша", DLC.OTHER, "#FFFFFF", "#D4213D"),
    Leader("john_curtin", "Джон Кёртин", "Австралия", DLC.OTHER, "#002B5C", "#FFFFFF"),
    Leader("alexander", "Александр", "Македония", DLC.OTHER, "#6E1D1D", "#E0C14F"),
    Leader("cyrus", "Кир", "Персия", DLC.OTHER, "#7A1E1E", "#F2D16B"),
    Leader("amanitore", "Аманиторе", "Нубия", DLC.OTHER, "#7A2E8E", "#F2C94C"),
    Leader("gitarja", "Гитарджа", "Индонезия", DLC.OTHER, "#008B8B", "#FFFFFF"),
    Leader("jayavarman", "Джаяварман VII", "Кхмер", DLC.OTHER, "#7A4B2A", "#E3C16F"),
    Leader("julius_caesar", "Юлий Цезарь", "Рим", DLC.OTHER, "#800000", "#FFD700"),
    Leader("lady_six_sky", "Леди Шесть Небес", "Майя", DLC.OTHER, "#4B0082", "#FFD700"),
    Leader("simon_bolivar", "Симон Боливар", "Гран Колумбия", DLC.OTHER, "#AA0000", "#FFD700"),
    Leader("menelik", "Менелик II", "Эфиопия", DLC.OTHER, "#6B2D5C", "#E3C16F"),
    Leader("ambiorix", "Амбиорикс", "Галлия", DLC.OTHER, "#2E8B57", "#FFD700"),
    Leader("basil", "Василий II", "Византия", DLC.OTHER, "#1C3F94", "#F2D16B"),
    Leader("hammurabi", "Хаммурапи", "Вавилон", DLC.OTHER, "#3B2F2F", "#C9A66B"),
    Leader("ba_trieu", "Ба Триё", "Вьетнам", DLC.OTHER, "#2E5EAA", "#FFD700"),
    Leader("kublai_khan", "Хубилай-хан", "Китай", DLC.OTHER, "#BA0000", "#FFD700"),
    Leader("joao", "Жуан III", "Португалия", DLC.OTHER, "#0055A4", "#F5D76E"),

    Leader("abraham_lincoln", "Авраам Линкольн", "Америка", DLC.OTHER, "#1F4E79", "#FFFFFF"),
    Leader("nzinga_mbande", "Нзинга Мбанде", "Конго", DLC.OTHER, "#009E60", "#FCD116"),
    Leader("saladin_vizier", "Саладин (Визирь)", "Арабия", DLC.OTHER, "#006B3F", "#FFFFFF"),
    Leader("nader_shah", "Надир-шах", "Персия", DLC.OTHER, "#7A1E1E", "#F2D16B"),
    Leader("suleiman_magnificent", "Сулейман (Величественный)", "Османы", DLC.OTHER, "#006633", "#FFFFFF"),
    Leader("tokugawa", "Токугава Иэясу", "Япония", DLC.OTHER, "#BC002D", "#FFFFFF"),
    Leader("qin_unifier", "Цинь Шихуанди (Объединитель)", "Китай", DLC.OTHER, "#BA0000", "#FFD700"),
    Leader("wu_zetian", "У Цзэтянь", "Китай", DLC.OTHER, "#BA0000", "#FFD700"),
    Leader("yongle", "Юнлэ", "Китай", DLC.OTHER, "#BA0000", "#FFD700"),
    Leader("cleopatra_ptolemaic", "Клеопатра (Птолемеевская)", "Египет", DLC.OTHER, "#DAA520", "#1F4E79"),
    Leader("ramses", "Рамзес II", "Египет", DLC.OTHER, "#DAA520", "#1F4E79"),
    Leader("sundiata", "Сундиата Кейта", "Мали", DLC.OTHER, "#FFD700", "#8B4513"),
    Leader("ludwig", "Людвиг II", "Германия", DLC.OTHER, "#000000", "#FFCE00"),
    Leader("sejong", "Седжон", "Корея", DLC.OTHER, "#003478", "#FFFFFF"),
    Leader("theodora", "Феодора", "Византия", DLC.OTHER, "#1C3F94", "#F2D16B"),
    Leader("elizabeth", "Елизавета I", "Англия", DLC.OTHER, "#B22222", "#FFFFFF"),
    Leader("harald_varangian", "Харальд Суровый (Варяги)", "Норвегия", DLC.OTHER, "#EF2B2D", "#FFFFFF"),
    Leader("victoria_age_steam", "Виктория (Эпоха Пара)", "Англия", DLC.OTHER, "#B22222", "#FFFFFF"),
]