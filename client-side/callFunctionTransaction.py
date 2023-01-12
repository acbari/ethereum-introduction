from web3 import Web3
from web3.auto import w3
from web3.middleware import geth_poa_middleware
import json
from fwev_abi import ABI

w3 = Web3(Web3.HTTPProvider('<put your infura_project_id here>'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

myAdr2 = '<put your account_2 address here>'
private_key2 = '<put the private_key of the account_2 here>'
nonce = w3.eth.getTransactionCount(myAdr2)

abi = ABI
scadr = Web3.toChecksumAddress("<put your smart contract address here>")
myContract = w3.eth.contract(address=scadr, abi=abi)

transaction = {
    'from': myAdr2,
    'value': 0,
    'gas': 2000000,
    'gasPrice': 2500000000,
    'nonce': nonce,
    'chainId': 11155111
}
#chain Id: 11155111 => sepolia test network

pk2 = "<put the RSA public key for account 2 here>"
deploy_txn = myContract.functions.req_connection(123,pk2).buildTransaction(transaction)
#req_connection function has two parameters: req_id and req_PK

signed_txn = w3.eth.account.sign_transaction(deploy_txn, private_key=private_key)
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(txn_hash.hex())

#theese codes bellow generated error to INFURA API: 429 Client Error: Too Many Requests for url
#we are missing a method to get the transaction status, whether it is succesfully recorded/failed?

#txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
#print(txn_receipt)
#print(txn_receipt['contractAddress'])
