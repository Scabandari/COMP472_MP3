import itertools
import json
import string


base_dictionary = {}
alphabets_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
            'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v',
            'w', 'x', 'y', 'z', ' ']
# mix in a space to counts for the appearance of single letter (eg." I ") as well as starting and ending letters

for i, j in itertools.product(alphabets_list, alphabets_list):
    base_dictionary[i + j] = 0
base_dictionary.pop('  ', None)  # removes the "  " double space instance because that's not part of any word
# print(base_dictionary)


def model_output(language_combined_txt, language):
    translator = str.maketrans(string.punctuation, ' '*len(string.punctuation))  # to replace all punctuation by space

    language_bigram_dictionary = base_dictionary
    with open(language_combined_txt) as file:

        data = file.readlines()
        # print(len(data))
        for line in data:
            # print(line)
            newline = line.translate(translator)
            for char in range(1, len(newline)):
                try:
                    language_bigram_dictionary[newline[char-1].lower() + newline[char].lower()] += 1
                except KeyError:
                    pass  # welcome to exception programming
    file.close()

    total_bigram_occurance = sum(language_bigram_dictionary.values())

    with open('bigram'+language+'.txt', 'w') as bigram_model_file:
        for key in language_bigram_dictionary:
            probability= "P("+key[1]+"|"+key[0]+"): "+str(language_bigram_dictionary[key]/total_bigram_occurance)+"\n"
            # print(probability)
            bigram_model_file.write(probability)
    bigram_model_file.close()

    with open('bigram' + language + '.json', 'w') as bigram_model_JSON_file:
        bigram_model_JSON_file.write(json.dumps(language_bigram_dictionary))
    bigram_model_JSON_file.close()

    return language_bigram_dictionary


def bigram_by_language(sentence):
    """
    Relies on the existence of bigram model json files. If they don't exist for a specific language A, run
        model_output(trainA.txt, A)
        where the file trainA.txt is the combined corpora for the language
    :param sentence: string of sentence in unknown language
    :return: language_approximation:
    """
    # refer to slide 6 NLP page 41
    # the algorithm is log(P(c))+sum(log(P(w|c)))
    # P(c) is 1/3, P(w|c) is the values in the language's bigram model file
    # smoothing using add-delta with delta=0.5, |vocabulary| = (27*27-1)/2 = 364
    pass


if __name__ == "__main__":
    LANGUAGE = 'OT'
    language_combined_text = 'train' + LANGUAGE + '.txt'
    language_model = model_output(language_combined_text, LANGUAGE)
    print(language_model)