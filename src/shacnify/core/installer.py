# src/shacnify/core/installer.py
import os
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
import time
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from .planner import Plan

from ..i18n.translator import t
from ..utils import run_command
from .detector import detect_framework
from . import steps

console = Console()

def create_new_project(project_name, recipe=None):
    """Hỏi người dùng template và tạo dự án React mới."""
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
        console.print(Panel(warning_message, title="[bold yellow]⚠️ LƯU Ý QUAN TRỌNG[/bold yellow]", border_style="yellow", expand=False))
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
    # Chạy init ở chế độ bình thường (không safe) khi tạo mới
    setup_project(recipe, safe=False)


def setup_project(recipe=None, safe=False):
    """Hàm chính điều phối toàn bộ quá trình cài đặt."""
    framework = detect_framework()
    if not framework:
        console.print(f"[bold red]❌ {t('error_not_react')}[/bold red]")
        return
        
    console.print(f"   - {t('framework_detected')}: [bold green]{framework.upper()}[/bold green]")

    plan = Plan(framework, safe_mode=safe)
    plan.display()

    # Nếu không có hành động nào, dừng lại
    if not plan.actions:
        return

    try:
        # Câu hỏi xác nhận cuối cùng
        confirmation = inquirer.confirm(
            message="Bạn có muốn thực hiện các thay đổi trên không?",
            default=False
        ).execute()

        if not confirmation:
            console.print(f"[yellow]{t('init_aborted')}[/yellow]")
            return
    except KeyboardInterrupt:
        console.print(f"\n[yellow]{t('init_aborted')}[/yellow]")
        return
    
    # Xây dựng danh sách các bước dựa trên kế hoạch (có thể cải tiến sau)
    # Hiện tại vẫn giữ nguyên các bước để đảm bảo tính đúng đắn
    install_steps = [
        ("dep_install", steps.install_tailwind_deps),
        ("tailwind_config", lambda: steps.configure_tailwind(framework, safe=safe)),
    ]
    
    if not safe:
        install_steps.append(("restructure_src", steps.restructure_src_directory))

    install_steps.extend([
        ("alias_config", lambda: steps.configure_alias(safe=safe)),
        ("shadcn_init", lambda: steps.initialize_shadcn(framework)),
        ("add_components", lambda: steps.add_components_during_init(recipe)),
    ])


    for name, func in install_steps:
        console.print(f"\n[cyan]--- {t(name)} ---[/cyan]")
        success = func()
        
        if success:
            console.print(f"[green]✅ {t(name)} {t('completed')}[/green]")
        else:
            console.print(f"[red]❌ {t(name)} {t('failed')}[/red]")
            console.print(f"[bold red]❌ {t('step_failed')}[/bold red]")
            return
    
    console.print(f"\n[bold green]🎉 {t('init_done')}[/bold green]")

def add_specific_components(components: tuple):
    """Hàm xử lý cho lệnh 'shacnify add'."""
    if not Path("components.json").exists():
        console.print("[bold red]❌ Lỗi: Shadcn/UI chưa được khởi tạo.[/bold red]")
        console.print("   Vui lòng chạy [cyan]shacnify init[/cyan] trước.")
        return

    selected_components = list(components)

    if not selected_components:
        selected_components = steps._prompt_for_components()
    
    steps._install_components(selected_components)
    console.print(f"\n[bold green]✅ Thêm component hoàn tất![/bold green]")