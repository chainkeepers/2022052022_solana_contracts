//SPDX-License-Identifier: Unlicense
pragma solidity ^0.8.7;

contract Counter {
    uint private counter;

    event counterEvent(
        uint indexed oldCounter,
        uint indexed newCounter,
        address sender
    );

    constructor(uint  _counter) {
        emit counterEvent(
            0,
            _counter,
            msg.sender
        );
        counter = _counter;
    }

    function retrieve() public view returns (uint) {
        return counter;
    }

    function setCounter(uint _counter) public {
        emit counterEvent(
            counter,
            _counter,
            msg.sender
        );
        counter = _counter;
    }

    function addCounter() public {
        emit counterEvent(
            counter,
            counter+1,
            msg.sender
        );
        counter += 1;
    }
}
