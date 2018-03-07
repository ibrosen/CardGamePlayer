from collections import defaultdict as dd


def bid(hand, player_no, phase_no, deck_top, reshuffled=False,
        player_data=None, suppress_player_data=False):
    '''Winning in Oh Tim is much harder than losing, as there are three
    losers per trick and only one winner. Furthermore, unless I am the
    first player of the trick I can know whether I lose but playing a card
    lower than at least 1 other in the trick, making it easier to
    predict my bid if I try to lose as many as possible. This bid works
    by bidding 0, unless I have a card that I know is either the highest
    in play or one of the highest (using card counting too). For each
    very high card i have I add 1 to my bid'''
    cardlist = ['A' + deck_top[1], 'K' + deck_top[1], 'Q' + deck_top[1],
                'J' + deck_top[1], '0' + deck_top[1]] + [str(i) + deck_top[1]
                                                         for i in range(9, 1, -1)]
    suits = ['H', 'D', 'C', 'S']
    suits.remove(deck_top[1])
    cardlist += ['A' + i for i in suits] + ['K' + i for i in suits] + \
                ['Q' + i for i in suits] + ['J' + i for i in suits] + \
                ['0' + i for i in suits] + [str(i) + j for i in range(9, 1, -1) for
                                            j in suits]

    # removes cards already played from cardlist
    if not player_data or reshuffled:
        carddict = dd(int)
        for card in cardlist:
            carddict[card] = 1
    if player_data:
        player_data[deck_top] = 0
        for card in player_data.keys():
            if player_data[card] == 0:
                cardlist.remove(card)
    probwin = 0
    handsort = []
    carddict = player_data
    p1prob = 1
    count = 0
    # sorts cards based on their winning value
    for card in cardlist:
        if card in hand:
            handsort.append(card)
    handsort2 = handsort.copy()
    # goes through cards from best to worst, if I have good cards probwin += 1
    for card in handsort2:

        if phase_no == 1 or phase_no == 19:
            if player_no == 0:
                if card[0] == 'A' or card[0] == 'K' or card[0] == 'Q' or \
                                card[0] == 'J' or card[0] == '0' or card[0] == '9':
                    p1prob = 0
                    break
                elif card[1] == deck_top[1]:
                    p1prob = 0
                    break
            else:
                if (card[0] == '4' or card[0] == '3' or card[0] == '2' or \
                                card[0] == '5') and not card[1] != deck_top[1]:
                    p1prob = 1
                else:
                    p1prob = 0
                    break
            continue

        if count == 0 and 0 < probwin < 3 and (card[0] == 'A' or card[0] == 'K'):
            probwin += 1

            count += 1

        if cardlist.index(card) < 5 and card in handsort:
            probwin += 1

        handsort.remove(card)
        if carddict:
            carddict[card] = 0

        cardlist.remove(card)
    # returns probwin, or the preset bid. Other than first round it returns
    # carddict, a dict of cards played, used to count cards
    if not player_data:
        if phase_no == 1 or phase_no == 19:
            return p1prob
        elif phase_no == 10:
            return 0
        elif phase_no % 4 == 0:
            if phase_no > 10:
                return (20 - phase_no) // 4
            else:
                return phase_no // 4

        else:
            return probwin
    else:
        if phase_no == 1 or phase_no == 19:
            return p1prob, carddict
        elif phase_no == 10:
            return 0, carddict
        elif phase_no % 4 == 0:
            if phase_no > 10:
                return (20 - phase_no) // 4, carddict
            else:
                return phase_no // 4, carddict

        else:
            return probwin, carddict


def is_valid_play(play, curr_trick, hand):
    # helper function to see if I have a leading suit in my hand
    def inhand(t, h):
        for element in h:
            if element[1] == t[0][1]:
                return True
        return False

    # goes through conditions for whether or not I can play the card
    if play not in hand:
        return False
    elif not curr_trick:
        return True
    elif inhand(curr_trick, hand) and play[1] == curr_trick[0][1]:
        return True
    elif inhand(curr_trick, hand) and not play[1] == curr_trick[0][1]:
        return False
    elif not inhand(curr_trick, hand):
        return True
    return False


