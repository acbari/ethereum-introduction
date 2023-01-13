#ref: https://cryptomarketpool.com/how-to-listen-for-ethereum-events-using-web3-in-python/
import json
from web3 import Web3
import asyncio
from fwev_abi import ABI2 as ABI

#event name: NewRequest

# add your blockchain connection information
infura_url = '<put your infura project URL here>'
web3 = Web3(Web3.HTTPProvider(infura_url))

# contract address and abi
sc_adr = Web3.toChecksumAddress('<put your deployed smart contract address here>')
sc_abi = ABI

contract = web3.eth.contract(address=sc_adr, abi=sc_abi)


# define function to handle events and print to the console
def handle_event(event):
    print(Web3.toJSON(event))
    # and whatever


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "NewRequest" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for NewRequest in event_filter.get_new_entries():
            handle_event(NewRequest)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "NewRequest" event for the contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.NewRequest.createFilter(fromBlock='latest')
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()

    
""" Result for the first transaction :
{"args": 

{"requester": "0x5D45d875FD3A150f38241B8B6A573b0C40C646d3",
"counter": 1,
"rid": 124},

"event": "NewRequest",
"logIndex": 3,
"transactionIndex": 3,
"transactionHash": "0x03a112ceccff8d362483f534e13445314535794cc038a048b2b79ddad6d71f6f",
"address": "0x43f2Ac40b62Dff261d19144d3Cae5b30efE7ed92",
"blockHash": "0x6ef2f57c161f774e0db374a85d96680f12354fd73568e0fbe1c8ba8bf630620d",
"blockNumber": 2676636

}
"""
