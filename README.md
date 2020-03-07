# [scrabblespy.herokuapp.com](scrabblespy.herokuapp.com)
Flask powered web app to help you win more games of Scrabble.

## Algorithms

First, let's talk about the aforementioned data structures that were created when initializing the dictionary. 

We start by sorting the dictionary by word length, descending.

We then iterate through the dictionary, creating a word hashmap.
This hashmap uses lexicographically sorted tilesets (A to Z) as keys, and a list of all valid word with that tileset as values.

**Example:**
```"AER" : ["are", "ear", "era"]```

The next data structure needed is a counter list, a list of ``Counter`` objects storing the letter frequency for each key in the word hashmap.

The last data structure is we need is the most simple one, a length to index hashmap. The key here will be wordmap key length, and the value will be the first index in the wordlist where this word length is seen.

With these 3 data structures, we have all the dictionary information necessary to be speedy with our anagrams.

### P-Solve (Permutation Solve):

This method is quicker for short tilesets containing ~2 or less blank tiles. Blank tiles will complicate things factorially.

First, we process any blank tiles by making a hashset holding all possible realizations of the tileset.

``"ABC?"`` becomes ``["ABCA", "ABCB", "ABCC", "ABCD", ... ,"ABCZ"]``
<br>
For each element in the hashset, we sort the tiles lexicographically and consider all combinations we could make.

For each combination, we simply check if the entry exists as a key in the wordmap. If it exists, each word in ``wordmap[key]`` can be played.

### F-Solve (Frequency Solve):

This algorithm uses a **way** simpler approach. We just run through the wordmap looking at ``Counter`` objects for each key, and if the count of each letter in our tileset is greater than or equal to the count of each letter in the key ``Counter``, we can make all words at ``wordmap[key]``. Each blank tile in our tileset contributes one degree of lenience for matching the ``Counter``.

We use the length to index hashmap to reduce our search. If our tileset is length 8, for example, there is no point considering word keys that have 9 more letters, we know we **cannot** make any of them. Don't bother searching them.

### Choosing Between Them
Edge case testing was conducted to find the cutoff points between algorithms. Number of blanks and number of standard letters in the tileset were the parameters. It turns out that any more than 2 blanks and **F-Solve** starts beating **P-Solve** fairly convincingly. The exact cutoffs are more particular than that, but that's the general idea. For in-game scenarios, P-Solve will almost always be used since the game of Scrabble only has 2 blank tiles. Implementing F-solve was a pretty academic exercise, but interesting nonetheless.
