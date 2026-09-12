import argparse
import pandas as pd
import json
import os
import sys
import re
import uuid
import subprocess
import requests


def _get_wayground_session() -> requests.Session | None:
    """Логінимось на Wayground для завантаження зображень."""
    # Шукаємо credentials у .env поряд зі скриптом або в scripts/
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

    email    = os.environ.get("WAYGROUND_EMAIL", "")
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


def _upload_to_wayground(session: requests.Session, img_path: str) -> str | None:
    """Завантажує PNG на Wayground S3 і повертає finalUrl."""
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


def _get_catbox_userhash() -> str:
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


def _upload_to_catbox(img_path: str, userhash: str) -> str | None:
    """Завантажує PNG на catbox.moe (постійне зберігання)."""
    try:
        with open(img_path, "rb") as f:
            img_data = f.read()
        payload = {"reqtype": "fileupload", "userhash": userhash}
        r = requests.post(
            "https://catbox.moe/user/api.php",
            data=payload,
            files={"fileToUpload": ("image.png", img_data, "image/png")},
            timeout=30,
        )
        url = r.text.strip()
        return url if url.startswith("https://") else None
    except Exception:
        return None


def _upload_to_litterbox(img_path: str) -> str | None:
    """Fallback: завантажує PNG на litterbox.catbox.moe (72h TTL)."""
    try:
        with open(img_path, "rb") as f:
            img_data = f.read()
        r = requests.post(
            "https://litterbox.catbox.moe/resources/internals/api.php",
            data={"reqtype": "fileupload", "time": "72h"},
            files={"fileToUpload": ("image.png", img_data, "image/png")},
            timeout=30,
        )
        url = r.text.strip()
        return url if url.startswith("https://") else None
    except Exception:
        return None

