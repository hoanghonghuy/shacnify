# src/shacnify/i18n/translator.py
import json
from pathlib import Path
from ..core.config_manager import get_config, set_config_value

# --- State cache ---
_MESSAGES_CACHE = {}
_CURRENT_LANG = None

def _load_language_messages():
    """Tải file ngôn ngữ vào cache nếu cần."""
    global _CURRENT_LANG, _MESSAGES_CACHE
    
    lang_from_config = get_config().get("language", "en")
    
    # Chỉ tải lại file nếu ngôn ngữ đã thay đổi
    if _CURRENT_LANG == lang_from_config:
        return

    _CURRENT_LANG = lang_from_config
    
    try:
        # Dành cho khi chạy tool đã được cài đặt
        from importlib.resources import files
        pkg_path = files('shacnify')
    except ImportError:
        # Dành cho khi đang phát triển (chạy trực tiếp)
        pkg_path = Path(__file__).parent.parent

    locale_file = pkg_path / "i18n" / "locales" / f"{_CURRENT_LANG}.json"
    
    if not locale_file.exists():
        # Fallback to English if the selected language file doesn't exist
        _CURRENT_LANG = "en"
        locale_file = pkg_path / "i18n" / "locales" / "en.json"

    _MESSAGES_CACHE = json.loads(locale_file.read_text(encoding='utf-8'))

def t(key: str) -> str:
    """Hàm dịch chính, luôn đảm bảo ngôn ngữ được cập nhật."""
    _load_language_messages()
    return _MESSAGES_CACHE.get(key, key)

def set_language(lang_code: str):
    """Đặt ngôn ngữ mới."""
    global _CURRENT_LANG
    set_config_value("language", lang_code)
    # Reset cache để lần gọi 't' tiếp theo sẽ tải lại đúng file
    _CURRENT_LANG = None