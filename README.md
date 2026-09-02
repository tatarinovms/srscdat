# srscdat

Генератор `geosite.dat` из списков Shadowrocket.

## Структура

```
srscdat/
├── update-geosite.sh      ← основной скрипт
├── src/
│   ├── convert.py         ← конвертер Shadowrocket → DLC
│   └── check.py           ← проверка geosite.dat
├── data/                  ← промежуточные файлы DLC (не коммитятся)
└── output/                ← сгенерированный geosite.dat
```

## Требования

- Python 3.6+
- Go 1.21+ (для domain-list-community)
- Git

## Использование

```bash
# Клонировать репозиторий
git clone <url> srscdat
cd srscdat

# Сгенерировать geosite.dat
./update-geosite.sh

# С проверкой результата
./update-geosite.sh --check
```

## Конфигурация

По умолчанию скрипт ищет списки Shadowrocket в `../ShadowRocketSimpleConfig/lists`. Это можно изменить через переменные окружения:

```bash
# Путь к спискам
SR_SRC_DIR=/path/to/lists ./update-geosite.sh

# Путь к domain-list-community (если уже скачан)
DLC_DIR=/path/to/domain-list-community ./update-geosite.sh

# Куда сохранить результат
OUTPUT_DIR=/path/to/output ./update-geosite.sh
```

## Формат списков

Поддерживаются правила Shadowrocket:

| Правило | Конвертируется в |
|---------|------------------|
| `DOMAIN-SUFFIX,example.com` | `domain:example.com` |
| `DOMAIN,example.com` | `full:example.com` |
| `DOMAIN-KEYWORD,example` | `keyword:example` |
| `IP-CIDR,...` | ❌ пропускается |
| `IP-ASN,...` | ❌ пропускается |

## Использование geosite.dat

### Xray/v2Ray
```json
{
  "routing": {
    "rules": [
      {
        "type": "field",
        "outboundTag": "proxy",
        "domain": ["geosite:MAIN"]
      }
    ]
  }
}
```

### Clash/Mihomo
```yaml
rules:
  - GEOSITE,MAIN,PROXY
  - GEOSITE,RUDIRECT,DIRECT
```

## Лицензия

MIT
