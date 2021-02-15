from collections import Counter
from utils import read_txt_lines, split_strings_to_words, split_strings_to_pair_words, read_txt_lines_to_dict
import os


def build_words_dict(words, threshold):
  dictionary = Counter(words)
  for word in list(dictionary):
    if not dictionary[word] > threshold:
      dictionary.pop(word)
  return dictionary


def unigram(dictionary):
  model = {}
  sum_all = sum(dictionary.values())
  for word in list(dictionary):
    model.update({word: dictionary[word] / sum_all})
  return model


def bigram(pair_dict, dictionary):
  model = {}
  sum_all = sum(dictionary.values())
  for pair in list(pair_dict):
    words = pair.split()
    first_word_count = dictionary[words[0]]
    if first_word_count != 0:
      model.update({pair: pair_dict[pair] / first_word_count})
  return model


def back_off(pair, lambda_1, lambda_2, lambda_3, e, bigram_model, unigram_model):
  p_bigram = 0
  p_unigram = 0

  words = pair.split()
  if words[1] in unigram_model:
    p_unigram = unigram_model[words[1]]

  if pair in bigram_model:
    p_bigram = bigram_model[pair]

  p = (lambda_3 * p_bigram) + (lambda_2 * p_unigram) + (lambda_1 * e)
  return p


def calc_probability(poem, lambda_1, lambda_2, lambda_3, e, bigram_model, unigram_model):
  p = 1
  words = poem.split()
  for i in range(len(words) - 1):
    pair = f"{words[i]} {words[i + 1]}"
    p *= back_off(pair, lambda_1, lambda_2, lambda_3,
                  e, bigram_model, unigram_model)
  return p


def predict_poet(poem, lambda_1, lambda_2, lambda_3, e,
                 ferdowsi_bigram, ferdowsi_unigram,
                 hafez_bigram, hafez_unigram,
                 molavi_bigram, molavi_unigram):
  p_ferdowsi = calc_probability(
      poem, lambda_1, lambda_2, lambda_3, e, ferdowsi_bigram, ferdowsi_unigram)
  p_hafez = calc_probability(
      poem, lambda_1, lambda_2, lambda_3, e, hafez_bigram, hafez_unigram)
  p_molavi = calc_probability(
      poem, lambda_1, lambda_2, lambda_3, e, molavi_bigram, molavi_unigram)

  if p_ferdowsi > p_hafez and p_ferdowsi > p_molavi:
    return 1
  elif p_hafez > p_ferdowsi and p_hafez > p_molavi:
    return 2
  elif p_molavi > p_ferdowsi and p_molavi > p_hafez:
    return 3


def run_test_prediction(test_set_dict, lambda_1, lambda_2, lambda_3, e,
                        ferdowsi_bigram, ferdowsi_unigram,
                        hafez_bigram, hafez_unigram,
                        molavi_bigram, molavi_unigram):
  sum_all = len(test_set_dict)
  true_predicts = 0
  for poem in test_set_dict:
    if test_set_dict[poem] == predict_poet(poem, lambda_1, lambda_2, lambda_3, e,
                                           ferdowsi_bigram, ferdowsi_unigram,
                                           hafez_bigram, hafez_unigram,
                                           molavi_bigram, molavi_unigram):
      true_predicts += 1
  return (true_predicts / sum_all)


train_sets_path = f"{os.path.dirname(__file__)}/train_set"

# ferdowsi
ferdowsi_poems = read_txt_lines(f"{train_sets_path}/ferdowsi_train.txt")
ferdowsi_words = split_strings_to_words(ferdowsi_poems)

ferdowsi_dict = build_words_dict(ferdowsi_words, 2)
ferdowsi_unigram = unigram(ferdowsi_dict)

ferdowsi_pairs = split_strings_to_pair_words(ferdowsi_poems)
ferdowsi_pair_dict = build_words_dict(ferdowsi_pairs, 0)
ferdowsi_bigram = bigram(ferdowsi_pair_dict, ferdowsi_dict)

# hafez
hafez_poems = read_txt_lines(f"{train_sets_path}/hafez_train.txt")
hafez_words = split_strings_to_words(hafez_poems)

hafez_dict = build_words_dict(hafez_words, 2)
hafez_unigram = unigram(hafez_dict)

hafez_pairs = split_strings_to_pair_words(hafez_poems)
hafez_pair_dict = build_words_dict(hafez_pairs, 0)
hafez_bigram = bigram(hafez_pair_dict, hafez_dict)

# molavi
molavi_poems = read_txt_lines(f"{train_sets_path}/molavi_train.txt")
molavi_words = split_strings_to_words(molavi_poems)

molavi_dict = build_words_dict(molavi_words, 2)
molavi_unigram = unigram(molavi_dict)

molavi_pairs = split_strings_to_pair_words(molavi_poems)
molavi_pair_dict = build_words_dict(molavi_pairs, 0)
molavi_bigram = bigram(molavi_pair_dict, molavi_dict)

# tests
test_set_path = f"{os.path.dirname(__file__)}/test_set"
test_set = read_txt_lines_to_dict(f"{test_set_path}/test case-3.txt")

lambda_3 = 0.17
lambda_2 = 0.8
lambda_1 = 0.03
e = 0.001

print(run_test_prediction(test_set, 0.2, 0.4, 0.4, 0.2,
                          ferdowsi_bigram, ferdowsi_unigram,
                          hafez_bigram, hafez_unigram,
                          molavi_bigram, molavi_unigram))

print(run_test_prediction(test_set, 0.1, 0.2, 0.7, 0.2,
                          ferdowsi_bigram, ferdowsi_unigram,
                          hafez_bigram, hafez_unigram,
                          molavi_bigram, molavi_unigram))

print(run_test_prediction(test_set, 0.4, 0.5, 0.1, 0.6,
                          ferdowsi_bigram, ferdowsi_unigram,
                          hafez_bigram, hafez_unigram,
                          molavi_bigram, molavi_unigram))

print(run_test_prediction(test_set, 0.02, 0.88, 0.1, 0.001,
                          ferdowsi_bigram, ferdowsi_unigram,
                          hafez_bigram, hafez_unigram,
                          molavi_bigram, molavi_unigram))

# best
print(run_test_prediction(test_set, lambda_1, lambda_2, lambda_3, e,
                          ferdowsi_bigram, ferdowsi_unigram,
                          hafez_bigram, hafez_unigram,
                          molavi_bigram, molavi_unigram))