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

txn_receipt = myContract.functions.getOwner().call()
print(txn_receipt)
