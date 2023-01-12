pragma solidity >= 0.8.0;

contract Firewall_EV{

    mapping(address => uint) public RID; //Requester_ID
    mapping(address => string) public RPK;

    mapping(uint => bool) public isRequested;
    mapping(uint => string) public EncVal;
    mapping(uint => string) public HashVal;
    
    string public Name;
    address public owner;
    uint public EVID;
    string public PK;
    
    constructor(string memory name, uint ev_id, string memory PK_EV) {
        owner = msg.sender;
        Name = name;
        EVID = ev_id;
        PK = PK_EV;
    }
    
    function req_connection(uint req_id, string memory req_PK ) public {
        require(
            isRequested[req_id] == false,
            "Request ID has been recorded!"
        );
        RID[msg.sender] = req_id;
        isRequested[req_id] = true;
        RPK[msg.sender] = req_PK;
    }

    function rep_connection(uint req_id, string memory enc_value, string memory hash_value ) public {
        require(
            msg.sender == owner,
            "Only owner can grant the connection!"
        );
        require(
            isRequested[req_id] == true,
            "Request ID is not recorded!"
        );
        EncVal[req_id] = enc_value;
        HashVal[req_id] = hash_value;
    }
        
    function update_PK(string memory new_PK ) public {
        require(
            msg.sender == owner,
            "Only owner can modify the public key!"
        );
        PK = new_PK;
    }
    
}
