from brownie import (
    network,
    config,
    Contract,
    MockV3Aggregator,
    MockWETH,
    MockDAI,
)
from scripts.helpful_modules.deploy_mocks import deploy_mocks
from scripts.helpful_modules.get_account import NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "dai_usd_price_feed": MockV3Aggregator,
    "fau_token": MockDAI,
    "weth_token": MockWETH,
}


def get_contract(contract_name):

    contract_type = contract_to_mock[contract_name]

    if network.show_active() in NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        try:
            contract_address = config["networks"][network.show_active()][contract_name]
            contract = Contract.from_abi(contract_type._name, contract_address, contract_type.abi)
        except KeyError:
            print(f"{network.show_active()} network is invalid")

    return contract
