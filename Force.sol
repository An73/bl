pragma solidity ^0.4.18;

contract Force {
    address addr;
    function Force(address a) public payable {
        addr = a;
    }
    
    function () public payable {
        selfdestruct(addr);
    }
}
