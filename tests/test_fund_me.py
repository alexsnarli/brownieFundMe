from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fundme
from brownie import network, accounts, exceptions
import pytest


def test_fund_and_withdraw():
    account = get_account()
    fundme = deploy_fundme()
    entrance_fee = fundme.getEntranceFee() + 100
    tx = fundme.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fundme.addressToAmountFunded(account) == entrance_fee
    tx2 = fundme.withdraw({"from": account})
    tx2.wait(1)
    assert fundme.addressToAmountFunded(account) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    fundme = deploy_fundme()
    badactor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fundme.withdraw({"from": badactor})
