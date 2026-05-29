class AgentHarness:
    
    def __init__(self, world, llm):
        self.world = world
        self.llm = llm
        
    def run(self):
        while True:
            observation = self.world.observe()
            
            action = self.llm.choose_action(observation)
            
            self.world.step(action)