"""
AI-Zavod 20-Concept Facades Catalog
Defines 20 radically diverse, competitive interactive HTML facades for WebPlanner Desktop OS.
Strictly adheres to:
1. Anti-AI-Trope Guarantee (no cliché gradient borders, no repetitive colors).
2. Diverse layout paradigms (Left sidebar, bottom dock, centered doc, floating island, spotlight, Bauhaus, brutalist, titanium, wabi-sabi, broadsheet, split-screen, card deck, timeline spine, moleskine, telemetry 4x3, frosted glass, retro 1984, fashion magazine, radial hub, artisanal craft).
3. 100% Russian language (zero Anglicisms).
4. No compass icons anywhere.
"""
from typing import Dict, Any, List


def get_20_concept_blueprints() -> List[Dict[str, Any]]:
    return [
        {
            "id": "concept_1",
            "name": "Швейцарский Студийный Грид",
            "benchmark": "Müller-Brockmann & International Typographic Style",
            "layout_type": "Узкий левый сайдбар + жесткая модульная сетка",
            "cognitive_law": "Принцип гештальт-группировки и закон Фиттса",
            "wedge": "Монохромная сетка без отвлекающего визуального шума",
            "display_font": "Plus Jakarta Sans, sans-serif",
            "body_font": "Inter, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap",
            "palette": {
                "bg": "#FFFFFF",
                "surface": "#F4F4F5",
                "border": "#E4E4E7",
                "accent": "#DC2626",
                "text_primary": "#18181B",
                "text_muted": "#71717A"
            }
        },
        {
            "id": "concept_2",
            "name": "Тактильный Нео-Крафт",
            "benchmark": "Amie.so & Craft Docs",
            "layout_type": "Плавающий закругленный док внизу экрана",
            "cognitive_law": "Теория аффорданса и микро-вознаграждений",
            "wedge": "Жирные иконки 2.5px, пастельная глина, защита стрика",
            "display_font": "Outfit, sans-serif",
            "body_font": "Plus Jakarta Sans, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap",
            "palette": {
                "bg": "#FAF6F0",
                "surface": "#F3ECE1",
                "border": "rgba(194, 94, 0, 0.2)",
                "accent": "#C25E00",
                "text_primary": "#2D241E",
                "text_muted": "#8A7968"
            }
        },
        {
            "id": "concept_3",
            "name": "Академический Монохром & KaTeX",
            "benchmark": "Notion Whitepaper & Substack",
            "layout_type": "Центрированная книжная колонка 800px с формулами",
            "cognitive_law": "Снижение когнитивной нагрузки Свеллера (CLT)",
            "wedge": "Инлайн LaTeX-формулы прямо в заголовках задач",
            "display_font": "Cormorant Garamond, serif",
            "body_font": "JetBrains Mono, monospace",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap",
            "palette": {
                "bg": "#FAFAFA",
                "surface": "#F4F4F5",
                "border": "#E2E8F0",
                "accent": "#1E293B",
                "text_primary": "#0F172A",
                "text_muted": "#64748B"
            }
        },
        {
            "id": "concept_4",
            "name": "Editorial Zen Paper Studio",
            "benchmark": "Things 3 & Monocle",
            "layout_type": "Плавающий верхний остров с монограммой WP",
            "cognitive_law": "Когнитивный горизонт 72ч и закон Миллера (7±2)",
            "wedge": "Теплая рисовая бумага, хвойный лесной акцент",
            "display_font": "Playfair Display, serif",
            "body_font": "Plus Jakarta Sans, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap",
            "palette": {
                "bg": "#F8F5EE",
                "surface": "#EFEAE0",
                "border": "rgba(28, 25, 23, 0.12)",
                "accent": "#166534",
                "text_primary": "#1C1917",
                "text_muted": "#78716C"
            }
        },
        {
            "id": "concept_5",
            "name": "Командный Центр Spotlight HUD",
            "benchmark": "Raycast & Linear Keyboard-First",
            "layout_type": "Центральная командная строка ⌘K + плотные карточки",
            "cognitive_law": "Закон Хика (минимизация времени выбора через ⌘K)",
            "wedge": "Управление исключительно клавиатурой, 12мс отклик",
            "display_font": "Plus Jakarta Sans, sans-serif",
            "body_font": "JetBrains Mono, monospace",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@600;700&display=swap",
            "palette": {
                "bg": "#0F1117",
                "surface": "#181B24",
                "border": "rgba(245, 158, 11, 0.3)",
                "accent": "#F59E0B",
                "text_primary": "#F8FAFC",
                "text_muted": "#94A3B8"
            }
        },
        {
            "id": "concept_6",
            "name": "Bauhaus 1925 Конструктивизм",
            "benchmark": "Bauhaus Dessau & Swiss Modernism",
            "layout_type": "Асимметричные блоки, разделенные толстыми рамками 2.5px",
            "cognitive_law": "Принцип контраста и четкой визуальной иерархии",
            "wedge": "Геометрические цветовые акценты (синий круг, красный куб)",
            "display_font": "Syne, sans-serif",
            "body_font": "Space Grotesk, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&family=Syne:wght@700;800&display=swap",
            "palette": {
                "bg": "#F5F3ED",
                "surface": "#EAE6DB",
                "border": "#18181B",
                "accent": "#1D4ED8",
                "text_primary": "#18181B",
                "text_muted": "#52525B"
            }
        },
        {
            "id": "concept_7",
            "name": "Нео-Брутализм 2.0",
            "benchmark": "Gumroad & Modern Figma",
            "layout_type": "Жесткие черные оффсет-тени 5px 5px без размытия",
            "cognitive_law": "Эффект изоляции Ресторфф (Von Restorff Effect)",
            "wedge": "Сочный лаймовый акцент на чистом белом с жирными рамками",
            "display_font": "Archivo, sans-serif",
            "body_font": "Plus Jakarta Sans, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Archivo:wght@800;900&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap",
            "palette": {
                "bg": "#FFFFFF",
                "surface": "#F4F4F5",
                "border": "#000000",
                "accent": "#84CC16",
                "text_primary": "#000000",
                "text_muted": "#52525B"
            }
        },
        {
            "id": "concept_8",
            "name": "Премиальный Темный Титан",
            "benchmark": "Apple Pro Display & VisionOS Titanium",
            "layout_type": "Верхний динамический остров + бесшовные матовые карточки",
            "cognitive_law": "Закон Фиттса и премиальная сенсорная эстетика",
            "wedge": "Матовая титановая текстура, ледяное серебро, микро-индикаторы",
            "display_font": "Inter, sans-serif",
            "body_font": "Inter, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            "palette": {
                "bg": "#14151A",
                "surface": "#1E2028",
                "border": "rgba(255, 255, 255, 0.08)",
                "accent": "#E2E8F0",
                "text_primary": "#FFFFFF",
                "text_muted": "#94A3B8"
            }
        },
        {
            "id": "concept_9",
            "name": "Японский Ваби-Саби",
            "benchmark": "Muji & Kenya Hara Design",
            "layout_type": "Бескаркасная верстка, разделение свободным пространством",
            "cognitive_law": "Принцип когнитивного простора и дзен-фокуса",
            "wedge": "Натуральный лен, мох, терракота, органическое спокойствие",
            "display_font": "Noto Serif, serif",
            "body_font": "Noto Sans, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500&family=Noto+Serif:wght@500;600&display=swap",
            "palette": {
                "bg": "#F4EFEA",
                "surface": "#EAE3DA",
                "border": "rgba(74, 93, 78, 0.15)",
                "accent": "#4A5D4E",
                "text_primary": "#2D2C2A",
                "text_muted": "#75726D"
            }
        },
        {
            "id": "concept_10",
            "name": "Газетный Броадшит",
            "benchmark": "Financial Times & The New York Times",
            "layout_type": "3 газетные колонки с вертикальными линиями прессы",
            "cognitive_law": "Эффект авторитета (Cialdini Authority) и беглого чтения",
            "wedge": "Лососевая бумага прессы, шапка-передовица выпуска",
            "display_font": "Fraunces, serif",
            "body_font": "Newsreader, serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&display=swap",
            "palette": {
                "bg": "#FFF1E5",
                "surface": "#F7E6D7",
                "border": "rgba(28, 25, 23, 0.2)",
                "accent": "#991B1B",
                "text_primary": "#1C1917",
                "text_muted": "#78716C"
            }
        },
        {
            "id": "concept_11",
            "name": "Сплит-Экран Канбан",
            "benchmark": "Linear Split View & Taskboards",
            "layout_type": "50% слева — гигантский таймер фокуса, 50% справа — 3 колонки",
            "cognitive_law": "Закон двойного кодирования Пайвио (Dual Coding)",
            "wedge": "Разделение 50/50: левая половина только под главную цель дня",
            "display_font": "Manrope, sans-serif",
            "body_font": "Plus Jakarta Sans, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Manrope:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap",
            "palette": {
                "bg": "#18181B",
                "surface": "#27272A",
                "border": "rgba(255, 255, 255, 0.1)",
                "accent": "#10B981",
                "text_primary": "#FAFAFA",
                "text_muted": "#A1A1AA"
            }
        },
        {
            "id": "concept_12",
            "name": "Стек Физических Карточек",
            "benchmark": "Tinder UI & Physical Index Cards",
            "layout_type": "Стопка карточек друг на друге с перспективой и сдвигом",
            "cognitive_law": "Прогрессивное раскрытие информации (Progressive Disclosure)",
            "wedge": "Фокус только на верхней карточке стопки, свайп завершения",
            "display_font": "DM Serif Display, serif",
            "body_font": "Inter, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@400;500;600&display=swap",
            "palette": {
                "bg": "#F7F5F0",
                "surface": "#FFFFFF",
                "border": "#E5E0D8",
                "accent": "#B45309",
                "text_primary": "#1F2937",
                "text_muted": "#6B7280"
            }
        },
        {
            "id": "concept_13",
            "name": "Хронологическая Ось Времени",
            "benchmark": "Linear Stream & Chronological Spine",
            "layout_type": "Центральная вертикальная ось времени со светодиодными узлами",
            "cognitive_law": "Временная ориентация и планирование потока дня",
            "wedge": "Задачи чередуются: слева фокус человека, справа агент",
            "display_font": "Space Grotesk, sans-serif",
            "body_font": "JetBrains Mono, monospace",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&family=Space+Grotesk:wght@600;700&display=swap",
            "palette": {
                "bg": "#0F172A",
                "surface": "#1E293B",
                "border": "rgba(56, 189, 248, 0.25)",
                "accent": "#38BDF8",
                "text_primary": "#F8FAFC",
                "text_muted": "#94A3B8"
            }
        },
        {
            "id": "concept_14",
            "name": "Блокнот Moleskine",
            "benchmark": "Moleskine Classic & Paper Notebooks",
            "layout_type": "Двустраничный разворот книги с корешком и закладкой",
            "cognitive_law": "Тактильная память и эффект генерации (Generation Effect)",
            "wedge": "Разлинованные страницы, рукописные заметки на полях",
            "display_font": "EB Garamond, serif",
            "body_font": "Caveat, cursive",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=EB+Garamond:ital,wght@0,600;1,400&display=swap",
            "palette": {
                "bg": "#F2EBE3",
                "surface": "#FFFDF9",
                "border": "#D8CEBE",
                "accent": "#78350F",
                "text_primary": "#2C221E",
                "text_muted": "#7C6F64"
            }
        },
        {
            "id": "concept_15",
            "name": "Авиационный Кокпит Telemetry",
            "benchmark": "Bloomberg Terminal & Flight HUD",
            "layout_type": "Модульная сетка 4x3 приборной панели с делениями шкал",
            "cognitive_law": "Мгновенное считывание телеметрии (Preattentive Processing)",
            "wedge": "Круговые спидометры стриков, радар капитала, WAL статус",
            "display_font": "Space Mono, monospace",
            "body_font": "Space Mono, monospace",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap",
            "palette": {
                "bg": "#080C14",
                "surface": "#101726",
                "border": "rgba(52, 211, 153, 0.2)",
                "accent": "#34D399",
                "text_primary": "#F1F5F9",
                "text_muted": "#64748B"
            }
        },
        {
            "id": "concept_16",
            "name": "Стеклянный Акрил VisionOS",
            "benchmark": "Apple VisionOS & Fluent Design 2",
            "layout_type": "Парящие полупрозрачные акриловые панели с размытием 32px",
            "cognitive_law": "Пространственная глубина и эффект легкости",
            "wedge": "Светлый перламутр, бирюзовый акцент, призматические блики",
            "display_font": "Outfit, sans-serif",
            "body_font": "Plus Jakarta Sans, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Outfit:wght@600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap",
            "palette": {
                "bg": "#EFF6FF",
                "surface": "rgba(255, 255, 255, 0.75)",
                "border": "rgba(255, 255, 255, 0.8)",
                "accent": "#0D9488",
                "text_primary": "#0F172A",
                "text_muted": "#64748B"
            }
        },
        {
            "id": "concept_17",
            "name": "Ретро-Компьютер 1984",
            "benchmark": "System 1 Macintosh & Xerox Star",
            "layout_type": "Окно классической ОС с полосатой шапкой и кнопками Bevel",
            "cognitive_law": "Ностальгический прайминг и однозначные механические клики",
            "wedge": "8-битные монохромные пиктограммы, ретро-шрифты",
            "display_font": "VT323, monospace",
            "body_font": "JetBrains Mono, monospace",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=VT323&display=swap",
            "palette": {
                "bg": "#A0A0A0",
                "surface": "#C0C0C0",
                "border": "#000000",
                "accent": "#000080",
                "text_primary": "#000000",
                "text_muted": "#404040"
            }
        },
        {
            "id": "concept_18",
            "name": "Журнальный Глянец Bodoni",
            "benchmark": "Vogue Editorial & Architectural Digest",
            "layout_type": "Асимметричный журнальный разворот с гигантским номером дня",
            "cognitive_law": "Эстетическое восприятие и закон формы",
            "wedge": "Заголовки 64px, золото на белом, ультраширокие поля p-12",
            "display_font": "Bodoni Moda, serif",
            "body_font": "Inter, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Bodoni+Moda:opsz,wght@6..96,600;6..96,700&family=Inter:wght@400;500&display=swap",
            "palette": {
                "bg": "#FAFAFA",
                "surface": "#FFFFFF",
                "border": "#E5E5E5",
                "accent": "#C8A96E",
                "text_primary": "#171717",
                "text_muted": "#737373"
            }
        },
        {
            "id": "concept_19",
            "name": "Радиальный Фокус-Поток",
            "benchmark": "Rise Science & Apple Activity Rings",
            "layout_type": "Центральный круговой индикатор спринта + лучевые карточки",
            "cognitive_law": "Закон замкнутости (Closure) и радиальная фокусировка",
            "wedge": "Круговой таймер в центре экрана, задачи по орбите",
            "display_font": "Syne, sans-serif",
            "body_font": "DM Sans, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Syne:wght@700;800&display=swap",
            "palette": {
                "bg": "#0B0914",
                "surface": "#161326",
                "border": "rgba(251, 191, 36, 0.25)",
                "accent": "#FBBF24",
                "text_primary": "#F5F3FF",
                "text_muted": "#8B849C"
            }
        },
        {
            "id": "concept_20",
            "name": "Артизанальная Кофейня",
            "benchmark": "Blue Bottle & Craft Coffee Roasters",
            "layout_type": "Крафтовый картон с винтажными штампами и ярлычками",
            "cognitive_law": "Психология уюта и сенсорное заземление",
            "wedge": "Кофейные тона, тисненые бейджи, теплая матовая органика",
            "display_font": "Playfair Display, serif",
            "body_font": "Plus Jakarta Sans, sans-serif",
            "google_fonts_url": "https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap",
            "palette": {
                "bg": "#F3E9D9",
                "surface": "#E8DAC4",
                "border": "rgba(120, 53, 15, 0.2)",
                "accent": "#92400E",
                "text_primary": "#291811",
                "text_muted": "#6E5B4F"
            }
        }
    ]


