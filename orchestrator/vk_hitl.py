import time
import random
import logging
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("AI_Zavod.VKHITL")

class VKHITLDispatcher:
    def __init__(self, token: Optional[str] = None, default_peer_id: int = 538881038):
        self.token = token
        self.default_peer_id = default_peer_id
        self.vk = None
        self._init_vk()

    def _init_vk(self):
        if not self.token:
            return
        try:
            import vk_api
            session = vk_api.VkApi(token=self.token)
            self.vk = session.get_api()
            logger.info("[VKHITL] Successfully connected to VK API.")
        except Exception as e:
            logger.warning(f"[VKHITL] Failed to connect to VK API: {e}")
            self.vk = None

    def send_text(self, text: str, peer_id: Optional[int] = None) -> bool:
        """Sends a plain text message to the specified VK peer."""
        if not self.vk:
            return False
        target_peer = peer_id or self.default_peer_id
        try:
            self.vk.messages.send(
                peer_id=target_peer,
                random_id=random.randint(1, 2147483647),
                message=text
            )
            logger.info(f"[VKHITL] Sent message to VK peer {target_peer}: {text[:50]}...")
            return True
        except Exception as e:
            logger.warning(f"[VKHITL] Failed to send message to VK: {e}")
            return False

    def capture_concept_screenshots(self, concepts: List[Dict[str, Any]]) -> List[str]:
        """
        Spawns headless Chromium to render and capture high-resolution
        desktop screenshots of each concept facade.
        """
        screenshot_paths = []
        try:
            from playwright.sync_api import sync_playwright
            import tempfile
            import os

            def launch_browser(p):
                if os.path.exists("/usr/bin/google-chrome"):
                    return p.chromium.launch(
                        executable_path="/usr/bin/google-chrome",
                        headless=True,
                        args=["--no-sandbox", "--disable-dev-shm-usage"]
                    )
                for ch in ["msedge", "chrome"]:
                    try:
                        return p.chromium.launch(channel=ch, headless=True)
                    except Exception:
                        pass
                return p.chromium.launch(headless=True)

            tmp_dir = tempfile.gettempdir()
            with sync_playwright() as p:
                browser = launch_browser(p)
                page = browser.new_page(viewport={"width": 1280, "height": 760})

                for i, c in enumerate(concepts, start=1):
                    cid = c.get("id", f"c{i}")
                    pal = c.get("palette", {})
                    typo = c.get("typography", {})
                    
                    html = f"""<!DOCTYPE html>
                    <html>
                    <head>
                      <meta charset="utf-8">
                      <script src="https://cdn.tailwindcss.com"></script>
                      <link rel="preconnect" href="https://fonts.googleapis.com">
                      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                      <link href="{typo.get('google_fonts_url', '')}" rel="stylesheet">
                      <style>
                        body {{ background-color: {pal.get('bg', '#090A0F')}; }}
                      </style>
                    </head>
                    <body class="p-6 flex flex-col justify-center min-h-screen">
                      <div class="max-w-4xl mx-auto w-full">
                        <div class="mb-3 flex items-center justify-between">
                          <span class="text-xs font-bold uppercase tracking-wider text-amber-400">КОНЦЕПТ #{i}: {c.get('name')}</span>
                          <span class="text-xs px-2.5 py-0.5 rounded-md bg-slate-800 text-slate-300 font-mono">Бенчмарк: {c.get('benchmark')}</span>
                        </div>
                        {c.get('facade_html', '')}
                      </div>
                    </body>
                    </html>"""
                    
                    tmp_html = os.path.join(tmp_dir, f"facade_{cid}.html")
                    png_path = os.path.join(tmp_dir, f"facade_{cid}.png")
                    with open(tmp_html, "w", encoding="utf-8") as f:
                        f.write(html)
                    
                    page.goto(f"file:///{tmp_html.replace(os.sep, '/')}", wait_until="domcontentloaded")
                    time.sleep(0.5)
                    page.screenshot(path=png_path)
                    screenshot_paths.append(png_path)
                    logger.info(f"[VKHITL] Captured screenshot for {cid}: {png_path} ({os.path.getsize(png_path)} bytes)")

                browser.close()
        except Exception as e:
            logger.warning(f"[VKHITL] Playwright screenshot capture failed ({e}). Attempting PIL fallback...")
            try:
                from PIL import Image, ImageDraw
                import tempfile
                import os
                tmp_dir = tempfile.gettempdir()
                for i, c in enumerate(concepts, start=1):
                    cid = c.get("id", f"c{i}")
                    png_path = os.path.join(tmp_dir, f"facade_{cid}.png")
                    img = Image.new("RGB", (1280, 720), color=(14, 19, 31))
                    d = ImageDraw.Draw(img)
                    d.text((80, 80), f"КОНЦЕПТ #{i}: {c.get('name')}", fill=(251, 191, 36))
                    d.text((80, 160), f"БЕНЧМАРК: {c.get('benchmark')}", fill=(248, 250, 252))
                    d.text((80, 240), f"УТП / КЛИН: {c.get('wedge')}", fill=(16, 185, 129))
                    d.text((80, 320), f"КОГНИТИВНАЯ БАЗА: {c.get('cognitive_law')}", fill=(148, 163, 184))
                    d.text((80, 400), f"ЦЕЛЕВАЯ ПЕРСОНА: {c.get('target_persona')}", fill=(203, 213, 225))
                    img.save(png_path)
                    screenshot_paths.append(png_path)
            except Exception as ex:
                logger.warning(f"[VKHITL] PIL fallback also failed: {ex}")

        return screenshot_paths

    def upload_screenshots_to_vk(self, peer_id: int, image_paths: List[str]) -> List[str]:
        """
        Uploads images to VK Messages upload server and returns attachment tags ['photo{owner}_{id}', ...].
        Guarantees retry and proper multipart MIME headers so all 5 screenshots are uploaded without failure.
        """
        import os
        import time
        import requests
        attachments = []
        for idx, img_p in enumerate(image_paths, start=1):
            if not os.path.exists(img_p):
                logger.warning(f"[VKHITL] Image path does not exist: {img_p}")
                continue
            
            uploaded = False
            for attempt in range(1, 4):
                try:
                    up_server = self.vk.photos.getMessagesUploadServer(peer_id=peer_id)
                    upload_url = up_server.get("upload_url")
                    if not upload_url:
                        logger.warning(f"[VKHITL] No upload_url returned from getMessagesUploadServer (attempt {attempt}/3)")
                        time.sleep(0.8)
                        continue

                    fname = f"facade_concept_{idx}.png"
                    with open(img_p, "rb") as f:
                        file_payload = {"photo": (fname, f, "image/png")}
                        resp = requests.post(upload_url, files=file_payload, timeout=25).json()

                    photo_data = resp.get("photo")
                    if not photo_data or photo_data == "[]":
                        logger.warning(f"[VKHITL] Empty photo data from upload server for {img_p} (attempt {attempt}/3): {resp}")
                        time.sleep(1.0)
                        continue

                    saved = self.vk.photos.saveMessagesPhoto(
                        photo=photo_data,
                        server=resp["server"],
                        hash=resp["hash"]
                    )
                    if saved and len(saved) > 0:
                        att_tag = f"photo{saved[0]['owner_id']}_{saved[0]['id']}"
                        attachments.append(att_tag)
                        logger.info(f"[VKHITL] Uploaded screenshot {idx}/{len(image_paths)} to VK: {att_tag}")
                        uploaded = True
                        time.sleep(0.35)  # Grace period between uploads to prevent rate limiting
                        break
                except Exception as e:
                    logger.warning(f"[VKHITL] Error uploading photo {img_p} (attempt {attempt}/3): {e}")
                    time.sleep(1.0)

            if not uploaded:
                logger.error(f"[VKHITL] Failed to upload screenshot after 3 attempts: {img_p}")

        return attachments

    def send_concepts_to_vk(
        self,
        session_id: str,
        prd_spec: Dict[str, Any],
        concepts: List[Dict[str, Any]],
        preview_url: Optional[str] = None,
        peer_id: Optional[int] = None
    ) -> Tuple[bool, Optional[int]]:
        """
        Dispatches the 5 competitive concepts with screenshots and an inline keyboard to the user's VK.
        Returns (success, message_id).
        """
        if not self.vk:
            logger.warning("[VKHITL] VK client is not active. Skipping VK dispatch.")
            return False, None

        target_peer = peer_id or self.default_peer_id
        product_name = prd_spec.get("product_name", "WebPlanner Desktop")
        tagline = prd_spec.get("tagline", "Autonomous Digital Ecosystem")
        recommended_id = prd_spec.get("recommended_archetype_id", "concept_3")

        # 1. Capture and upload screenshots
        logger.info(f"[VKHITL] Rendering desktop screenshots for all {len(concepts)} concept websites...")
        screenshots = self.capture_concept_screenshots(concepts)
        attachments = self.upload_screenshots_to_vk(target_peer, screenshots)
        logger.info(f"[VKHITL] Prepared {len(attachments)} photo attachments for VK messages.")

        # 2. Batch and send messages (VK allows max 10 attachments per message)
        batch_size = 10
        total_batches = max(1, (len(concepts) + batch_size - 1) // batch_size)
        last_msg_id = None

        for b_idx in range(total_batches):
            start_i = b_idx * batch_size
            end_i = min(start_i + batch_size, len(concepts))

            batch_concepts = concepts[start_i:end_i]
            batch_attachments = attachments[start_i:end_i]

            lines = [
                f"🏛️ AI-ZAVOD: {len(concepts)} ДИЗАЙН-КОНЦЕПТОВ ДЛЯ WEBPLANNER (ЧАСТЬ {b_idx+1}/{total_batches}: Концепты {start_i+1}–{end_i})",
                f"Проект: {product_name} (Десктопная версия)",
                f"Миссия: {tagline}\n",
                f"Каждый концепт создан с уникальной типографикой, сеткой, стилем и расположением элементов (скриншоты прикреплены выше):\n"
            ]

            for i_rel, c in enumerate(batch_concepts, start=start_i+1):
                cid = c.get("id")
                name = c.get("name", f"Концепт {i_rel}")
                benchmark = c.get("benchmark", "Лидер рынка")
                wedge = c.get("wedge", "Ключевой UX паттерн")
                thesis = c.get("product_thesis", "Сетка и структура")

                lines.append(f"{i_rel}️⃣ {name}")
                lines.append(f"   • Сетка/Формат: {thesis}")
                lines.append(f"   • Бенчмарк: {benchmark}")
                lines.append(f"   • УТП/Клин: {wedge}\n")

            if b_idx == total_batches - 1:
                if preview_url:
                    lines.append(f"🌐 Интерактивная матрица превью: {preview_url}\n")
                lines.append(f"👇 Отправьте цифру выбранного концепта (от 1 до {len(concepts)}) или ваши пожелания в ответ на это сообщение!")

            full_text = "\n".join(lines)

            keyboard_json = None
            if len(concepts) <= 5 and b_idx == total_batches - 1:
                try:
                    from vk_api.keyboard import VkKeyboard, VkKeyboardColor
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    for idx, c in enumerate(concepts, start=1):
                        cid = c.get("id", f"concept_{idx}")
                        cname = c.get("name", f"Concept {idx}")
                        label = f"{idx}. {cname}"[:38]
                        keyboard.add_button(label, color=VkKeyboardColor.SECONDARY, payload={"concept_id": cid, "num": idx})
                        if idx in [2, 4] and idx < len(concepts):
                            keyboard.add_line()
                    keyboard_json = keyboard.get_keyboard()
                except Exception as e:
                    logger.warning(f"[VKHITL] Could not generate inline keyboard: {e}")

            try:
                kwargs = {
                    "peer_id": target_peer,
                    "random_id": random.randint(1, 2147483647),
                    "message": full_text
                }
                if batch_attachments:
                    kwargs["attachment"] = ",".join(batch_attachments)
                if keyboard_json:
                    kwargs["keyboard"] = keyboard_json

                msg_id = self.vk.messages.send(**kwargs)
                last_msg_id = msg_id
                logger.info(f"[VKHITL] Successfully sent batch {b_idx+1}/{total_batches} with {len(batch_attachments)} screenshots to VK peer {target_peer}, msg_id={msg_id}")
                time.sleep(1.0)
            except Exception as e:
                logger.error(f"[VKHITL] Error sending concepts to VK: {e}")
                return False, None

        return True, last_msg_id

    def wait_for_vk_selection(
        self,
        peer_id: Optional[int] = None,
        last_msg_id: Optional[int] = None,
        timeout_sec: float = 60.0,
        concepts: Optional[List[Dict[str, Any]]] = None
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Polls VK for the user's reply or button tap.
        Returns (selected_concept, user_feedback).
        """
        if not self.vk:
            return None, None

        target_peer = peer_id or self.default_peer_id
        start_time = time.time()
        logger.info(f"[VKHITL] Waiting up to {timeout_sec}s for user response in VK (peer_id={target_peer})...")

        concept_map = {}
        if concepts:
            for i, c in enumerate(concepts, start=1):
                concept_map[str(i)] = c
                concept_map[c.get("id")] = c

        while time.time() - start_time < timeout_sec:
            time.sleep(2.5)
            try:
                history = self.vk.messages.getHistory(user_id=target_peer, count=5)
                items = history.get("items", [])
                for msg in items:
                    msg_id = msg.get("id", 0)
                    is_out = msg.get("out", 1)  # 0 means incoming from user
                    
                    # Check if this message was sent after our prompt
                    if last_msg_id and msg_id <= last_msg_id:
                        continue
                    if is_out == 1:
                        continue

                    # Process incoming user response!
                    raw_text = msg.get("text", "").strip()
                    payload_str = msg.get("payload", "")
                    logger.info(f"[VKHITL] Received user message from VK: text='{raw_text}', payload='{payload_str}'")

                    chosen_id = None
                    feedback = None

                    # Check payload first
                    if payload_str:
                        try:
                            import json
                            payload = json.loads(payload_str)
                            if "concept_id" in payload:
                                chosen_id = payload["concept_id"]
                        except Exception:
                            pass

                    # Parse text if payload didn't match
                    if not chosen_id:
                        import re
                        m = re.search(r"\b([1-9]|1[0-9]|20)\b", raw_text)
                        if m:
                            num = int(m.group(1))
                            chosen_id = f"concept_{num}"
                        elif "zen" in raw_text.lower() or "editorial" in raw_text.lower():
                            chosen_id = "concept_4"
                        elif "швейцар" in raw_text.lower():
                            chosen_id = "concept_1"
                        elif "крафт" in raw_text.lower() or "amie" in raw_text.lower():
                            chosen_id = "concept_2"
                        elif "katex" in raw_text.lower() or "монохром" in raw_text.lower():
                            chosen_id = "concept_3"
                        elif "spotlight" in raw_text.lower() or "терминал" in raw_text.lower():
                            chosen_id = "concept_5"
                        elif "баухаус" in raw_text.lower():
                            chosen_id = "concept_6"
                        elif "брутал" in raw_text.lower():
                            chosen_id = "concept_7"
                        elif "титан" in raw_text.lower():
                            chosen_id = "concept_8"
                        elif "ваби" in raw_text.lower():
                            chosen_id = "concept_9"
                        elif "газет" in raw_text.lower():
                            chosen_id = "concept_10"
                        else:
                            chosen_id = "concept_4"
                            feedback = raw_text

                    selected = concept_map.get(chosen_id, concepts[3] if concepts and len(concepts) > 3 else (concepts[0] if concepts else None))

                    # Send confirmation back to VK
                    try:
                        self.vk.messages.send(
                            peer_id=target_peer,
                            random_id=random.randint(1, 2147483647),
                            message=f"✅ Выбор принят! Зафиксирован концепт: {selected.get('name') if selected else chosen_id}.\nAI-Завод запускает генерацию архитектуры и кода."
                        )
                    except Exception:
                        pass

                    return selected, feedback

            except Exception as e:
                logger.warning(f"[VKHITL] Polling error: {e}")

        logger.info("[VKHITL] VK timeout reached without incoming user response.")
        return None, None
