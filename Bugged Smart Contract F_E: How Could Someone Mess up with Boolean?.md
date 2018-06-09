#  Bugged Smart Contract F_E: How Could Someone Mess up with Boolean?

Recently SECBIT team found a serious bug about the `if` condition in a deployed ERC20 smart contract called F_E(intentionally hidden, see Footnote for details) and here is the bugged part:

```js
//Function for transer the coin from one address to another
function transferFrom(address from, address to, uint value) returns (bool success) {

    //checking account is freeze or not
    if (frozenAccount[msg.sender]) return false;

    //checking the from should have enough coins
    if(balances[from] < value) return false;

    //checking for allowance
    if( allowed[from][msg.sender] >= value ) return false;

    //checking for overflows
    if(balances[to] + value < balances[to]) return false;

    balances[from] -= value;
    allowed[from][msg.sender] -= value;
    balances[to] += value;

    // Notify anyone listening that this transfer took place
    Transfer(from, to, value);

    return true;
}
```

Pay attention to this line: `if( allowed[from][msg.sender] >= value ) return false;` It has a serious bug: the developer messed up with the boolean judgment - if the input value is smaller than or equal to allowed value, the transfer session would stop execution by returning false. This makes no sense because the transferFrom() requires the transferring value not exceeding the allowed value in the first place. Suppose this function asks the allowed value to be smaller than the input, the attackers could easily ignore the allowance: after this condition, the `allowed[from][msg.sender] -= value;` would cause an underflow for that the allowed part is smaller than the value. The attacker could transfer any amount of tokens of any accounts to an appointed account (the `_to` address) because the allowed value is initialized to 0 and the attacker could bypass this restriction even without the victim's private key.



Comparing to this one, we could take the UET bug as a reference (see Reference 1, 2 and 4 for details):

```js
function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
    // mitigates the ERC20 short address attack
    if(msg.data.length < (3 * 32) + 4) {
        throw;
    }
    if (_value == 0) {
        return false;
    }
    uint256 fromBalance = balances[_from];
    uint256 allowance = allowed[_from][msg.sender];
    bool sufficientFunds = fromBalance <= _value;
    bool sufficientAllowance = allowance <= _value;
    bool overflowed = balances[_to] + _value > balances[_to];
    if (sufficientFunds && sufficientAllowance && !overflowed) {
        balances[_to] += _value;
        balances[_from] -= _value;
        allowed[_from][msg.sender] -= _value;
        Transfer(_from, _to, _value);
        return true;
    } else {
        return false;
    }
}
```

With every necessary condition checked, the only problem here is that the programmer was so careless that every judging condition got set as the opposite, e.g. let `fromBalace <= _value` means the transferred money should be no less than the balance. If we just set this condition, there is no doubt that an underflow will occur. 



Now some deployed contracts like RemiCoin(RMC) and RoyalClassicCoin(RCL) (see Reference 3 for details) have this kind of bug as well. SECBIT strongly suggest anyone in concern be extremely careful when trading. Sadly we SECBIT team have tried but could not get in touch with the developer team.







#### Footnote

F_E is an intentionally hidden name of the contract with SHA3 256: 62c2235a3744a1d15cc15bb7f778e3228e07a9fd73cc8aae727a079dd21f0642

#### Reference

1. CVE-2018-10468: http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-10468
2. UselessEthereumToken(UET), ERC20 Token, allows attackers to steal all victim's balances (CVE-2018-10468): <https://medium.com/@jonghyk.song/uselessethereumtoken-uet-erc20-token-allows-attackers-to-steal-all-victims-balances-543d42ac808e>
3. RemiCoin: https://etherscan.io/address/0x7Dc4f41294697a7903C4027f6Ac528C5d14cd7eB#code
4. UET:  https://etherscan.io/address/0x27f706edde3aD952EF647Dd67E24e38CD0803DD6#code
