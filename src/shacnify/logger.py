# src/shacnify/logger.py
import logging
from pathlib import Path

# Log file sẽ được lưu ở ~/.shacnify/shacnify.log
LOG_DIR = Path.home() / ".shacnify"
LOG_FILE = LOG_DIR / "shacnify.log"

def setup_logger():
    """Thiết lập logger để ghi vào file."""
    LOG_DIR.mkdir(exist_ok=True)
    
    # Cấu hình logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=LOG_FILE,
        filemode='a' # 'a' để ghi tiếp vào file, 'w' để ghi đè
    )
    
    return logging.getLogger(__name__)

logger = setup_logger()