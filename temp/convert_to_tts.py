#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TTS Conversion Script for Ukrainian Markdown Articles
Converts Markdown educational content to audiobook-optimized plain text
"""

import re

def convert_to_tts(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove GitHub links at the beginning
    content = re.sub(r'^https?://github\.com/[^\n]+\n*', '', content)
    
    # Convert structural markers
    content = re.sub(r'^# (.+)$', r'Розділ: \1', content, flags=re.MULTILINE)
    content = re.sub(r'^## (.+)$', r'Підрозділ: \1', content, flags=re.MULTILINE)
    content = re.sub(r'^### (.+)$', r'Пункт: \1', content, flags=re.MULTILINE)
    content = re.sub(r'^#### (.+)$', r'Підпункт: \1', content, flags=re.MULTILINE)
    
    # Remove Docus components
    content = re.sub(r'::(note|quote|important|caution|warning|tip|steps|field-group)\n', '', content)
    content = re.sub(r'^::field\{[^}]+\}\n', '', content, flags=re.MULTILINE)
    content = re.sub(r'^::\n?', '', content, flags=re.MULTILINE)
    
    # Remove image references
    content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', '', content)
    
    # Convert links - keep only text
    content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
    
    # Remove code blocks but keep description
    content = re.sub(r'```[\s\S]*?```', lambda m: convert_code_block(m.group(0)), content)
    
    # Remove standalone horizontal rules
    content = re.sub(r'^---+\s*$', '', content, flags=re.MULTILINE)
    
    # Convert English terms to phonetic Ukrainian
    replacements = {
        'Transaction Script': 'Транзекшн Скріпт',
        'transaction script': 'транзекшн скріпт',
        'Active Record': 'Ектів Рекорд',
        'active record': 'ектів рекорд',
        'Domain Model': 'Домен Модел',
        'domain model': 'домен модел',
        'Martin Fowler': 'Мартін Фаулер (англійською Martin Fowler)',
        'Eric Evans': 'Ерік Еванс (англійською Eric Evans)',
        'aggregates': 'агрегейтс',
        'value objects': 'вел\'ю об\'єктс',
        'domain events': 'домен івентс',
        'domain services': 'домен сервісіс',
        'Value Objects': 'Вел\'ю Об\'єктс',
        'Aggregates': 'Агрегейтс',
        'Domain Services': 'Домен Сервісіс',
        'Domain Events': 'Домен Івентс',
        'Domain-Driven Design': 'Домен-Дрівен Дізайн',
        'DDD': 'Ді-Ді-Ді',
        'CRUD': 'Сі-Ар-Ю-Ді',
        'Patterns of Enterprise Application Architecture': 'Паттернс оф Ентерпрайз Епплікейшн Аркітекчер',
        'help desk': 'хелп деск',
        'SLA': 'Ес-Ель-Ей',
        'ubiquitous language': 'юбіквітос ленгвідж',
        'bounded context': 'баундед контекст',
        'Primitive Obsession': 'прімітів обсешн',
        'POCOs': 'Пі-О-Сі-Оуз',
        '.NET': 'дот-нет',
        'POJOs': 'Пі-О-Джей-Оуз',
        'Java': 'Джава',
        'POPOs': 'Пі-О-Пі-Оуз',
        'Python': 'Пайтон',
        'aggregate root': 'агрегейт рут',
        'immutable': 'ім\'ютабл',
        'command': 'команд',
        'concurrency': 'конкаренсі',
        'eventual consistency': 'івенчуал консистенсі',
        'core subdomain': 'кор саб-домен',
        'supporting subdomains': 'сапортінг саб-доменс',
        'generic subdomains': 'дженерік саб-доменс',
    }
    
    for eng, ukr in replacements.items():
        content = content.replace(eng, ukr)
    
    # Clean up multiple blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Clean up spaces
    content = re.sub(r' +', ' ', content)
    content = re.sub(r'^ +', '', content, flags=re.MULTILINE)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

def convert_code_block(code_match):
    """Convert code blocks to narrative descriptions"""
    code = code_match.group(0)
    
    # Simple placeholder - in real implementation, this would intelligently convert code
    if 'class Color' in code or 'Color' in code:
        return 'Розглянемо приклад класу Колор з відповідною логікою.'
    elif 'class Person' in code:
        return 'Розглянемо приклад класу Персон з відповідними полями та методами.'
    elif 'class Ticket' in code:
        return 'Розглянемо приклад класу Тікет з відповідною бізнес-логікою.'
    elif 'SQL' in code or 'UPDATE' in code:
        return 'Розглянемо приклад Ес-Ку-Ель запиту для оновлення даних.'
    elif 'json' in code.lower():
        return 'Розглянемо приклад структури даних у форматі Джі-Сон.'
    else:
        return 'Розглянемо відповідний приклад коду.'

if __name__ == '__main__':
    input_file = r'y:\Work\kostyl.dev\temp\college\content\1.software-design\4.complex-business-logic_new.md'
    output_file = r'y:\Work\kostyl.dev\temp\college\content\1.software-design\4.complex-business-logic_new.tts.txt'
    convert_to_tts(input_file, output_file)
    print(f'Converted {input_file} to {output_file}')
