from brownie import config, network
from brownie import Counter
from scripts.helpful_scripts import get_account


def deploy():
    account = get_account()
    counter = Counter.deploy(
        0,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "publish_source", False
        ),
    )
    tx = counter.setCounter(41, {"from": account})
    tx = counter.addCounter({"from": account})
    tx.wait(1)
    print(tx.events)
    print(f"Current counter is: {counter.retrieve()}")


def main():
    deploy()
