import string 
import pdb 

punctuation_to_exclude = string.punctuation + "``"


def filtering_patterns(individual_filler): 
    if len(individual_filler) == 0 or ('NFP' in individual_filler) or ('LS' in individual_filler) or ("XX" in individual_filler): 
        return "exclude"
    else: 
        # unigrams 
        if len(individual_filler) == 1: 
            if individual_filler[0] in punctuation_to_exclude or (individual_filler[0] == 'DET') or (individual_filler[0] == 'IN'): 
                return "exclude"
            else: 
                return "include"
            


        elif len(individual_filler) == 2: 
            if individual_filler[0] in punctuation_to_exclude  or (individual_filler == ['CD', '.']) or (individual_filler == ['IN', 'DT'] or (individual_filler == ['$', '$'])): 
                return "exclude"
            elif individual_filler[0] == 'DT' and individual_filler[1] in punctuation_to_exclude: 
                return "exclude"
            else: 
                return "include"
        else: 
            if 'XX' in individual_filler or (individual_filler[0] in punctuation_to_exclude) or ('IN' and 'DT' in individual_filler): 
                return "exclude"
            else: 
                return "include"  
    