def process_code_blocks(data):
    # regex to find code blocks: ```lang\ncode\n```
    code_block_pattern = re.compile(r'```(\w*)\n([\s\S]*?)\n```')

    # Ініціалізуємо catbox-хеш для завантаження зображень питань
    catbox_hash = _get_catbox_userhash()
    if catbox_hash:
        print("🔑 Catbox.moe — зображення питань завантажуються постійно")
    else:
        print("⚠️  CATBOX_USERHASH не знайдено — litterbox.catbox.moe (72h TTL)")

    for item in data:
        if not isinstance(item, dict):
            continue

        q_text = item.get("Question Text", "")
        if not q_text:
            continue

        match = code_block_pattern.search(q_text)
        if match:
            lang = match.group(1)
            code_content = match.group(2)

            lang_mapped = lang.lower() if lang else ""
            if lang_mapped in ("csharp", "c#"):
                lang_mapped = "cs"

            print(f"🔍 Знайдено блок коду ({lang if lang else 'plain'}) в питанні: '{q_text[:30]}...'")

            ext = lang_mapped if lang_mapped else "txt"
            temp_code_file = f"temp_code_{os.getpid()}.{ext}"
            temp_img_file  = f"temp_code_{os.getpid()}.png"

            try:
                with open(temp_code_file, "w", encoding="utf-8") as f:
                    f.write(code_content)

                silicon_cmd = [
                    "silicon",
                    "--no-window-controls",
                    "--theme", "Visual Studio Dark+",
                    "--no-round-corner",
                    "--pad-horiz", "0",
                    "--pad-vert", "0",
                ]
                if lang_mapped:
                    silicon_cmd.extend(["-l", lang_mapped])
                silicon_cmd += [temp_code_file, "-o", temp_img_file]

                print("🎨 Рендеринг зображення коду за допомогою silicon...")
                subprocess.run(silicon_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

                image_url = None

                # Спроба 1: catbox.moe (постійне зберігання)
                if catbox_hash:
                    print("🚀 Завантаження на catbox.moe...")
                    image_url = _upload_to_catbox(temp_img_file, catbox_hash)
                    if image_url:
                        print(f"🔗 Зображення завантажено (catbox): {image_url}")

                # Спроба 2: litterbox fallback (72h)
                if not image_url:
                    print("🚀 Fallback: завантаження на litterbox.catbox.moe...")
                    image_url = _upload_to_litterbox(temp_img_file)
                    if image_url:
                        print(f"🔗 Зображення завантажено (litterbox): {image_url}")

                if image_url:
                    item["Image Link"] = image_url
                    item["Question Text"] = code_block_pattern.sub("", q_text).strip()
                else:
                    print("⚠️ Не вдалося завантажити зображення — посилання залишається порожнім")

            except Exception as e:
                print(f"⚠️ Не вдалося обробити блок коду: {e}")

            finally:
                if os.path.exists(temp_code_file):
                    os.remove(temp_code_file)
                if os.path.exists(temp_img_file):
                    os.remove(temp_img_file)

def convert_json_to_xlsx(json_path, xlsx_path):
    columns = [
        "Question Text", "Question Type", "Option 1", "Option 2", 
        "Option 3", "Option 4", "Option 5", "Correct Answer", 
        "Time in seconds", "Image Link", "Answer explanation"
    ]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Якщо JSON це просто словник з одним полем (наприклад {"questions": [...]})
        if isinstance(data, dict):
            # Спроба знайти масив всередині
            for key in data.keys():
                if isinstance(data[key], list):
                    data = data[key]
                    break
                    
        if not isinstance(data, list):
            print(f"❌ Помилка: {json_path} не містить масиву питань.")
            return
            
        process_code_blocks(data)
            
        df = pd.DataFrame(data, columns=columns)
        df = df.astype(object)
        
        # Пост-процесинг для нормалізації даних, якщо AI згенерував їх неточно
        for index, row in df.iterrows():
            q_type = str(row.get('Question Type', '')).strip()
            ans = str(row.get('Correct Answer', ''))
            
            if q_type == 'Multiple Choice':
                m = re.search(r'\d+', ans)
                if m:
                    df.at[index, 'Correct Answer'] = m.group(0)
            elif q_type == 'Checkbox':
                m = re.findall(r'\d+', ans)
                if m:
                    df.at[index, 'Correct Answer'] = ",".join(m)
            elif q_type.lower() == 'fill-in-the-blank':
                df.at[index, 'Question Type'] = 'Fill-in-the-Blank'
                if pd.notna(ans) and str(ans).strip() != "":
                    if pd.isna(row.get('Option 1')) or str(row.get('Option 1')).strip() == "":
                        df.at[index, 'Option 1'] = ans
                df.at[index, 'Correct Answer'] = ""
                for opt in ['Option 2', 'Option 3', 'Option 4', 'Option 5']:
                    df.at[index, opt] = ""
        
        # Створюємо директорію для файлу, якщо її немає
        os.makedirs(os.path.dirname(os.path.abspath(xlsx_path)), exist_ok=True)
        
        df.to_excel(xlsx_path, index=False, engine='openpyxl')
        print(f"✅ Успішно створено {xlsx_path} ({len(data)} питань).")
        
    except Exception as e:
        print(f"❌ Помилка під час обробки {json_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Конвертер JSON тестів у формат Wayground (XLSX).")
    parser.add_argument("input", help="Шлях до вхідного JSON файлу або папки з JSON файлами")
    parser.add_argument("-o", "--output", help="Шлях до вихідного XLSX файлу або папки (опціонально)", default=None)
    
    args = parser.parse_args()
    
    # Якщо передано файл
    if os.path.isfile(args.input):
        if not args.input.endswith('.json'):
            print("Помилка: Вхідний файл має бути формату .json")
            sys.exit(1)
            
        out_path = args.output
        if not out_path:
            out_path = args.input.rsplit('.', 1)[0] + '.xlsx'
        elif os.path.isdir(out_path):
            out_path = os.path.join(out_path, os.path.basename(args.input).rsplit('.', 1)[0] + '.xlsx')
            
        convert_json_to_xlsx(args.input, out_path)
        
    # Якщо передано папку
    elif os.path.isdir(args.input):
        out_dir = args.output if args.output else args.input
        os.makedirs(out_dir, exist_ok=True)
        
        json_files = [f for f in os.listdir(args.input) if f.endswith('.json')]
        if not json_files:
            print(f"У папці '{args.input}' не знайдено JSON файлів.")
            return
            
        print(f"Знайдено {len(json_files)} JSON файлів. Починаємо конвертацію...")
        for j_file in json_files:
            in_path = os.path.join(args.input, j_file)
            out_path = os.path.join(out_dir, j_file.rsplit('.', 1)[0] + '.xlsx')
            convert_json_to_xlsx(in_path, out_path)
    else:
        print(f"Помилка: Шляху '{args.input}' не існує.")
        sys.exit(1)

if __name__ == "__main__":
    main()
