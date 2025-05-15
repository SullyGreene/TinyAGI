from TinyAGI.agent import AgentSystem

if __name__ == '__main__':
    agent = AgentSystem(config_files='Tests/ollama_agent_test.json')
    agent.run()
