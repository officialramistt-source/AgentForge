import os
import json
import logging
import webbrowser
from typing import Dict, Any, List, Tuple, Optional

logger = logging.getLogger("AI_Zavod.HITLMatrix")

def generate_matrix_html(
    session_id: str,
    prd_spec: Dict[str, Any],
    concepts: List[Dict[str, Any]],
    output_path: str
) -> str:
    """
    Generates a standalone, elite HTML matrix preview comparing all 5 competitive product concepts.
    Allows live interactive tab switching and direct one-click selection.
    """
    product_name = prd_spec.get("product_name", "Autonomous App")
    tagline = prd_spec.get("tagline", "Executive Digital Platform")
    recommended_id = prd_spec.get("recommended_archetype_id", "concept_3")

    concepts_json = json.dumps(concepts, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Zavod HITL Matrix: {product_name}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{
            background-color: #06080D;
            color: #F8FAFC;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        .font-serif {{ font-family: 'Playfair Display', serif; }}
        .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    </style>
</head>
<body class="min-h-screen p-4 sm:p-8 flex flex-col items-center">

    <!-- Floating Island Header -->
    <header class="w-full max-w-6xl mx-auto rounded-3xl bg-[#0E131F]/90 border border-slate-800/80 shadow-2xl backdrop-blur-xl p-6 mb-8 text-center">
        <div class="inline-flex items-center space-x-2 px-3.5 py-1 rounded-full text-xs font-semibold tracking-wider uppercase bg-amber-500/10 text-amber-400 border border-amber-500/20 mb-3">
            🎯 Human-in-the-Loop Concept Matrix • 5 World-Class Archetypes
        </div>
        <h1 class="text-3xl sm:text-4xl font-bold font-serif italic text-white tracking-tight mb-2">
            {product_name}
        </h1>
        <p class="text-sm text-slate-400 max-w-xl mx-auto">
            {tagline}
        </p>
    </header>

    <!-- Floating Navigation Bar for the 5 Concepts -->
    <nav class="w-full max-w-5xl mx-auto rounded-2xl bg-[#0F1424] border border-slate-800 shadow-xl p-2 mb-8 flex flex-wrap items-center justify-center gap-2">
    """

    for i, c in enumerate(concepts):
        cid = c["id"]
        cname = c["name"].split("(")[0].strip()
        benchmark = c.get("benchmark", "")
        is_rec = cid == recommended_id
        badge = "⭐ ТОП PM" if is_rec else f"#{i+1}"

        html += f"""
        <button onclick="selectTab('{cid}')" id="tab-{cid}" class="tab-btn px-4 py-2.5 rounded-xl text-xs font-semibold transition-all duration-200 flex items-center space-x-2 bg-transparent text-slate-400 hover:text-white">
            <span class="text-[10px] px-2 py-0.5 rounded-md {'bg-amber-500/20 text-amber-300 font-bold' if is_rec else 'bg-slate-800 text-slate-400'}">{badge}</span>
            <span>{cname}</span>
            <span class="text-[10px] text-slate-500 font-normal">({benchmark})</span>
        </button>
        """

    html += """
    </nav>

    <!-- Concept Views Container -->
    <main class="w-full max-w-6xl mx-auto mb-12">
    """

    for c in concepts:
        cid = c["id"]

        html += f"""
        <div id="view-{cid}" class="concept-view hidden space-y-6">
            <!-- Strategic PM Analysis Card -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-4 p-6 rounded-3xl bg-[#0E131F] border border-slate-800/80 shadow-xl">
                <div class="md:col-span-1 border-b md:border-b-0 md:border-r border-slate-800/80 pb-4 md:pb-0 md:pr-4">
                    <span class="text-[10px] uppercase font-bold text-amber-400 tracking-wider">Бенчмарк Конкурента</span>
                    <h3 class="text-base font-bold text-white mt-1">{c.get('benchmark', 'Global Standard')}</h3>
                    <div class="mt-4">
                        <span class="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Когнитивный Закон</span>
                        <p class="text-xs text-slate-300 mt-1">{c.get('cognitive_law')}</p>
                    </div>
                </div>

                <div class="md:col-span-2 border-b md:border-b-0 md:border-r border-slate-800/80 pb-4 md:pb-0 md:pr-4">
                    <span class="text-[10px] uppercase font-bold text-indigo-400 tracking-wider">Продуктовая Гипотеза (PM Thesis)</span>
                    <p class="text-xs text-slate-200 mt-1 leading-relaxed">{c.get('product_thesis')}</p>
                    <div class="mt-3">
                        <span class="text-[10px] uppercase font-bold text-emerald-400 tracking-wider">Ключевой Клин (Wedge)</span>
                        <p class="text-xs text-emerald-200 mt-0.5 font-medium">{c.get('wedge')}</p>
                    </div>
                </div>

                <div class="md:col-span-1 flex flex-col justify-between">
                    <div>
                        <span class="text-[10px] uppercase font-bold text-slate-400 tracking-wider">Целевая Персона</span>
                        <p class="text-xs text-slate-300 mt-1 font-semibold">{c.get('target_persona')}</p>
                        <div class="mt-2 text-[11px] text-slate-500">
                            Стиль: <span class="text-slate-300">{c.get('theme_name')}</span>
                        </div>
                    </div>
                    <div class="mt-4 pt-4 border-t border-slate-800">
                        <button onclick="chooseConcept('{cid}', '{c.get('name')}')" class="w-full py-2.5 px-4 rounded-xl text-xs font-bold text-slate-900 bg-amber-400 hover:bg-amber-300 shadow-lg active:scale-95 transition">
                            ✅ Выбрать Этот Концепт
                        </button>
                    </div>
                </div>
            </div>

            <!-- Live Interactive UI Facade -->
            <div class="p-1 rounded-3xl border border-slate-800 shadow-2xl">
                {c.get('facade_html', '')}
            </div>
        </div>
        """

    html += f"""
    </main>

    <!-- Selection Confirmation Modal / Bar -->
    <div id="selection-bar" class="fixed bottom-6 inset-x-4 max-w-xl mx-auto rounded-2xl bg-[#141B2D]/95 border border-amber-500/30 shadow-2xl p-4 backdrop-blur-xl flex items-center justify-between z-50">
        <div class="flex items-center space-x-3">
            <span class="text-xl">🚀</span>
            <div>
                <div class="text-xs font-bold text-white">Выбран концепт: <span id="selected-label" class="text-amber-400">Concept</span></div>
                <div class="text-[11px] text-slate-400">Нажмите для подтверждения в консоли или скопируйте ID: <code id="selected-id" class="text-amber-300 font-mono font-bold">concept_3</code></div>
            </div>
        </div>
        <button onclick="confirmSelection()" class="px-4 py-2 rounded-xl text-xs font-bold text-slate-950 bg-amber-400 hover:bg-amber-300 shadow-md active:scale-95 transition">
            Подтвердить
        </button>
    </div>

    <script>
        const concepts = {concepts_json};
        let activeId = '{recommended_id}';

        function selectTab(id) {{
            activeId = id;
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                btn.classList.remove('bg-amber-500/20', 'text-amber-300', 'border', 'border-amber-500/40');
                btn.classList.add('bg-transparent', 'text-slate-400');
            }});
            const activeTab = document.getElementById('tab-' + id);
            if (activeTab) {{
                activeTab.classList.add('bg-amber-500/20', 'text-amber-300', 'border', 'border-amber-500/40');
                activeTab.classList.remove('bg-transparent', 'text-slate-400');
            }}

            document.querySelectorAll('.concept-view').forEach(view => {{
                view.classList.add('hidden');
            }});
            const activeView = document.getElementById('view-' + id);
            if (activeView) {{
                activeView.classList.remove('hidden');
            }}

            const concept = concepts.find(c => c.id === id);
            if (concept) {{
                document.getElementById('selected-label').textContent = concept.name;
                document.getElementById('selected-id').textContent = concept.id;
            }}
        }}

        function chooseConcept(id, name) {{
            selectTab(id);
            alert('Концепт выбран: ' + name + ' (' + id + ').\\n\\nВернитесь в консоль и нажмите Enter или введите этот номер!');
        }}

        function confirmSelection() {{
            alert('Концепт ' + activeId + ' зафиксирован! Передайте его в терминал.');
        }}

        // Initialize default tab
        document.addEventListener('DOMContentLoaded', () => {{
            selectTab(activeId);
        }});
    </script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    logger.info(f"[HITLMatrix] Generated interactive preview matrix at: {output_path}")
    return output_path

