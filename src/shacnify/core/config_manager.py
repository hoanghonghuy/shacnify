# src/shacnify/core/config_manager.py
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".shacnify"
CONFIG_PATH = CONFIG_DIR / "config.json"

def ensure_config_exists():
    """Đảm bảo file và thư mục config tồn tại."""
    CONFIG_DIR.mkdir(exist_ok=True)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.write_text("{}", encoding='utf-8')

def get_config():
    """Đọc toàn bộ file config."""
    ensure_config_exists()
    try:
        return json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return {}

def set_config_value(key, value):
    """Lưu một cặp key-value vào file config."""
    config = get_config()
    # Nếu value là chuỗi chứa dấu phẩy, chuyển nó thành list
    if isinstance(value, str) and ',' in value:
        config[key] = [item.strip() for item in value.split(',')]
    else:
        config[key] = value
    CONFIG_PATH.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding='utf-8')