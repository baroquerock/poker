# Poker Hand Strength Evaluator

## Idea

The approach behind this implementation is described [here](http://suffe.cool/poker/evaluator.html). The core idea is to transform the input into numerical representation, where each bit signifies card rank, card suit, or a prime number associated with the card rank. Then it is possible to build a lookup table to map that numerical representation into the final score. Even though there are 2,598,960 possible combinations of 5 cards, the number of possible scores is just 7462, so the lookup table will be pretty small.


## Implementation

* There are two main classes HandEvaluator and PokerTable. PokerTable is initialized once during HandEvaluator initialization, and can be used for all subsequent evaluation calls. 

* Three poker game types are supported: five-card-draw, texas-holdem, and omaha-holdem. Texas-holdem and omaha-holdem are implemented by enumerating possible hand combinations.

* The cost of one evaluation call in O(1), even for texas-holdem and and omaha-holdem, since the number of possible combinations is fixed (texas-holdem - C(7, 5) = 21, omaha-holdem - C(5, 3) * C(4, 2) = 60)











