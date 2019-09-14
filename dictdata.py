from collections import Counter, defaultdict
import pickle


class DictData:

    def __init__(self, dictionary):
        self.word_map = pickle.load(open(dictionary + "wm.pickle", "rb"))
        self.counter_list = pickle.load(open(dictionary + "cl.pickle", "rb"))
        self.len_ind_map = pickle.load(open(dictionary + "lim.pickle", "rb"))

    def start_index(self, length):
        while length not in self.len_ind_map:
            length -= 1
            if length <= 0:
                return len(self.counter_list)
        return self.len_ind_map[length]
