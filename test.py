import collections
i = iter(range(10))
# print(next(i))
# print(next(i))

# 迭代常常是隐形的。模拟 for i in xxx:


def for_simulator(iterable):
    iterator = iter(iterable)
    while True:
        try:
            print(next(iterator))
        except StopIteration:
            break


for_simulator(range(10))


# poker game

Cards = collections.namedtuple('Card', 'rank suit')


class Poker:

    ranks = [str(i) for i in range(2, 11)] + list('JQKA')
    suits = 'flower red black kuai'.split()

    def __init__(self):
        self._cards = [Cards(rank, suit) for suit in self.suits for rank in self.ranks]

    def __getitem__(self, item):
        return self._cards[item]

    def __len__(self):
        return len(self._cards)


poker = Poker()
print(poker[-1])
# 做排序处理

suit_values = {'flower': 1, 'red': 2, 'black': 3, 'kuai': 4}


def card_value(card):
    rank_value = Poker.ranks.index(card.rank)
    suit_value = suit_values[card.suit]
    return rank_value + suit_value


print(sorted(poker, key=card_value))

# Slice()
s = '---------ellen-------12---'
name = slice(9, 14)
age = slice(-5, -3)
print(s[name], s[age])



