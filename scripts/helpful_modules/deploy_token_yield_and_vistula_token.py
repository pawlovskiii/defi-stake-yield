from scripts.helpful_modules.get_account import get_account
from scripts.helpful_modules.add_allowed_tokens import add_allowed_tokens
from scripts.helpful_modules.dict_of_tokens import dict_of_allowed_tokens
from brownie import TokenYield, VLAToken, config, network
from web3 import Web3

KEPT_BALANCE = Web3.toWei(100, "ether")
INITIAL_SUPPLY = 1000000000000000000000000


def deploy_token_yield_and_vistula_token_contracts():
    account = get_account()

    vistula_token = VLAToken.deploy(
        INITIAL_SUPPLY, {"from": account}, publish_source=config["networks"][network.show_active()]["verify"]
    )
    token_yield = TokenYield.deploy(
        vistula_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    tx = vistula_token.transfer(token_yield.address, vistula_token.totalSupply() - KEPT_BALANCE, {"from": account})
    tx.wait(1)

    add_allowed_tokens(token_yield, dict_of_allowed_tokens(vistula_token), account)

    return token_yield, vistula_token
