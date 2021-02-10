from web3 import Web3
from web3.auto.infura import w3
from web3.middleware import geth_poa_middleware
from contract import compileContract
import json

w3 = Web3(Web3.HTTPProvider('<put your infura_project_id here>'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

myAdr = '0xa5C64A61D225Bc5614a2CE5fAc81926438e93844'
private_key = '<put your private_key here>'
nonce = w3.eth.getTransactionCount(myAdr)

abi, bc = compileContract("solc-windows.exe","owner.sol")
abi = json.loads(abi)
myContract = w3.eth.contract(address="0x5F06b8d51Cd337d48913C365000CA3b1465dAbA0", abi=abi)

transaction = {
    'from': myAdr,
    'value': 0,
    'gas': 2000000,
    'gasPrice': 1000000000,
    'nonce': nonce,
    'chainId': 4
}

deploy_txn = myContract.functions.changeOwner('0x1C49AA3FEAb57bc27Ad79F0De64862786766F611').buildTransaction(transaction)
signed_txn = w3.eth.account.sign_transaction(deploy_txn, private_key=private_key)
txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
print(txn_hash)
txn_receipt = w3.eth.waitForTransactionReceipt(txn_hash)
print(txn_receipt)
print(txn_receipt['contractAddress'])
