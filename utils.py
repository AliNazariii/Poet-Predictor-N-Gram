from itertools import chain


def read_txt_lines(file_path):
  lines = []
  redundant_chars = "؟،*:\""
  with open(file_path, 'r') as f:
    for line in f.readlines():
      for char in redundant_chars:
        line = line.replace(char, '')
      line = line.replace("  ", " ")
      lines.append(f"<s> {line.rstrip()} </s>")
  return lines


def split_strings_to_words(strings_list):
  words = []
  for line in strings_list:
    words = chain(words, line.split())
  return list(words)


def split_strings_to_pair_words(strings_list):
  pairs = []
  for line in strings_list:
    words = line.split()
    for i in range(len(words) - 1):
      pairs.append(f"{words[i]} {words[i + 1]}")
  return list(pairs)


def read_txt_lines_to_dict(file_path):
  dictionary = {}
  redundant_chars = "؟،*:\""
  with open(file_path, 'r') as f:
    for line in f.readlines():
      line = line.split("\t")
      poet = int(line[0])
      poem = line[1]
      for char in redundant_chars:
        poem = poem.replace(char, '')
      poem = poem.replace("  ", " ")
      dictionary.update({f"<s> {poem.rstrip()} </s>": poet})
  return dictionary
