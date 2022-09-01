from scripts.get_account import get_account
from brownie import VLAToken, TokenYield, config, network
from web3 import Web3

KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_vistula_token():
    account = get_account()
    vistula_token = VLAToken.deploy(10000000000, {"from": account})
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

    # weth_token = get_contract("fau_token")
    # fau_token = get_contract("weth_token")

    add_allowed_tokens(token_yield)


def add_allowed_tokens(token_yield):
    pass


def main():
    deploy_token_yield()
