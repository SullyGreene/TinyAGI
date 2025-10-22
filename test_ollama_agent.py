from TinyAGI.agent import AgentSystem

if __name__ == '__main__':
    agent = AgentSystem(config_files='config/ollama_agent_poem.json')
    agent.run()
