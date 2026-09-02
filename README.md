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

## Содержимое geosite.dat

Файл содержит 13 категорий доменов (1805 всего):

| Категория | Доменов | Описание |
|-----------|---------|----------|
| `AI` | 97 | AI-сервисы (ChatGPT, Claude, Gemini, Copilot и др.) |
| `FITNESS` | 4 | Сервисы для спорта и здоровья |
| `GAMES` | 22 | Игровые платформы и CDN |
| `MAIN` | 254 | Основные сервисы: соцсети, медиа, инструменты |
| `MUSIC` | 12 | Музыкальные стриминги и лейблы |
| `NEVAMESSENGER` | 61 | Мессенджер |
| `REDTUBE` | 16 | RedTube и связанные CDN |
| `RUADS` | 174 | Российская реклама, трекинг, аналитика |
| `RUBANKING` | 671 | Российские банки и финансовые сервисы |
| `RUDIRECT` | 337 | Российские локальные сервисы (DIRECT) |
| `RUIPCHECKER` | 9 | Сервисы проверки IP-адреса |
| `VIDEO` | 41 | Видео стриминговые платформы |
| `ZETASERVICES` | 107 | Сервисы аналога ВК |

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
