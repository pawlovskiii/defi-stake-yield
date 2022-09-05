import pytest
from scripts.helpful_modules.get_account import LOCAL_BLOCKCHAIN_ENVIRONMENTS
from brownie import network


def isNetworkLocal() -> None:
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
