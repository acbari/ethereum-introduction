from web3 import Web3
from web3.auto.infura import w3

w3 = Web3(Web3.HTTPProvider('<put your infura_project_id here>'))
LastBlock = w3.eth.blockNumber
print(LastBlock)

from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

BlockInfo = w3.eth.get_block(LastBlock)

print(BlockInfo)
print(BlockInfo['difficulty'])
print(BlockInfo['timestamp'])
print(BlockInfo['totalDifficulty'])
