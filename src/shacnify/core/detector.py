# src/shacnify/core/detector.py
import json
from pathlib import Path

def detect_framework():
    """Phát hiện framework của dự án hiện tại."""
    if Path("next.config.js").exists():
        return "nextjs"
    if Path("vite.config.js").exists() or Path("vite.config.ts").exists():
        return "vite"
    
    package_json_path = Path("package.json")
    if package_json_path.exists():
        content = json.loads(package_json_path.read_text(encoding='utf-8'))
        if "react-scripts" in content.get("dependencies", {}) or "react-scripts" in content.get("devDependencies", {}):
            return "cra"
            
    return None