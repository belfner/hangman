import pickle
import json
import operator
import time

with open('count_1w.txt', 'r') as f:
    words = f.read().split('\n')

words = [(word.split('\t')[0], int(word.split('\t')[1])) for word in words[:-1]]

# x = 1
# while True:
words_lengths = set([len(word[0]) for word in words])
print(words_lengths)
# save all possible_words of the same length into separate files

first_guess = ['' for _ in range(20)]

# 20

for length in sorted(list(words_lengths))[:19]:
    word_subset = sorted([word for word in words if len(word[0]) == length], key=lambda x: x[1], reverse=True)
    with open(f'subsets/{length}.txt', 'w') as outfile:
        outfile.write('\n'.join(['\t'.join([word[0], str(word[1])]) for word in sorted(word_subset, key=lambda x: x[1], reverse=True)]))

    pickle.dump(word_subset, open(f'subsets/{length}.pkl', 'wb'))
    start = time.time()
    letters = {}
    for word in word_subset:
        for letter in word[0]:
            letters[letter] = letters.get(letter, 0) + 1
    letters = sorted(list(letters.items()),key=lambda x:x[1],reverse=True)

    print(time.time()-start,',')

# from string import ascii_lowercase
#
# def only_chars(chars, guessing_word):
#     for char in guessing_word:
#         if not char in chars:
#             return False
#     return True
#
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


#
#
# with open('wiki-100k.txt', 'r', encoding='utf-8') as f:
#     possible_words = f.read().split('\n')
# print(possible_words)
# possible_words = [guessing_word.lower() for guessing_word in possible_words if guessing_word[:4] != '#!co' and only_chars(ascii_lowercase,guessing_word)]
# for guessing_word in possible_words:
#     if ' ' in guessing_word:
#         print(guessing_word)
# possible_words = f7(possible_words)
# words_lengths = set([len(guessing_word) for guessing_word in possible_words])
# print(words_lengths)
#
# for length in sorted(list(words_lengths))[0:19]:
#     word_subset = [guessing_word for guessing_word in possible_words if len(guessing_word) == length]
#     # with open(f'subsets/{length}.txt', 'w') as outfile:
#     #     outfile.write('\n'.join(['\t'.join([guessing_word[0], str(guessing_word[1])]) for guessing_word in sorted(word_subset, key=lambda x: x[1], reverse=True)]))
#     pickle.dump(word_subset, open(f'subsets/{length}.pkl', 'wb'))
#     letters = {}
#     for guessing_word in word_subset:
#         for letter in guessing_word:
#             letters[letter] = letters.get(letter, 0) + 1
#
#     print(sorted(list(letters.items()), key=lambda x: x[1], reverse=True), ',')

# import json
#
# j_dict = json.load(open('words_dictionary.json', 'r'))
# possible_words = list(j_dict.keys())
#
# possible_words = f7(possible_words)
#
# words_lengths = set([len(guessing_word) for guessing_word in possible_words])
# print(words_lengths)
#
# for length in sorted(list(words_lengths))[0:19]:
#     word_subset = [guessing_word for guessing_word in possible_words if len(guessing_word) == length]
#     # with open(f'subsets/{length}.txt', 'w') as outfile:
#     #     outfile.write('\n'.join(['\t'.join([guessing_word[0], str(guessing_word[1])]) for guessing_word in sorted(word_subset, key=lambda x: x[1], reverse=True)]))
#     pickle.dump(word_subset, open(f'subsets/{length}.pkl', 'wb'))
#     letters = {}
#     for guessing_word in word_subset:
#         for letter in guessing_word:
#             letters[letter] = letters.get(letter, 0) + 1
#     print(sorted(list(letters.items()), key=lambda x: x[1], reverse=True), ',')













    # first_guess[length] =

# print(first_guess)
# pickle.dump(possible_words,open('third.pkl','wb'))
#
# import timeit
# r1 = r'''
# with open('count_1w.txt','r') as f:
#     possible_words = f.read().split('\n')
#
# possible_words = {guessing_word.split('\t')[0]:int(guessing_word.split('\t')[1]) for guessing_word in possible_words[:-1]}
# '''
#
# r2 = '''
# import pickle
# possible_words = pickle.load(open('third.pkl','rb'))
# '''
#
# print(timeit.timeit(r1,number = 1))
# print(timeit.timeit(r2,number = 1))
