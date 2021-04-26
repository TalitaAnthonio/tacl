import json 
import pdb 
from pprint import pprint 

path = "dev-set-coreferenced.json"

# 'filler1', 'filler2', 'filler3', 'filler4', 'filler5', 'filler6', 'filler7', 'filler8', 'filler9', 'filler10', 'filler11', 'filler12', 'filler13', 'filler14', 'filler15', 'filler16', 'filler17', 'filler18', 'filler19', 'filler20', 'filler21', 'filler22', 'filler23', 'filler24', 'filler25', 'filler26', 'filler27', 'filler28', 'filler29']

def read_json_lines(path_to_json_lines):
    d = {} 
    with open(path_to_json_lines) as json_lines_file: 
         for line in json_lines_file: 
             line = json.loads(line)
             d[line['id']] = line
             
    return d 


class DevelopmentInstance: 

    def __init__(self, instance): 
        self.instance = instance
        self.num_fillers = len(self.instance.keys())-1
        self.id = instance['id']


    def parse_coref(self): 
        for filler, _ in self.instance.items(): 
            print(self.instance[filler])
            #print(self.instance[filler]['sents'])

            print("============")
    





def main(): 
    development_set_coreferenced = read_json_lines(path)

    for key, _ in development_set_coreferenced.items(): 
        pprint(development_set_coreferenced[key].keys())
        dev_object = DevelopmentInstance(development_set_coreferenced[key])
        print(dev_object.num_fillers)
        print(dev_object.id)
        dev_object.parse_coref()
        break 
        #pdb.set_trace()

main()