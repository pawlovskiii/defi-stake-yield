def add_allowed_tokens(token_yield, dict_of_allowed_tokens, account):
    for token in dict_of_allowed_tokens:
        add_tx = token_yield.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)
        set_tx = token_yield.setPriceFeedContract(token.address, dict_of_allowed_tokens[token], {"from": account})
        set_tx.wait(1)
    return token_yield