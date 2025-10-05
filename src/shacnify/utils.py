# src/shacnify/utils.py
import subprocess
from pathlib import Path
from rich.console import Console
from .logger import setup_logger, get_log_file_path 

console = Console()

def run_command(command, cwd=None, interactive=False):
    """Chạy một lệnh shell và ghi lại lỗi nếu có."""
    project_name = Path(cwd).name if cwd else Path.cwd().name
    current_logger = setup_logger(project_name)
    
    current_logger.info(f"--- Running Command ---")
    current_logger.info(f"Command: {command}")
    current_logger.info(f"Directory: {cwd or Path.cwd()}")
    
    try:
        if interactive:
            subprocess.run(command, shell=True, cwd=cwd, check=True)
        else:
            process = subprocess.run(
                command, shell=True, cwd=cwd, check=True,
                capture_output=True, text=True, encoding='utf-8'
            )
    except subprocess.CalledProcessError as e:
        stderr_output = e.stderr if hasattr(e, 'stderr') and e.stderr else "Không có output lỗi chi tiết."
        error_message = (
            f"--- Command Failed ---\n"
            f"Command: {command}\n"
            f"Return Code: {e.returncode}\n"
            f"Stderr:\n{stderr_output.strip()}"
        )
        current_logger.error(error_message)
        
        # 🔽 Sử dụng hàm mới để lấy đường dẫn file log
        log_path = get_log_file_path(project_name)
        console.print(f"[red]   Lỗi! Chi tiết đã được ghi vào file log:[/red]")
        console.print(f"[dim]{log_path}[/dim]")
        return False
    except FileNotFoundError:
        current_logger.error(f"Command not found: {command.split()[0]}")
        return False
        
    current_logger.info("--- Command Succeeded ---")
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