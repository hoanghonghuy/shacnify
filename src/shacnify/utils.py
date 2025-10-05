# src/shacnify/utils.py
import subprocess
from pathlib import Path
from rich.console import Console
from .logger import logger, LOG_FILE

console = Console()

def run_command(command, cwd=None, interactive=False):
    """Chạy một lệnh shell và ghi lại lỗi nếu có."""
    logger.info(f"Running command: {command}")
    try:
        if interactive:
            process = subprocess.run(command, shell=True, cwd=cwd, check=True)
        else:
            # Chụp lại stderr để ghi log nếu có lỗi
            process = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
    except subprocess.CalledProcessError as e:
        # GHI LỖI CHI TIẾT VÀO FILE LOG
        error_message = f"Command failed: {command}\nReturn Code: {e.returncode}"
        # e.stderr chỉ tồn tại khi capture_output=True
        stderr_output = e.stderr if hasattr(e, 'stderr') else "N/A"
        error_message += f"\nStderr:\n{stderr_output}"
        
        logger.error(error_message)
        
        # Thông báo cho người dùng
        console.print(f"[red]   Lỗi! Chi tiết đã được ghi vào file log:[/red]")
        console.print(f"[dim]{LOG_FILE}[/dim]")
        return False
    except FileNotFoundError:
        logger.error(f"Command not found: {command.split()[0]}")
        return False
    return True

def write_file(path, content):
    """Ghi nội dung vào một file."""
    try:
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        console.print(f"[bold red]❌ Không thể ghi file {path}: {e}[/bold red]")
        return False