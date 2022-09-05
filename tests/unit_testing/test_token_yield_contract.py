import pytest
from brownie import exceptions
from scripts.helpful_modules.network_check import isNetworkLocal
from scripts.helpful_modules.get_account import get_account
from scripts.helpful_modules.get_contract import get_contract
from scripts.helpful_modules.deploy_token_yield_and_vistula_token import deploy_token_yield_and_vistula_token_contracts


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


def test_stake_tokens(amount_staked):
    # Arrange
    isNetworkLocal()
    account = get_account()
    yield_token, vistula_token = deploy_token_yield_and_vistula_token_contracts()
    # Act
    vistula_token.approve(yield_token.address, amount_staked, {"from": account})
    yield_token.stakeTokens(amount_staked, vistula_token.address, {"from": account})
    # Assert
    assert yield_token.stakingBalance(vistula_token.address, account.address) == amount_staked
    assert yield_token.uniqueTokensStaked(account.address) == 1
    assert yield_token.stakers(0) == account.address
    return yield_token, vistula_token
