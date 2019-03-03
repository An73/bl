pragma solidity ^0.4.18;

contract Korol {
    address public king;
    
    function Korol(address addr) public {
        king = addr;
    }
    
    function sendToKing() public payable {
        king.call.value(100000000000000000000)();
    }
    
    function ()external payable {
        revert();
    } 
}