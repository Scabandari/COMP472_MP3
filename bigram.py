import itertools
import json
import string
import math

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

translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))  # to replace all punctuation by space


def model_output(language_combined_txt, language):
    language_bigram_dictionary = base_dictionary
    with open(language_combined_txt) as file:

        data = file.readlines()
        # print(len(data))
        for line in data:
            # print(line)
            newline = line.translate(translator)
            for char in range(1, len(
                    newline)):  # TODO this doesn't consider the very first letter of this corpora, must add it after this for loop to key "space+letter"
                try:
                    language_bigram_dictionary[newline[char - 1].lower() + newline[char].lower()] += 1
                except KeyError:
                    pass  # welcome to exception programming
    file.close()

    total_bigram_occurance = sum(language_bigram_dictionary.values())

    with open('bigram' + language + '.txt', 'w') as bigram_model_file:
        for key in language_bigram_dictionary:
            probability = "P(" + key[1] + "|" + key[0] + "): " + str(
                language_bigram_dictionary[key] / total_bigram_occurance) + "\n"
            # print(probability)
            bigram_model_file.write(probability)
    bigram_model_file.close()

    with open('bigram' + language + '.json', 'w') as bigram_model_JSON_file:
        bigram_model_JSON_file.write(json.dumps(language_bigram_dictionary))
    bigram_model_JSON_file.close()

    return language_bigram_dictionary


def bigram_by_language(sentence, sol_file_name=None):
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
    if type(sentence) is tuple:
        sentence = sentence[0]
    # for letter in sentence:
    #     letter = letter.lower()
    sentence = sentence.lower()
    sentence = sentence.rstrip()

    DELTA = 0.5
    VOCAB = len(alphabets_list)*len(alphabets_list)
    print(VOCAB)
    P_c = math.log10(1 / 3)

    new_sentence = sentence.translate(translator)  # get rid of punctuations
    # print(new_sentence)

    results = {}
    # load language bigram models
    with open('bigramEN.json') as modelfile:
        bigram = json.loads(modelfile.read())
        results['EN'] = {'bigram_model': bigram, 'probability': P_c, 'sum': sum(bigram.values()) + VOCAB}
        modelfile.close()
    # print(bigram_EN)
    with open('bigramFR.json') as modelfile:
        bigram = json.loads(modelfile.read())
        results['FR'] = {'bigram_model': bigram, 'probability': P_c, 'sum': sum(bigram.values()) + VOCAB}
        modelfile.close()
    # print(bigram_FR)
    with open('bigramOT.json') as modelfile:
        bigram = json.loads(modelfile.read())
        results['OT'] = {'bigram_model': bigram, 'probability': P_c, 'sum': sum(bigram.values()) + VOCAB}
        modelfile.close()
    # print(bigram_OT)

    if sol_file_name is None:
        file_name = 'out_test.txt'
    else:
        file_name = sol_file_name
    with open(file_name, 'a') as writefile:
        writefile.write('BIGRAM MODEL:\n')

        for i in range(1, len(new_sentence)):
            bigram = new_sentence[i - 1] + new_sentence[i]
            if bigram == "  ":
                continue

            writefile.write("\nBIGRAM: \"" + bigram + "\"\n")
            for language in results:
                P_w_c = math.log10((results[language]['bigram_model'][bigram] + DELTA)/results[language]['sum'])
                results[language]['probability'] += P_w_c
                writefile.write(language+": P("+bigram[1]+"|"+bigram[0]+") = " + str(P_w_c)+"---->> log prob of sentence so far: " + str(results[language]['probability'])+"\n")
        placeholder = -9999999999.99999
        best_guess = ''
        for language in results:
            if results[language]['probability']>placeholder:
                best_guess=language
                placeholder = results[language]['probability']

        writefile.write("According to the Bigram model, the sentence is in " + best_guess)
        writefile.close()
        return best_guess
    pass


if __name__ == "__main__":
    # LANGUAGE = 'OT'
    # language_combined_text = 'train' + LANGUAGE + '.txt'
    # language_model = model_output(language_combined_text, LANGUAGE, 'bigram_experiment_')
    # print(language_model)
    from utils import get_sentences
    sentences_list = []
    sentences_file = 'experiment2_sentences.txt'
    get_sentences(sentences_file, sentences_list)


    with open('bigram_experiment.txt', 'a') as writefile:
        for i in range(len(sentences_list)):
            guess = bigram_by_language(sentences_list[i][0], sol_file_name=str(i)+'bigram_test.txt', model_filename='bigram_experiment_')
            writefile.write(sentences_list[i][0] + "           Best guess: " + guess+'\n\n')
    # bigram_by_language('sophie a mange', model_filename='bigram_experiment_')