#!/usr/bin/env python3
import os
import re
import sys
import argparse
import requests
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO

# Спробуємо імпортувати ddgs. Якщо його немає, дамо інструкцію зі встановлення.
try:
    from ddgs import DDGS
except ImportError:
    print("Помилка: Бібліотека 'ddgs' не встановлена.", file=sys.stderr)
    print("Будь ласка, встановіть її за допомогою команди:", file=sys.stderr)
    print("pip install ddgs requests pillow", file=sys.stderr)
    sys.exit(1)


def sanitize_filename(name):
    """Очищує ім'я файлу від заборонених символів."""
    return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip()


def get_image_dir_from_md_path(md_path):
    """
    Аналізує шлях до markdown файлу за правилами prompt.md та повертає шлях
    до папки із зображеннями відносно кореня проекту (public/images/...).
    Наприклад:
      content/12.html-css/05.html-forms.md -> public/images/html-css/html-forms
    """
    normalized_path = os.path.normpath(md_path)
    parts = normalized_path.split(os.sep)

    if "content" in parts:
        content_idx = parts.index("content")
        rel_parts = parts[content_idx + 1 :]
    else:
        # Якщо папка content не знайдена в шляху, використовуємо останні частини шляху
        rel_parts = parts[-3:] if len(parts) >= 3 else parts

    cleaned_parts = []
    for part in rel_parts:
        if part.endswith(".md"):
            part = part[:-3]  # видаляємо розширення
        # Видаляємо числові префікси, наприклад "12.html-css" -> "html-css"
        cleaned_part = re.sub(r"^\d+\.", "", part)
        cleaned_parts.append(cleaned_part)

    return os.path.join("public", "images", *cleaned_parts)


def get_next_image_number(folder):
    """Визначає наступний номер зображення в папці."""
    if not os.path.exists(folder):
        return 1
    
    existing_files = os.listdir(folder)
    numbers = []
    for filename in existing_files:
        match = re.match(r"^(\d+)\.", filename)
        if match:
            numbers.append(int(match.group(1)))
    
    return max(numbers) + 1 if numbers else 1


def get_image_info(url, headers):
    """Отримує інформацію про зображення (розмір, формат) без повного завантаження."""
    try:
        response = requests.get(url, headers=headers, timeout=10, stream=True)
        response.raise_for_status()
        
        # Читаємо тільки початок файлу для визначення розміру
        content_type = response.headers.get("content-type", "")
        
        # Для SVG не можемо визначити розмір, але це пріоритетний формат
        if "svg" in content_type:
            return {"width": 9999, "height": 9999, "format": "svg", "size": int(response.headers.get("content-length", 0))}
        
        # Для растрових зображень використовуємо PIL
        img_data = BytesIO()
        for chunk in response.iter_content(8192):
            img_data.write(chunk)
            if img_data.tell() > 50000:  # Читаємо максимум 50KB для визначення розміру
                break
        
        img_data.seek(0)
        img = Image.open(img_data)
        
        return {
            "width": img.width,
            "height": img.height,
            "format": img.format.lower() if img.format else "unknown",
            "size": int(response.headers.get("content-length", 0))
        }
    except Exception as e:
        return None


