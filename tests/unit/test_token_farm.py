from brownie import network, exceptions
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.deploy import deploy_token_farm_and_dapp_token
from web3 import Web3
import pytest

AMOUNT_STAKED = Web3.toWei(1, "ether")

def main():
    pass

def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip
    account = get_account()    
    non_owner = get_account(index = 1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()

    # Act
    price_feed_address = get_contract("eth_usd_price_feed")
    token_farm.setPriceFeedContract(dapp_token.address, price_feed_address,  {"from": account})
    
    # Assert
    assert token_farm.tokenPriceFeedMapping(dapp_token.address) == price_feed_address

def test_set_price_feed_contract_with_non_owner():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip
    account = get_account()    
    non_owner = get_account(index = 1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()

    # Act
    price_feed_address = get_contract("eth_usd_price_feed")
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(dapp_token.address, price_feed_address,  {"from": non_owner})
    
def test_stake_tokens():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip
    account = get_account()    
    non_owner = get_account(index = 1)
    token_farm, dapp_token = deploy_token_farm_and_dapp_token()

    # Act
    dapp_token.approve(token_farm.address, AMOUNT_STAKED, {"from": account})
    token_farm.stakeTokens(AMOUNT_STAKED, dapp_token.address, {"from": account})

    # Assert
    assert token_farm.stakingBalance(dapp_token.address, account.address) == AMOUNT_STAKED
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    return token_farm, dapp_token


def test_issue_tokens():
    pass