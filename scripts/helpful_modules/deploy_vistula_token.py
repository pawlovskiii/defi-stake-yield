from scripts.helpful_modules.get_account import get_account
from brownie import VLAToken


def deploy_vistula_token_contract():
    account = get_account()
    vistula_token = VLAToken.deploy(1000000000000000000000000, {"from": account})
    return vistula_token
