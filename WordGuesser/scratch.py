import pickle
import json
import operator
import time
import string
import statistics


with open('en.txt', 'r',encoding='utf-8') as f:
    words = f.read().split('\n')

words = [(word.split(' ')[0], int(word.split(' ')[1])) for word in words[:-1]]
print(len(words))

def only_chars(chars, word):
    for char in word:
        if not char in chars:
            return False
    return True

words = [word for word in words if only_chars(string.ascii_lowercase,word[0])][:40000]
# with open('out.csv','w') as outfile:
#     outfile.write(',\n'.join([str(guessing_word[1]) for guessing_word in words]))

print(len(words))
# https://github.com/hermitdave/FrequencyWords/blob/master/content/2018/en/en_full.txt

words_lengths = set([len(word[0]) for word in words])
print(words_lengths)
words_sorted = [[] for _ in range(50)]
for length in sorted(list(words_lengths)):
    word_subset = [word for word in words if len(word[0]) == length]
    med = int(statistics.median([word[1] for word in word_subset]))
    lenlen = len([word for word in word_subset if word[1]>=med])
    print(length,len(word_subset),med,lenlen)
    print(word_subset[-10:])
    pickle.dump(word_subset, open(f'subsets_new/{length}.pkl', 'wb'))
    # print([guessing_word for guessing_word in word_subset[lenlen-10:lenlen+10]])
    # print(' '.join([guessing_word[0] for guessing_word in word_subset if guessing_word[1]>=med]))
    words_sorted[length] = words_sorted
word_subset = [word for word in words if len(word[0]) == 18]
print(word_subset[:100])
# x = 1