def score_phase(bids, tricks, deck_top, player_data=None,
                suppress_player_data=False):
    pos_dict = dd(int)
    score_dict = dd(int)

    for i in range(0, 4):
        pos_dict[i] = i
        score_dict[i] = 0
    # For each trick, a list of highest to lowest winning power is made
    # the first card both in the list and in the trick will then win


    # creates a list of the highest 13 or 26 cards (depends on whether a
    # trump is the leading suit. The winning card is always in these 13 or 16
    for trick in tricks:
        ranklist = ['A' + deck_top[1], 'K' + deck_top[1], 'Q' + deck_top[1],
                    'J' + deck_top[1], '0' + deck_top[1]] + [str(i) + deck_top[1]
                                                             for i in
                                                             range(9, 1, -1)]
        if trick[0][1] != deck_top[1]:
            ranklist += ['A' + trick[0][1], 'K' + trick[0][1], 'Q' + trick[0][1],
                         'J' + trick[0][1], '0' + trick[0][1]] + [str(i) +
                                                                  trick[0][1]
                                                                  for i in
                                                                  range(9, 1, -1)]
            # finds the first card in the sorted list and the trick, which will be
            # the winning card. Finds the position of this card in the trick, used later
        for card in ranklist:
            if card in trick:
                poswin = trick.index(card)
                break

        for playa in pos_dict.keys():
            if pos_dict[playa] == poswin:
                score_dict[playa] += 1

                # resorts the player positions
            pos_dict[playa] = (pos_dict[playa] + 4 - poswin) % 4
    pos = 0
    for bid in bids:
        if score_dict[pos] == bid:
            score_dict[pos] += 10
        pos += 1
    p0_score = score_dict[0]
    p1_score = score_dict[1]
    p2_score = score_dict[2]
    p3_score = score_dict[3]

    return p0_score, p1_score, p2_score, p3_score,


def play(curr_trick, hand, prev_tricks, player_no, deck_top, phase_bids,
         player_data=None, suppress_player_data=False,
         is_valid=is_valid_play, score=score_phase):
    # making a list of all cards in order from highest to lowest value
    cards = ['A' + deck_top[1], 'K' + deck_top[1], 'Q' + deck_top[1],
             'J' + deck_top[1], '0' + deck_top[1]] + [str(i) + deck_top[1]
                                                      for i in range(9, 1, -1)]
    # redefining to allow me to copy code from Q3
    trick = curr_trick
    if trick and trick[0][1] != deck_top[1]:
        cards += ['A' + trick[0][1], 'K' + trick[0][1], 'Q' + trick[0][1],
                  'J' + trick[0][1], '0' + trick[0][1]] + [str(i) + trick[0][1]
                                                           for i in
                                                           range(9, 1, -1)]
    suits = ['H', 'D', 'C', 'S']
    for card in cards:
        if card[1] in suits:
            suits.remove(card[1])
    cards += ['A' + i for i in suits] + ['K' + i for i in suits] + \
             ['Q' + i for i in suits] + ['J' + i for i in suits] + \
             ['0' + i for i in suits] + [str(i) + j for i in range(9, 1, -1) for
                                         j in suits]

    # uses player data and card counting to remove already played cards
    # from the cardlist, to make the function faster as in later steps
    # the cardlist will be used a lot
    carddict = player_data

    if carddict:
        carddict[deck_top] = 0
        for key in carddict.keys():
            if carddict[key] == 0:
                cards.remove(key)

        if prev_tricks:
            for card in prev_tricks[-1]:
                carddict[card] = 0
    # based on my bid and score, seeing if I want to win or lose tricks
    mybid = phase_bids[player_no]
    myscore = score((11, 11, 11, 11), prev_tricks, deck_top)[player_no]
    winbool = False
    if myscore != mybid:
        winbool = True

    # creates a list of all playable cards in my hand for the current trick
    handlist = []
    for card in cards:
        if card in hand:
            handlist.append(card)
    finallst = []
    for card in handlist:
        if is_valid_play(card, curr_trick, hand):
            finallst.append(card)
    '''If I want to win the trick, I will see if my highest card wins the 
    trick at the current stage of the trick. if it does, it plays the card
    (doesn't play the lowest card to still win, as some strategies dictate
    as that wouldnt work with the bidding system I have whereby I only bid 
    if i have a very high card), then plays this card. If even my highest
    card doesn't win, it plays my lowest playable card, in the hopes
    that a future trick will be won with the high card'''
    final = finallst[0]
    if winbool:
        card = finallst[0]

        for card1 in curr_trick:
            if cards.index(card1) < cards.index(card):
                final = finallst[-1]
                break

    # If I want to lose, i look through my playable cards for the first one
    # to lose the trick for sure, which will be when another card in the trick
    # has a lower index in the cardlist, which is sorted from highest to
    # lowest value. If I am first in the trick, I will play my lowest card
    # so that I hopefully lose the trick
    else:
        if not curr_trick:
            if player_data:
                return finallst[-1], carddict
            else:
                return finallst[-1]

        for card in finallst:

            for card1 in curr_trick:
                if cards.index(card) > cards.index(card1):
                    if player_data:
                        return card, carddict
                    else:
                        return card

        if player_data:
            return finallst[-1], carddict
        else:
            return finallst[-1]

    if player_data:
        return final, carddict
    else:
        return final