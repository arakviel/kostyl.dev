import argparse
import pandas as pd
import json
import os
import sys
import re
import subprocess

def process_code_blocks(data):
    # regex to find code blocks: ```lang\ncode\n```
    code_block_pattern = re.compile(r'```(\w*)\n([\s\S]*?)\n```')
    
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
            
            print(f"🔍 Знайдено блок коду ({lang if lang else 'plain'}) в питанні: '{q_text[:30]}...'")
            
            # 1. Створити тимчасовий файл для коду
            ext = lang if lang else "txt"
            temp_code_file = f"temp_code_{os.getpid()}.{ext}"
            temp_img_file = f"temp_code_{os.getpid()}.png"
            
            try:
                with open(temp_code_file, "w", encoding="utf-8") as f:
                    f.write(code_content)
                
                # 2. Запустити silicon
                silicon_cmd = [
                    "silicon", 
                    "--no-window-controls", 
                    "--theme", "Visual Studio Dark+",
                    "--no-round-corner",
                    "--pad-horiz", "0",
                    "--pad-vert", "0",
                    "-o", temp_img_file, 
                    temp_code_file
                ]
                if lang:
                    silicon_cmd.extend(["-l", lang])
                
                print(f"🎨 Рендеринг зображення коду за допомогою silicon...")
                subprocess.run(silicon_cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # 3. Залити на catbox.moe
                print(f"🚀 Завантаження зображення на catbox.moe...")
                upload_cmd = [
                    "curl", "-s", "-F", "reqtype=fileupload",
                    "-F", f"fileToUpload=@{temp_img_file}",
                    "https://catbox.moe/user/api.php"
                ]
                result = subprocess.run(upload_cmd, capture_output=True, text=True, check=True)
                image_url = result.stdout.strip()
                
                if image_url.startswith("https://"):
                    print(f"🔗 Зображення завантажено: {image_url}")
                    item["Image Link"] = image_url
                    # Видаляємо блок коду з тексту запитання, щоб він не дублювався
                    item["Question Text"] = code_block_pattern.sub("", q_text).strip()
                else:
                    print(f"⚠️ Помилка завантаження: {result.stdout}")
            
            except Exception as e:
                print(f"⚠️ Не вдалося обробити блок коду: {e}")
            
            finally:
                # Очистити тимчасові файли
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
