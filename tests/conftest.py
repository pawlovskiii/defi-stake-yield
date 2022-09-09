import pytest
from web3 import Web3
from brownie import MockERC20
from scripts.helpful_modules.get_account import get_account


@pytest.fixture
def staked_amount():
    return Web3.toWei(1, "ether")


@pytest.fixture
def random_erc20():
    account = get_account()
    erc20 = MockERC20.deploy({"from": account})
    return erc20
