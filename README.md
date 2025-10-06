# Shacnify CLI

A powerful, universal command-line tool to kickstart your projects with pre-configured templates and boilerplates, saving you from repetitive setup tasks.

The initial version focuses on scaffolding modern React projects (Vite, Next.js, CRA) with a complete Shadcn/UI and Tailwind CSS setup, but is designed to be easily extensible for other frameworks and languages like C#.

---
## Key Features

-   **Project Creation**: Scaffold a new project from scratch (`create` command).
-   **Project Enhancement**: Enhance an existing project with new features (`init` command).
-   **Multi-Framework Support**: Automatically detects and configures for **Vite**, **Next.js**, and **Create React App**.
-   **Smart Component Installation**: Interactively select Shadcn/UI components to add, or add them anytime with the `add` command.
-   **Recipes**: Use pre-defined "recipes" (`--recipe auth`, `--recipe dashboard`) to install a collection of components for common use-cases in one go.
-   **Configuration Management**: Remembers your preferences (default components, language) for a personalized experience.
-   **i18n Support**: The CLI interface is available in both English and Vietnamese.

---
## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/hoanghonghuy/shacnify-cli.git
    ```
    *(Remember to replace the URL with your actual repository URL)*

2.  Navigate into the project directory:
    ```bash
    cd shacnify-cli
    ```

3.  Install the tool in editable mode using pip. This makes the `shacnify` command available globally on your system.
    ```bash
    pip install -e .
    ```
    *(Note: You may need to add Python's Scripts directory to your system's PATH environment variable if the command is not found after installation.)*

---
## Usage

Once installed, you can use the `shacnify` command from any directory.

#### **Create a New Project from Scratch**

This is the most common use case. The tool will guide you through creating a new React project and setting up everything automatically.

```bash
shacnify create my-awesome-app
```
You can also use a recipe to pre-install a set of components:
```bash
shacnify create my-dashboard --recipe dashboard
```

#### **Enhance an Existing Project**
If you already have a React project, navigate into its root directory and run:
```bash
shacnify init
```

#### **Add Components Later**
You can add more Shadcn/UI components at any time.
```bash
# Add specific components
shacnify add dialog toast table

# Run in interactive mode to select from a list
shacnify add
```

#### **Manage Configuration**
Customize the tool to your liking.
```bash
# Set your favorite components to be pre-selected
shacnify config set default_components button,card,input,dialog,sonner

# Set your default language
shacnify lang set vi
```

---
## Future Roadmap
The vision for Shacnify is to become a true universal scaffolding tool. Future plans include:

-   Adding support for C# templates (e.g., ASP.NET Core API with pre-configured services, Console App with DI).
-   Adding support for other frontend frameworks (e.g., Vue, Svelte).
-   A plugin system to allow the community to add their own templates and recipes.
-   More advanced configuration options and pre-flight checks.

---
## License
This project is licensed under the MIT License. See the LICENSE file for details.