import pytest
from brownie import exceptions
from scripts.helpful_modules.network_check import isNetworkLocal
from scripts.helpful_modules.get_account import get_account
from scripts.helpful_modules.get_contract import get_contract
from scripts.helpful_modules.deploy_mocks import INITIAL_PRICE_FEED_VALUE, DECIMALS
from scripts.helpful_modules.deploy_token_yield_and_vistula_token import (
    deploy_token_yield_and_vistula_token_contracts,
)


def test_set_price_feed_contract():
    # Arrange
    isNetworkLocal()
    non_owner = get_account(index=1)
    yield_token, vistula_token = deploy_token_yield_and_vistula_token_contracts()
    # Act
    price_feed_address = get_contract("eth_usd_price_feed")
    # Assert
    assert yield_token.tokenPriceFeedMapping(vistula_token.address) == price_feed_address
    with pytest.raises(exceptions.VirtualMachineError):
        yield_token.setPriceFeedContract(vistula_token.address, price_feed_address, {"from": non_owner})


def test_get_token_value():
    # Arrange
    isNetworkLocal()
    yield_token, vistula_token = deploy_token_yield_and_vistula_token_contracts()
    # Act / Assert
    assert yield_token.getTokenValue(vistula_token.address) == (
        INITIAL_PRICE_FEED_VALUE,
        DECIMALS,
    )
