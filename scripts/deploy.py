from brownie import FundMe, accounts, network, config, MockV3Aggregator
from web3 import Web3

from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fundme():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pricefeed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        pricefeed_address = MockV3Aggregator[-1].address
        print("Mocks deployed")

    # Pass the pricefeed contract to fundme contract
    print("Deploying FundMe")
    fundme = FundMe.deploy(
        pricefeed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print("Contract deployed to address", fundme)
    return fundme


def main():
    deploy_fundme()
