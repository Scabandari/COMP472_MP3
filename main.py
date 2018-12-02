from utils import (unigram_keys, assign_probs, print_unigram, assign_freqs,
                   combine_txt_files, output_models, get_sentences, create_solutions,
                   compare_unigrams)

# todo before finishing, 10 correct/incorrect sentences are correct after including 3rd language other?
# Note: trainOT.txt is The Little Prince and Moby Dick provided but passed through google translate to get Dutch
# which uses the same alphabet

sentences_list = []  # list of lists, one for each line or sentence in sentence.txt, 10 sentences
"""[ 
    ('I'm OK.',['i', 'm', 'o','k' ),
    ('I hate AI', ['i', 'h' ....]),
    ... 
   ]
"""
sentences_file = 'sentences.txt'
get_sentences(sentences_file, sentences_list)

ten_right = []
ten_right_file = 'test.txt'  #'10_correct_unigram.txt'
get_sentences(ten_right_file, ten_right)

english_txts = ['en-moby-dick.txt', 'en-the-little-prince.txt']
combine_txt_files(english_txts, 'trainEN.txt')  # outputs both English files as 'trainEN.TXT'

french_txts = ['fr-le-petit-prince.txt', 'fr-vingt-mille-lieues-sous-les-mers.txt']
combine_txt_files(french_txts, 'trainFR.txt')

# todo IF WE'RE GIVEN NEW FILES FOR TRAINING DURING DEMO JUST COMMENT OUT THE combine_txt_files ABOVE
# assign_freqs() below will read the texts if names of files are correct

############################ TRAINING THE MODELS ##################################################
# UNIGRAM ENGLISH ###################################################################################
unigram_models_en = {}
unigram_keys(unigram_models_en)

assign_freqs('trainEN.txt', unigram_models_en, unigram=True)

total_chars = 0
for key in unigram_models_en.keys():
    total_chars += unigram_models_en[key]['freq']

assign_probs(total_chars, unigram_models_en, unigram=True)
print("English Unigram total chars: {}".format(total_chars))
print_unigram(unigram_models_en)

# UNIGRAM FRENCH ####################################################################################
unigram_models_fr = {}
unigram_keys(unigram_models_fr)

assign_freqs('trainFR.txt', unigram_models_fr, unigram=True)

total_chars = 0
for key in unigram_models_fr.keys():
    total_chars += unigram_models_fr[key]['freq']

assign_probs(total_chars, unigram_models_fr, unigram=True)
print("French Unigram total chars: {}".format(total_chars))
print_unigram(unigram_models_en)

# UNIGRAM OTHER ############################################################################################
unigram_models_ot = {}
unigram_keys(unigram_models_ot)

assign_freqs('trainOT.txt', unigram_models_ot, unigram=True)

total_chars = 0
for key in unigram_models_ot.keys():
    total_chars += unigram_models_ot[key]['freq']

assign_probs(total_chars, unigram_models_ot, unigram=True)
print("OTHER(Dutch) Unigram total chars: {}".format(total_chars))
print_unigram(unigram_models_ot)

# BIRGRAMS ENGLISH ######################################################################################


# BIRGRAMS FRENCH ######################################################################################


# BIRGRAMS OTHER ######################################################################################


######################################################################################################
# output_models(unigram_en, unigram_fr, unigram_ot=None, bigram_en=None, bigram_fr=None, bigram_ot=None)
output_models(unigram_models_en, unigram_models_fr, unigram_models_ot)  # todo include more models here as they're developed
# outputs txt files for specific models, their probabilities for each input chars for uni and char pairs for bi

unigrams = [
    ('FRENCH', unigram_models_fr),
    ('ENGLISH', unigram_models_en),
    ('OTHER', unigram_models_ot)
]

bigrams = []

create_solutions(sentences_list, unigrams, bigrams=None)  # when bigrams finished pass in here


##### testing only ############
#create_solutions(ten_right, unigrams, bigrams=None)
#compare_unigrams(unigram_models_en, unigram_models_fr, 'uni_comparisons.txt', unigram_models_ot)
########################