import pytest
from brownie import exceptions
from scripts.helpful_modules.network_check import isNetworkLocal
from scripts.helpful_modules.get_account import get_account
from scripts.helpful_modules.get_contract import get_contract
from scripts.helpful_modules.deploy_mocks import INITIAL_PRICE_FEED_VALUE, DECIMALS
from scripts.helpful_modules.deploy_token_yield_and_vistula_token import (
    KEPT_BALANCE,
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


def test_issue_tokens(amount_staked):
    # Arrange
    isNetworkLocal()
    account = get_account()
    yield_token, vistula_token = test_stake_tokens(amount_staked)
    starting_balance = vistula_token.balanceOf(account.address)
    # Act
    yield_token.issueTokens({"from": account})
    # Arrange
    assert vistula_token.balanceOf(account.address) == starting_balance + INITIAL_PRICE_FEED_VALUE


def test_get_user_total_value_with_different_tokens(amount_staked, random_erc20):
    # Arrange
    isNetworkLocal()
    account = get_account()
    yield_token, vistula_token = test_stake_tokens(amount_staked)
    # Act
    yield_token.addAllowedTokens(random_erc20.address, {"from": account})
    yield_token.setPriceFeedContract(random_erc20.address, get_contract("eth_usd_price_feed"), {"from": account})
    random_erc20_stake_amount = amount_staked * 2
    random_erc20.approve(yield_token.address, random_erc20_stake_amount, {"from": account})
    yield_token.stakeTokens(random_erc20_stake_amount, random_erc20.address, {"from": account})
    # Assert
    total_value = yield_token.getUserTotalValue(account.address)
    assert total_value == INITIAL_PRICE_FEED_VALUE * 3


def test_get_token_value():
    # Arrange
    isNetworkLocal()
    yield_token, vistula_token = deploy_token_yield_and_vistula_token_contracts()
    # Act / Assert
    assert yield_token.getTokenValue(vistula_token.address) == (
        INITIAL_PRICE_FEED_VALUE,
        DECIMALS,
    )


def test_unstake_tokens(amount_staked):
    # Arrange
    isNetworkLocal()
    account = get_account()
    yield_token, vistula_token = test_stake_tokens(amount_staked)
    # Act
    yield_token.unstakeTokens(vistula_token.address, {"from": account})
    assert vistula_token.balanceOf(account.address) == KEPT_BALANCE
    assert yield_token.stakingBalance(vistula_token.address, account.address) == 0
    assert yield_token.uniqueTokensStaked(account.address) == 0


def test_add_allowed_tokens():
    # Arrange
    isNetworkLocal()
    account = get_account()
    non_owner = get_account(index=1)
    yield_token, vistula_token = deploy_token_yield_and_vistula_token_contracts()
    # Act
    yield_token.addAllowedTokens(vistula_token.address, {"from": account})
    # Assert
    assert yield_token.allowedTokens(0) == vistula_token.address
    with pytest.raises(exceptions.VirtualMachineError):
        yield_token.addAllowedTokens(vistula_token.address, {"from": non_owner})
