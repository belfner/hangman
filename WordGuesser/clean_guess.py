import pickle
from typing import List, Tuple, Dict


class WordGuesser:
    # all letters in order of their frequency in english according to
    # 'https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
    all_letters = 'eariotnslcudpmhgbfywkvxzjq'

    # signals whether to count the same letter multiple times
    count_duplicates = False

    # signals whether the characters should be weighted with the weight of the string the character came from
    weighted = False

    def __init__(self, word):
        self.word_to_be_guessed = word
        self.word_length = len(self.word_to_be_guessed)

        # TODO remove since unnecessary
        # check if guessing_word is 4-18 characters
        if self.word_length < 4 or self.word_length > 18:
            raise ValueError(f'Word must be 4-18 characters in length. {self.word_to_be_guessed} is {self.word_length}.')

        self.possible_words = self._load_words()

        # known_letters will be updated whenever a letter that is guessed is in the word to be guessed
        # '*' indicates a unknown character
        self.known_letters = '*' * self.word_length
        self.num_wrong_guesses = 0
        self.guessed_letters = []
        self.wrong_letters = []

        # flag for when all letters in the word have been found
        self.done = False

    def _load_words(self) -> List[Tuple[str, int]]:
        """
        load all possible_words the same length as the guessing_word to be guessed
        Returns
        -------
        ([(str,int)]: list of tuples of possible_words and their weights
        """
        return pickle.load(open(f'subsets_new/{self.word_length}.pkl', 'rb'))

    # TODO could be removed
    def is_letter_in_the_word(self, letter: str) -> bool:
        """
        This method should be overwritten
        Parameters
        ----------
        letter (str): the letter guessed

        Returns
        -------
        (bool): whether the letter is in the word
        """
        return letter in self.word_to_be_guessed

    @staticmethod
    def _check_match(word: str, known_letters_pattern: str) -> Tuple[bool, str]:
        """
        Check if a word matches the known letters pattern. The character '*' represents an unknown letter in the pattern.
        Also counts the letters that are in the positions where the characters are unknown in the known letters pattern
        use_duplicates signals e
        Examples:
        check_match('moose','m**s*',True) -> (True,'ooe')
        check_match('moose','m**s*',False) -> (True,'oe')
        check_match('goose','m**s*',False) -> (False,'')

        Parameters
        ----------
        word (str): guessing_word to be compared
        known_letters_pattern (str): currently known letters

        Returns
        -------
        (bool): does the word matches the known letters pattern
        (str):  the letters that are in the positions where the characters are unknown in the known letters pattern
        """

        missing_letters = ''

        for word_char, pattern_char in zip(word, known_letters_pattern):
            if pattern_char != '*':
                # if letters in the same position don't match the word could not match the known letters pattern
                if word_char != pattern_char:
                    return False, ''
            else:
                if WordGuesser.count_duplicates:
                    missing_letters += word_char
                else:
                    if word_char not in missing_letters:
                        missing_letters += word_char
        return True, missing_letters

    # TODO check if the count_duplicates flag is redundant with the check_match function
    @staticmethod
    def _create_guess_list(str_list: List[Tuple[str, int]], guessed_letters: List[str] = '') -> List[str]:
        """
        Generates a dictionary with all characters with weights according to their occurrences in the strings of the str_list. The result
        can be weighted with the weight of the string the character came from
        Parameters
        ----------
        str_list ([(str, int)]): list of tuples of strings and their weights
        guessed_letters([str]): list of letters that have already been guessed
        Returns
        -------
        ([str]): list of letter their weight value
        """

        # dictionary that will hold letters and their weights
        frequency_dict = {}
        for word, freq in str_list:
            if not WordGuesser.count_duplicates:
                word = ''.join(set(list(word)))
            for letter in word:
                if WordGuesser.weighted:
                    frequency_dict[letter] = frequency_dict.get(letter, 0) + freq
                else:
                    frequency_dict[letter] = frequency_dict.get(letter, 0) + 1

        # add all missing characters with descending weights in order of their frequency in all possible_words
        for i, letter in enumerate(WordGuesser.all_letters):
            frequency_dict[letter] = frequency_dict.get(letter, -i)

        guess_list = WordGuesser._create_sorted_frequency_list(frequency_dict)

        # remove any letters that have already been guessed
        guess_list = [guess for guess in guess_list if guess not in guessed_letters]

        return guess_list

    @staticmethod
    def _create_sorted_frequency_list(frequency_dict: Dict[str, int]) -> List[str]:
        """
        Converts a dictionary of letters and their weights to a list of letter and weight tuples sorted in descending order by the weight value
        Parameters
        ----------
        frequency_dict ({str:int}): dictionary of all letters and their weights

        Returns
        -------
        ([str]): list of letter their weight value
        """
        return [letter for letter, frequency in sorted(list(frequency_dict.items()), key=lambda x: x[1], reverse=True)]

    def _get_new_words(self, words: List[Tuple[str, int]], known_letters: str) -> Tuple[List[Tuple[str, int]], List[Tuple[str, int]]]:
        letter_list = []
        new_words = []

        for word, freq in words:
            # check if word contains a letter that is
            for letter in self.wrong_letters:
                if letter in word:
                    continue
            match, letters = WordGuesser._check_match(word, known_letters)
            if match:
                letter_list.append((letters, freq))
                new_words.append((word, freq))

        return new_words, letter_list

    # TODO maybe remove old function
    def guess_word(self, max_incorrect_guesses: int = 6):
        """"""

        # # TODO replace placeholder control for when guessing_word is not recognized
        # word_set = [word[0] for word in possible_words]
        # if self.word_to_be_guessed not in word_set:
        #     raise ValueError(f'The word "{self.word_to_be_guessed} is not in the known list of possible_words')

        # known_letters will be updated whenever a letter that is guessed is in the word to be guessed
        # '*' indicates a unknown character
        known_letters = '*' * self.word_length

        # track the number of times a letter has been guessed that is not in the word to be guessed
        num_wrong_guesses = 0

        # collects guessed letters to prevent guessing the same letter multiple times
        guessed_letters = []

        # TODO improve comments here
        letter_list = self.possible_words

        while self.word_to_be_guessed != known_letters:
            # get sorted letter frequency list
            guess_list = WordGuesser._create_guess_list(letter_list, guessed_letters)

            # guess letters in order of their calculated_weights
            for guess in guess_list:
                # prevent guessing the same letter multiple times
                guessed_letters.append(guess)
                # check if all letters have been guessed
                if len(guessed_letters) >= 26:
                    return num_wrong_guesses, known_letters

                # check if letter is in guessing_word
                if self.is_letter_in_the_word(guess):
                    # insert letter in to known_letters_pattern at correct places
                    for i, letter in enumerate(self.word_to_be_guessed):
                        if guess == letter:
                            known_letters = known_letters[:i] + letter + known_letters[i + 1:]
                    break
                else:
                    num_wrong_guesses += 1

            self.possible_words, letter_list = WordGuesser._get_new_words(self.possible_words, known_letters)

        return num_wrong_guesses, known_letters

    # TODO maybe unnecessary
    def get_guess_list(self) -> List[str]:
        # get sorted letter frequency list
        self.possible_words, letter_list = WordGuesser._get_new_words(self.possible_words, self.known_letters)
        return WordGuesser._create_guess_list(letter_list, self.guessed_letters)

    def get_guess(self) -> str:
        # get sorted letter frequency list
        self.possible_words, letter_list = self._get_new_words(self.possible_words, self.known_letters)
        guess = WordGuesser._create_guess_list(letter_list, self.guessed_letters)[0]
        return guess

    def _update_known_letters(self, letter: str, positions: List[int]) -> None:
        for position in positions:
            self.known_letters = self.known_letters[:position] + letter + self.known_letters[position + 1:]

    def letter_guessed(self, letter: str, positions: List[int]) -> int:
        if letter in self.guessed_letters:
            raise ValueError(f'The letter "{letter}" has already been guessed')
        self.guessed_letters.append(letter)

        if len(positions) > 0:
            self._update_known_letters(letter, positions)
            # check if all letters are known
            if '*' not in self.known_letters:
                self.done = True
        else:
            self.num_wrong_guesses += 1
            self.wrong_letters.append(letter)

        return self.num_wrong_guesses


