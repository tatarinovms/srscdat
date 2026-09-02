#!/usr/bin/env python3
"""
Проверяет сгенерированный geosite.dat файл.
Распаковывает protobuf и выводит статистику.
"""
import struct
import sys

# Минимальный парсер protobuf для GeoSiteList
def read_varint(data, pos):
    """Читает varint из protobuf."""
    result = 0
    shift = 0
    while True:
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        if not (b & 0x80):
            break
        shift += 7
    return result, pos

def read_field(data, pos):
    """Читает поле protobuf."""
    tag, pos = read_varint(data, pos)
    field_number = tag >> 3
    wire_type = tag & 0x07
    if wire_type == 2:  # Length-delimited
        length, pos = read_varint(data, pos)
        value = data[pos:pos+length]
        pos += length
        return field_number, value, pos
    elif wire_type == 0:  # Varint
        value, pos = read_varint(data, pos)
        return field_number, value, pos
    return field_number, None, pos

def parse_domain(domain_data):
    """Парсит Domain message."""
    pos = 0
    result = {}
    while pos < len(domain_data):
        field_number, value, pos = read_field(domain_data, pos)
        if field_number == 1:  # type
            result['type'] = value
        elif field_number == 2:  # value
            result['value'] = value.decode('utf-8', errors='replace')
    return result

def parse_site(site_data):
    """Парсит GeoSite message."""
    pos = 0
    result = {'domains': []}
    while pos < len(site_data):
        field_number, value, pos = read_field(site_data, pos)
        if field_number == 1:  # country_code
            result['country_code'] = value.decode('utf-8', errors='replace')
        elif field_number == 2:  # domain
            result['domains'].append(parse_domain(value))
    return result

def parse_list(data):
    """Парсит GeoSiteList message."""
    pos = 0
    entries = []
    while pos < len(data):
        field_number, value, pos = read_field(data, pos)
        if field_number == 1:  # entry
            entries.append(parse_site(value))
    return entries

def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else '/Volumes/HDD/project/geosite.dat'
    
    with open(filepath, 'rb') as f:
        data = f.read()
    
    entries = parse_list(data)
    
    print(f"Файл: {filepath}")
    print(f"Размер: {len(data)} байт")
    print(f"Категорий: {len(entries)}")
    print()
    
    total_domains = 0
    for entry in sorted(entries, key=lambda x: x['country_code']):
        code = entry['country_code']
        domains = entry['domains']
        total_domains += len(domains)
        
        # Подсчет по типам
        types = {}
        for d in domains:
            t = str(d.get('type', 'unknown'))
            types[t] = types.get(t, 0) + 1
        
        type_str = ', '.join(f'{t}: {c}' for t, c in sorted(types.items()))
        print(f"  {code}: {len(domains)} доменов ({type_str})")
    
    print(f"\nВсего доменов: {total_domains}")

if __name__ == '__main__':
    main()
