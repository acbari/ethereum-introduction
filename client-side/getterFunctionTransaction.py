from web3 import Web3
from web3.auto import w3
from web3.middleware import geth_poa_middleware
import json
from fwev_abi import ABI   #fwev_abi.py has ABI variable that contain the ABI string of the smart contract 

w3 = Web3(Web3.HTTPProvider('<put your infura_project_id here>'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

myAdr = '<put your account address here>'
private_key = '<put your private_key here>'
nonce = w3.eth.getTransactionCount(myAdr) #get the transaction count of our account

abi = ABI
myContract = w3.eth.contract(address="<put your deployed smart contract address here>", abi=abi)

txn_receipt = myContract.functions.owner().call() #change owner() function with the getter_function/public_variable that you want call/read

print(txn_receipt)
