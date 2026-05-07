#!/usr/bin/env python3
"""
Скрипт для автоматичної вставки зображень у markdown файли за маркерами.

Використання:
1. Додайте маркери у markdown файл:
   <!-- IMAGE: kubernetes architecture -->
   
2. Запустіть скрипт:
   python insert_images.py content/07.tools/02.kubernetes/01.why-kubernetes.md

Скрипт знайде всі маркери та вставить відповідні зображення з папки.
"""

import os
import re
import sys
import argparse


def get_image_dir_from_md_path(md_path):
    """Визначає папку з зображеннями для даного markdown файлу."""
    normalized_path = os.path.normpath(md_path)
    parts = normalized_path.split(os.sep)

    if "content" in parts:
        content_idx = parts.index("content")
        rel_parts = parts[content_idx + 1 :]
    else:
        rel_parts = parts[-3:] if len(parts) >= 3 else parts

    cleaned_parts = []
    for part in rel_parts:
        if part.endswith(".md"):
            part = part[:-3]
        cleaned_part = re.sub(r"^\d+\.", "", part)
        cleaned_parts.append(cleaned_part)

    return os.path.join("public", "images", *cleaned_parts)


def find_image_markers(content):
    """Знаходить всі маркери IMAGE у тексті."""
    pattern = r'<!--\s*IMAGE:\s*(.+?)\s*-->'
    matches = re.finditer(pattern, content)
    return [(m.group(0), m.group(1), m.start(), m.end()) for m in matches]


def get_next_image_number(image_dir):
    """Визначає наступний доступний номер зображення."""
    if not os.path.exists(image_dir):
        return 1
    
    files = os.listdir(image_dir)
    numbers = []
    for f in files:
        match = re.match(r'^(\d+)\.', f)
        if match:
            numbers.append(int(match.group(1)))
    
    return max(numbers) + 1 if numbers else 1


def get_images_in_dir(image_dir):
    """Повертає список всіх зображень у папці, відсортованих за номером."""
    if not os.path.exists(image_dir):
        return []
    
    images = []
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif', '.webp')):
            match = re.match(r'^(\d+)\.', filename)
            if match:
                num = int(match.group(1))
                images.append((num, filename))
    
    images.sort(key=lambda x: x[0])
    return images


def insert_images_into_markdown(md_path, dry_run=False):
    """Вставляє зображення у markdown файл за маркерами."""
    
    if not os.path.exists(md_path):
        print(f"❌ Файл не знайдено: {md_path}")
        return False
    
    # Читаємо вміст файлу
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Знаходимо маркери
    markers = find_image_markers(content)
    
    if not markers:
        print(f"ℹ️  Маркерів IMAGE не знайдено у файлі {md_path}")
        return False
    
    print(f"📄 Файл: {md_path}")
    print(f"🔍 Знайдено {len(markers)} маркерів IMAGE")
    
    # Визначаємо папку з зображеннями
    image_dir = get_image_dir_from_md_path(md_path)
    print(f"📁 Папка зображень: {image_dir}")
    
    # Отримуємо список зображень
    images = get_images_in_dir(image_dir)
    
    if not images:
        print(f"⚠️  Зображень не знайдено у папці {image_dir}")
        print(f"💡 Спочатку завантажте зображення за допомогою fetch_images.py")
        return False
    
    print(f"🖼️  Доступно {len(images)} зображень: {', '.join([f[1] for f in images])}")
    
    # Створюємо мапу: маркер -> зображення
    # Використовуємо наступне доступне зображення для кожного маркера
    image_index = 0
    replacements = []
    
    for marker_full, marker_text, start, end in markers:
        if image_index >= len(images):
            print(f"⚠️  Недостатньо зображень для всіх маркерів (потрібно {len(markers)}, є {len(images)})")
            break
        
        img_num, img_filename = images[image_index]
        
        # Формуємо шлях для markdown
        rel_path = image_dir.replace("public/", "/")
        img_path = f"{rel_path}/{img_filename}"
        
        # Формуємо markdown для зображення
        img_markdown = f"![{marker_text}]({img_path}){{.diagram-img}}"
        
        replacements.append({
            'marker': marker_full,
            'marker_text': marker_text,
            'image': img_filename,
            'markdown': img_markdown
        })
        
        image_index += 1
    
    # Виводимо план заміни
    print("\n" + "=" * 70)
    print("📋 ПЛАН ВСТАВКИ:")
    print("=" * 70)
    for i, r in enumerate(replacements, 1):
        print(f"{i}. Маркер: <!-- IMAGE: {r['marker_text']} -->")
        print(f"   Зображення: {r['image']}")
        print(f"   Вставка: {r['markdown']}")
        print()
    
    if dry_run:
        print("🔍 Режим перегляду (dry-run). Зміни не застосовано.")
        return True
    
    # Виконуємо заміну
    new_content = content
    for r in reversed(replacements):  # Йдемо з кінця, щоб не зламати позиції
        new_content = new_content.replace(r['marker'], r['markdown'])
    
    # Зберігаємо файл
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Зображення успішно вставлено у файл!")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Автоматична вставка зображень у markdown файли за маркерами.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Приклади використання:

1. Додайте маркери у ваш markdown файл:
   
   ## Архітектура Kubernetes
   <!-- IMAGE: kubernetes architecture -->
   
   Kubernetes складається з...

2. Завантажте зображення:
   python fetch_images.py "kubernetes architecture" --md content/k8s.md

3. Вставте зображення у файл:
   python insert_images.py content/k8s.md

4. Перегляд без змін (dry-run):
   python insert_images.py content/k8s.md --dry-run
        """
    )
    parser.add_argument("markdown_file", type=str, help="Шлях до markdown файлу")
    parser.add_argument("--dry-run", action="store_true", help="Показати план без застосування змін")
    
    args = parser.parse_args()
    
    success = insert_images_into_markdown(args.markdown_file, args.dry_run)
    sys.exit(0 if success else 1)
