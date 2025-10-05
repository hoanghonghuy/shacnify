# src/shacnify/core/steps.py
import json
import os
from pathlib import Path
from rich.console import Console
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from ..utils import run_command, write_file
from .templates import (
    get_tailwind_config_content,
    get_components_json_content,
    get_app_tsx_content,
    get_main_tsx_content,
    get_main_layout_tsx_content,
    get_home_page_tsx_content,
)
from .recipes import RECIPES
from .config_manager import get_config
from ..i18n.translator import t

console = Console()

def restructure_src_directory():
    """Dọn dẹp thư mục src và tạo cấu trúc src-layout mới."""
    src_path = Path("src")
    
    # --- Dọn dẹp ---
    files_to_remove = [
        src_path / "App.css",
        src_path / "App.tsx",
        src_path / "assets" / "react.svg",
    ]
    for f in files_to_remove:
        if f.exists():
            f.unlink()
    
    assets_dir = src_path / "assets"
    if assets_dir.exists() and not any(assets_dir.iterdir()):
        assets_dir.rmdir()

    # --- Tạo cấu trúc mới ---
    dirs_to_create = [
        src_path / "components" / "ui",
        src_path / "lib",
        src_path / "layouts",
        src_path / "pages",
    ]
    for d in dirs_to_create:
        d.mkdir(parents=True, exist_ok=True)
    
    # --- Tạo file mẫu mới ---
    write_file(src_path / "App.tsx", get_app_tsx_content())
    write_file(src_path / "main.tsx", get_main_tsx_content())
    write_file(src_path / "layouts" / "MainLayout.tsx", get_main_layout_tsx_content())
    write_file(src_path / "pages" / "HomePage.tsx", get_home_page_tsx_content())
    
    # Cài đặt react-router-dom cần thiết cho cấu trúc mới
    return run_command("npm install react-router-dom")

def _prompt_for_components():
    """Hàm riêng để hiển thị giao diện lựa chọn và trả về danh sách component."""
    config = get_config()
    default_selection = config.get("default_components", ["button", "input", "form", "card"])
    
    available_components = [
        "button", "input", "form", "card", "dialog", "table", "sonner", "dropdown-menu", 
        "avatar", "badge", "alert", "label", "select", "checkbox", "radio-group", 
        "slider", "switch", "textarea"
    ]
    available_components.sort()

    try:
        console.print("\n[bold cyan]💡 Chọn các component bạn muốn cài đặt (dùng phím cách để chọn, enter để xác nhận):[/bold cyan]")
        selected_components = inquirer.checkbox(
            message="Các component có sẵn:",
            choices=[
                Choice(name, enabled=name in default_selection) 
                for name in available_components
            ],
            validate=lambda result: len(result) >= 1,
            invalid_message="Bạn phải chọn ít nhất một component.",
            instruction="(Ấn <space> để chọn, <a> để chọn tất cả, <i> để đảo ngược lựa chọn)",
        ).execute()
        return selected_components
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Đã hủy lựa chọn component.[/yellow]")
        return []

def _install_components(component_list):
    """Hàm riêng để cài đặt một danh sách component cho trước."""
    if not component_list:
        console.print("[yellow]Không có component nào được chọn để cài đặt.[/yellow]")
        return True

    console.print(f"\n[cyan]🚀 Sẽ cài đặt {len(component_list)} component:[/cyan]")
    all_success = True
    for comp in component_list:
        console.print(f"   - Đang thêm [bold magenta]{comp}[/bold magenta]...")
        
        success = run_command(f"npx shadcn@latest add {comp} -y", interactive=True)
        
        if success:
            console.print(f"   [green]✅ Đã thêm {comp} thành công[/green]")
        else:
            console.print(f"   [red]❌ Thêm {comp} thất bại. Vui lòng kiểm tra file log.[/red]")
            all_success = False

    return all_success

def add_components_during_init(recipe=None):
    """Hàm dùng cho lệnh init, xử lý recipe và config."""
    config = get_config()
    selected_components = []

    if recipe and recipe in RECIPES:
        selected_components = RECIPES[recipe]
        console.print(f"\n[bold cyan]💡 Áp dụng công thức từ cờ lệnh: '{recipe}'[/bold cyan]")
    elif config.get("default_recipe") and config["default_recipe"] in RECIPES:
        recipe_name = config["default_recipe"]
        selected_components = RECIPES[recipe_name]
        console.print(f"\n[bold cyan]💡 Áp dụng công thức mặc định từ config: '{recipe_name}'[/bold cyan]")
    else:
        selected_components = _prompt_for_components()

    return _install_components(selected_components)

def install_tailwind_deps():
    return run_command("npm install -D tailwindcss postcss autoprefixer tailwindcss-animate")

def configure_tailwind(framework):
    """Cấu hình Tailwind và ghi đè file CSS chính."""
    tailwind_config_content = get_tailwind_config_content(framework)
    if not write_file("tailwind.config.js", tailwind_config_content): return False
    
    postcss_content = "module.exports = { plugins: { tailwindcss: {}, autoprefixer: {} } }"
    if not write_file("postcss.config.js", postcss_content): return False
    
    css_path_str = "app/globals.css" if framework == "nextjs" else "src/index.css"
    css_path = Path(css_path_str)
    
    # Tạo file nếu nó không tồn tại
    if not css_path.exists():
        css_path.parent.mkdir(parents=True, exist_ok=True)
        css_path.touch()

    tailwind_directives = "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n"
    # Luôn ghi đè file CSS chính để đảm bảo sạch sẽ
    write_file(css_path_str, tailwind_directives)
            
    return True

def configure_alias():
    """Cấu hình alias path cho jsconfig.json hoặc tsconfig.json."""
    config_file = "tsconfig.json" if Path("tsconfig.json").exists() else "jsconfig.json"
    
    try:
        data = {}
        if Path(config_file).exists():
            data = json.loads(Path(config_file).read_text(encoding='utf-8'))
        
        if "compilerOptions" not in data: data["compilerOptions"] = {}
        data["compilerOptions"]["baseUrl"] = "."
        data["compilerOptions"]["paths"] = {"@/*": ["./src/*"]}
        if "include" not in data: data["include"] = ["src"]
            
        write_file(config_file, json.dumps(data, indent=2))
    except Exception as e:
        console.print(f"[yellow]⚠️  Không thể tự động cấu hình alias: {e}[/yellow]")
        return False
        
    return True

def initialize_shadcn(framework):
    """Tạo file components.json và cài các dependency cốt lõi của Shadcn.
    
    CẬP NHẬT: Chủ động cài thêm các dependency cho component FORM để tránh lỗi treo.
    """
    components_json_content = get_components_json_content(framework)
    if not write_file("components.json", components_json_content): return False
    
    # Các dependency cốt lõi của Shadcn
    core_deps = "class-variance-authority clsx lucide-react tailwind-merge"
    
    # Các dependency đặc biệt cho FORM
    form_deps = "react-hook-form zod @hookform/resolvers"
    
    return run_command(f"npm install {core_deps} {form_deps}")