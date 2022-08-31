// SPDX-License-Identifier: MIT
pragma solidity ^0.8.5;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract VLAToken is ERC20 {
    constructor(uint256 initialSupply) ERC20("Vistula", "VLA") {
        _mint(msg.sender, initialSupply);
    }
}