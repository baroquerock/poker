from sys import stdin
from hand_evaluator import HandEvaluator

# inspired by http://suffe.cool/poker/evaluator.html

if __name__ == "__main__":

	evaluator = HandEvaluator()
	for line in stdin:
		try:
			print(evaluator.evaluate(line.strip()))
		except Exception as e:
			print('Error: {}'.format(str(e)))

			