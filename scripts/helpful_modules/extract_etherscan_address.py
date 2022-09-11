TESTNET_NETWORKS = ["goerli", "rinkeby"]


def extractLinkToEtherscanWebsite(testnet, contractAddress):
    if testnet in TESTNET_NETWORKS:
        print(f"\nhttps://{testnet}.etherscan.io/address/{contractAddress}\n")
