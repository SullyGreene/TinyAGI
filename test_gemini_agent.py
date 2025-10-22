from TinyAGI.agent import AgentSystem

if __name__ == '__main__':
    print("Running Gemini Agent Test...")
    agent_system = AgentSystem(config_files='config/gemini_agent_test.json')
    agent_system.run()
