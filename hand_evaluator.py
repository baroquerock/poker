from functools import reduce
from itertools import combinations
from collections import defaultdict
from poker_table import PokerTable



class HandEvaluator(object):

	def __init__(self):

		self.card_ranks = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, 
						   '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 
						   'Q': 10, 'K': 11, 'A': 12}

		self.suits = {'c': 1, 'd': 2, 'h': 4, 's': 8}

		self.card_primes = {'2': 2, '3': 3, '4': 5, '5': 7, '6': 11, 
					   '7': 13, '8': 17, '9': 19, 'T': 23, 
					   'J': 29, 'Q': 31, 'K': 37, 'A': 41}

		self.game_types = {'five-card-draw': 1, 
			  			   'texas-holdem': 2, 
			               'omaha-holdem': 3}

		self.rank_table = PokerTable()


	def get_raw_rank(self, hand):

		has_flush = reduce(lambda x, y: x & y, hand) & 0xF000
		q = reduce(lambda x, y: x | y, hand) >> 16
		
		if has_flush:
			return self.rank_table.flush_ranks[q]

		if q in self.rank_table.high_card_ranks:
			return self.rank_table.high_card_ranks[q]

		primes = [card & 0xFF for card in hand]

		prime_prod = reduce(lambda x, y: x * y, primes)
		return self.rank_table.remaining_ranks[prime_prod]


	def preprocess_hand(self, raw_hand):

		SIZE, CARD_SIZE = len(raw_hand), 2
		hand = []
		for i in range(0, SIZE, CARD_SIZE):
			val, suit = raw_hand[i], raw_hand[i+1]

			if val not in self.card_ranks or suit not in self.suits:
				raise Exception("incorrect card value")

			p = format(self.card_primes[val], '#010b')[2:]
			r = format(self.card_ranks[val], '#06b')[2:]
			s = format(self.suits[suit], '#06b')[2:]
			b = format(1 << self.card_ranks[val], '#018b')[2:]
			card = b + s + r + p
			hand.append(int(card, 2))

		return hand


	def get_rank(self, hand, board, game_type):

		if game_type == 1:

			if len(hand) != 5:
				raise Exception("wrong hand length")

			return self.get_raw_rank(hand)

		if game_type == 2:

			if len(hand) != 2:
				raise Exception("wrong hand length")
			if len(board) != 5:
				raise Exception("wrong board length")

			return min(self.get_raw_rank(comb) for comb in combinations(board + hand, 5))

		if game_type == 3:

			if len(hand) != 4:
				raise Exception("wrong hand length")
			if len(board) != 5:
				raise Exception("wrong board length")

			return min(self.get_raw_rank(b + h) for b in combinations(board, 3) \
			                                 for h in combinations(hand, 2))


	def evaluate(self, poker_round):

		poker_round = poker_round.split()
		game_type = poker_round[0].strip()

		if game_type not in self.game_types:
			raise Exception("game type is not supported")

		game_type = self.game_types[game_type]

		raw_hands = poker_round[1:]
		if not raw_hands:
			raise Exception("empty hands")

		hands = [self.preprocess_hand(hand.strip()) for hand in raw_hands]

		board = None
		if game_type != 1:		
			board, hands, raw_hands = hands[0], hands[1:], raw_hands[1:]
	
		hand_values = [self.get_rank(hand, board, game_type) for hand in hands]
		unique = sorted(list(set(hand_values)), reverse = True)
		groups = defaultdict(list)
		for v, h in zip(hand_values, raw_hands):
			groups[v].append(h)

		return ' '.join('='.join(sorted(groups[v])) for v in unique)

