from scripts.helpful_modules.network_check import isNetworkLocal
from scripts.helpful_modules.get_account import get_account
from scripts.helpful_modules.get_contract import get_contract
from scripts.helpful_modules.deploy_mocks import INITIAL_PRICE_FEED_VALUE
from scripts.helpful_modules.deploy_token_yield_and_vistula_token import (
    KEPT_BALANCE,
    deploy_token_yield_and_vistula_token_contracts,
)


def test_stake_tokens(staked_amount):
    # Arrange
    isNetworkLocal()
    account = get_account()
    yield_token, vistula_token = deploy_token_yield_and_vistula_token_contracts()
    # Act
    vistula_token.approve(yield_token.address, staked_amount, {"from": account})
    yield_token.stakeTokens(staked_amount, vistula_token.address, {"from": account})
    # Assert
    assert yield_token.stakingBalance(vistula_token.address, account.address) == staked_amount
    assert yield_token.uniqueTokensStaked(account.address) == 1
    assert yield_token.stakers(0) == account.address
    return yield_token, vistula_token


def test_issue_tokens(staked_amount):
    # Arrange
    isNetworkLocal()
    account = get_account()
    yield_token, vistula_token = test_stake_tokens(staked_amount)
    starting_balance = vistula_token.balanceOf(account.address)
    # Act
    yield_token.issueTokens({"from": account})
    # Arrange
    assert vistula_token.balanceOf(account.address) == starting_balance + INITIAL_PRICE_FEED_VALUE


def test_get_user_total_value_with_different_tokens(staked_amount, random_erc20):
    # Arrange
    isNetworkLocal()
    account = get_account()
    yield_token, vistula_token = test_stake_tokens(staked_amount)
    # Act
    yield_token.addAllowedTokens(random_erc20.address, {"from": account})
    yield_token.setPriceFeedContract(random_erc20.address, get_contract("eth_usd_price_feed"), {"from": account})
    random_erc20_stake_amount = staked_amount * 2
    random_erc20.approve(yield_token.address, random_erc20_stake_amount, {"from": account})
    yield_token.stakeTokens(random_erc20_stake_amount, random_erc20.address, {"from": account})
    # Assert
    total_value = yield_token.getUserTotalValue(account.address)
    assert total_value == INITIAL_PRICE_FEED_VALUE * 3


def test_unstake_tokens(staked_amount):
    # Arrange
    isNetworkLocal()
    account = get_account()
    yield_token, vistula_token = test_stake_tokens(staked_amount)
    # Act
    yield_token.unstakeTokens(vistula_token.address, {"from": account})
    assert vistula_token.balanceOf(account.address) == KEPT_BALANCE
    assert yield_token.stakingBalance(vistula_token.address, account.address) == 0
    assert yield_token.uniqueTokensStaked(account.address) == 0
