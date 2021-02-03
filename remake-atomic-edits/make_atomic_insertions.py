import json
from progress.bar import Bar
from objects import BaseRevisedWikiHow
from get_insertions import get_consecutive_insertions

path_to_insertions = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/insertions.json"


with open(path_to_insertions, 'r') as json_in:
    wikihow_possible_insertions = json.load(json_in)


def main():
    #   def __init__(self, filename, revision_nr, base_sentence, revised_sentence):

    collection = []
    bar = Bar("Processing", max=len(wikihow_possible_insertions))
    for base_revision_pair in wikihow_possible_insertions:
        bar.next()

        base_revision_pair_object = BaseRevisedWikiHow(
            base_revision_pair["Filename"], 1, base_revision_pair["All_Versions"][0], base_revision_pair["All_Versions"][-1])
        insertions = base_revision_pair_object.get_possible_insertions()

        if insertions:
            consecutive_insertions = get_consecutive_insertions(insertions)

        if len(consecutive_insertions) == 1:
            entry = {"filename": base_revision_pair_object.filename,
                     "base_tokenized": base_revision_pair_object.base_tokenized,
                     "revised_tokenized": base_revision_pair_object.revised_tokenized,
                     "insertion_phrases": consecutive_insertions}

            collection.append(entry)
    bar.finish()

    print(len(collection))
    with open("WikiHowAtomicInsertionsTest.json", 'w') as json_out:
        json.dump(collection, json_out)

main() 
