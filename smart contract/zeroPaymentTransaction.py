from web3 import Web3
from web3.auto.infura import w3
from web3.middleware import geth_poa_middleware

w3 = Web3(Web3.HTTPProvider('<put your infura_project_id here>'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

myAdr = '0xa5C64A61D225Bc5614a2CE5fAc81926438e93844'
private_key = '<put your private_key here>'
nonce = w3.eth.getTransactionCount(myAdr)
message = "Hello world"

transaction = {
    'from': myAdr,
    'to': '0x1C49AA3FEAb57bc27Ad79F0De64862786766F611',
    'value': 0,
    'gas': 2000000,
    'gasPrice': 1000000000,
    'nonce': nonce,
    'data': message.encode(),
    'chainId': 4
}

signed_tx = w3.eth.account.signTransaction(transaction, private_key)
print("Sending transaction...")
txn_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
print(txn_hash)
txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
print(txn_receipt)