def score_image(info, url):
    """Оцінює якість зображення за різними критеріями."""
    if not info:
        return 0
    
    score = 0
    
    # Формат (SVG найкращий для діаграм)
    format_scores = {"svg": 100, "png": 80, "jpg": 60, "jpeg": 60, "webp": 70, "gif": 40}
    score += format_scores.get(info["format"], 30)
    
    # Розмір зображення (оптимально 1000-2000px по ширині)
    width = info["width"]
    if width >= 1000 and width <= 2000:
        score += 50
    elif width >= 800 and width < 1000:
        score += 40
    elif width > 2000 and width <= 3000:
        score += 35
    elif width < 800:
        score += 10  # Занадто маленькі
    
    # Пріоритет офіційним та якісним технічним джерелам
    priority_domains = [
        # Офіційні документації
        "kubernetes.io", "docker.com", "github.com", "gitlab.com",
        # Хмарні провайдери
        "microsoft.com", "azure.com", "google.com", "aws.amazon.com", "cloud.google.com",
        # Технічні блоги та ресурси
        "medium.com", "dev.to", "digitalocean.com", "redhat.com", "ibm.com",
        "nginx.com", "apache.org", "mozilla.org", "cloudflare.com",
        # Освітні платформи
        "freecodecamp.org", "codecademy.com", "udemy.com", "pluralsight.com",
        # Технічні видання
        "infoq.com", "dzone.com", "hackernoon.com", "towards.dev",
        # Спеціалізовані ресурси
        "spacelift.io", "k21academy.com", "phoenixnap.com", "ionos.com",
        "simform.com", "nops.io", "rancher.com", "cncf.io",
        # Блоги компаній
        "atlassian.com", "jetbrains.com", "stackoverflow.com", "stackexchange.com"
    ]
    if any(domain in url for domain in priority_domains):
        score += 30
    
    # Бонус за великі файли (більше деталей)
    if info["size"] > 100000:  # > 100KB
        score += 10
    
    return score


