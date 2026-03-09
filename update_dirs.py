import os
import re
import yaml

content_dir = 'content'

icon_map = {
    'csharp': 'i-devicon-csharp',
    'cpp': 'i-devicon-cplusplus',
    'javascript': 'i-devicon-javascript',
    'typescript': 'i-devicon-typescript',
    'java': 'i-devicon-java',
    'python': 'i-devicon-python',
    'html-css': 'i-devicon-html5',
    'react': 'i-devicon-react',
    'aspnet': 'i-devicon-dot-net-core',
    'adonet': 'i-devicon-dot-net-core',
    'databases': 'i-lucide-database',
    'sql': 'i-lucide-database',
    'tools': 'i-lucide-wrench',
    'fundamentals': 'i-lucide-book-open',
    'software-engineering': 'i-lucide-code-2',
    'ddd': 'i-lucide-layers',
    'media-streaming': 'i-lucide-video',
    'api': 'i-lucide-network',
    'minimal-api': 'i-lucide-zap',
    'auth': 'i-lucide-shield-check',
    'security': 'i-lucide-shield-alert',
    'network': 'i-lucide-globe',
    'bom': 'i-lucide-monitor',
    'events': 'i-lucide-mouse-pointer-click',
    'oop': 'i-lucide-box',
    'architecture': 'i-lucide-building-2',
    'intro': 'i-lucide-play',
    'start': 'i-lucide-play',
    'advanced': 'i-lucide-zap',
    'core': 'i-lucide-cpu',
    'system': 'i-lucide-server',
    'ms-sql-server': 'i-devicon-microsoftsqlserver',
    'multi-table': 'i-lucide-table',
    'aggregate': 'i-lucide-calculator',
    'backup': 'i-lucide-save',
    'full-text': 'i-lucide-search',
    'triggers': 'i-lucide-bolt',
}

title_map = {
    'csharp': 'C#',
    'cpp': 'C++',
    'javascript': 'JavaScript',
    'typescript': 'TypeScript',
    'java': 'Java',
    'python': 'Python',
    'html-css': 'HTML & CSS',
    'aspnet': 'ASP.NET',
    'adonet': 'ADO.NET',
    'ddd': 'DDD',
    'oop': 'OOP',
    'api': 'API',
    'sql': 'SQL',
    'ms-sql-server-start': 'MS SQL Server Start',
}

def get_nice_title(raw_name):
    if raw_name in title_map:
        return title_map[raw_name]
    parts = raw_name.split('-')
    title = ' '.join(p.capitalize() for p in parts)
    for k, v in title_map.items():
        title = re.sub(rf'\b{k}\b', v, title, flags=re.IGNORECASE)
    return title

def get_icon(raw_name):
    for k, v in icon_map.items():
        if k in raw_name:
            return v
    return 'i-lucide-folder'

def has_cyrillic(text):
    return bool(re.search('[а-яА-ЯіІїЇєЄґҐ]', text))

for root, d_names, _ in os.walk(content_dir):
    for d in d_names:
        if d.startswith('.'):
            continue
        
        dir_path = os.path.join(root, d)
        dir_yml = os.path.join(dir_path, '.navigation.yml')
        
        raw_name = re.sub(r'^\d+\.', '', d)
        
        data = {}
        if os.path.exists(dir_yml):
            try:
                with open(dir_yml, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or {}
            except Exception:
                pass
                
        old_title = data.get('title', '')
        
        # Don't touch title if it's cyrillic
        if old_title and has_cyrillic(str(old_title)):
            pass
        else:
            data['title'] = get_nice_title(raw_name)
            
        old_icon = data.get('icon', '')
        # Only update icon if it's not set or it's a default looking one or we have a good match
        if not old_icon or 'folder' in old_icon or not old_icon.startswith('i-'):
            data['icon'] = get_icon(raw_name)
            
        with open(dir_yml, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False)
            
print("Done updating .navigation.yml files.")
