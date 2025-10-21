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

### From PyPI

Get the stable core of TinyAGI in seconds with `pip`:

> **Note:** The PyPI package is currently on beta preview 0.0.2. For the latest features and updates, we recommend installing from GitHub.

<details>
  <summary>Show command</summary>

  ```bash
  pip install TinyAGI==0.0.2
  ```
</details>

### **From GitHub**

Clone and set up dependencies:

 > Recommended for latest reslease
<details>
  <summary>Show commands</summary>

  ```bash
  git clone https://github.com/SullyGreene/TinyAGI.git
  cd TinyAGI
  python setup_env.py
  ```

> **Note:** `setup_env.py` creates a `venv` environment `tinyagi_venv`, installs dependencies, and downloads necessary NLTK data.

</details>

---

## 🔧 **Setup Instructions**

1. **Clone the Repository**

   <details>
     <summary>Show commands</summary>

   ```bash
   git clone https://github.com/SullyGreene/TinyAGI.git
   cd TinyAGI
   ```
   </details>

2. **Set Up the Virtual Environment**

   Ensure Python 3.8+ is installed.

   <details>
     <summary>Show command</summary>

   ```bash
   python setup_env.py
   ```
   </details>

3. **Configure Environment Variables**

   Copy the example `.env` file and add your API keys.

   <details>
     <summary>Show commands</summary>

   ```bash
   cp .env.example .env
   ```
   </details>

4. **Run the Server**

   <details>
     <summary>Show command</summary>

   ```bash
   python start_server.py
   ```

   The server will be accessible at `http://localhost:5000`.

   </details>

---

## 🛠 **Usage**

### **Using the CLI**

Interact with TinyAGI through the command-line interface.

- **Generate Text**

   <details>
     <summary>Show command</summary>

   ```bash
   python -m TinyAGI.services.cli_manager generate --prompt "Tell me a joke."
   ```

   - **Options:**
       - `--prompt` or `-p`: The text prompt.
       - `--config` or `-c`: Path to a custom configuration file.
       - `--stream` or `-s`: Enable streaming output.

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
