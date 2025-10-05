# src/shacnify/core/installer.py
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
import time
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

from ..i18n.translator import t
from ..utils import run_command
from .detector import detect_framework
from . import steps

console = Console()

def create_new_project(project_name, recipe=None):
    if Path(project_name).exists():
        console.print(f"[bold red]❌ {t('folder_exists').format(project_name=project_name)}[/bold red]")
        return

    framework_choice = inquirer.select(
        message=t('select_template'),
        choices=[
            Choice("vite", name="Vite (Nhanh, được khuyên dùng)"),
            Choice("nextjs", name="Next.js (Full-stack, App Router)"),
            Choice("cra", name="Create React App (Cũ hơn)"),
        ],
        default="vite",
    ).execute()
    
    if framework_choice == 'vite':
        warning_message = (
            f"[bold]Khi Vite hỏi:[/bold]\n\n"
            f"   [white on magenta] Install with npm and start now? [/]\n\n"
            f">>> [bold yellow]Vui lòng chọn 'No' (hoặc bấm N)[/bold yellow] <<<\n\n"
            f"[dim]{t('shacnify_will_handle_install')}[/dim]"
        )
        console.print(Panel(warning_message, title="[bold yellow]⚠️LƯU Ý QUAN TRỌNG[/bold yellow]", border_style="yellow", expand=False))
        console.print("[dim]Chuẩn bị trong 2 giây...[/dim]")
        time.sleep(2)
    
    command_map = {
        "vite": f"npm create vite@latest {project_name} -- --template react-ts",
        "nextjs": f"npx create-next-app@latest {project_name}",
        "cra": f"npx create-react-app {project_name}"
    }
    
    console.print(f"\n[cyan]STEP 1: {t('creating_project').format(framework=framework_choice.upper())}[/cyan]")
    
    if not run_command(command_map[framework_choice], interactive=True):
        console.print(f"[bold red]❌ {t('create_project_failed')}[/bold red]")
        return

    project_path = Path(project_name).resolve()
    console.print(f"[green]✅ {t('project_created_successfully')}[/green]")
    
    os.chdir(project_path)
    
    console.print(f"\n[cyan]STEP 2: {t('installing_dependencies')}[/cyan]")
    with console.status(t('running_npm_install'), spinner="dots"):
        if not run_command("npm install"):
            console.print(f"[bold red]❌ {t('dependency_install_failed')}[/bold red]")
            return
            
    console.print(f"[green]✅ {t('dependencies_installed')}[/green]")
    
    console.print(f"\n[cyan]STEP 3: {t('setting_up_shadcn')}[/cyan]")
    setup_project(recipe)


def setup_project(recipe=None):
    """Hàm chính điều phối toàn bộ quá trình cài đặt."""
    framework = detect_framework()
    if not framework:
        console.print(f"[bold red]❌ {t('error_not_react')}[/bold red]")
        return
        
    console.print(f"   - {t('framework_detected')}: [bold green]{framework.upper()}[/bold green]")
    
    install_steps = [
        ("dep_install", steps.install_tailwind_deps),
        ("tailwind_config", lambda: steps.configure_tailwind(framework)),
        ("restructure_src", steps.restructure_src_directory),
        ("alias_config", steps.configure_alias),
        ("shadcn_init", lambda: steps.initialize_shadcn(framework)),
        ("add_components", lambda: steps.add_components_during_init(recipe)),
    ]

    # 🔽 LUỒNG HIỂN THỊ MỚI
    for name, func in install_steps:
        # Hiển thị tiêu đề của bước trước khi chạy
        console.print(f"\n[cyan]--- {t(name)} ---[/cyan]")
        
        # Gọi hàm thực thi bước đó
        success = func()
        
        # Sau khi chạy xong, mới hiển thị kết quả
        if success:
            console.print(f"[green]✅ {t(name)} {t('completed')}[/green]")
        else:
            console.print(f"[red]❌ {t(name)} {t('failed')}[/red]")
            console.print(f"[bold red]❌ {t('step_failed')}[/bold red]")
            # Dừng lại nếu có lỗi
            return
    
    console.print(f"\n[bold green]🎉 {t('init_done')}[/bold green]")

def add_specific_components(components: tuple):
    if not Path("components.json").exists():
        console.print("[bold red]❌ Lỗi: Shadcn/UI chưa được khởi tạo.[/bold red]")
        console.print("   Vui lòng chạy [cyan]shacnify init[/cyan] trước.")
        return

    selected_components = list(components)

    if not selected_components:
        selected_components = steps._prompt_for_components()
    
    steps._install_components(selected_components)
    console.print(f"\n[bold green]✅ Thêm component hoàn tất![/bold green]")