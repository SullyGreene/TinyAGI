<p align="center">
  <img src="https://raw.githubusercontent.com/SullyGreene/TinyAGI/refs/heads/main/Static/logo.png" alt="TinyAGI Logo">
</p>


# 🧠 TinyAGI

**TinyAGI** is a powerful, modular Artificial General Intelligence (AGI) framework crafted for seamless integration and management of AI agents, plugins, and tools. With its adaptable and extensible architecture, TinyAGI enables dynamic loading of components from local and GitHub-hosted sources, empowering you to customize and scale for a multitude of use cases. It's designed to be lightweight, easy to understand, and highly extensible.

[![PyPI Version](https://img.shields.io/pypi/v/TinyAGI)](https://pypi.org/project/TinyAGI/) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/SullyGreene/TinyAGI/blob/main/LICENSE) [![GitHub Stars](https://img.shields.io/github/stars/SullyGreene/TinyAGI?style=social)](https://github.com/SullyGreene/TinyAGI/stargazers) [![Twitter Follow](https://img.shields.io/twitter/follow/SullyGreene?style=social)](https://twitter.com/SullyGreene)

> **Disclaimer:** This is a **preview release** (version 0.0.2) of **TinyAGI**, which is currently under active development. This release is intended for **testing, feedback, and early experimentation**. Please be aware that the API is subject to change, and frequent updates are expected.

---

## 📖 **Table of Contents**

- [🧩 Features](#-features)
- [📦 Installation](#-installation)
- [🔧 Setup Instructions](#-setup-instructions)
- [🛠️ Usage](#-usage)
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
  - 📑 **Comprehensive Documentation**: Easily accessible Markdown files for every component.
  - 🔥 **Robust Error Handling**: Advanced logging and error management for smooth operation.

---

## 📦 Installation

The recommended way to install TinyAGI for the latest features is by cloning the repository from GitHub.

### **1. Clone the Repository**

```bash
git clone https://github.com/SullyGreene/TinyAGI.git
cd TinyAGI
```

### **2. Run the Installation Script**

The installation script will set up a dedicated virtual environment, install all dependencies, download required NLTK data, create a `.env` file from the example, and move the project to a fixed installation location (default `C:\TinyAGI`).

<details>
  <summary><b>For Windows</b></summary>

  Simply run the Windows batch script. It will automatically create a local virtual environment and install all dependencies.
  ```batch
  installation_windows.bat
  ```
  The script will install TinyAGI to `C:\TinyAGI` by default. You can customize this path by creating a `config\windows_installation.ini` file in the cloned directory *before* running the script, and setting `custom_install_path=Your\Desired\Path`.
  The script will also offer to add an `agi` command alias to your system PATH for easy access to the CLI.
  **Note:** Run this script from a temporary location after cloning, as it will move the project files to the designated installation directory.
  ```
  The script will install TinyAGI to `C:\TinyAGI` by default. You can customize this path by creating a `config\windows_installation.ini` file in the cloned directory *before* running the script, and setting `custom_install_path=Your\Desired\Path`.
  The script will also offer to add an `agi` command alias to your system PATH for easy access to the CLI.
  **Note:** Run this script from a temporary location after cloning, as it will move the project files to the designated installation directory.
  ```
</details>

<details>
  <summary><b>For macOS / Linux</b></summary>

  Run the shell script to set up the environment and install dependencies.
  ```bash
  chmod +x installation_unix.sh
  ./installation_unix.sh
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

Access comprehensive documentation in the [`Documents/`](https://github.com/SullyGreene/TinyAGI/tree/main/Documents) directory.

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

---
