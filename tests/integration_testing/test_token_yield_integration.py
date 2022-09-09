from scripts.helpful_modules.network_check import isNetworkLocal
from scripts.helpful_modules.get_account import get_account
from scripts.helpful_modules.get_contract import get_contract
from scripts.helpful_modules.deploy_token_yield_and_vistula_token import deploy_token_yield_and_vistula_token_contracts


def test_stake_and_issue_correct_amounts(staked_amount):
    # Arrange
    isNetworkLocal()
    yield_token, vistula_token = deploy_token_yield_and_vistula_token_contracts()
    account = get_account()
    vistula_token.approve(yield_token.address, staked_amount, {"from": account})
    yield_token.stakeTokens(staked_amount, vistula_token.address, {"from": account})
    starting_balance = vistula_token.balanceOf(account.address)
    price_feed_contract = get_contract("dai_usd_price_feed")
    (_, price, _, _, _) = price_feed_contract.latestRoundData()
    amount_token_to_issue = (price / 10 ** price_feed_contract.decimals()) * staked_amount
    # Act
    issue_tx = yield_token.issueTokens({"from": account})
    issue_tx.wait(1)
    # Assert
    assert vistula_token.balanceOf(account.address) == amount_token_to_issue + starting_balance
