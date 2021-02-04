# file to put the objects in 

class CorefChain: 

    def __init__(self, coreference_chain_in_dict): 
        self.coreference_in_instance = coreference_chain_in_dict
    
    @property 
    def chainlength(self): 
        return len(self.coreference_in_instance)
    
    @property
    def sortedchain(self): 
        return sorted(self.coreference_in_instance, key=lambda x:x['sentenceIndex'], reverse=True)

    # returns the distance between the revised sentence and the previous mention 
    @property 
    def distance_to_reference(self): 
        sorted_chain = sorted(self.coreference_in_instance, key=lambda x:x['sentenceIndex'], reverse=True)
        distance = sorted_chain[0]['sentenceIndex'] - sorted_chain[1]['sentenceIndex']
        return distance
    

