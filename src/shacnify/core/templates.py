# src/shacnify/core/templates.py
import json

def get_tailwind_config_content(framework):
    content_paths = {
        "cra": '"./src/**/*.{js,jsx,ts,tsx}"',
        "vite": '"./index.html", "./src/**/*.{js,ts,jsx,tsx}"',
        "nextjs": '"./pages/**/*.{js,ts,jsx,tsx}", "./components/**/*.{js,ts,jsx,tsx}", "./app/**/*.{js,ts,jsx,tsx}"'
    }
    path = content_paths.get(framework, content_paths["cra"])
    
    return f"""/** @type {{import('tailwindcss').Config}} */
module.exports = {{
  darkMode: ["class"],
  content: [{path}],
  prefix: "",
  theme: {{
    container: {{
      center: true,
      padding: "2rem",
      screens: {{ "2xl": "1400px" }},
    }},
    extend: {{
      keyframes: {{
        "accordion-down": {{ from: {{ height: "0" }}, to: {{ height: "var(--radix-accordion-content-height)" }} }},
        "accordion-up": {{ from: {{ height: "var(--radix-accordion-content-height)" }}, to: {{ height: "0" }} }},
      }},
      animation: {{
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      }},
    }},
  }},
  plugins: [require("tailwindcss-animate")],
}}"""

def get_components_json_content(framework):
    css_file = "app/globals.css" if framework == "nextjs" else "src/index.css"
    is_app_dir = framework == "nextjs"
    
    config = {
        "$schema": "https://ui.shadcn.com/schema.json",
        "style": "default",
        "rsc": is_app_dir,
        "tsx": True,
        "tailwind": {
            "config": "tailwind.config.js",
            "css": css_file,
            "baseColor": "slate",
            "cssVariables": True
        },
        "aliases": {
            "components": "@/components",
            "utils": "@/lib/utils"
        }
    }
    return json.dumps(config, indent=2)

def get_app_tsx_content():
    """Template cho file App.tsx chính, chứa router."""
    return """import { Routes, Route, BrowserRouter } from "react-router-dom";
import MainLayout from "@/layouts/MainLayout";
import HomePage from "@/pages/HomePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<HomePage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
"""

def get_main_tsx_content():
    """Template cho file main.tsx, file khởi động của Vite."""
    return """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""

def get_main_layout_tsx_content():
    """Template cho layout chính."""
    return """import { Outlet } from "react-router-dom";

const MainLayout = () => {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <header className="container mx-auto py-4">
        {/* Header content goes here */}
      </header>
      <main className="container mx-auto flex-grow">
        <Outlet />
      </main>
      <footer className="container mx-auto py-4 mt-8 border-t">
        {/* Footer content goes here */}
      </footer>
    </div>
  );
};

export default MainLayout;
"""

def get_home_page_tsx_content():
    """Template cho trang chủ demo."""
    return """import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";

const HomePage = () => {
  return (
    <div className="flex flex-col items-center justify-center gap-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold tracking-tight lg:text-5xl">
          Chào mừng đến với Shacnify
        </h1>
        <p className="mt-4 text-lg text-muted-foreground">
          Dự án của bạn đã được cài đặt thành công với Shadcn/UI.
        </p>
      </div>
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Bắt đầu thôi!</CardTitle>
          <CardDescription>
            Chỉnh sửa file này tại{" "}
            <code className="px-1 py-0.5 bg-muted rounded font-mono text-sm">
              src/pages/HomePage.tsx
            </code>
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Button className="w-full">Đây là một Button</Button>
        </CardContent>
      </Card>
    </div>
  );
};

export default HomePage;
"""