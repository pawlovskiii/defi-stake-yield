from scripts.helpful_modules.get_contract import get_contract
from scripts.helpful_modules.get_account import get_account
from scripts.helpful_modules.add_allowed_tokens import add_allowed_tokens
from brownie import TokenYield, VLAToken, config, network
from web3 import Web3

KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_token_yield_and_vistula_token_contracts():
    account = get_account()
    vistula_token = VLAToken.deploy(
        1000000000000000000000000, {"from": account}, publish_source=config["networks"][network.show_active()]["verify"]
    )
    token_yield = TokenYield.deploy(
        vistula_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    tx = vistula_token.transfer(token_yield.address, vistula_token.totalSupply() - KEPT_BALANCE, {"from": account})
    tx.wait(1)

    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")

    dict_of_allowed_tokens = {
        vistula_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }

    add_allowed_tokens(token_yield, dict_of_allowed_tokens, account)
    return token_yield, vistula_token
