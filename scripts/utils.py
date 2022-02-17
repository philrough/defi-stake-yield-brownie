from brownie import accounts, network, config, Contract, interface, DappToken, MockWETH, MockFAU, MockV3Aggregator

INITIAL_PRICE_FEED_VALUE = 2000000000000000000000
DECIMALS = 18

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local" "mainnet-fork"]

contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator, "dai_usd_price_feed": MockV3Aggregator, "weth_token": MockWETH, "fau_token": MockFAU}

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in FORKED_LOCAL_ENVIRONMENTS or network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract




def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()
    print("Deploying mock fau...")
    fau_token = MockFAU.deploy({"from": account})
    print("Deploying mock weth...")
    weth_token = MockWETH.deploy({"from": account})
    print("Deploying Mock Price Feed...")
    mock_price_feed = MockV3Aggregator.deploy(
        DECIMALS, INITIAL_PRICE_FEED_VALUE, {"from": account}
    )