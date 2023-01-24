# import the following dependencies
import json
from web3 import Web3
import asyncio
from fwev_abi import ABI2 as ABI
import json

# add your blockchain connection information
infura_url = 'infura project url'
web3 = Web3(Web3.HTTPProvider(infura_url))

# contract address and abi
sc_adr = Web3.toChecksumAddress('contract address')
sc_abi = ABI

contract = web3.eth.contract(address=sc_adr, abi=sc_abi)


# define function to handle events and print to the console
def handle_event(event):
    strval = Web3.toJSON(event)
	data = json.loads(strval)
	print(data)
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
