from brownie import (
    network,
    config,
    Contract,
)
from scripts.helpful_modules.deploy_mocks import deploy_mocks
from scripts.helpful_modules.dict_of_mocks import contract_to_mock
from scripts.helpful_modules.get_account import NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS


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
