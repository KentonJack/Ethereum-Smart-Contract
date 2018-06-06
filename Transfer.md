# Silly Bugs in Smart Contracts

Even a Solidity beginner could notice that thousands of contracts deployed on Ethereum platform contain critical bugs. Taking transfer() and transferFrom() as an example, SECBIT Lab has scanned contracts on Ethereum and found 81 of them have made mistakes on simple comparison conditions. Moreover, code containing this problem could be seen all over, even on professional websites like StackOverflow or StackExchange!

#### Analysis of Bug Examples

Please notify that all code in this section contains vulnerabilities. Do Not Copy the Code.

Here is a snippet:

```js
function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
        //same as above. Replace this line with the following if you want to protect against wrapping uints.
        //if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && balances[_to] + _value > balances[_to]) {
        if (balances[_from] >= _value  && _value > 0)
        {
            balances[_to] += _value;
            balances[_from] -= _value;
            allowed[_from][msg.sender] -= _value;
            Transfer(_from, _to, _value);
            return true;
        } else { return false; }
}
```

The problem here is that the programmer just commented out the correct `if` condition. When calling transferFrom(), checking `allowed` is of the highest priority. Without this, the attacker could drain much more tokens than permitted in the first place. Do not forget to check `allowed` just like this one, unless you do not mind someone attacking your contract.



This is not the end of it, and we will go over another example:

```js
function transferFrom(address _from, address _to, uint256 _value) returns (bool success) {
    var _allowance = allowed[_from][msg.sender];
    if(_value > _allowance) {
        throw;
    }
    balances[_to] += _value;
    balances[_from] -= _value;
    allowed[_from][msg.sender] -= _value;
    Transfer(_from, _to, _value);
    return true;
}
```

It is good to see the developer's work for checking `allowed` before executing the following steps, but another requirement is missing: check the account balance. When you buy a bagel or donut, of course you will check your pocket to see if you have enough money because no one likes to dine and dash. This rule applies to smart contracts as well - always check if you get enough money when trading.



Now I will introduce a ridiculous one we SECBIT team found on StackOverflow:

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

With every necessary condition checked, the only problem here is that the programmer was so careless that every judging condition was quite the opposite, e.g. let `fromBalace <= _value` means the transferred money should be no less than the balance and of course it makes no sense. We cannot assume that all code on the website is bug-free, so please do not directly copy code from the website until you fully understand and finish inspecting the snippet, as some of them, in my opinion, is a trap for anyone not aware of risks in smart contracts: e.g. attackers set up the trap first, waiting for someone falling into it, then hack into the contract and grab all the money.

In fact, if you search this snippet online, you would find that many deployed contracts are using this wrong version, e.g. [UET](https://etherscan.io/address/0x27f706edde3aD952EF647Dd67E24e38CD0803DD6#code) and [BPT](https://etherscan.io/address/0x2160E6c0aE8cA7D62fE1F57fC049F8363283Ff5f#code). (see Reference 1,2, 5 and 6)

#### Tips for Avoiding Vulnerabilities

Most contracts are based on ERC20, so I will talk about some points when implementing your own contract, mainly on transfer() and transferFrom():

Let us take a look at transfer() first. The recipient's address should be checked ahead to avoid sending money to an empty address that is unrecoverable after this process. If someone wants to destroy tokens, he or she should refer to the burn operation in BurnableToken.sol(see Reference 3). Aside from this, the sending value requires checking, yet it could actually be zero for that in ERC20 specification(see Reference 3 and 4), a transfer with 0 token would still count as a legal one and the program will trigger a Transfer event as well.

Now it is time for reviewing transferFrom(). An additional requirement is relevant to the `allowed` variable:

```js
mapping (address => mapping (address => uint256)) internal allowed
```
To set up `allowed`, you may want to check approve():
```js
function approve(address _spender, uint256 _value) public returns (bool)
{
    allowed[msg.sender][_spender] = _value;
    emit Approval(msg.sender, _spender, _value);
    return true;
}
```
The `_spender` is the one who gets the approval from the owner, and it is possible to update `allowed` calling this function again. Meanwhile, please be aware that this action could lead to Re-approval risk: `approve` allows the `spender` account using a given number of tokens by updating the value of `allowance`. Suppose the spender account is able to control miners' confirming order of transferring, then `spender` could use up all `allowance` before `approve` comes into effect. After `approve` is effective, `spender` has access to the new `allowance`, causing total tokens spent greater than expected and resulting in [Re-approval attack](https://docs.google.com/document/d/1YLPtQxZu1UAvO9cZ1O2RPXBbT0mooh4DYKjA_jp-RLM/). Multiple approaches is available for fixing, e.g. require the `spender` to possess a 0 `allowance` for updating the `allowance` or check if the `allowance` of the `spender` equals to the current balance when approving.

#### Interesting Points in Popular ERC20 code

On GitHub, there are two versions of ERC20 that are being referred to mostly: [OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-solidity/tree/master/contracts/token/ERC20) and [ConsenSys](https://github.com/ConsenSys/Tokens/tree/master/contracts/eip20). The interface design between two repos resembles a lot, whereas the actual implementation differs: OpenZeppelin makes use of SafeMath, and ConsenSys adds some requirements of its own to get rid of overflow/underflow. The most fascinating part in ConsenSys is:

```js
if (allowance < MAX_UINT256) {
            allowed[_from][msg.sender] -= _value;
}
```

By this judgment, the program could give approval just once for transferFrom() if the allowance is set to MAX_UINT256, while in OpenZeppelin, the program needs to call approve() again for allocation when the allowance gets used up. This one is barely seen in smart contracts, and it is worth taking a shot.



All in all, strictly follow the ERC20 specifications and you shall be fine. Take a look at OpenZeppelin, ConsenSys and SECBIT offical blog, you could always learn something new.



#### References

1. UselessEthereumToken(UET), ERC20 Token, allows attackers to steal all victim's balances (CVE-2018-10468): <https://medium.com/@jonghyk.song/uselessethereumtoken-uet-erc20-token-allows-attackers-to-steal-all-victims-balances-543d42ac808e>

​     2. CVE-2018-10468: <http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2018-10468>

3. OpenZeppelin: https://github.com/OpenZeppelin/openzeppelin-solidity/tree/master/contracts/token/ERC20
4. ConsenSys: https://github.com/ConsenSys/Tokens/tree/master/contracts/eip20
5. UET: https://etherscan.io/address/0x27f706edde3aD952EF647Dd67E24e38CD0803DD6#code
6. BPT: https://etherscan.io/address/0x2160E6c0aE8cA7D62fE1F57fC049F8363283Ff5f#code
