# This script was previously used to make WikiHowAtomicInsertions


import json
from progress.bar import Bar
import nltk

path_to_insertions = '../../../PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/insertions.json'

with open(path_to_insertions, 'r') as json_in:
    wikihow_possible_insertions = json.load(json_in)


def main():
    collection = []
    bar = Bar("Processing", max=len(wikihow_possible_insertions))
    for base_revision_pair in wikihow_possible_insertions:
        bar.next()

        if len(base_revision_pair["All_Versions"]) > 2:
            # take the sentence before the revised sentence
            previous_version = base_revision_pair["All_Versions"][-2]
        else:
            # take the first sentence
            previous_version = base_revision_pair["All_Versions"][0]

        # use only the previous version
        base_revision_pair_object = BaseRevisedWikiHow(
            base_revision_pair["Filename"], base_revision_pair["Key"], previous_version, base_revision_pair["All_Versions"][-1])
        insertions = base_revision_pair_object.get_possible_insertions()

        if insertions:
            consecutive_insertions = get_consecutive_insertions(insertions)

            if len(consecutive_insertions) == 1:
                entry = {"filename": base_revision_pair_object.filename,
                         "base_tokenized": base_revision_pair_object.base_tokenized,
                         "id": base_revision_pair_object.revision_nr,
                         "revised_tokenized": base_revision_pair_object.revised_tokenized,
                         "revised_sentence": base_revision_pair_object.revised_sentence,
                         "insertion_phrases": consecutive_insertions}

                collection.append(entry)
    bar.finish()

    #with open("WikiHowAtomicInsertions.json", 'w') as json_out:
    #    json.dump(collection, json_out)


if __name__ == "__main__":
    import sys
    sys.path.append('../')
    from objects.revision_object import *
    from get_insertions import get_consecutive_insertions
    main()
