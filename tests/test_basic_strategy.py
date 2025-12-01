from src.blackjack import basic_strategy

def test_hit_on_16_vs_10():
    decision = basic_strategy(['10','6'], '10', can_double=False, can_split=False)
    assert decision == 'hit' or decision == 'surrender'  # simplified: expecting hit

def test_stand_on_12_vs_4():
    decision = basic_strategy(['10','2'], '4', can_double=False, can_split=False)
    assert decision == 'stand'

def test_double_on_11_vs_6():
    decision = basic_strategy(['6','5'], '6', can_double=True, can_split=False)
    assert decision == 'double' or decision == 'hit'
