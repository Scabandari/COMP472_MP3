import math


alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
            'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
            'q', 'r', 's', 't', 'u', 'v',
            'w', 'x', 'y', 'z']


def compare_unigrams(english, french, output_file, other=None):
    """
    Take the tr
    :param english:
    :param french:
    :return:
    """
    if other:
        with open(output_file, 'a') as f:
            for letter in alphabet:
                f.write("letter: {}, english: {}, french: {}, other: {}\n".format(
                    letter,
                    english[letter]['prob'],
                    french[letter]['prob'],
                    other[letter]['prob']))
    else:
        with open(output_file, 'a') as f:
            for letter in alphabet:
                f.write("letter: {}, english: {}, french: {}\n".format(
                    letter,
                    english[letter]['prob'],
                    french[letter]['prob']))


def output_models(unigram_en, unigram_fr, unigram_ot=None, bigram_en=None, bigram_fr=None, bigram_ot=None):
    """
    See page 2 of documentation, for unigram & bigram, french, english + 3rd option, 6 .txt files
    :return:
    """
    files = [
        ('unigramEN.txt', unigram_en),
        ('unigramFR.txt', unigram_fr),
        ('unigramOT.txt', unigram_ot)
        # ('bigramEN.txt', bigram_en),
        # ('bigramFR.txt', bigram_fr),
        # ('unigramOT.txt', unigram_ot),
        # ('bigramOT.txt', bigram_ot)
    ]

    for file_model in files:
        file = file_model[0]
        model = file_model[1]
        with open(file, mode='a') as f:
            for letter in alphabet:
                f.write("({}) = {}\n".format(letter, model[letter]['prob']))  # model[key]['prob'] ==> nested dicts


def combine_txt_files(txt_files, output_name):
    """
    Take a list of input txt files and concatenate them to create one file,
    for why seen project description page1 at the bottom Input: ...
    :param txt_files:
    :param output_name:
    :return:
    """
    with open(output_name, mode='a') as output_file:
        for file in txt_files:
            with open(file, mode='r') as f:
                try:
                    for line in f:
                        output_file.write(line)
                except UnicodeDecodeError:
                    print("UnicodeDecodeError\n\n\n")


def most_likely_lanuage(latest_sum_of_logs):
    most_likely = 'FRENCH'
    english = 'ENGLISH'
    other = 'OTHER'
    if latest_sum_of_logs[most_likely] < latest_sum_of_logs[english]:
        most_likely = english
    if latest_sum_of_logs[most_likely] < latest_sum_of_logs[other]:
        most_likely = other
    return most_likely


def reset_sum_of_logs(sum_of_logs):
    for key in sum_of_logs.keys():
        sum_of_logs[key] = 0


def create_solutions(sentences_list, unigrams, bigrams=None):
    """
    Given a sentence and the trained models output the solution files in txt format. See output 2. page 2 of
    problem description
    :param sentences_list: list of tuples like so: ('I'm OK.',['i', 'm', 'o','k' ) sentence then
    list of letters
    :param n_grams: list of dicts, our trained models for unigram_en, unigram_fr, unigram_ot, bigram_en ...
    :return: None
    """
    log_prob = " ==> log of prob of sentence so far: "
    according_to_uni = "According to the unigram model, the sentence is in "
    according_to_bi = "According to the bigram model, the sentence is in "

    counter = 1
    latest_sum_of_logs_unigram = {
        'FRENCH': 0,
        'ENGLISH': 0,
        'OTHER': 0
    }
    # latest_sum_of_logs_bigram = {
    #     'FRENCH': 0,
    #     'ENGLISH': 0,
    #     'OTHER': 0
    # }
    for sentence_tuple in sentences_list:
        # todo reset latest sum of logs
        output_file = "out{}.txt".format(counter)
        counter += 1
        with open(output_file, 'w') as f:
            original_sentence = sentence_tuple[0]
            f.write(original_sentence + "\n")
            f.write("UNIGRAM MODEL: \n")
            sentence_as_list = sentence_tuple[1]
            for letter in sentence_as_list:
                f.write("\nUNIGRAM: {}\n".format(letter))
                for unigram in unigrams:
                    language = unigram[0]
                    #f.write(language + "\n")
                    model = unigram[1]  # {'a': {'freq': 1, 'prob': 0.01}, 'b'....}
                    probability = model[letter]['prob']
                    latest_sum_of_logs_unigram[language] += math.log10(probability)
                    output_sentence = "{}: P({}) = {}".format(language, letter, probability)
                    output_sentence += log_prob
                    output_sentence += str(latest_sum_of_logs_unigram[language])
                    output_sentence += "\n"
                    f.write(output_sentence)
            winner = most_likely_lanuage(latest_sum_of_logs_unigram)
            temp_sentence = according_to_uni + winner
            output_sentence = temp_sentence + "\n---------------------------------------------\n"
            f.write(output_sentence)
            print("\nUnigram: {}:\n{}".format(original_sentence, temp_sentence))
        reset_sum_of_logs(latest_sum_of_logs_unigram)