def _safe_print(text: str = ""):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode("ascii"))

def prompt_cli_selection(
    concepts: List[Dict[str, Any]],
    prd_spec: Dict[str, Any],
    matrix_path: str,
    default_id: Optional[str] = None
) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Displays the ASCII selection matrix in terminal, opens the browser preview,
    and awaits the developer's decision.
    """
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    def_id = default_id or prd_spec.get("recommended_archetype_id", "concept_3")
    
    _safe_print("\n" + "=" * 76)
    _safe_print(" 🏛️  AI-ZAVOD HUMAN-IN-THE-LOOP: ВЫБОР ИЗ 5 КОНКУРЕНТНЫХ КОНЦЕПТОВ")
    _safe_print("=" * 76)
    _safe_print(f" Продукт: {prd_spec.get('product_name', 'App')} | {prd_spec.get('tagline', '')}")
    _safe_print("-" * 76)

    concept_by_num = {}
    for i, c in enumerate(concepts, start=1):
        cid = c["id"]
        concept_by_num[str(i)] = c
        concept_by_num[cid] = c
        is_rec = " ⭐ [ТОП PM РЕКОМЕНДАЦИЯ]" if cid == def_id else ""
        _safe_print(f" [{i}] {c.get('name')}{is_rec}")
        _safe_print(f"     • Конкурент:  {c.get('benchmark')}")
        _safe_print(f"     • Когниция:   {c.get('cognitive_law')}")
        _safe_print(f"     • УТП/Клин:   {c.get('wedge')}")
        _safe_print(f"     • Персона:    {c.get('target_persona')}")
        _safe_print()

    _safe_print(f" 🌐 Интерактивная матрица с живыми фасадами сохранена:")
    _safe_print(f"    {matrix_path}")

    try:
        webbrowser.open("file://" + os.path.abspath(matrix_path))
        _safe_print("    (Превью автоматически открыто в вашем браузере)")
    except Exception:
        pass

    _safe_print("-" * 76)
    _safe_print(" Введите номер концепта [1-5], либо текстовый комментарий для гибрида,")
    _safe_print(f" либо нажмите [Enter] для подтверждения рекомендации PM ({def_id}):")

    try:
        choice = input(" >>> Выбор [1-5 / гибрид]: ").strip()
    except EOFError:
        choice = ""

    feedback = None
    if not choice:
        selected = next((c for c in concepts if c["id"] == def_id), concepts[0])
    elif choice in concept_by_num:
        selected = concept_by_num[choice]
    else:
        selected = next((c for c in concepts if c["id"] == def_id), concepts[0])
        feedback = choice
        print(f" ℹ️ Зафиксирован гибридный комментарий автора: '{feedback}'")

    print(f" ✅ Утвержден концепт: {selected.get('name')} ({selected.get('id')})")
    print("=" * 76 + "\n")
    return selected, feedback
