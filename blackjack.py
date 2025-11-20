from typing import List

CARD_VALUE_MAP = {
    'A': 11, 'K': 10, 'Q': 10, 'J': 10,
    '10': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4':4, '3':3, '2':2
}

def normalize_card(card: str) -> str:
    # Accept "A♠" or "A", "10♦" -> "10"
    s = str(card).strip()
    # take leading rank chars (A,K,Q,J,10,2-9)
    # remove suits and whitespace
    rank = ''
    for ch in s:
        if ch.isdigit() or ch.upper() in "AKQJ":
            rank += ch
        else:
            break
    rank = rank.upper()
    if rank == '':
        rank = s[0].upper()
    return rank

def hand_value(cards: List[str]):
    # returns (total, is_soft)
    total = 0
    aces = 0
    for c in cards:
        if c == 'A':
            aces += 1
            total += 11
        else:
            total += CARD_VALUE_MAP.get(c, int(c))
    # reduce aces if bust
    while total > 21 and aces:
        total -= 10
        aces -= 1
    is_soft = ('A' in cards) and (total + (10 * aces) <= 21) and any(c == 'A' for c in cards)
    return total, is_soft

def is_pair(cards: List[str]):
    return len(cards) == 2 and cards[0] == cards[1]

def basic_strategy(player: List[str], dealer: str, can_double=True, can_split=True):
    """
    Simplified basic strategy implementation:
    Returns one of: 'hit','stand','double','split','surrender'
    This covers hard totals, soft totals, and simple pair rules.
    """
    # convert ranks like '10' to '10', 'K'->10 etc. but strategy uses ranks for pair detection.
    # Keep ranks as provided (A,2-10,J,Q,K)
    # Dealer as rank string
    # First: pairs
    if is_pair(player) and can_split:
        r = player[0]
        if r == 'A' or r == '8':
            return 'split'
        if r in ('10','K','Q','J'):
            return 'stand'
        if r == '9':
            if dealer in ('7','10','J','Q','K','A'):
                return 'stand'
            return 'split'
        if r == '7':
            if dealer in ('8','9','10','J','Q','K','A'):
                return 'hit'
            return 'split'
        if r == '6':
            if dealer in ('7','8','9','10','J','Q','K','A'):
                return 'hit'
            return 'split'
        if r == '5':
            # treat as 10 total: usually double vs 2-9
            if dealer in ('2','3','4','5','6','7','8','9'):
                return 'double' if can_double else 'hit'
            return 'hit'
        if r == '4':
            if dealer in ('5','6'):
                return 'split'
            return 'hit'
        if r == '3' or r == '2':
            if dealer in ('8','9','10','J','Q','K','A'):
                return 'hit'
            return 'split'

    # compute value
    total, is_soft_hand = hand_value(player)

    # Soft totals
    if is_soft_hand and total <= 21:
        # Represent common soft strategy (simplified)
        if total >= 19:
            return 'stand'
        if total == 18:
            if dealer in ('9','10','J','Q','K','A'):
                return 'hit'
            if dealer in ('3','4','5','6') and can_double:
                return 'double'
            return 'stand'
        if total <= 17:
            if dealer in ('4','5','6') and can_double:
                return 'double'
            return 'hit'

    # Hard totals
    if total >= 17:
        return 'stand'
    if 13 <= total <= 16:
        if dealer in ('2','3','4','5','6'):
            return 'stand'
        return 'hit'
    if total == 12:
        if dealer in ('4','5','6'):
            return 'stand'
        return 'hit'
    if total == 11:
        return 'double' if can_double else 'hit'
    if total == 10:
        if dealer not in ('10','J','Q','K','A'):
            return 'double' if can_double else 'hit'
        return 'hit'
    if total == 9:
        if dealer in ('3','4','5','6') and can_double:
            return 'double'
        return 'hit'
    return 'hit'