def unigram_keys(dict_):
    """
    Take an empty dict and assign each letter of the alphabet as a key w/ corresponding
    dict for frequencies and probabilites, intialized to zero
    :param dict_:
    :return: None
    """
    for letter in alphabet:
        dict_[letter] = {
            'freq': 0.5,  # initialized to 0.5 for add-delta smoothing
            'prob': 0
        }


def in_alphabet(letter):
    for letter_ in alphabet:
        if letter_ == letter:
            return True
    return False


def print_unigram(dict_):
    """
     Takes unigram freqs dict and prints the freqs in order a, b, c
    :param dict_:
    :return:
    """
    for letter in alphabet:
        print("{}: frequency: {}, probability: {}".format(letter, dict_[letter]['freq'], dict_[letter]['prob']))
    print("\n\n\n")


def assign_freqs(text_file, freq_dict, unigram=True):
    """
    Take the unigram or bigram frequency dict, examine each letter in the doc. If its in alphabet
    increment the frequency for that letter in the dict. For ex.
    {'a': {'freq': 1, 'prob': 0.01}, 'b'....}
    :param text_file:
    :param freq_dict:
    :param unigram:
    :return:
    """
    if unigram:
        with open(text_file) as f:
            try:
                for line in f:
                    for word in line.split(" "):
                        for char in word:
                            # char_ = char(char_)
                            char = char.lower()
                            if in_alphabet(char):
                                freq_dict[char]['freq'] += 1
            except UnicodeDecodeError:
                print("UnicodeDecodeError\n\n\n\n")
        return


def assign_probs(total_instances, freq_dict, unigram=True):
    """
    Take frequency dict, total instances and calculate the probabilities for that letter.
    UPDATE: basically above but add-delta smoothing, see notes slide 50
    :param total_instances: total relevant chars or char pairs for bigrams examined in all docs of a certain language
    :param freq_dict: One for each language and unigram vs bigram
    :param unigram: False => bigram
    :return: None, this updates the freq_dict
    """
    if unigram:
        for key in freq_dict.keys():
            frequency = freq_dict[key]['freq']
            numerator = frequency  # 0.5 already factored in when initialized
            denominator = total_instances + 0.5 * len(alphabet)   # squared is for bigrams
            probability = numerator/denominator
            freq_dict[key]['prob'] = probability
        return


def get_sentences(text_file, sentences_list):
    """
    Take in a txt file, read each line and break it into chars. Add that list to sentences_list
    :param text_file: 'sentences.txt' or whatever the name of our input txt file of sentences is
    :param sentences_list: List of lists, one for each line in text_file
    :return:
    """
    with open(text_file, 'r') as f:
        for line in f:
            next_sentence = []
            for letter in line:
                letter = letter.lower()
                if letter in alphabet:  # exclude punctuation and empty spaces
                    next_sentence.append(letter)
            sentences_list.append((line, next_sentence))
