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


def test_stake_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing!")
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
