import string 

punctuation_to_exclude = string.punctuation + "``"


def filtering_patterns(individual_filler): 
    if individual_filler[0] == '.' or ('LS' in individual_filler or 'NFP' in individual_filler) or (individual_filler == ['CD', '.']) or (individual_filler == ['IN', 'DT'] or (individual_filler == ['$', '$'])): 
          return "exclude"
    elif individual_filler[0] == 'DT' and individual_filler[1] in punctuation_to_exclude: 
          return "exclude"
    else: 
        return "include"

           