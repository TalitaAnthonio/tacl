import pandas as pd 
import math 
import pdb 

def make_filtered_df(df, list_with_keys, path_name): 
    df = df[df["Input.id"].isin(list_with_keys)]
    df.to_csv(path_name, sep='\t')



def main(): 
    #to_exclude_for_now = ["Do_a_Mountain_Bike_Bunny_Hop35", "Get_Your_Husband_to_Stop_Looking_at_Porn48", 
    #"Use_an_External_Flash9", "Accept_Yourself_As_Bisexual9"]
    

    # take the ones that have to be done again out. 
    df = pd.read_csv("aliki_annotations_latest_new.tsv", sep='\t')
    #df = df[~df["Input.id"].isin(to_exclude_for_now)]

    # ['Input.id', 'Input.Line2', 'Input.Answer1', 'Input.Answer2',
    #   'Input.Context2', 'Input.Line1', 'Input.Context1', 'Input.Info',
    #   'Input.Differences', 'Input.Title', 'Input.human-inserted-or-not',
    #   'Input.CorrectReference', 'Answer.annotation-answer.answer-base',
    #   'Answer.annotation-answer.answer-not-sure',
    #   'Answer.annotation-answer.answer-revised', 'Answer.annotation-comments',
    #   'Approve', 'Reject'],

    equally_good_collection = []
    none_fit_collection = []
    
    # collect those where the human-inserted is not in there 
    not_human_inserted = []
    not_human_inserted_equally_good = []
    not_human_inserted_none_fit = []
    not_human_inserted_first_pred_better = []
    not_human_inserted_second_pred_better = []



    # collect those where human-inserted is in there. 
    human_inserted = []
    human_inserted_equally_good = []
    human_inserted_none_fit = []
    human_inserted_human_better = []
    human_inserted_other_better = []
    for index, row in df.iterrows():
        # check how many there are with "equally good"
        equally_good = row["Answer.annotation-answer.answer-not-sure"]
        first_answer_from_user = row["Answer.annotation-answer.answer-base"] 
        second_answer_from_user = row["Answer.annotation-answer.answer-revised"]
        info = row["Input.Info"]
        setting = row["Input.human-inserted-or-not"]


        # check in which setting the inpiut belonhs 
        if setting == "not-human-inserted": 
           not_human_inserted.append(row["Input.id"])
           if equally_good == True: 
                comment = str(row["Answer.annotation-comments"])
                if comment != "nan":
                    not_human_inserted_none_fit.append(row["Input.id"]) 
                else: 
                    not_human_inserted_equally_good.append(row["Input.id"])
           else: 
                if info == "answer1-first" and first_answer_from_user == True: 
                    not_human_inserted_first_pred_better.append(row["Input.id"])
                
                elif info == "answer2-first" and second_answer_from_user == True: 
                    not_human_inserted_first_pred_better.append(row["Input.id"])
                else:
                    not_human_inserted_second_pred_better.append(row["Input.id"]) 


        else: 
            human_inserted.append(row["Input.id"])
            # check for equally good 
            if equally_good == True: 
                comment = str(row["Answer.annotation-comments"])
                if comment != "nan":
                    human_inserted_none_fit.append(row["Input.id"]) 
                else: 
                    human_inserted_equally_good.append(row["Input.id"])

            else: 
                if info == "answer1-first" and first_answer_from_user == True: 
                    human_inserted_human_better.append(row["Input.id"])
                
                elif info == "answer2-first" and second_answer_from_user == True: 
                    human_inserted_human_better.append(row["Input.id"])
                else:
                    human_inserted_other_better.append(row["Input.id"]) 

                    

    make_filtered_df(df, not_human_inserted_equally_good, "equally-good-not-human.csv")
    
    

    # check the results for human inserted 
    print("============ human inserted =============================")
    print("total human inserted", len(human_inserted))
    print("human = better", len(human_inserted_human_better))
    print("other = better", len(human_inserted_other_better))
    print("none fit", len(human_inserted_none_fit))
    print("equally good", len(human_inserted_equally_good))

    print("========= not human inserted =============================")
    print("total not human inserted", len(not_human_inserted))
    print("total equally good", len(not_human_inserted_equally_good))
    print("total none fit", len(not_human_inserted_none_fit))
    print("first pred is better", len(not_human_inserted_first_pred_better))
    print("second pred is better", len(not_human_inserted_second_pred_better))




main()