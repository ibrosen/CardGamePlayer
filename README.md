# CardGamePlayer
First year Foundations of Computing assignment, came 8th out of the tournament with 400+ students. Foundations of Computing was my first exposure to programming, and I haven't refactored the code, so there are DEFINITELY some inefficiencies in it, but for me it's a nice reminder of when I found how much I enjoyed programming.

The project was to create a rudimentary AI to play a variant of the Oh Hell card game. The bot that you wrote was then played against the bots of all the other students in the cohort, with a live updating leaderboard.

My strategy was fairly simple. For the game, the person with the highest valued card "wins" the hand and gets +1 point. At the start of every round, of which there are many, you bid to say how many hands you expect to win. For the first round, everyone has 1 card, the second, 2, up until round 10 where everyone has 10 cards. From there, until round 20, everyone has one less card per round.

If you currectly bid, you get +10. So for a round where you have one card, if you bid 0 and lose the hand, you get 10 points, whereas someone that "wins" the round but bids 0, only gets 1 point (+1 for the hand, +0 for not bidding correctly).

So my strategy is based on the fact that every hand has 4 players and 1 winner, and if you aren't first, you can often be sure you're going to lose by playing a card lower than the person(s) before you.

As such, my bid was equal to the number of REALLY good cards in my hand. For those, I'd play them fairly early on, for all my other cards, I'd play the highest card in my hand that was sure to lose the hand. So basically I'd bid low and rely on the fact that I can fairly easily lose most rounds.
