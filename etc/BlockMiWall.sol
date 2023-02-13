// SPDX-License-Identifier: GPL-3.0
pragma solidity >= 0.8.0;

contract BlockMiWall{
    //data EV
    string public Name;     //Car nick name
    address public Owner;   //Owner's Account 
    uint public EVID;       //ID of the electric vehicle
    //string public PK;       //EV's public key
    mapping(uint => string) public PK;
    mapping(uint => uint) public updateTime;
    uint public ctrPK;

    //Request management
    uint public number;                            //Record max counter
    mapping(uint => address) public Req_ID;     //Request_counter: requester account
    mapping(address => uint) public Req_Number;      //Requester account: Request_counter
    mapping(uint => string) public Req_Data;    //account: secret(secret( MAC_adr, Req_secretnumber))
    mapping(uint => string) public Req_PK;      //account: RSA Public key

    //Reply management
    mapping(uint => string) public Rep_Data;      //Request_number: secret( IP, Port, EV_secretnumber)
    
    //Event management
    event NewRequest(uint indexed number, address indexed requester, string Req_Data, string pk);
    event NewReply(uint indexed number, string Rep_Data);

    constructor(string memory CarNickName, uint ev_id, string memory PK_EV) {
        Owner = msg.sender;
        Name = CarNickName;
        EVID = ev_id;
        
        number = 0;
        ctrPK = 1;
        PK[ctrPK] = PK_EV;
        updateTime[ctrPK] = block.timestamp;
    }
    
    function req_connection(string memory SecretData, string memory req_PK ) public returns (uint ctr_){
        if (Req_Number[msg.sender] == 0){
            number = number + 1;
            Req_ID[number] = msg.sender;
            Req_Number[msg.sender] = number;
        }
        Req_Data[number] =  SecretData;
        Req_PK[number] = req_PK;    

        ctr_ = number;
        emit NewRequest(ctr_, msg.sender, SecretData, req_PK);
    }

    function rep_connection(uint req_counter, string memory enc_value ) public {
        require(
            msg.sender == Owner,
            "Only owner can grant the connection!"
        );
        require(
            req_counter <= number && req_counter > 0,
            "Index out of range"
        );

        Rep_Data[req_counter] = enc_value;
       
        emit NewReply(req_counter, enc_value);
    }
    
    function update_PK(string memory new_PK ) public {
        require(
            msg.sender == Owner,
            "Only owner can modify the public key!"
        );
        ctrPK = ctrPK + 1;
        PK[ctrPK] = new_PK;
        updateTime[ctrPK] = block.timestamp;
    }

    function getPK() public view returns (string memory PK_)
    {
        PK_ = PK[ctrPK];
    }
}