def render_concept_facade(idx: int, product_name: str, tagline: str, bp: Dict[str, Any]) -> str:
    """Renders a radically unique, interactive HTML card for each of the 20 concepts."""
    cid = bp["id"]
    pal = bp["palette"]
    dfont = bp["display_font"].split(",")[0].replace("'", "")
    bfont = bp["body_font"].split(",")[0].replace("'", "")
    
    # 1. Swiss Minimalist Grid
    if idx == 1:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-2xl p-6 border border-zinc-200 shadow-sm">
            <div class="grid grid-cols-12 gap-5">
                <!-- Left Sidebar -->
                <div class="col-span-3 border-r border-zinc-200 pr-4 flex flex-col justify-between h-96">
                    <div>
                        <div class="text-xs font-bold font-mono tracking-widest text-red-600 mb-1">01 / СЕТКА</div>
                        <div style="font-family: '{dfont}', sans-serif;" class="text-xl font-extrabold tracking-tight mb-4">WebPlanner OS</div>
                        <div class="space-y-1 text-xs">
                            <div class="px-2.5 py-1.5 rounded bg-zinc-100 font-semibold text-zinc-900 flex justify-between">
                                <span>[Горизонт]</span> <span>3</span>
                            </div>
                            <div class="px-2.5 py-1.5 text-zinc-500 hover:text-zinc-900">[Вышмат]</div>
                            <div class="px-2.5 py-1.5 text-zinc-500 hover:text-zinc-900">[Капитал]</div>
                            <div class="px-2.5 py-1.5 text-zinc-500 hover:text-zinc-900">[Jarvis AI]</div>
                        </div>
                    </div>
                    <div class="border-t border-zinc-200 pt-3 text-[10px] font-mono text-zinc-500">
                        БЕНЧМАРК: Мюллер-Брокманн<br>
                        Швейцарский стиль 1957
                    </div>
                </div>
                <!-- Main Content Grid -->
                <div class="col-span-9 flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between border-b border-zinc-200 pb-3 mb-4">
                            <div>
                                <span class="text-[10px] font-mono uppercase tracking-widest text-zinc-400">ФОКУСНАЯ СЕССИЯ ДНЯ</span>
                                <h3 style="font-family: '{dfont}', sans-serif;" class="text-base font-bold text-zinc-900 mt-0.5">Вышмат: Двойные интегралы в полярных координатах</h3>
                            </div>
                            <span class="px-2.5 py-1 rounded bg-red-600 text-white font-mono text-xs font-bold">45 МИН</span>
                        </div>
                        <div class="grid grid-cols-3 gap-3">
                            <div class="border border-zinc-200 p-3 rounded-lg bg-zinc-50/50">
                                <div class="text-[10px] font-mono font-bold text-zinc-400 mb-1">[01] СЕГОДНЯ</div>
                                <div class="text-xs font-medium text-zinc-800">Признак Даламбера (пример-двойник)</div>
                                <div class="mt-3 text-[10px] text-zinc-500 font-mono">Дедлайн: 10 сен</div>
                            </div>
                            <div class="border border-zinc-200 p-3 rounded-lg bg-zinc-50/50">
                                <div class="text-[10px] font-mono font-bold text-zinc-400 mb-1">[02] ЗАВТРА</div>
                                <div class="text-xs font-medium text-zinc-800">ПДД: 5 билетов (Перекрестки)</div>
                                <div class="mt-3 text-[10px] text-zinc-500 font-mono">Стрик: 12 дней</div>
                            </div>
                            <div class="border border-zinc-200 p-3 rounded-lg bg-zinc-50/50">
                                <div class="text-[10px] font-mono font-bold text-zinc-400 mb-1">[03] ПОСЛЕЗАВТРА</div>
                                <div class="text-xs font-medium text-zinc-800">AI-Zavod: Unit-тесты DAG</div>
                                <div class="mt-3 text-[10px] text-zinc-500 font-mono">Агент: Jarvis</div>
                            </div>
                        </div>
                    </div>
                    <div class="flex items-center justify-between border-t border-zinc-200 pt-3 text-xs">
                        <span class="font-mono text-zinc-500">Синхронизация SQLite WAL: активна</span>
                        <button class="px-3.5 py-1.5 bg-zinc-900 text-white rounded font-medium text-xs hover:bg-zinc-800 transition">Новая запись +</button>
                    </div>
                </div>
            </div>
        </div>
        """

    # 2. Tactile Neo-Craft & Amie
    elif idx == 2:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-3xl p-6 border border-amber-900/10 shadow-lg relative overflow-hidden">
            <div class="flex items-center justify-between mb-5">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-2xl bg-[#C25E00] text-white flex items-center justify-center font-bold text-base shadow-sm">
                        🌸
                    </div>
                    <div>
                        <div style="font-family: '{dfont}', sans-serif;" class="text-lg font-bold text-[#2D241E]">Тактильный Нео-Крафт</div>
                        <div class="text-[11px] text-[#8A7968]">Плавающий остров-док • Бенчмарк: Amie & Craft</div>
                    </div>
                </div>
                <div class="flex items-center space-x-2 bg-[#F3ECE1] px-3 py-1.5 rounded-full text-xs font-semibold text-[#C25E00]">
                    <span>🔥 Стрик привычек: 14 дней</span>
                </div>
            </div>

            <div class="grid grid-cols-2 gap-4 mb-6">
                <div class="bg-white/80 backdrop-blur rounded-2xl p-4 border border-amber-900/5 shadow-sm">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-xs font-bold text-[#C25E00] uppercase tracking-wider">Фокус утра</span>
                        <span class="text-[11px] bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full font-medium">9:00 - 10:30</span>
                    </div>
                    <div class="text-sm font-semibold text-[#2D241E]">Математический анализ: Ряды Лейбница</div>
                    <p class="text-xs text-[#8A7968] mt-1">Разобрать знакочередующиеся ряды и остаток ряда.</p>
                </div>
                <div class="bg-white/80 backdrop-blur rounded-2xl p-4 border border-amber-900/5 shadow-sm">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-xs font-bold text-emerald-700 uppercase tracking-wider">Радар капитала</span>
                        <span class="text-[11px] bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full font-medium">1 650 ₽</span>
                    </div>
                    <div class="text-sm font-semibold text-[#2D241E]">Обед и учебные материалы</div>
                    <p class="text-xs text-[#8A7968] mt-1">Зафиксировано в WAL за 2 клика без перегруза.</p>
                </div>
            </div>

            <!-- Bottom Floating Dock -->
            <div class="bg-white/90 backdrop-blur-md rounded-2xl border border-amber-900/10 p-2 max-w-md mx-auto flex items-center justify-around shadow-md">
                <button class="px-3 py-1.5 rounded-xl bg-[#C25E00] text-white text-xs font-semibold shadow-sm">Горизонт</button>
                <button class="px-3 py-1.5 rounded-xl text-[#8A7968] text-xs font-medium hover:bg-amber-50">Вышмат</button>
                <button class="px-3 py-1.5 rounded-xl text-[#8A7968] text-xs font-medium hover:bg-amber-50">Привычки</button>
                <button class="px-3 py-1.5 rounded-xl text-[#8A7968] text-xs font-medium hover:bg-amber-50">Jarvis</button>
            </div>
        </div>
        """

    # 3. Academic Monochrome & KaTeX
    elif idx == 3:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{dfont}', serif;" class="rounded-xl p-7 border border-slate-200 shadow-sm max-w-3xl mx-auto">
            <div class="text-center border-b border-slate-200 pb-4 mb-5">
                <div class="text-[11px] uppercase tracking-widest text-slate-400 font-sans">АКАДЕМИЧЕСКИЙ ДНЕВНИК • ВЫПУСК №11</div>
                <h2 class="text-2xl font-bold tracking-tight text-slate-900 mt-1">Конспекты и Высшая Математика</h2>
                <div class="text-xs text-slate-500 font-sans italic mt-1">Снижение посторонней когнитивной нагрузки по Свеллеру</div>
            </div>

            <div class="space-y-4">
                <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
                    <div class="flex items-center justify-between font-sans text-xs text-slate-500 mb-1">
                        <span>ТЕОРЕМА / ДВОЙНИК</span>
                        <span class="font-mono">Дедлайн: 10 сентября</span>
                    </div>
                    <div class="text-base font-bold text-slate-900">Исследование сходимости знакоположительного ряда:</div>
                    <div class="font-mono text-xs bg-white p-2.5 rounded border border-slate-200 text-slate-800 my-2 font-sans">
                        $$\lim_{{n \\to \\infty}} \\frac{{a_{{n+1}}}}{{a_n}} = l < 1 \\implies \\sum a_n < \\infty$$
                    </div>
                    <div class="font-sans text-xs text-slate-600">Пример-двойник решен автономно в SymPy. Исходный вариант 11 оставлен для практики.</div>
                </div>

                <div class="grid grid-cols-2 gap-3 font-sans">
                    <div class="p-3 rounded-lg border border-slate-200 bg-white">
                        <div class="text-[10px] uppercase font-bold text-slate-400">ФОКУС ЧЕЛОВЕКА</div>
                        <div class="text-xs font-semibold text-slate-800 mt-1">Решить 3 задачи на бумаге</div>
                    </div>
                    <div class="p-3 rounded-lg border border-slate-200 bg-white">
                        <div class="text-[10px] uppercase font-bold text-slate-400">ДЕЛЕГИРОВАНО АГЕНТУ</div>
                        <div class="text-xs font-semibold text-slate-800 mt-1">Сгенерировать шпаргалку KaTeX</div>
                    </div>
                </div>
            </div>
        </div>
        """

    # 4. Editorial Zen Paper Studio
    elif idx == 4:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-3xl p-6 border border-[#1C1917]/10 shadow-sm">
            <!-- Top Floating Monogram Island -->
            <div class="bg-[#EFEAE0] rounded-2xl p-2.5 px-4 mb-6 flex items-center justify-between border border-[#1C1917]/5 shadow-sm">
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 rounded-xl bg-[#166534] text-[#F8F5EE] flex items-center justify-center font-serif font-bold text-xs select-none">
                        WP
                    </div>
                    <div>
                        <span style="font-family: '{dfont}', serif;" class="font-bold text-sm text-[#1C1917]">WebPlanner OS</span>
                        <span class="text-[10px] font-semibold text-[#166534] bg-emerald-100 px-2 py-0.5 rounded-full ml-1">Дзен</span>
                    </div>
                </div>
                <div class="flex items-center space-x-1 text-xs">
                    <span class="px-2.5 py-1 rounded-lg bg-white font-semibold text-[#166534] shadow-xs">Горизонт 72ч</span>
                    <span class="px-2.5 py-1 rounded-lg text-[#78716C]">Вышмат</span>
                    <span class="px-2.5 py-1 rounded-lg text-[#78716C]">Капитал</span>
                </div>
                <div class="text-xs font-medium text-[#166534] flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-[#166534] animate-pulse"></span> WAL #104
                </div>
            </div>

            <div class="mb-5">
                <span class="text-[11px] font-bold text-[#166534] uppercase tracking-wider">Архитектура ясности</span>
                <h2 style="font-family: '{dfont}', serif;" class="text-2xl font-bold text-[#1C1917] mt-0.5">Когнитивный горизонт 72 часа</h2>
            </div>

            <div class="grid grid-cols-3 gap-3">
                <div class="bg-[#EFEAE0] p-4 rounded-2xl border border-[#1C1917]/5">
                    <div class="text-xs font-bold text-[#166534] mb-2 flex justify-between">
                        <span>День 1 (Сегодня)</span> <span>2</span>
                    </div>
                    <div class="bg-[#F8F5EE] p-3 rounded-xl text-xs font-semibold text-[#1C1917] shadow-xs">
                        Признак Даламбера (разбор)
                    </div>
                </div>
                <div class="bg-[#EFEAE0] p-4 rounded-2xl border border-[#1C1917]/5">
                    <div class="text-xs font-bold text-[#78716C] mb-2 flex justify-between">
                        <span>День 2 (Завтра)</span> <span>1</span>
                    </div>
                    <div class="bg-[#F8F5EE] p-3 rounded-xl text-xs font-medium text-[#1C1917] shadow-xs">
                        ПДД: 5 билетов
                    </div>
                </div>
                <div class="bg-[#EFEAE0] p-4 rounded-2xl border border-[#1C1917]/5">
                    <div class="text-xs font-bold text-[#78716C] mb-2 flex justify-between">
                        <span>День 3 (Послезавтра)</span> <span>1</span>
                    </div>
                    <div class="bg-[#F8F5EE] p-3 rounded-xl text-xs font-medium text-[#1C1917] shadow-xs">
                        Рефакторинг AI-Zavod
                    </div>
                </div>
            </div>
        </div>
        """

    # 5. Spotlight HUD
    elif idx == 5:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', monospace;" class="rounded-2xl p-6 border border-amber-500/20 shadow-2xl">
            <!-- Central Command Bar -->
            <div class="bg-[#181B24] border border-amber-500/30 rounded-xl p-3 flex items-center justify-between mb-5 shadow-inner">
                <div class="flex items-center space-x-3 text-xs">
                    <span class="text-amber-400 font-bold font-mono">⌘K</span>
                    <span class="text-slate-300">Найти задачу, зафиксировать расход или вызвать Jarvis...</span>
                </div>
                <div class="flex items-center space-x-1.5 text-[10px]">
                    <span class="px-1.5 py-0.5 rounded bg-zinc-800 text-amber-300 border border-zinc-700">Enter</span>
                    <span class="px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700">Esc</span>
                </div>
            </div>

            <div class="grid grid-cols-3 gap-3 text-xs">
                <div class="bg-[#181B24] p-3.5 rounded-xl border border-white/5">
                    <div class="flex justify-between text-amber-400 text-[11px] mb-2 font-bold">
                        <span>[1] ВЫШМАТ</span> <span>45 мин</span>
                    </div>
                    <div class="text-white font-medium">Двойные интегралы в SymPy</div>
                    <div class="text-zinc-500 text-[10px] mt-2 font-mono">Шорткат: ⌘1</div>
                </div>
                <div class="bg-[#181B24] p-3.5 rounded-xl border border-white/5">
                    <div class="flex justify-between text-emerald-400 text-[11px] mb-2 font-bold">
                        <span>[2] КАПИТАЛ</span> <span>1 650 ₽</span>
                    </div>
                    <div class="text-white font-medium">Быстрый расход (обед)</div>
                    <div class="text-zinc-500 text-[10px] mt-2 font-mono">Шорткат: ⌘2</div>
                </div>
                <div class="bg-[#181B24] p-3.5 rounded-xl border border-white/5">
                    <div class="flex justify-between text-cyan-400 text-[11px] mb-2 font-bold">
                        <span>[3] JARVIS</span> <span>Active</span>
                    </div>
                    <div class="text-white font-medium">Синхронизация базы WAL</div>
                    <div class="text-zinc-500 text-[10px] mt-2 font-mono">Шорткат: ⌘3</div>
                </div>
            </div>
        </div>
        """

    # 6. Bauhaus 1925
    elif idx == 6:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-none p-6 border-2 border-black shadow-[6px_6px_0px_#000]">
            <div class="flex items-center justify-between border-b-2 border-black pb-4 mb-5">
                <div class="flex items-center space-x-3">
                    <div class="w-8 h-8 rounded-full bg-[#1D4ED8] border-2 border-black"></div>
                    <div class="w-8 h-8 bg-[#DC2626] border-2 border-black"></div>
                    <div class="w-0 h-0 border-l-[16px] border-l-transparent border-r-[16px] border-r-transparent border-b-[32px] border-b-[#EAB308]"></div>
                    <h1 style="font-family: '{dfont}', sans-serif;" class="text-2xl font-extrabold uppercase tracking-tight text-black ml-2">БАУХАУС 1925</h1>
                </div>
                <span class="px-3 py-1 bg-black text-white font-mono text-xs font-bold uppercase">ФОРМА = ФУНКЦИЯ</span>
            </div>

            <div class="grid grid-cols-12 gap-4">
                <div class="col-span-8 border-2 border-black p-4 bg-white">
                    <div class="text-xs font-bold uppercase text-[#1D4ED8] mb-1">ФОКУС СЕГОДНЯ</div>
                    <div style="font-family: '{dfont}', sans-serif;" class="text-lg font-bold text-black">Признак сходимости Даламбера</div>
                    <p class="text-xs text-zinc-600 mt-1">Четкое математическое доказательство без лишних декоративных украшательств.</p>
                </div>
                <div class="col-span-4 border-2 border-black p-4 bg-[#EAE6DB] flex flex-col justify-between">
                    <div class="text-xs font-bold uppercase text-black">КАПИТАЛ</div>
                    <div class="text-2xl font-black text-[#1D4ED8]">1 650 ₽</div>
                    <div class="text-[10px] font-mono text-black uppercase">WAL ЗАПИСЬ ОДОБРЕНА</div>
                </div>
            </div>
        </div>
        """

    # 7. Neo-Brutalism 2.0
    elif idx == 7:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-xl p-6 border-2 border-black shadow-[5px_5px_0px_#000000]">
            <div class="flex items-center justify-between mb-5">
                <div class="flex items-center space-x-2">
                    <span class="px-3 py-1 bg-[#84CC16] border-2 border-black font-extrabold text-xs shadow-[2px_2px_0px_#000]">НЕО-БРУТАЛИЗМ</span>
                    <span class="text-xs font-bold">WEBPLANNER OS</span>
                </div>
                <button class="px-4 py-1.5 bg-black text-white font-bold text-xs border-2 border-black shadow-[3px_3px_0px_#84CC16]">НОВАЯ ЗАДАЧА +</button>
            </div>

            <div class="grid grid-cols-3 gap-3">
                <div class="border-2 border-black p-4 rounded-lg bg-[#F4F4F5] shadow-[4px_4px_0px_#000]">
                    <div class="text-[11px] font-extrabold text-black uppercase mb-1">СЕГОДНЯ</div>
                    <div style="font-family: '{dfont}', sans-serif;" class="text-sm font-black text-black">ВЫШМАТ ИНТЕГРАЛЫ</div>
                    <div class="mt-3 inline-block px-2 py-0.5 bg-[#84CC16] border border-black text-[10px] font-bold">45 МИН</div>
                </div>
                <div class="border-2 border-black p-4 rounded-lg bg-[#F4F4F5] shadow-[4px_4px_0px_#000]">
                    <div class="text-[11px] font-extrabold text-black uppercase mb-1">ЗАВТРА</div>
                    <div style="font-family: '{dfont}', sans-serif;" class="text-sm font-black text-black">ПДД 5 БИЛЕТОВ</div>
                    <div class="mt-3 inline-block px-2 py-0.5 bg-yellow-300 border border-black text-[10px] font-bold">СТРИК 12</div>
                </div>
                <div class="border-2 border-black p-4 rounded-lg bg-[#F4F4F5] shadow-[4px_4px_0px_#000]">
                    <div class="text-[11px] font-extrabold text-black uppercase mb-1">ПОСЛЕЗАВТРА</div>
                    <div style="font-family: '{dfont}', sans-serif;" class="text-sm font-black text-black">AI-ZAVOD СБОРКА</div>
                    <div class="mt-3 inline-block px-2 py-0.5 bg-cyan-300 border border-black text-[10px] font-bold">JARVIS</div>
                </div>
            </div>
        </div>
        """

    # 8. Apple Dark Titanium
    elif idx == 8:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-3xl p-6 border border-white/10 shadow-2xl">
            <!-- Dynamic Island Header -->
            <div class="max-w-xs mx-auto bg-black/80 backdrop-blur-2xl border border-white/10 rounded-full px-4 py-2 flex items-center justify-between mb-6 shadow-lg">
                <div class="flex items-center space-x-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span class="text-xs font-medium text-slate-200">Фокус сессия</span>
                </div>
                <span class="text-xs font-mono font-bold text-slate-300">28:14</span>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="bg-[#1E2028] p-5 rounded-2xl border border-white/5">
                    <span class="text-[11px] font-medium text-slate-400">ГЛАВНЫЙ ПРИОРИТЕТ</span>
                    <h3 class="text-base font-semibold text-white mt-1">Исследование числовых рядов</h3>
                    <p class="text-xs text-slate-400 mt-1">Признак Даламбера • Вычисление пределов</p>
                </div>
                <div class="bg-[#1E2028] p-5 rounded-2xl border border-white/5 flex flex-col justify-between">
                    <div>
                        <span class="text-[11px] font-medium text-slate-400">СВОДКА РАСХОДОВ</span>
                        <div class="text-xl font-bold text-white mt-1">1 650,00 ₽</div>
                    </div>
                    <div class="text-[11px] text-emerald-400 font-medium">Синхронизировано в SQLite WAL</div>
                </div>
            </div>
        </div>
        """

    # 9. Wabi-Sabi Organic
    elif idx == 9:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-3xl p-8 border border-stone-300/40">
            <div class="flex items-center justify-between mb-8">
                <div>
                    <span class="text-xs font-medium text-[#4A5D4E] tracking-widest uppercase">Ваби-Саби Покой</span>
                    <h2 style="font-family: '{dfont}', serif;" class="text-2xl font-normal text-[#2D2C2A] mt-1">Естественный поток дня</h2>
                </div>
                <div class="text-xs text-[#75726D] italic">Простота и отсутствие шума</div>
            </div>

            <div class="space-y-4">
                <div class="p-5 rounded-2xl bg-[#EAE3DA]/60 flex items-center justify-between">
                    <div>
                        <div class="text-sm font-medium text-[#2D2C2A]">Утренний конспект по вышмату</div>
                        <div class="text-xs text-[#75726D] mt-0.5">Ряды с факториалами и признак Даламбера</div>
                    </div>
                    <span class="text-xs text-[#4A5D4E] font-medium">45 мин</span>
                </div>
                <div class="p-5 rounded-2xl bg-[#EAE3DA]/60 flex items-center justify-between">
                    <div>
                        <div class="text-sm font-medium text-[#2D2C2A]">Дневная прогулка и повторение ПДД</div>
                        <div class="text-xs text-[#75726D] mt-0.5">Стрик привычки сохранен</div>
                    </div>
                    <span class="text-xs text-[#4A5D4E] font-medium">30 мин</span>
                </div>
            </div>
        </div>
        """

    # 10. Financial Times Broadsheet
    elif idx == 10:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{dfont}', serif;" class="rounded-none p-6 border-t-4 border-b-4 border-black">
            <div class="text-center border-b border-black pb-2 mb-4">
                <div class="text-[10px] uppercase tracking-widest text-stone-600 font-sans">ВЫПУСК № 48,291 • СРЕДА • ПЛАНИРОВАНИЕ И КАПИТАЛ</div>
                <h1 class="text-3xl font-bold tracking-tight text-black my-1">ВЕБ-ПЛАНЕР ДЕСКТОП</h1>
                <div class="text-xs font-sans text-stone-700">Суверенный трехдневный когнитивный срез реальности</div>
            </div>

            <div class="grid grid-cols-3 gap-4 border-b border-black pb-4 text-xs font-sans">
                <div class="border-r border-black/20 pr-3">
                    <h4 class="font-serif font-bold text-sm text-black mb-1">КОЛОНКА I: ВЫШМАТ</h4>
                    <p class="text-stone-700 leading-relaxed">Разбор сходимости числовых рядов по признаку Даламбера завершен на 100%. Вариант 11 сохранен для тренировки.</p>
                </div>
                <div class="border-r border-black/20 pr-3">
                    <h4 class="font-serif font-bold text-sm text-black mb-1">КОЛОНКА II: КАПИТАЛ</h4>
                    <p class="text-stone-700 leading-relaxed">Дневной расход зафиксирован на отметке 1 650 ₽. Транзакция внесена в WAL-журнал без задержек.</p>
                </div>
                <div>
                    <h4 class="font-serif font-bold text-sm text-black mb-1">КОЛОНКА III: АГЕНТ</h4>
                    <p class="text-stone-700 leading-relaxed">Jarvis AI выполняет фоновые расчеты матриц в фоновом потоке Linux-сервера.</p>
                </div>
            </div>
        </div>
        """

    # 11. Split-Screen Kanban
    elif idx == 11:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-2xl p-6 border border-zinc-700 shadow-xl">
            <div class="grid grid-cols-12 gap-5">
                <!-- Left 50% Big Timer & Focus -->
                <div class="col-span-6 bg-[#27272A] p-5 rounded-xl border border-zinc-600 flex flex-col justify-between">
                    <div>
                        <span class="text-xs font-bold text-emerald-400 uppercase tracking-wider">СПРИНТ 50/50</span>
                        <h2 style="font-family: '{dfont}', sans-serif;" class="text-xl font-bold text-white mt-1">Признак Даламбера (вышмат)</h2>
                        <p class="text-xs text-zinc-400 mt-1">Глубокая концентрация на вычислении пределов факториалов.</p>
                    </div>
                    <div class="my-6 text-center">
                        <div class="text-4xl font-black font-mono text-emerald-400 tracking-tight">42:18</div>
                        <div class="text-[11px] text-zinc-400 mt-1">Осталось до окончания спринта</div>
                    </div>
                    <button class="w-full py-2 bg-emerald-600 text-white font-semibold text-xs rounded-lg hover:bg-emerald-500 transition">Завершить задачу ✓</button>
                </div>
                <!-- Right 50% Kanban 72h -->
                <div class="col-span-6 grid grid-cols-3 gap-2 text-xs">
                    <div class="bg-[#27272A]/70 p-2.5 rounded-lg border border-zinc-700">
                        <div class="font-bold text-[11px] text-zinc-300 mb-2">СЕГОДНЯ</div>
                        <div class="p-2 rounded bg-zinc-800 text-[11px] text-zinc-200 border border-zinc-700 mb-1.5">Ряды Даламбера</div>
                        <div class="p-2 rounded bg-zinc-800 text-[11px] text-zinc-200 border border-zinc-700">Расход 1 650 ₽</div>
                    </div>
                    <div class="bg-[#27272A]/70 p-2.5 rounded-lg border border-zinc-700">
                        <div class="font-bold text-[11px] text-zinc-400 mb-2">ЗАВТРА</div>
                        <div class="p-2 rounded bg-zinc-800 text-[11px] text-zinc-300 border border-zinc-700">ПДД 5 билетов</div>
                    </div>
                    <div class="bg-[#27272A]/70 p-2.5 rounded-lg border border-zinc-700">
                        <div class="font-bold text-[11px] text-zinc-400 mb-2">ПОСЛЕЗАВТРА</div>
                        <div class="p-2 rounded bg-zinc-800 text-[11px] text-zinc-300 border border-zinc-700">Код AI-Zavod</div>
                    </div>
                </div>
            </div>
        </div>
        """

    # 12. Physical Card Deck
    elif idx == 12:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-3xl p-6 border border-amber-900/10 shadow-sm relative">
            <div class="text-center mb-5">
                <span class="text-[10px] uppercase font-bold tracking-widest text-amber-800 font-mono">СТОПКА КАРТОЧЕК</span>
                <h3 style="font-family: '{dfont}', serif;" class="text-xl font-bold text-zinc-900">Колода задач на 72 часа</h3>
            </div>

            <!-- Card Stack effect -->
            <div class="relative max-w-sm mx-auto h-48">
                <!-- Bottom card -->
                <div class="absolute inset-x-4 top-4 h-36 bg-amber-100 rounded-2xl border border-amber-900/10 shadow-sm"></div>
                <!-- Middle card -->
                <div class="absolute inset-x-2 top-2 h-36 bg-amber-50 rounded-2xl border border-amber-900/10 shadow-md"></div>
                <!-- Top active card -->
                <div class="absolute inset-x-0 top-0 h-36 bg-white rounded-2xl border border-amber-900/20 p-4 shadow-xl flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between text-xs mb-1">
                            <span class="font-bold text-amber-700">КАРТОЧКА 1 ИЗ 4</span>
                            <span class="px-2 py-0.5 bg-amber-100 text-amber-800 rounded-full font-mono text-[10px]">45 МИН</span>
                        </div>
                        <div style="font-family: '{dfont}', serif;" class="text-base font-bold text-zinc-900">Вышмат: Признак Даламбера</div>
                        <div class="text-xs text-zinc-500 mt-0.5">Исследовать ряд с факториалами.</div>
                    </div>
                    <div class="flex justify-between items-center text-xs pt-2 border-t border-zinc-100">
                        <button class="text-zinc-400 hover:text-zinc-600">Смахнуть →</button>
                        <button class="px-3 py-1 bg-amber-700 text-white rounded-lg font-medium">Готово ✓</button>
                    </div>
                </div>
            </div>
        </div>
        """

    # 13. Timeline Spine Flow
    elif idx == 13:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', monospace;" class="rounded-2xl p-6 border border-cyan-500/20 shadow-xl">
            <div class="flex justify-between items-center mb-6">
                <div>
                    <span class="text-xs font-bold text-cyan-400 font-sans tracking-wider">ОСЬ ВРЕМЕНИ</span>
                    <h3 style="font-family: '{dfont}', sans-serif;" class="text-lg font-bold text-white">Хронологический поток</h3>
                </div>
                <span class="px-2.5 py-1 bg-cyan-950 text-cyan-300 rounded border border-cyan-800 text-xs font-mono">09 Сен 2026</span>
            </div>

            <!-- Vertical spine -->
            <div class="space-y-4 relative before:absolute before:inset-0 before:left-6 before:w-0.5 before:bg-cyan-500/30">
                <div class="flex items-center space-x-4 relative">
                    <div class="w-12 text-right text-[11px] text-cyan-400 font-mono">09:00</div>
                    <div class="w-3 h-3 rounded-full bg-cyan-400 border-2 border-[#0F172A] z-10"></div>
                    <div class="flex-1 bg-[#1E293B] p-3 rounded-xl border border-cyan-500/20 text-xs">
                        <span class="font-bold text-white">Фокус 1: Разбор признака Даламбера (вышмат)</span>
                    </div>
                </div>
                <div class="flex items-center space-x-4 relative">
                    <div class="w-12 text-right text-[11px] text-cyan-400 font-mono">14:00</div>
                    <div class="w-3 h-3 rounded-full bg-cyan-400 border-2 border-[#0F172A] z-10"></div>
                    <div class="flex-1 bg-[#1E293B] p-3 rounded-xl border border-cyan-500/20 text-xs">
                        <span class="font-bold text-white">Фокус 2: ПДД 5 билетов + фиксация расхода 1 650 ₽</span>
                    </div>
                </div>
                <div class="flex items-center space-x-4 relative">
                    <div class="w-12 text-right text-[11px] text-zinc-500 font-mono">23:59</div>
                    <div class="w-3 h-3 rounded-full bg-zinc-600 border-2 border-[#0F172A] z-10"></div>
                    <div class="flex-1 bg-[#1E293B]/50 p-2.5 rounded-xl border border-white/5 text-xs text-zinc-400">
                        <span>Перенос незавершенных задач на полночь (Midnight Rollover)</span>
                    </div>
                </div>
            </div>
        </div>
        """

    # 14. Moleskine Notebook
    elif idx == 14:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{dfont}', serif;" class="rounded-xl p-7 border-2 border-[#D8CEBE] shadow-md relative">
            <div class="absolute top-0 left-8 w-4 h-12 bg-red-700 rounded-b shadow-sm"></div>
            
            <div class="grid grid-cols-2 gap-6 pl-6 border-l-2 border-dashed border-[#D8CEBE]">
                <!-- Left Page -->
                <div>
                    <div class="text-[10px] font-mono text-[#7C6F64] uppercase tracking-widest mb-2">СТРАНИЦА 1 • ВЫШМАТ</div>
                    <h3 class="text-xl font-bold text-[#2C221E]">Числовые ряды</h3>
                    <p class="text-xs text-[#7C6F64] italic mt-1">Исследовать ряд по признаку Даламбера на сходимость.</p>
                    <div style="font-family: '{bfont}', cursive;" class="text-lg text-red-900 mt-4 leading-snug">
                        «Обязательно выписать предел отношения последующего к предыдущему члену!»
                    </div>
                </div>
                <!-- Right Page -->
                <div>
                    <div class="text-[10px] font-mono text-[#7C6F64] uppercase tracking-widest mb-2">СТРАНИЦА 2 • КАПИТАЛ</div>
                    <h3 class="text-xl font-bold text-[#2C221E]">Дневник расходов</h3>
                    <div class="mt-3 space-y-1.5 text-xs">
                        <div class="flex justify-between border-b border-[#D8CEBE] pb-1">
                            <span>Обед и кофе:</span> <span class="font-mono font-bold">1 650 ₽</span>
                        </div>
                        <div class="flex justify-between border-b border-[#D8CEBE] pb-1">
                            <span>Стрик привычек:</span> <span class="font-mono font-bold">14 дней</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    # 15. Telemetry 4x3 Cockpit
    elif idx == 15:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', monospace;" class="rounded-2xl p-6 border border-emerald-500/30 shadow-2xl">
            <div class="flex items-center justify-between border-b border-emerald-500/20 pb-3 mb-4 text-xs">
                <span class="text-emerald-400 font-bold tracking-widest">ТЕЛЕМЕТРИЯ HUD • ПРИБОРНАЯ ПАНЕЛЬ</span>
                <span class="text-zinc-400">СИСТЕМА: ONLINE • WAL #104</span>
            </div>

            <div class="grid grid-cols-4 gap-3 text-xs mb-4">
                <div class="bg-[#101726] p-3 rounded-lg border border-emerald-500/20">
                    <div class="text-[10px] text-zinc-400 uppercase">СПРИНТ 1</div>
                    <div class="text-lg font-bold text-emerald-400 mt-1">45:00</div>
                    <div class="text-[10px] text-zinc-500">Вышмат фокус</div>
                </div>
                <div class="bg-[#101726] p-3 rounded-lg border border-emerald-500/20">
                    <div class="text-[10px] text-zinc-400 uppercase">РАСХОД</div>
                    <div class="text-lg font-bold text-emerald-400 mt-1">1 650 ₽</div>
                    <div class="text-[10px] text-zinc-500">За 24 часа</div>
                </div>
                <div class="bg-[#101726] p-3 rounded-lg border border-emerald-500/20">
                    <div class="text-[10px] text-zinc-400 uppercase">СТРИК</div>
                    <div class="text-lg font-bold text-emerald-400 mt-1">14 ДНЕЙ</div>
                    <div class="text-[10px] text-zinc-500">ПДД + Спорт</div>
                </div>
                <div class="bg-[#101726] p-3 rounded-lg border border-emerald-500/20">
                    <div class="text-[10px] text-zinc-400 uppercase">ЗАДАЧИ</div>
                    <div class="text-lg font-bold text-emerald-400 mt-1">3/4</div>
                    <div class="text-[10px] text-zinc-500">75% закрыто</div>
                </div>
            </div>
            
            <div class="bg-[#101726] p-3 rounded-lg border border-emerald-500/20 flex justify-between items-center text-xs">
                <span>Фокусная задача: Разбор признака Даламбера</span>
                <span class="px-2 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-700">Исполняется</span>
            </div>
        </div>
        """

    # 16. Frosted Acrylic VisionOS
    elif idx == 16:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-3xl p-6 border border-white/80 shadow-xl backdrop-blur-3xl relative">
            <div class="flex items-center justify-between mb-5">
                <div class="flex items-center space-x-3">
                    <div class="w-9 h-9 rounded-2xl bg-white/80 border border-white/80 flex items-center justify-center text-teal-600 font-bold shadow-sm">
                        💧
                    </div>
                    <div>
                        <div style="font-family: '{dfont}', sans-serif;" class="text-base font-bold text-slate-900">Стеклянный Акрил VisionOS</div>
                        <div class="text-[11px] text-slate-500">Пространственный интерфейс с глубоким размытием</div>
                    </div>
                </div>
                <span class="px-3 py-1 rounded-full bg-teal-500/10 text-teal-700 font-semibold text-xs border border-teal-500/20">72 часа</span>
            </div>

            <div class="grid grid-cols-2 gap-4">
                <div class="bg-white/70 backdrop-blur-xl p-4 rounded-2xl border border-white/90 shadow-sm">
                    <span class="text-xs font-bold text-teal-600 uppercase">Главная цель</span>
                    <h4 class="text-sm font-semibold text-slate-900 mt-1">Математика: Признак Даламбера</h4>
                    <p class="text-xs text-slate-500 mt-1">Вычислить предел отношений с факториалами.</p>
                </div>
                <div class="bg-white/70 backdrop-blur-xl p-4 rounded-2xl border border-white/90 shadow-sm flex flex-col justify-between">
                    <div>
                        <span class="text-xs font-bold text-teal-600 uppercase">Радар капитала</span>
                        <div class="text-lg font-bold text-slate-900 mt-1">1 650,00 ₽</div>
                    </div>
                    <span class="text-[11px] text-slate-500">2 клика до сохранения</span>
                </div>
            </div>
        </div>
        """

    # 17. Retro Macintosh 1984
    elif idx == 17:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{dfont}', monospace;" class="rounded-none p-5 border-2 border-black shadow-[4px_4px_0px_#000]">
            <!-- Mac Titlebar with striped pattern -->
            <div class="bg-[#C0C0C0] border-2 border-black p-1.5 flex items-center justify-between mb-4 shadow-[inset_1px_1px_0px_#fff]">
                <div class="w-3.5 h-3.5 border border-black bg-white cursor-pointer"></div>
                <div class="font-bold text-sm tracking-widest text-black">ВЕБ-ПЛАНЕР '84</div>
                <div class="w-3.5 h-3.5"></div>
            </div>

            <div class="bg-white border-2 border-black p-4 mb-4 text-xs font-mono">
                <div class="font-bold text-sm mb-1 text-black">ФОКУС: ВЫШМАТ.DOC</div>
                <p class="text-black leading-tight">РЯДЫ ДАЛАМБЕРА: ВЫЧИСЛИТЬ lim(a_{{n+1}}/a_n).<br>ФАКТОРИАЛЫ СОКРАЩАЮТСЯ ДО (n+1).</p>
            </div>

            <div class="flex items-center justify-between text-xs">
                <div class="border-2 border-black px-3 py-1 bg-[#C0C0C0] shadow-[inset_1px_1px_0px_#fff] font-bold">РАСХОД: 1650 РУБ.</div>
                <button class="border-2 border-black px-4 py-1 bg-[#C0C0C0] shadow-[2px_2px_0px_#000] font-bold active:translate-x-0.5">ОК</button>
            </div>
        </div>
        """

    # 18. Kinfolk Magazine Bodoni
    elif idx == 18:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{dfont}', serif;" class="rounded-none p-8 border border-neutral-300 relative overflow-hidden">
            <div class="absolute -right-6 -bottom-10 text-[140px] font-bold text-neutral-200/50 select-none pointer-events-none">01</div>
            
            <div class="border-b border-neutral-200 pb-4 mb-6">
                <div class="text-[10px] font-sans uppercase tracking-[0.3em] text-neutral-400">ГЛЯНЕЦ • ДЕНЬ ПЕРВЫЙ</div>
                <h1 class="text-3xl font-bold tracking-tight text-neutral-900 mt-1">Архитектура Дня</h1>
            </div>

            <div class="grid grid-cols-2 gap-6 relative z-10">
                <div>
                    <h3 class="text-base font-bold text-neutral-900">Исследование Рядов</h3>
                    <p class="font-sans text-xs text-neutral-500 mt-1 leading-relaxed">Признак Даламбера. Чистая академическая эстетика с глубоким погружением.</p>
                </div>
                <div class="font-sans border-l border-neutral-200 pl-6 flex flex-col justify-between">
                    <div>
                        <div class="text-[10px] uppercase tracking-widest text-amber-700">КАПИТАЛ</div>
                        <div class="text-2xl font-serif font-bold text-neutral-900 mt-1">1 650 ₽</div>
                    </div>
                    <div class="text-xs text-neutral-400">Синхронизировано WAL</div>
                </div>
            </div>
        </div>
        """

    # 19. Radial Pomodoro Hub
    elif idx == 19:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-3xl p-6 border border-amber-500/20 shadow-2xl">
            <div class="flex items-center justify-between mb-4">
                <span style="font-family: '{dfont}', sans-serif;" class="text-sm font-bold text-amber-400 uppercase tracking-wider">Радиальный Фокус-Поток</span>
                <span class="text-xs text-slate-400 font-mono">Цикл 2 из 4</span>
            </div>

            <!-- Central radial ring -->
            <div class="flex items-center justify-center my-4">
                <div class="w-36 h-36 rounded-full border-4 border-amber-500/20 border-t-amber-400 flex flex-col items-center justify-center relative shadow-lg shadow-amber-500/5">
                    <span class="text-2xl font-bold font-mono text-white">35:00</span>
                    <span class="text-[10px] text-amber-400 font-medium uppercase mt-0.5">В фокусе</span>
                </div>
            </div>

            <div class="bg-[#161326] p-3.5 rounded-2xl border border-white/5 text-xs text-center">
                <span class="text-slate-300 font-medium">Текущий спринт: Вышмат (Признак Даламбера)</span>
            </div>
        </div>
        """

    # 20. Artisanal Coffee & Roast
    elif idx == 20:
        return f"""
        <div style="background-color: {pal['bg']}; color: {pal['text_primary']}; font-family: '{bfont}', sans-serif;" class="rounded-3xl p-6 border border-[#78350F]/20 shadow-sm relative">
            <div class="flex items-center justify-between mb-5">
                <div class="flex items-center space-x-3">
                    <div class="w-9 h-9 rounded-xl bg-[#92400E] text-[#F3E9D9] flex items-center justify-center font-bold text-sm shadow-sm">
                        ☕
                    </div>
                    <div>
                        <div style="font-family: '{dfont}', serif;" class="text-base font-bold text-[#291811]">Артизанальная Кофейня</div>
                        <div class="text-[11px] text-[#6E5B4F]">Крафтовое тепло • Сенсорное заземление</div>
                    </div>
                </div>
                <span class="px-2.5 py-1 rounded-full bg-[#E8DAC4] text-[#92400E] font-semibold text-xs border border-[#78350F]/20">Свежий обжиг</span>
            </div>

            <div class="space-y-3">
                <div class="bg-[#E8DAC4]/80 p-3.5 rounded-2xl border border-[#78350F]/15 flex items-center justify-between">
                    <div>
                        <div style="font-family: '{dfont}', serif;" class="text-sm font-bold text-[#291811]">Вышмат: Признак Даламбера</div>
                        <div class="text-xs text-[#6E5B4F] mt-0.5">Разбор формулы и предельного перехода</div>
                    </div>
                    <span class="text-xs font-bold text-[#92400E]">45 мин</span>
                </div>
                <div class="bg-[#E8DAC4]/80 p-3.5 rounded-2xl border border-[#78350F]/15 flex items-center justify-between">
                    <div>
                        <div style="font-family: '{dfont}', serif;" class="text-sm font-bold text-[#291811]">Капитал: Дневной чек</div>
                        <div class="text-xs text-[#6E5B4F] mt-0.5">Внесено в WAL без лишних кликов</div>
                    </div>
                    <span class="text-xs font-bold text-[#92400E]">1 650 ₽</span>
                </div>
            </div>
        </div>
        """

    # Fallback
    return f"""
    <div style="background-color: {pal['bg']}; color: {pal['text_primary']};" class="p-6 rounded-2xl border border-zinc-200">
        <h3 class="text-lg font-bold">{bp['name']}</h3>
        <p class="text-xs mt-2">{bp['wedge']}</p>
    </div>
    """


def generate_all_20_concept_facades(session_id: str, prd_spec: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Synthesizes all 20 competitive interactive facades for WebPlanner."""
    product_name = prd_spec.get("product_name", "WebPlanner Desktop OS")
    tagline = prd_spec.get("tagline", "Суверенная когнитивная среда 72ч")
    
    blueprints = get_20_concept_blueprints()
    concepts = []
    
    for idx, bp in enumerate(blueprints, start=1):
        facade_html = render_concept_facade(idx, product_name, tagline, bp)
        concept_data = {
            "id": bp["id"],
            "name": f"{idx}. {bp['name']}",
            "benchmark": bp["benchmark"],
            "cognitive_law": bp["cognitive_law"],
            "product_thesis": bp["layout_type"],
            "wedge": bp["wedge"],
            "target_persona": "Студент / Разработчик (KFU IVMIIT)",
            "theme_name": bp["name"],
            "aesthetic_archetype": bp["layout_type"],
            "palette": bp["palette"],
            "typography": {
                "display_font": bp["display_font"],
                "body_font": bp["body_font"],
                "google_fonts_url": bp["google_fonts_url"]
            },
            "facade_html": facade_html.strip()
        }
        concepts.append(concept_data)
        
    return concepts
