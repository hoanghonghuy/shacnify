# src/shacnify/core/planner.py
from pathlib import Path
from rich.table import Table
from rich.console import Console

console = Console()

class Plan:
    def __init__(self, framework, safe_mode=False):
        self.framework = framework
        self.safe_mode = safe_mode
        self.actions = []
        self._generate()

    def _generate(self):
        """Phân tích dự án và xây dựng danh sách các hành động."""
        # Kế hoạch cho các file cấu hình
        self._plan_config_files()
        
        # Kế hoạch cho việc tái cấu trúc 'src'
        if not self.safe_mode:
            self._plan_src_restructure()

    def _plan_config_files(self):
        tailwind_config = Path("tailwind.config.js")
        if not tailwind_config.exists() or not self.safe_mode:
            action = "OVERWRITE" if tailwind_config.exists() else "CREATE"
            self.actions.append((action, "tailwind.config.js", "File cấu hình Tailwind"))

        # Tương tự cho các file khác nếu cần...

    def _plan_src_restructure(self):
        # Liệt kê các file sẽ bị ảnh hưởng
        if Path("src/App.tsx").exists():
            self.actions.append(("DELETE", "src/App.tsx", "File App component mặc định"))
        if Path("src/App.css").exists():
            self.actions.append(("DELETE", "src/App.css", "File CSS của App mặc định"))
        
        self.actions.append(("CREATE", "src/layouts/", "Thư mục Layouts"))
        self.actions.append(("CREATE", "src/pages/", "Thư mục Pages"))
        self.actions.append(("OVERWRITE", "src/main.tsx", "File khởi động ứng dụng"))

    def display(self):
        """Hiển thị kế hoạch cho người dùng xem."""
        if not self.actions:
            console.print("[green]🔍 Dự án đã được cấu hình. Không có thay đổi nào cần thực hiện.[/green]")
            return

        table = Table(title="[bold cyan]Kế hoạch thực thi của Shacnify[/bold cyan]")
        table.add_column("Hành động", style="yellow")
        table.add_column("Đối tượng", style="magenta")
        table.add_column("Mô tả", style="white")

        for action, target, description in self.actions:
            style = "green"
            if action == "OVERWRITE":
                style = "yellow"
            elif action == "DELETE":
                style = "bold red"
            table.add_row(f"[{style}]{action}[/]", target, description)
        
        console.print(table)