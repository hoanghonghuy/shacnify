# src/shacnify/logger.py
import logging
from pathlib import Path

LOG_DIR = Path.home() / ".shacnify" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Xóa tất cả các handler cũ để tránh ghi log trùng lặp
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

def get_log_file_path(project_name: str) -> Path:
    """Trả về đường dẫn đầy đủ đến file log cho một dự án cụ thể."""
    return LOG_DIR / f"{project_name}.log"

def setup_logger(project_name: str):
    """Thiết lập logger để ghi vào file log riêng cho từng dự án."""
    log_file = get_log_file_path(project_name)
    
    # Cấu hình logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] - %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='a', encoding='utf-8'),
        ]
    )
    return logging.getLogger(project_name)

def get_active_project_name():
    """Lấy tên dự án từ thư mục làm việc hiện tại."""
    return Path.cwd().name

# Tạo một logger mặc định khi module được import
logger = setup_logger(get_active_project_name())