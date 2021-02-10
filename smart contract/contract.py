from eth_account import Account
from eth_account.messages import encode_defunct
import json, random, subprocess

def compileContract(solcPath, contractFile, genModule=False):
    """solc download link for windows: https://github.com/ethereum/solidity/releases
    """

    #solc-windows.exe --bin --abi owner.sol
    res = subprocess.check_output([solcPath,"--bin","--abi",contractFile], shell=True)
    res = str(res).split("Contract JSON ABI")
    abi = res[1][4:-5]
    bytecode = res[0].split("Binary:")[1][4:-4]
    #print(abi)
    #print(bytecode)
    if genModule:
        fnames = contractFile.split(".")
        fname = fnames[len(fnames)-2]+"_module.py"
        with open(fname, "w") as f:
            f.write("ABI = \"\"\""+abi+"\"\"\"" + "\n\n")
            f.write("BC = \"\"\""+bytecode+"\"\"\"")
    return abi, bytecode

def genContract(solcPath, contractFile, trx=None, prm = []):
    from web3.auto.infura import w3
    abi, bytecode = compileContract(solcPath, contractFile)
    abi = json.loads(abi)
    myContract = w3.eth.contract(abi=abi, bytecode=bytecode)
    if trx == None:
        return myContract
    else:  
        if len(prm) == 3:
            deploy_txn = myContract.constructor(prm[0],prm[1],prm[2]).buildTransaction(trx)
        elif len(prm) == 2:
            deploy_txn = myContract.constructor(prm[0],prm[1]).buildTransaction(trx)
        elif len(prm) == 1:
            deploy_txn = myContract.constructor(prm[0]).buildTransaction(trx)
        else:
            deploy_txn = myContract.constructor().buildTransaction(trx)
        return deploy_txn
        
if __name__ == "__main__":
    #test compile contract owner.sol
    abi, bytecode = compileContract("solc-windows.exe","owner.sol")
    print(abi)
    print(bytecode)
    
    #compile and generate module
    abi, bytecode = compileContract("solc-windows.exe","ballot.sol", True)
    print(abi)
    print(bytecode)
    
