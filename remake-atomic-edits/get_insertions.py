from revision_object import BaseRevisionPair
import difflib
import pdb
import json


def to_json(filename, object_to_dump):
    with open(filename, 'w') as json_out:
        json.dump(object_to_dump, json_out)


def to_csv(filename, object_to_dump):
    with open(filename, 'w') as tsv_out:
        for elem in object_to_dump:
            insertion_phrases = [' '.join(phrase)
                                 for phrase in elem['insertion_phrases']]
            line_to_write = "{0}\t{1}\t{2}\n".format(' '.join(elem["base_tokenized"]), ' '.join(
                elem["revised_tokenized"]), ' '.join(insertion_phrases))
            tsv_out.write(line_to_write)


def naive_insertions(base_tokenized, revised_tokenized):
    unique_tokens_from_base = list(set(base_tokenized))
    possible_insertions_in_revision = [
        token for token in revised_tokenized if token not in unique_tokens_from_base]
    print(possible_insertions_in_revision)


def get_consecutive_insertions(list_of_insertions):
    """
        Given a list of insertions i.e., [('Rank',11) ('after',12), ('that',13)]
        Return a list with [] elements where consecutive words are togeteher: [['Rank', 'after', 'that']]
    """
    # initialize with the first word
    # initialize the index
    if len(list_of_insertions) == 1:
        return [[list_of_insertions[0][0]]]
    else:
        # initialize to the first index
        chunks = [[list_of_insertions[0][0]]]
        final_chunks_list = []
        index = 0
        for i in range(len(list_of_insertions)-1):
            if abs(list_of_insertions[i][1]-list_of_insertions[i+1][1]) == 1:
                # print("values with absolute distance")
                chunks[index].append(list_of_insertions[i+1][0])
            else:
                final_chunks_list.append(chunks)
                # chunks = []
                chunks.append([list_of_insertions[i+1][0]])
                # print(chunks)
                # print(final_chunks_list)
                index += 1

        # print("final chunks")
        if final_chunks_list != []:
            return final_chunks_list[-1]
        else:
            return chunks


def main():
    collection = []
    for line in data:
        # print(nr)
        line = line.strip()
        filename, revision_name, base_sentence, revised_sentence = line.split(
            '\t')
        # get everything that is in revision but not in base
        base_revised_pair = BaseRevisionPair(
            filename, revision_name, base_sentence, revised_sentence)
        base_tokenized = base_revised_pair.base_tokenized
        revised_tokenized = base_revised_pair.revised_tokenized

        # check if the revised sentence length is bigger than the base sentence length

        if len(revised_tokenized) > len(base_tokenized):

            insertions = base_revised_pair.get_possible_insertions()

            consec_insertions = get_consecutive_insertions(insertions)
            entry = {"filename": filename,
                     "base_tokenized": base_tokenized,
                     "revised_tokenized": revised_tokenized,
                     "base_sentence": base_sentence,
                     "revised_sentence": revised_sentence,
                     "insertions": insertions,
                     "insertion_phrases": consec_insertions,
                     "num_of_inserion_phrases": len(consec_insertions)}
            collection.append(entry)
    #to_json("./processed_files/boardgame_insertion_phrases.json", collection)
    #to_csv("./processed_files/boardgame_insertion_phrases.tsv", collection)


if __name__ == "__main__":
    with open('../boardgame_diffs.tsv', 'r') as file_in:
        data = file_in.readlines()
    main()
