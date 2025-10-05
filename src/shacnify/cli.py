# src/shacnify/cli.py
import click
import shutil
from rich.console import Console
from rich.table import Table

from .logger import logger 
from .i18n.translator import t, set_language
from .core.installer import setup_project, create_new_project, add_specific_components
from .core.config_manager import get_config, set_config_value, CONFIG_PATH
from .core.recipes import RECIPES

console = Console()
AVAILABLE_RECIPES = list(RECIPES.keys())

def check_environment():
    """Kiểm tra xem các dependency cần thiết (npm) có trong PATH không."""
    if not shutil.which("npm"):
        error_message = "Lệnh 'npm' không được tìm thấy. Node.js chưa được cài đặt hoặc chưa được thêm vào biến môi trường PATH."
        
        logger.error(f"--- PRE-FLIGHT CHECK FAILED ---")
        logger.error(error_message)

        console.print("[bold red]LỖI MÔI TRƯỜDNG[/bold red]")
        console.print(error_message)
        console.print("Vui lòng cài đặt Node.js (bao gồm npm) và đảm bảo đường dẫn được thêm vào PATH, sau đó khởi động lại terminal/IDE.")
        return False
    return True

@click.group()
def main_cli():
    """🚀 shacnify - Tool cài đặt đỉnh cao cho React + Shadcn/UI."""
    pass

@main_cli.command()
@click.argument("project_name")
@click.option(
    "--recipe",
    type=click.Choice(AVAILABLE_RECIPES, case_sensitive=False),
    help="Chọn một công thức cài đặt sẵn."
)
def create(project_name, recipe):
    """Tạo một dự án React mới từ đầu và cài đặt Shadcn/UI."""
    if not check_environment(): return
    console.print(f"[bold green]🚀 Bắt đầu tạo dự án mới: {project_name}[/bold green]")
    create_new_project(project_name, recipe)

@main_cli.command()
@click.option(
    "--recipe",
    type=click.Choice(AVAILABLE_RECIPES, case_sensitive=False),
    help="Chọn một công thức cài đặt sẵn."
)
@click.option(
    "--safe",
    is_flag=True,
    help="Chạy ở chế độ an toàn, bỏ qua việc tái cấu trúc thư mục src và ghi đè file."
)
def init(recipe, safe):
    """Khởi tạo Shadcn/UI và Tailwind CSS cho dự án hiện tại."""
    if not check_environment(): return
    console.print(f"[bold cyan]{t('init_start')}[/bold cyan]")
    if safe:
        console.print("[yellow]🟡 Chạy ở chế độ an toàn (safe mode). Sẽ không tái cấu trúc thư mục 'src' hoặc ghi đè file cấu hình.[/yellow]")
    setup_project(recipe, safe)

@main_cli.command()
@click.argument("components", nargs=-1)
def add(components):
    """Thêm một hoặc nhiều component vào dự án đã khởi tạo."""
    if not check_environment(): return
    if not components:
        console.print("[cyan]Chạy ở chế độ tương tác...[/cyan]")
    add_specific_components(components)

@main_cli.group()
def config():
    """Xem và quản lý cấu hình của shacnify."""
    pass

@config.command("view")
def view_config():
    """Xem tất cả các cấu hình hiện tại."""
    config_data = get_config()
    if not config_data:
        console.print("[yellow]Chưa có cấu hình nào được thiết lập.[/yellow]")
        return
    
    table = Table(title="Cấu hình Shacnify")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="magenta")

    for key, value in config_data.items():
        table.add_row(key, str(value))
    
    console.print(table)

@config.command("set")
@click.argument("key")
@click.argument("value")
def set_config(key, value):
    """Thiết lập một giá trị cấu hình. Vd: set default_components button,card,input"""
    set_config_value(key, value)
    console.print(f"[green]✅ Đã lưu cấu hình: [cyan]{key}[/cyan] = [magenta]{get_config().get(key)}[/magenta][/green]")

@config.command("path")
def config_path():
    """Hiển thị đường dẫn đến file config.json."""
    console.print(f"📄 Đường dẫn file cấu hình: [green]{CONFIG_PATH}[/green]")

@main_cli.group()
def lang():
    """Quản lý ngôn ngữ của tool."""
    pass

@lang.command("set")
@click.argument("language_code", type=click.Choice(['en', 'vi']))
def set_lang_command(language_code):
    """Đặt ngôn ngữ mặc định (en hoặc vi)."""
    set_language(language_code)
    new_t = __import__('shacnify.i18n.translator', fromlist=['t']).t
    console.print(f"🌍 [green]{new_t('lang_changed')}[/green]")

@lang.command("get")
def get_lang_command():
    """Xem ngôn ngữ hiện tại."""
    console.print(f"🌍 [yellow]{t('lang_current')}[/yellow]")

if __name__ == "__main__":
    main_cli()