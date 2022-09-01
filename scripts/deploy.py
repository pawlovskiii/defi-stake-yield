from scripts.get_contract import get_contract
from scripts.get_account import get_account
from brownie import VLAToken, TokenYield, config, network
from web3 import Web3

KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_vistula_token():
    account = get_account()
    vistula_token = VLAToken.deploy(1000000000000000000000000, {"from": account})
    return vistula_token


def deploy_token_yield():
    account = get_account()
    token_yield = TokenYield.deploy(
        deploy_vistula_token().address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    tx = deploy_vistula_token().transfer(
        token_yield.address, deploy_vistula_token().totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(1)

    weth_token = get_contract("fau_token")
    fau_token = get_contract("weth_token")
    dict_of_allowed_tokens = {
        deploy_vistula_token(): get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }

    add_allowed_tokens(token_yield, dict_of_allowed_tokens, account)
    return token_yield


def add_allowed_tokens(token_yield, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_yield.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_yield.setPriceFeedContract(token.address, dict_of_allowed_tokens[token], {"from": account})
        set_tx.wait(1)
    return token_yield


def main():
    deploy_token_yield()
