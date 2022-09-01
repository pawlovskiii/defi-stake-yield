from brownie import network, LinkToken, MockV3Aggregator, MockDAI, MockWETH
from scripts.get_account import get_account

INITIAL_PRICE_FEED_VALUE = 2000000000000000000000
DECIMALS = 18


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_PRICE_FEED_VALUE):

    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    account = get_account()
    print("Deploying Mock Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    print(f"Deployed to {mock_price_feed.address}")
    print("Deploying Mock DAI...")
    dai_token = MockDAI.deploy({"from": account})
    print(f"Deployed to {dai_token.address}")
    print("Deploying Mock WETH")
    weth_token = MockWETH.deploy({"from": account})
    print(f"Deployed to {weth_token.address}")
