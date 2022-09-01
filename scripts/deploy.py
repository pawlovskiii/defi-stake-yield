from scripts.get_account import get_account
from brownie import VLAToken, TokenYield, config, network


def deploy_vistula_token():
    account = get_account()
    vistula_token = VLAToken.deploy(10000000000, {"from": account})
    return vistula_token


def vistula_token():
    pass


def deploy_token_yield():
    account = get_account()
    token_yield = TokenYield.deploy(
        deploy_vistula_token().address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )


def main():
    deploy_vistula_token()
    deploy_token_yield()
    pass
