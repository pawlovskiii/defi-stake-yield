from scripts.helpful_modules.get_contract import get_contract
from scripts.helpful_modules.get_account import get_account
from scripts.helpful_modules.add_allowed_tokens import add_allowed_tokens
from scripts.helpful_modules.deploy_vistula_token import deploy_vistula_token_contract
from brownie import TokenYield, config, network
from web3 import Web3

KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_token_yield_contract():
    account = get_account()
    token_yield = TokenYield.deploy(
        deploy_vistula_token_contract().address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    tx = deploy_vistula_token_contract().transfer(
        token_yield.address, deploy_vistula_token_contract().totalSupply() - KEPT_BALANCE, {"from": account}
    )
    tx.wait(1)

    weth_token = get_contract("fau_token")
    fau_token = get_contract("weth_token")
    dict_of_allowed_tokens = {
        deploy_vistula_token_contract(): get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }

    add_allowed_tokens(token_yield, dict_of_allowed_tokens, account)
    return token_yield
