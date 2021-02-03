import spacy
import difflib
import pdb
from collections import defaultdict

tagger = spacy.load("en_core_web_sm")
diff = difflib.Differ()


class BaseRevisionPair:
    def __init__(self, filename, revision_nr, base_sentence, revised_sentence):
        self.filename = filename
        self.revision_nr = revision_nr
        self.base_sentence = base_sentence
        self.revised_sentence = revised_sentence

    @property
    def base_tokenized(self):
        base_parsed = tagger(self.base_sentence.strip())
        return [token.text for token in base_parsed]

    @property
    def revised_tokenized(self):
        revised_parsed = tagger(self.revised_sentence.strip())
        return [token.text for token in revised_parsed]

    def get_possible_insertions(self):
        base_parsed = tagger(self.base_sentence.strip())
        base_tokenized = [token.text for token in base_parsed]

        revised_parsed = tagger(self.revised_sentence.strip())
        revised_tokenized = [token.text for token in revised_parsed]

        difference_getter = list(diff.compare(
            base_tokenized, revised_tokenized))

        insertions = [token.replace(
            "+", "").strip() for token in difference_getter if token.startswith('+') and token != '+']

        # check for duplicates
        duplicate_indexes = check_duplicates(revised_tokenized, insertions)

        if duplicate_indexes == {}:
            insertions_indexes = [(insertion, revised_tokenized.index(
                insertion)) for insertion in insertions if insertion in revised_tokenized]
            return insertions_indexes
        else:
            # i do nothing wirh insertions here
            insertions = []
            for index, token in enumerate(difference_getter):
                if token.startswith('+') and len(token.split()) > 1:
                    insertions.append((token.replace("+", "").strip(), index))
            return insertions


class BaseRevisedWikiHow(BaseRevisionPair):
    def __init__(self, filename, revision_nr, base_sentence, revised_sentence):
        super().__init__(filename, revision_nr, base_sentence, revised_sentence)


def check_duplicates(seq, insertions, use_check=True):
    """
        Check if there are duplicates in the insertions

        Arguments:
            seq {list}: the sequence that needs to be checked
            insertions {list}: list containing the insertions (all elements with +) provided by difflib
            use_check: "True" returns a those cases which have double indexes, False: returns a list with {listelem: {indexes}}
                        for all cases

    """
    tally = defaultdict(list)
    for i, item in enumerate(seq):
        tally[item].append(i)
    # if the list of locs is bigger than 1 (aka: there is more than one index) append to res.
    if use_check:
        res = [(key, locs) for key, locs in tally.items()
               if len(locs) > 1 and key in insertions]
        return {elem1: elem2 for elem1, elem2 in res}
    else:
        res = [(key, locs) for key, locs in tally.items()]
        return {elem1: elem2 for elem1, elem2 in res}
