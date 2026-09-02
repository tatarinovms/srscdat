#!/usr/bin/env python3
"""
Конвертирует Shadowrocket-списки в формат domain-list-community.
DOMAIN-SUFFIX → domain:
DOMAIN, → full:
DOMAIN-KEYWORD, → keyword:
IP-CIDR/IP-ASN → пропускаются (geosite не поддерживает)
"""
import os
import re
import sys

def convert_file(src_path, dst_path):
    """Конвертирует один .list файл."""
    lines = []
    stats = {'domain': 0, 'full': 0, 'keyword': 0, 'skipped': 0}
    
    with open(src_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Убираем порядковый номер (если есть)
            line = re.sub(r'^\d+\|', '', line)
            
            if line.startswith('DOMAIN-SUFFIX,'):
                value = line.split(',', 1)[1].lower()
                lines.append(f'domain:{value}')
                stats['domain'] += 1
            elif line.startswith('DOMAIN,'):
                value = line.split(',', 1)[1].lower()
                lines.append(f'full:{value}')
                stats['full'] += 1
            elif line.startswith('DOMAIN-KEYWORD,'):
                value = line.split(',', 1)[1].lower()
                lines.append(f'keyword:{value}')
                stats['keyword'] += 1
            else:
                stats['skipped'] += 1
    
    with open(dst_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sorted(lines)))
    
    return stats

def main():
    src_dir = sys.argv[1] if len(sys.argv) > 1 else '/Volumes/HDD/project/ShadowRocketSimpleConfig/lists'
    dst_dir = sys.argv[2] if len(sys.argv) > 2 else 'data'
    
    os.makedirs(dst_dir, exist_ok=True)
    
    total = {'domain': 0, 'full': 0, 'keyword': 0, 'skipped': 0}
    
    for filename in sorted(os.listdir(src_dir)):
        if not filename.endswith('.list'):
            continue
        
        src_path = os.path.join(src_dir, filename)
        name = filename[:-5]  # убираем .list
        dst_path = os.path.join(dst_dir, name)
        
        stats = convert_file(src_path, dst_path)
        
        for k in total:
            total[k] += stats[k]
        
        print(f'  {name}: {stats["domain"]} domain, {stats["full"]} full, {stats["keyword"]} keyword, {stats["skipped"]} skipped')
    
    print(f'\nИтого: {total["domain"]} domain, {total["full"]} full, {total["keyword"]} keyword, {total["skipped"]} skipped')
    print(f'Сохранено в: {dst_dir}')

if __name__ == '__main__':
    main()
