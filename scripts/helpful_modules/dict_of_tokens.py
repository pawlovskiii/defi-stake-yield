from scripts.helpful_modules.get_contract import get_contract


def dict_of_allowed_tokens(vistula_token):

    weth_token = get_contract("weth_token")
    fau_token = get_contract("fau_token")

    dict_of_tokens = {
        vistula_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }

    return dict_of_tokens
