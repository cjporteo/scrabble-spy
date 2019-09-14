from rack import Rack
import time


def solve_tiles(tiles, dd, pref, suff, substring, includes, t=100):
    time_0 = time.time()

    def get_runtime():
        return round(1000*(time.time() - time_0), 2)

    for c in tiles:
        if not(65 <= ord(c) <= 90) and not(97 <= ord(c) <= 122) and c != '?':
            return ['Invalid Input', get_runtime(), []]
    for x in [pref, suff, substring]:
        for c in x:
            if not(65 <= ord(c) <= 90) and not(97 <= ord(c) <= 122) and c != '.':
                return ['Invalid Input', get_runtime(), []]
    for c in includes:
        if not(65 <= ord(c) <= 90) and not(97 <= ord(c) <= 122):
            return ['Invalid Input', get_runtime(), []]

    for c in pref + suff + substring:
        if c != '.':
            tiles += c

    rack = Rack(tiles, dd, t, pref, suff, substring, includes)
    cutoffs = {0: 15,
               1: 10,
               2: 7,
               3: 0}
    with open('./counter.txt', 'r') as fin:
        counter = int(fin.read())
    if tiles != "":
        with open('./counter.txt', 'w') as fout:
            fout.writelines(str(counter+1))

    if rack.num_letters >= cutoffs[min(rack.num_blanks, 3)]:
        res = rack.frequency_solve()
        solver = 'F'
    else:
        res = rack.permute_solve()
        solver = 'P'

    if len(res) < 1:
        return ['No Valid Words', get_runtime(), []]

    return ['{}-Solve'.format(solver), get_runtime(), [[word, len(word)] for word in res[:t]]]
