from itertools import product, combinations
from collections import Counter


class Rack:

    def __init__(self, tiles, dd, t, pref, suff, substring, includes):
        self.tiles = tiles.upper()
        self.dd = dd
        self.t = t
        self.pref = pref.upper()
        self.suff = suff.upper()
        self.substring = substring.upper()
        self.includes = includes.upper()
        self.num_blanks = tiles.count('?')
        self.num_letters = len(tiles) - self.num_blanks

    def get_choices(self):

        order = "ABCDEFGHIJKLMNOPQRSTUVWXYZ?"
        tiles = ''.join(sorted(self.tiles.upper(), key=lambda item: order.index(item)))

        letters = tiles[:self.num_letters]
        options = list(product(order[:-1], repeat=self.num_blanks))

        res = set([])

        for opt in options:
            word = letters + ''.join(opt)
            res.add(''.join(sorted(word)))

        return res

    def get_subsets(self, choices):

        if not choices:
            return []

        res_set = set([])
        res_list = []

        for n in reversed(range(len(self.tiles))):
            for choice in choices:
                subsets = list(combinations(choice, n+1))
                for subset in subsets:
                    selection = ''.join(subset)
                    if selection not in res_set:
                        res_set.add(selection)
                        res_list.append(selection)

        return res_list

    def starts(self, word):
        if len(self.pref) > len(word):
            return False
        for i in range(len(self.pref)):
            if self.pref[i] != '-' and self.pref[i] != word[i]:
                return False
        return True

    def ends(self, word):
        if len(self.suff) > len(word):
            return False
        rsuff = self.suff[::-1]
        rword = word[::-1]
        for i in range(len(rsuff)):
            if rsuff[i] != '-' and rsuff[i] != rword[i]:
                return False
        return True

    def is_substring(self, word):
        if len(self.substring) > len(word):
            return False
        end_index = len(word) - len(self.substring) + 1
        for i in range(end_index):
            flag = False
            for j in range(len(self.substring)):
                if self.substring[j] != '-' and self.substring[j] != word[i+j]:
                    flag = True
                    break
            if not flag:
                return True
        return False


    def contains_all(self, word):
        for c in self.includes:
            if c not in word:
                return False
        return True

    def is_okay(self, word):
        return self.starts(word) \
               and self.ends(word) \
               and self.is_substring(word) \
               and self.contains_all(word)

    def permute_solve(self):

        subsets = self.get_subsets(self.get_choices())
        res = []

        for subset in subsets:
            if subset in self.dd.word_map:
                plays = self.dd.word_map[subset]
                for play in plays:
                    if self.is_okay(play):
                        res.append(play)
                        self.t -= 1
                        if self.t <= 0:
                            return res

        return res

    def frequency_solve(self):

        tile_freq = Counter(self.tiles)
        res = []

        def match(key_freq):
            mismatch = 0
            for letter in key_freq:
                if key_freq[letter] > tile_freq[letter]:
                    mismatch += key_freq[letter] - tile_freq[letter]
                    if tile_freq['?'] < mismatch:
                        return False
            return True

        for i in range(self.dd.start_index(len(self.tiles)), len(self.dd.counter_list)):
            if match(self.dd.counter_list[i][0]):
                for play in self.dd.word_map[self.dd.counter_list[i][1]]:
                    if self.is_okay(play):
                        res.append(play)
                        self.t -= 1
                        if self.t <= 0:
                            return res
        return res