import time

if __name__ == '__main__':
    guessing_word = 'humane'
    wg = WordGuesser(guessing_word)

    while not wg.done:
        guess = wg.get_guess()
        positions = [i for i, letter in enumerate(guessing_word) if guess == letter]
        wg.letter_guessed(guess, positions)
    print(wg.wrong_letters)
    # total_time = 0
    # for x in range(10):
    #     wg = WordGuesser(guessing_word)
    #     start = time.perf_counter()
    #     num_wrong, letters_known = wg.guess_word()
    #     total_time += (time.perf_counter() - start)
    # # print(num_wrong, letters_known)
    # print(total_time)
    # possible_words = pickle.load(open(f'subsets_new/{8}.pkl', 'rb'))
    # weighted = True
    # duplicates = True
    # total_time = 0
    # tot_wrong = 0
    # itts = 10000
    # guessing_words = random.sample(possible_words, itts)
    # for i in range(itts):
    #     possible_words = pickle.load(open(f'subsets/{8}.pkl', 'rb'))
    #     word_to_be_guessed = guessing_words[i][0]
    #     print(word_to_be_guessed)
    #     start = time.perf_counter()
    #     num_wrong, _ = guess_word(word_to_be_guessed, possible_words,weighted,duplicates)
    #     total_time += (time.perf_counter() - start)
    #     tot_wrong += num_wrong
    #     print(num_wrong)
    # print(f'Total wrong: {tot_wrong}')
    # print(f'Average time: {total_time / itts} s')
    # print(f'Weighted: {weighted}\nDuplicates counted: {duplicates}')
    # print(f'Guessed {word_to_be_guessed} with {num_wrong_guesses} wrong guesses')
