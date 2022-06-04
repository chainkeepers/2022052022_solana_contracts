from scripts.helpful_scripts import get_account
from brownie import Counter


def test_event_is_fired():
    account = get_account()
    counter = Counter.deploy(1, {"from": account})

    number = counter.retrieve()
    assert number == 1
    
    transaction = counter.setCounter(2, {"from": account})
    transaction.wait(1)
    assert transaction.events["counterEvent"] is not None
    assert transaction.events["counterEvent"]["newCounter"] == 2
