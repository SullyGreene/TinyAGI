import TinyAGI as agi

if __name__ == '__main__':
    agent = agi.AgentSystem(config_files='config/ollama_agent_poem.json')
    agent.run()