from itertools import combinations
from functools import reduce


class PokerTable(object):

    def __init__(self):

        # 10 straight flushes, 156 - full house and four of a kind hands,
        # 1277 - simple flushes, 10 - simple straights, 
        # 858 - two pair and three of a kind hands,
        # 2860 - pair hands, 1277 - high cards
        self.number_of_ranks = [10, 156, 156, 1277, 10, 858, 858, 2860, 1277]
        self.prefix_sum_of_ranks = None
        self.compute_prefix_sum()

        # numeric representations of straights that result from bit manipulation
        self.straights = [7936, 3968, 1984, 992, 496, 248, 124, 62, 31, 4111]
        self.primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

        self.flush_ranks = {}
        self.high_card_ranks = {}
        self.remaining_ranks = {}

        
        self.compute_flushes_and_high_cards()
        self.compute_full_house_and_four_kind()
        self.compute_three_kind()
        self.compute_two_pair()
        self.compute_one_pair()


    def compute_prefix_sum(self):
        N = len(self.number_of_ranks)
        self.prefix_sum_of_ranks = [0 for _ in range(N)]

        curr = 0
        for i in range(N):
            curr += self.number_of_ranks[i]
            self.prefix_sum_of_ranks[i] = curr


    def compute_flushes_and_high_cards(self):
       
        f, s = 0, self.prefix_sum_of_ranks[3]
        f, s = f + 1, s + 1

        for num in self.straights:

            self.flush_ranks[num] = f
            self.high_card_ranks[num] = s
            f, s = f + 1, s + 1


        bit_idx = range(0, 13)
        combs = combinations(bit_idx, 5)
        f, s = self.prefix_sum_of_ranks[2], self.prefix_sum_of_ranks[7]
        f, s = f + 1, s + 1

        for comb in combs:
            num = ['1'  if i in comb else '0' for i in range(13)]
            num = int(''.join(num), 2)
            if num not in self.flush_ranks:
                self.flush_ranks[num] = f
                self.high_card_ranks[num] = s
                f, s = f + 1, s + 1


    def compute_full_house_and_four_kind(self):

        combs = combinations(self.primes, 2)

        four_of_a_kind_numbers = []
        full_house_numbers = []

        for comb in combs:
            four_of_a_kind_numbers.append( ((comb[0], comb[1]), comb[0] ** 4 * comb[1]) )
            four_of_a_kind_numbers.append( ((comb[1], comb[0]), comb[0] * comb[1] ** 4) )

            full_house_numbers.append( ((comb[0], comb[1]), comb[0] ** 3 * comb[1] ** 2) )
            full_house_numbers.append( ((comb[1], comb[0]), comb[0] ** 2 * comb[1] ** 3) )

        four_of_a_kind_numbers.sort(reverse = True)
        full_house_numbers.sort(reverse = True)

        fk, fh = self.prefix_sum_of_ranks[0], self.prefix_sum_of_ranks[1]
        fk, fh = fk + 1, fh + 1
        for four_kind, full_house in zip(four_of_a_kind_numbers, full_house_numbers):
            self.remaining_ranks[four_kind[1]] = fk
            self.remaining_ranks[full_house[1]] = fh
            fk, fh = fk + 1, fh + 1


    def compute_three_kind(self):

        combs = combinations(self.primes, 3)
        three_kind_numbers = []

        for comb in combs:
            prod = reduce(lambda x, y: x * y, comb)
            for i in range(3):
                three = sorted([comb[x] for x in range(3) if x != i], reverse=True)
                three = [comb[i]] + three
                three_kind_numbers.append( (three, comb[i] ** 3 * (prod / comb[i])) )

        three_kind_numbers.sort(reverse = True)

        t = self.prefix_sum_of_ranks[4] + 1

        for three_kind in three_kind_numbers:
            self.remaining_ranks[three_kind[1]] = t
            t += 1


    def compute_two_pair(self):

        combs = combinations(self.primes, 3)
        two_pair_numbers = []

        for comb in combs:
            prod = reduce(lambda x, y: x * y, (z ** 2 for z in comb))
            for i in range(3):
                pair = [comb[x] for x in range(3) if x != i]
                pair = [pair[1], pair[0]] if pair[1] > pair[0] else [pair[0], pair[1]]
                pair.append(comb[i])
                two_pair_numbers.append( (tuple(pair), prod / comb[i]) )


        two_pair_numbers.sort(reverse = True)

        t = self.prefix_sum_of_ranks[5] + 1
        for two_pair in two_pair_numbers:
            self.remaining_ranks[two_pair[1]] = t
            t += 1


    def compute_one_pair(self):

        combs = combinations(self.primes, 4)
        one_pair_numbers = []

        for comb in combs:
            prod = reduce(lambda x, y: x * y, comb)
            for i in range(4):
                pair = sorted([comb[x] for x in range(4) if x != i], reverse = True)
                pair = [comb[i]] + pair
                one_pair_numbers.append( (tuple(pair), comb[i] ** 2 * (prod / comb[i])) )


        one_pair_numbers.sort(reverse = True)

        t = self.prefix_sum_of_ranks[6] + 1
        for one_pair in one_pair_numbers:
            self.remaining_ranks[one_pair[1]] = t
            t += 1

