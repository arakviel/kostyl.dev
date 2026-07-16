#!/usr/bin/env python3
"""
Генерує зображення для варіантів відповідей тесту.
Читає JSON з питаннями, рендерить кожен варіант через silicon,
створює mapping.json для wayground_add_images.py.
"""
import json
import os
import subprocess
import sys
import requests
import uuid
import hashlib


def get_catbox_userhash():
    """Читає CATBOX_USERHASH з .env."""
    env_dirs = [
        os.path.dirname(os.path.abspath(__file__)),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"),
    ]
    for d in env_dirs:
        env_file = os.path.join(d, ".env")
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            break
    return os.environ.get("CATBOX_USERHASH", "")


def get_wayground_session():
    """Логінимось на Wayground."""
    env_dirs = [
        os.path.dirname(os.path.abspath(__file__)),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "scripts"),
    ]
    for d in env_dirs:
        env_file = os.path.join(d, ".env")
        if os.path.exists(env_file):
            with open(env_file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, _, v = line.partition("=")
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            break

    email = os.environ.get("WAYGROUND_EMAIL", "")
    password = os.environ.get("WAYGROUND_PASSWORD", "")
    if not email or not password:
        return None

    try:
        resp = requests.post(
            "https://wayground.com/_authserver/public/public/v1/auth/login/local",
            json={"username": email, "password": password, "requestId": str(uuid.uuid4())},
            headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0",
                     "Origin": "https://wayground.com"},
            timeout=15,
        )
        sid = resp.cookies.get("_sid")
        if not sid:
            return None
        session = requests.Session()
        session.cookies.set("_sid", sid, domain="wayground.com")
        session.headers.update({"User-Agent": "Mozilla/5.0", "Origin": "https://wayground.com"})
        return session
    except Exception:
        return None


def upload_to_catbox(img_path, userhash):
    """Завантажує PNG на catbox.moe."""
    try:
        with open(img_path, "rb") as f:
            img_data = f.read()
        r = requests.post(
            "https://catbox.moe/user/api.php",
            data={"reqtype": "fileupload", "userhash": userhash},
            files={"fileToUpload": ("image.png", img_data, "image/png")},
            timeout=30,
        )
        url = r.text.strip()
        return url if url.startswith("https://") else None
    except Exception:
        return None


def upload_to_wayground(session, img_path):
    """Завантажує PNG на Wayground S3."""
    try:
        with open(img_path, "rb") as f:
            img_data = f.read()
        r = session.post(
            "https://media.quizizz.com/_mdserver/main/getUploadURL"
            "?destination=quizzes&enableAcceleration=true",
            timeout=15,
        )
        if r.status_code != 200 or not r.json().get("success"):
            return None
        res = r.json()["data"]
        s3 = requests.put(
            res["signedUrl"],
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=img_data,
            timeout=30,
        )
        return res["finalUrl"] if s3.status_code == 200 else None
    except Exception:
        return None


def render_code_to_image(code_text, lang, output_path):
    """Рендерить код через silicon."""
    ext = lang if lang else "txt"
    temp_file = f"/tmp/answer_{os.getpid()}.{ext}"
    try:
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(code_text)
            cmd = [
                "silicon", "--no-window-controls",
                "--theme", "Visual Studio Dark+",
                "--no-round-corner",
                "--pad-horiz", "0", "--pad-vert", "0",
            ]
        if lang:
            cmd.extend(["-l", lang])
        cmd += [temp_file, "-o", output_path]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception as e:
        print(f"  ⚠️ Помилка silicon: {e}")
        return False
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)


def main():
    if len(sys.argv) < 3:
        print("Використання: python3 generate_answer_images.py <json_path> <quiz_id>")
        print("  json_path — шлях до JSON з питаннями")
        print("  quiz_id   — ID тесту на Wayground")
        sys.exit(1)

    json_path = sys.argv[1]
    quiz_id = sys.argv[2]

    with open(json_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    if isinstance(questions, dict):
        for key in questions:
            if isinstance(questions[key], list):
                questions = questions[key]
                break

    # Створюємо папку для зображень
    img_dir = os.path.join(os.path.dirname(json_path) or ".", "answer_images")
    os.makedirs(img_dir, exist_ok=True)

    # Авторизація
    wg_session = get_wayground_session()
    catbox_hash = get_catbox_userhash()

    if wg_session:
        print("🔑 Wayground авторизовано")
    elif catbox_hash:
        print("🔑 Catbox авторизовано")
    else:
        print("❌ Немає авторизації — зображення не завантажаться")
        sys.exit(1)

    mapping = []
    temp_files = []

    for q_idx, q in enumerate(questions):
        q_type = q.get("Question Type", "Multiple Choice")
        if q_type in ("Open-Ended", "Draw", "Fill-in-the-Blank"):
            continue

        print(f"\n[{q_idx}] {q.get('Question Text', '')[:60]}...")

        for opt_idx in range(1, 6):
            opt_key = f"Option {opt_idx}"
            opt_text = q.get(opt_key, "")
            if not opt_text:
                continue

            # Перевіряємо чи є блок коду у варіанті
            import re
            code_match = re.search(r'```(\w*)\n([\s\S]*?)\n```', str(opt_text))
            if not code_match:
                continue

            lang = code_match.group(1) or ""
            code = code_match.group(2)

            print(f"  📝 opt {opt_idx-1}: код ({lang or 'plain'})")

            # Рендеримо
            img_name = f"q{q_idx}_opt{opt_idx-1}.png"
            img_path = os.path.join(img_dir, img_name)

            if not render_code_to_image(code, lang, img_path):
                continue

            temp_files.append(img_path)

            # Завантажуємо
            image_url = None
            if wg_session:
                image_url = upload_to_wayground(wg_session, img_path)
                if image_url:
                    print(f"    🚀 Wayground: {image_url[:60]}...")

            if not image_url and catbox_hash:
                image_url = upload_to_catbox(img_path, catbox_hash)
                if image_url:
                    print(f"    🚀 Catbox: {image_url}")

            if image_url:
                mapping.append({
                    "question_index": q_idx,
                    "option_index": opt_idx - 1,
                    "image_path": image_url,
                })
            else:
                print(f"    ⚠️ Не вдалося завантажити")

    # Зберігаємо mapping
    mapping_path = os.path.join(os.path.dirname(json_path) or ".", "answer_mapping.json")
    with open(mapping_path, "w") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Зображення згенеровано: {len(mapping)} шт")
    print(f"📁 Mapping: {mapping_path}")
    print(f"\nДля застосування запусти:")
    print(f"  python3 scripts/wayground_add_images.py --quiz-id {quiz_id} --mapping {mapping_path}")

    # Прибираємо тимчасові файли
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)


if __name__ == "__main__":
    main()
