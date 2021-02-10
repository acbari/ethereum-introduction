// SPDX-License-Identifier: GPL-3.0

pragma solidity >= 0.8.0;

contract ForumOne {
    
    mapping(address => bool) public Voter;
    struct Content {
        string name; // weight is accumulated by delegation
        uint vote; // person delegated to
        bool blocked;   // index of the voted proposal
        address[] voter;
    }
    
    mapping(address => bool) public isAdmin;
    mapping(address => bool) public isContributor;
    mapping(address => uint) public contributor;
    mapping(address => bool) public isBlockedAdmin;
    mapping(uint => bool) public isBlockedContent;
    
    string public Name;
    address owner;
    mapping(uint => Content) public contents;
    uint private AC;
    uint private CC;
    uint private TV;
    
    //0x5B38Da6a701c568545dCfcB03FcB875f56beddC4,0xAb8483F64d9C6d1EcF9b849Ae677dD3315835cb2
    //0x5b38da6a701c568545dCfcb03Fcb875f56beddc4,0xab8483f64d9c6d1ecf9b849ae677dd3315835cb2
    
    constructor(string memory name, uint thresholdValue) {
        owner = msg.sender;
        Name = name;
        TV = thresholdValue;
        if (TV < 3){
            TV = 3;
        }
        isAdmin[msg.sender] = true;
    }
    
    function addAdmin(address adminsAdr) public {
        require(
            msg.sender == owner,
            "Only owner can enroll new admin"
        );
        isAdmin[adminsAdr] = true;
    }
    
    //admin access
    function addContrib(address newContrib) public {
        require(
            isAdmin[msg.sender] == true,
            "Only admin can enroll new contributor."
        );
        require(
            isContributor[newContrib] == false,
            "The contributor already exist."
        );
        isContributor[newContrib] = true;
        contributor[newContrib] = AC;
        AC = AC + 1;
    }
    function removeContrib(address delContrib) public {
        require(
            isAdmin[msg.sender] == true,
            "Only admin can remove the contributor."
        );
        require(
            isContributor[delContrib] == true,
            "The contributor does not exist."
        );
        isContributor[delContrib] = true;
    }
    function blockContrib(address adr) public {
        require(
            isAdmin[msg.sender] == true,
            "Only admin can block the contributor."
        );
        isBlockedAdmin[adr] = true;
    }
    function unBlockContrib(address adr) public {
        require(
            isAdmin[msg.sender] == true,
            "Only admin can block the contributor."
        );
        isBlockedAdmin[adr] = false;
    }
    
    function blockContent(uint index) public {
        require(
            isAdmin[msg.sender] == true,
            "Only admin can block the content."
        );
        isBlockedContent[index] = true;
    }
    function setThreshold(uint value) public {
        require(
            isAdmin[msg.sender] == true,
            "Only admin can block the content."
        );
        TV = value;
    }
    
    //contributor access
    function addContent(string memory newContent) public {
        require(
            isContributor[msg.sender] == true,
            "Only contributor can create new content"
        );
        require(
            isBlockedAdmin[msg.sender] == false,
            "The contributor is block by admin"
        );
        contents[CC].name = newContent;
        contents[CC].vote = 1;
        contents[CC].blocked = false;
        contents[CC].voter.push(msg.sender);
    }
    function upVote(uint index) public {
        require(
            isContributor[msg.sender] == true,
            "Only contributor can create new content"
        );
        require(
            isBlockedAdmin[msg.sender] == false,
            "The contributor is block by admin"
        );
        require(
            isVoteContent(index) == false,
            "The contributor has voted"
        );
        contents[CC].vote += 1;
        contents[CC].voter.push(msg.sender);
    }
    function downVote(uint index) public {
        require(
            isContributor[msg.sender] == true,
            "Only contributor can create new content"
        );
        require(
            isBlockedAdmin[msg.sender] == false,
            "The contributor is block by admin"
        );
        require(
           isVoteContent(index) == false,
            "The contributor has voted"
        );
        contents[CC].vote -= 1;
        contents[CC].voter.push(msg.sender);
    }
    function getContent(uint index) public view returns (string memory content_){
        require(
            isContributor[msg.sender] == true,
            "Only contributor can get the raw content"
        );
        require(
            isBlockedAdmin[msg.sender] == false,
            "The contributor is block by admin"
        );
        content_ = contents[index].name;
    }
    function isVoteContent(uint index) public view returns (bool isExist_){
        isExist_ = false;
        for (uint i = 0; i < contents[index].voter.length; i++) {
            if (msg.sender == contents[index].voter[i]){
                isExist_ = true;
            }
        }
    }
    
    //anyone access
    function getValidContent(uint index) public view returns (string memory content_){
        require(
            contents[CC].vote >= TV,
            "Only contributor can create new content"
        );
        content_ = contents[index].name;
    }
    
    
}
