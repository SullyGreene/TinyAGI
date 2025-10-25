# 🧠 TinyAGI

**TinyAGI** is a powerful, modular Artificial General Intelligence (AGI) framework crafted for seamless integration and management of AI agents, plugins, and tools. With its adaptable and extensible architecture, TinyAGI enables dynamic loading of components from local and GitHub-hosted sources, empowering you to customize and scale for a multitude of use cases. It's designed to be lightweight, easy to understand, and highly extensible.

[![PyPI Version](https://img.shields.io/pypi/v/TinyAGI)](https://pypi.org/project/TinyAGI/) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/SullyGreene/TinyAGI/blob/main/LICENSE) [![GitHub Stars](https://img.shields.io/github/stars/SullyGreene/TinyAGI?style=social)](https://github.com/SullyGreene/TinyAGI/stargazers) [![Twitter Follow](https://img.shields.io/twitter/follow/SullyGreene?style=social)](https://twitter.com/SullyGreene)

> **Disclaimer:** This is a **preview release** (version 0.0.2) of **TinyAGI**, which is currently under active development. This release is intended for **testing, feedback, and early experimentation**. Please be aware that the API is subject to change, and frequent updates are expected.

---

## 📖 **Table of Contents**

- [🧩 Features](#-features)
- [📦 Installation](#-installation)
- [🔧 Setup Instructions](#-setup-instructions)
- [🛠️ Usage](#️-usage)
  - [Interactive CLI](#interactive-cli)
  - [Direct Commands](#direct-commands)
  - [API Server](#api-server)
  - [Programmatic Usage](#programmatic-usage)
- [📚 Documentation](#-documentation)
- [🧪 Testing](#-testing)
- [📝 Contributing](#-contributing)
- [🛡 License](#-license)
- [📞 Contact](#-contact)
- [🗺️ Roadmap](#-roadmap)

---

## 🧩 Features
  
  - 🌐 **Agent System**: Manage various AI agents, from OpenAI to Ollama and LLaMA.
  - 🔌 **Plugin Manager**: Seamlessly expand functionality with versatile plugins.
  - 🛠 **Tool Integration**: Use tools like the Wikipedia API to enhance capabilities.
  - 🔄 **Dynamic Loading**: Load components locally or clone from GitHub repositories on the fly.
  - 🚀 **Task Automation**: Orchestrate agents, plugins, and tools to define and execute complex tasks.
  - 🖥️ **Dual Interface**: Interact via a feature-rich interactive CLI or a RESTful API server.
  - 📑 **Comprehensive Documentation**: Easily accessible Markdown files for every component.
  - 🔥 **Robust Error Handling**: Advanced logging and error management for smooth operation.

---

## 📦 Installation

The recommended way to install TinyAGI is by using the installation scripts, which automate the entire process from downloading the code to setting up the environment.
The installation script will handle everything:
- Check for prerequisites (Git, Python).
- Clone the project to a fixed location (`C:\TinyAGI` on Windows).
- Create a dedicated virtual environment.
- Install all required dependencies.
- Create a default `.env` file for your API keys.

### **1. Clone the Repository**

First, clone the repository to your local machine:
```bash
git clone https://github.com/SullyGreene/TinyAGI.git
cd TinyAGI
```

### **2. Run the Installation Script**

<details>
  <summary><b>For Windows</b></summary>

  Run the `install.bat` script. It will check for prerequisites (Git, Python), set up a virtual environment, install dependencies, and create a default `.env` file.
  ```batch
  install.bat
  ```
  The script will install TinyAGI to `C:\TinyAGI` by default. You can customize this path by creating a `config\windows_installation.ini` file in the cloned directory *before* running the script, and setting `custom_install_path=Your\Desired\Path`.
  The script will also offer to add an `agi` command alias to your system PATH for easy access to the CLI.
  **Note:** Run this script from a temporary location after cloning, as it will move the project files to the designated installation directory.

</details>

<details>
  <summary><b>For macOS / Linux</b></summary>

  Run the shell script to set up the environment and install dependencies.
  ```bash
  chmod +x install.sh
  ./install.sh
  ```
</details>

### **3. Configure Environment Variables**

After the installation script completes, a `.env` file will be created in the root directory. Open this file and add your API keys (e.g., for OpenAI, Gemini) to enable the corresponding agents.

```env
# .env
OPENAI_API_KEY="your-key-here"
GEMINI_API_KEY="your-key-here"
```

---

## 📖 Programmatic Usage

You can easily integrate `TinyAGI` into your own Python projects. The core of the framework is the `AgentSystem`, which orchestrates agents, plugins, and tools to execute tasks defined in a configuration file.

Here is a basic example of how to run the agent system from a Python script:

```python
import TinyAGI as agi
import os

def main():
    # Ensure the config path is correct relative to your script
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'agent_config.json')
    
    # Initialize and run the agent system
    agent_system = agi.AgentSystem(config_files=config_path)
    agent_system.run()

if __name__ == '__main__':
    main()
```

## 🛠 **Usage**

### **Running the Interactive CLI**

<details>
  <summary><b>For Windows</b></summary>
  
  ```batch
  cli.bat
  ```
</details>

<details>
  <summary><b>For macOS / Linux</b></summary>

  ```bash
  poetry run cli
  ```
</details>

This will start the interactive CLI, where you can use the following commands:

- `generate`: Generate text from a prompt.
- `config`: Display current configuration.
- `exit`: Exit the CLI.

### **Starting the Server**

<details>
  <summary><b>For Windows</b></summary>
  
  ```batch
  start_server.bat
  ```
</details>

<details>
  <summary><b>For macOS / Linux</b></summary>
  
  ```bash
  poetry run start
  ```
</details>

### **Accessing the API**

- **Chat Endpoint**

   <details>
     <summary>Show command</summary>

   ```bash
   curl -X POST http://localhost:5000/chat \
        -H "Content-Type: application/json" \
        -d '{"messages": [{"role": "user", "content": "Hello!"}], "stream": false}'
   ```
   </details>

- **Generate Text Endpoint**

   <details>
     <summary>Show command</summary>

   ```bash
   curl -X POST http://localhost:5000/generate \
        -H "Content-Type: application/json" \
        -d '{"prompt": "Write a short story about a dragon.", "stream": false}'
   ```
   </details>

- **Embed Endpoint**

   <details>
     <summary>Show command</summary>

   ```bash
   curl -X POST http://localhost:5000/embed \
        -H "Content-Type: application/json" \
        -d '{"input": "Sample text for embedding."}'
   ```
   </details>

---

## 📚 **Documentation**

Access comprehensive documentation in the `README.md` files in each directory.

---

## 🧪 **Testing**

Run TinyAGI tests to verify functionality.

### **Testing Ollama**

   <details>
     <summary>Show command</summary>

   ```bash
   python test_ollama_agent.py
   ```

   - **Expected Output**:

      ```
      Response from OllamaAgent:
      The capital of France is Paris.
      ```

   - **Troubleshooting Tips**:
      - Ensure the Ollama server is running at `http://localhost:11434`.
      - Confirm correct API keys and authentication.

   </details>

---

## 🧪 **Testing**

Run the test suite to ensure all components are working correctly. Make sure you have installed the development dependencies with `poetry install`.

   <details>
     <summary>Show command</summary>

   ```sh
   poetry run pytest
   ```

   </details>

---

## 📝 **Contributing**

Join the TinyAGI community by contributing your code, ideas, or feedback!

1. **Fork the Repository**

   <details>
     <summary>Show commands</summary>

   ```bash
   git checkout -b feature/YourFeatureName
   ```
   </details>

2. **Commit Your Changes**

   <details>
     <summary>Show command</summary>

   ```bash
   git commit -m "Add feature: YourFeatureName"
   ```
   </details>

3. **Push to Your Fork**

   <details>
     <summary>Show command</summary>

   ```bash
   git push origin feature/YourFeatureName
   ```
   </details>

4. **Submit a Pull Request**

---

## 🛡 **License**

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

---

## 📞 **Contact**

💬 **Get in Touch**

- **X (formerly Twitter)**: [@SullyGreene](https://twitter.com/SullyGreene)
- **GitHub**: [SullyGreene](https://github.com/SullyGreene)
- **PyPI**: [TinyAGI on PyPI](https://pypi.org/project/TinyAGI/)

---

## 🗺️ **Roadmap**

TinyAGI’s vision includes scaling to meet diverse AI needs. Here’s what’s planned:

<details>
  <summary>Phase 1: Core Enhancements 🚀</summary>

- **Agent Expansion**: Support additional agents and tools for specific domains.
- **Plugin Ecosystem**: Expand with plugins for data analysis, visual generation, and task-specific fine-tuning.
- **Advanced Error Handling**: Improve diagnostic logs and error handling.

</details>

<details>
  <summary>Phase 2: Advanced Task Orchestration 🤖</summary>

- **Multi-Agent Collaboration**: Enable agents to collaborate on complex tasks.
- **Task Scheduling & Automation**: Automate recurring actions and analysis.
- **Smart Prompting**: Dynamic prompt optimization for better task performance.

</details>

<details>
  <summary>Phase 3: Enhanced API and Developer Experience 🛠️</summary>

- **API V2**: Improve task queueing, agent behavior management, and access controls.
- **Interactive Documentation**: Launch an interactive portal with live code examples.
- **CLI Improvements**: Add user-friendly CLI commands.

</details>

<details>
  <summary>Phase 4: Ecosystem & Community Growth 🌍</summary>

- **Plugin Marketplace**: Set up a community-driven marketplace for plugins.
- **TinyAGI Hub**: A central hub for resources, tutorials, and community feedback.

</details>

<details>
  <summary>Phase 5: Scalability and Enterprise-Readiness 🏢</summary>

- **Distributed Agent Management**: Support for multi-server deployments.
- **Performance Optimization**: Improve resource use for concurrent agent management.
- **Enterprise Security**

: Enhanced data encryption and access control.

</details>
