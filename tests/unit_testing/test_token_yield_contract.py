import pytest
from brownie import network, exceptions
from scripts.helpful_modules.get_account import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.helpful_modules.get_contract import get_contract
from scripts.helpful_modules.deploy_token_yield_and_vistula_token import deploy_token_yield_and_vistula_token_contracts


def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
    non_owner = get_account(index=1)
    yield_token, vistula_token = deploy_token_yield_and_vistula_token_contracts()

    # Act
    price_feed_address = get_contract("eth_usd_price_feed")

    # Assert
    assert yield_token.tokenPriceFeedMapping(vistula_token.address) == price_feed_address
    with pytest.raises(exceptions.VirtualMachineError):
        yield_token.setPriceFeedContract(vistula_token.address, price_feed_address, {"from": non_owner})