def download_image(url, folder, filename):
    """Завантажує зображення за URL та зберігає у вказану папку."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        parsed_url = urlparse(url)
        ext = os.path.splitext(parsed_url.path)[1]
        if not ext or len(ext) > 5:
            content_type = response.headers.get("content-type", "")
            if "image/jpeg" in content_type:
                ext = ".jpg"
            elif "image/png" in content_type:
                ext = ".png"
            elif "image/svg+xml" in content_type:
                ext = ".svg"
            elif "image/gif" in content_type:
                ext = ".gif"
            elif "image/webp" in content_type:
                ext = ".webp"
            else:
                ext = ".jpg"

        full_filename = f"{filename}{ext}"
        filepath = os.path.join(folder, full_filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath, ext
    except Exception as e:
        print(f" Не вдалося завантажити {url}: {e}", file=sys.stderr)
        return None, None


def fetch_and_download(query, limit=10, output_dir=None, md_path=None, interactive=False, min_width=800):
    """Шукає картинки через DuckDuckGo та завантажує їх."""
    # Визначаємо папку завантаження
    if md_path:
        target_dir = get_image_dir_from_md_path(md_path)
        print(f"📁 Шлях визначено автоматично за md-файлом: {target_dir}")
    elif output_dir:
        target_dir = output_dir
    else:
        target_dir = "downloads"

    os.makedirs(target_dir, exist_ok=True)
    print(f"🔍 Шукаємо зображення за запитом: '{query}' (ліміт: {limit})...")

    try:
        with DDGS() as ddgs:
            # Збільшуємо ліміт пошуку для кращого вибору
            search_limit = limit * 3 if interactive else limit * 2
            results = ddgs.images(
                query=query,
                region="wt-wt",
                safesearch="moderate",
                max_results=search_limit,
            )

            if not results:
                print("❌ Зображень за таким запитом не знайдено.")
                return []

            print(f"✅ Знайдено {len(results)} зображень. Аналізую якість...")

            # Аналізуємо та оцінюємо зображення
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            
            scored_images = []
            for idx, item in enumerate(results):
                img_url = item.get("image")
                print(f"  [{idx+1}/{len(results)}] Аналізую: {img_url[:60]}...")
                
                info = get_image_info(img_url, headers)
                if info and info["width"] >= min_width:
                    score = score_image(info, img_url)
                    scored_images.append({
                        "url": img_url,
                        "info": info,
                        "score": score,
                        "title": item.get("title", "")
                    })
                    print(f"    ✓ {info['width']}x{info['height']} {info['format'].upper()} | Оцінка: {score}")
                else:
                    print(f"    ✗ Пропущено (занадто мале або недоступне)")

            if not scored_images:
                print("❌ Не знайдено якісних зображень за критеріями.")
                return []

            # Сортуємо за оцінкою
            scored_images.sort(key=lambda x: x["score"], reverse=True)

            # Інтерактивний вибір або автоматичне завантаження
            if interactive:
                print("\n" + "=" * 70)
                print("🎯 ТОП ЗОБРАЖЕНЬ (відсортовано за якістю):")
                print("=" * 70)
                for idx, img in enumerate(scored_images[:limit], 1):
                    print(f"{idx}. Оцінка: {img['score']} | {img['info']['width']}x{img['info']['height']} | {img['info']['format'].upper()}")
                    print(f"   URL: {img['url'][:80]}")
                    print(f"   Назва: {img['title'][:80]}")
                    print()
                
                selected = input(f"Введіть номери для завантаження (через кому, наприклад: 1,2,3) або Enter для топ-{min(3, len(scored_images))}: ").strip()
                
                if selected:
                    indices = [int(x.strip()) - 1 for x in selected.split(",") if x.strip().isdigit()]
                    selected_images = [scored_images[i] for i in indices if 0 <= i < len(scored_images)]
                else:
                    selected_images = scored_images[:min(3, len(scored_images))]
            else:
                # Автоматично беремо топ-N
                selected_images = scored_images[:limit]

            # Завантажуємо вибрані зображення
            downloaded_paths = []
            start_number = get_next_image_number(target_dir)
            
            print(f"\n📥 Завантажую {len(selected_images)} зображень...")
            for idx, img in enumerate(selected_images):
                img_number = start_number + idx
                filename = f"{img_number:02d}"
                
                print(f"  [{idx+1}/{len(selected_images)}] Завантаження: {img['url'][:60]}...")
                saved_path, ext = download_image(img["url"], target_dir, filename)
                
                if saved_path:
                    downloaded_paths.append(saved_path)
                    print(f"    ✅ Збережено: {os.path.basename(saved_path)}")

            # Виводимо готові посилання у форматі markdown
            if downloaded_paths:
                print("\n" + "=" * 70)
                print("📋 ГОТОВІ ВСТАВКИ ДЛЯ MARKDOWN:")
                print("=" * 70)
                for path in downloaded_paths:
                    # Отримуємо шлях відносно папки 'public'
                    parts = path.split(os.sep)
                    if "public" in parts:
                        pub_idx = parts.index("public")
                        md_img_path = "/" + "/".join(parts[pub_idx + 1 :])
                    else:
                        md_img_path = "/" + path.replace(os.sep, "/")

                    print(f"![{query}]({md_img_path}){{.diagram-img}}")
                print("=" * 70 + "\n")
                
                return downloaded_paths

    except Exception as e:
        print(f"❌ Помилка під час пошуку: {e}", file=sys.stderr)
        return []


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Скрипт для пошуку та завантаження якісних зображень.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:
  # Автоматичне завантаження топ-3 зображень
  python fetch_images.py "kubernetes architecture" --md content/07.tools/02.kubernetes/01.why-kubernetes.md
  
  # Інтерактивний вибір з 10 варіантів
  python fetch_images.py "docker compose" --md content/docker.md -l 10 -i
  
  # Завантаження з мінімальною шириною 1200px
  python fetch_images.py "kubernetes diagram" --md content/k8s.md --min-width 1200
        """
    )
    parser.add_argument("query", type=str, help="Пошуковий запит (наприклад, 'kubernetes architecture')")
    parser.add_argument("-l", "--limit", type=int, default=3, help="Кількість зображень для завантаження (типово 3)")
    parser.add_argument("-o", "--output", type=str, default=None, help="Папка для збереження (використовується якщо немає --md)")
    parser.add_argument("--md", type=str, default=None, help="Шлях до md-файлу, щоб автоматично побудувати структуру папок")
    parser.add_argument("-i", "--interactive", action="store_true", help="Інтерактивний режим вибору зображень")
    parser.add_argument("--min-width", type=int, default=800, help="Мінімальна ширина зображення в пікселях (типово 800)")

    args = parser.parse_args()
    fetch_and_download(args.query, args.limit, args.output, args.md, args.interactive, args.min_width)
