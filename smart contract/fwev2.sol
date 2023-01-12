pragma solidity >= 0.8.0;

contract Firewall_EV{

    mapping(uint => bool) public isRequested;   //req_id: Requested status
    mapping(uint => bool) public isReplied;     //req_id: Replied status
    mapping(uint => string) public EncVal;      //req_id: reply_EncVal
    mapping(uint => string) public HashVal;     //req_id: reply_HashVal
    
    string public Name;
    address public owner;
    uint public EVID;
    string public PK;

    uint public ctr;
    mapping(uint => uint) public Rctr;      //ctr: req_id
    mapping(uint => address) public R_Adr;  //req_id: req_address
    mapping(uint => string) public R_PK;    //req_id: req_pk
    
    event NewRequest(address indexed requester, uint indexed counter, uint indexed rid);
    event NewReply(uint indexed rid, string result);

    constructor(string memory name, uint ev_id, string memory PK_EV) {
        owner = msg.sender;
        Name = name;
        EVID = ev_id;
        PK = PK_EV;
        ctr = 0;
    }
    
    function req_connection(uint req_id, string memory req_PK ) public returns (uint ctr_){
        require(
            isRequested[req_id] == false,
            "Request ID has been recorded!"
        );

        isRequested[req_id] = true;
        
        ctr = ctr + 1;
        Rctr[ctr] = req_id;
        R_Adr[req_id] = msg.sender;
        R_PK[req_id] = req_PK;
        ctr_ = ctr;
        
        isReplied[req_id] = false;
        emit NewRequest(msg.sender, ctr, req_id);
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
        isReplied[req_id] = true;
        emit NewReply(req_id, enc_value);
    }
    
    function update_PK(string memory new_PK ) public {
        require(
            msg.sender == owner,
            "Only owner can modify the public key!"
        );
        PK = new_PK;
    }
    
    function get_Req_id(uint index) public view returns (uint rid_){
        require(
            index <= ctr && index > 0,
            "Index out of range"
        );
        rid_ = Rctr[index];
    }

}
