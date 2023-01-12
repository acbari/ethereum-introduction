from web3 import Web3
from web3.auto import w3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider('<put your infura_project_id here>'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

myAdr = '<put your account address here>'
private_key = '<put the private_key of your account here>'
nonce = w3.eth.getTransactionCount(myAdr)

transaction = {
    'from': myAdr,
    'to': '<put the destination address here>',
    'value': 1000000000,
    'gas': 2000000,
    'gasPrice': 2500000000,
    'nonce': nonce,
    'chainId': 11155111
}

signed_tx = w3.eth.account.signTransaction(transaction, private_key)
print("Sending transaction...")
txn_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(txn_hash.hex())

#txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
#print(txn_receipt)
