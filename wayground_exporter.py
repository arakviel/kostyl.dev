import argparse
import pandas as pd
import json
import os
import sys

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
            
        df = pd.DataFrame(data, columns=columns)
        
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
