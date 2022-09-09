import pytest
from brownie import exceptions
from scripts.helpful_modules.network_check import isNetworkLocal
from scripts.helpful_modules.get_account import get_account
from scripts.helpful_modules.deploy_token_yield_and_vistula_token import (
    deploy_token_yield_and_vistula_token_contracts,
)


def test_add_allowed_tokens():
    # Arrange
    isNetworkLocal()
    account = get_account()
    non_owner = get_account(index=1)
    yield_token, vistula_token = deploy_token_yield_and_vistula_token_contracts()
    # Act
    yield_token.addAllowedTokens(vistula_token.address, {"from": account})
    # Assert
    assert yield_token.allowedTokens(0) == vistula_token.address
    with pytest.raises(exceptions.VirtualMachineError):
        yield_token.addAllowedTokens(vistula_token.address, {"from": non_owner})


def test_token_is_allowed():
    # Arrange
    isNetworkLocal()
    account = get_account()
    yield_token, vistula_token = deploy_token_yield_and_vistula_token_contracts()
    # Act
    yield_token.tokenIsAllowed(vistula_token.address, {"from": account})
    # Assert
    assert yield_token.tokenIsAllowed(vistula_token.address) == True
