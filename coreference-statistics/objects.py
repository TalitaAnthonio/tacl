# file to put the objects in 

class CorefChain: 

    def __init__(self, coreference_chain_in_dict): 
        self.coreference_in_instance = coreference_chain_in_dict
    
    @property 
    def chainlen(self): 
        return len(self.coreference_in_instance)
    
    