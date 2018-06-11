# An Incompatibility in Smart Contract Threatening DAPP Ecosystem

There are many smart contracts deployed on Ethereum platform and they have been working fine for months, while SECBIT team found that 2603 contracts are facing an incompatibility that could lead to transactions on exchanges being reverted (see Reference 3 and 4) - missing return value in functions like transfer(), transferFrom() or approve(). There is an issue link on GitHub: https://github.com/ethereum/solidity/issues/4116. One could easily verify the incompatibility after updating the Solidity version to 0.4.22. If not handled well, trades involving these contracts would revert, causing billions of dollars stuck in contracts. However, many people are not aware of this issue at all.

#### Affected Smart Contracts

According to SECBIT team's statistics, a total of 2603 contracts are not compatible with Solidity 0.4.22, here is a list of famous tokens ranking Top100 in market cap which is incompatible:

| Ranking | Name    | transfer() | transferFrom() | approve() | Market Cap (Million Dollars) |
| ------- | ------- | ---------- | -------------- | --------- | ---------------------------- |
| 17      | bnb     | ○          |                |           | 18.54                        |
| 21      | OmiseGo |            | ○              | ○         | 11.65                        |
| 99      | SOC     | ○          |                |           | 1.39                         |
| 118     | HPB     | ○          | ○              | ○         | 1.11                         |
| 129     | PAY     | ○          | ○              | ○         | 0.96                         |
| 184     | CREDIT  | ○          |                |           | 0.59                         |

All statistics are collected on June 08, 2018 from coinmarketcap. SECBIT team has published a list of all incompatible contracts: . This table is only intended for DAPP developer's reference, please pay attention to all the smart contracts listed and try your best to avoid the incompatibility, especially if you are working with one of them.

#### Developing Team and Official Template

We cannot simply blame the contract developing team for the incompatible issue, since they strictly followed official guidance. After carefully inspecting samples of incompatible contracts, SECBIT team uncovered that a great mass of them followed two official examples: OpenZeppelin (990 of them) and [Ethereum official Website](https://ethereum.org/token) (1703 of them). It turned out that OpenZeppelin had this issue since a [commit](https://github.com/OpenZeppelin/openzeppelin-solidity/blob/52120a8c428de5e34f157b7eaed16d38f3029e66/contracts/token/BasicToken.sol) on March 21, 2017 until they patched it in a [commit](https://github.com/OpenZeppelin/openzeppelin-solidity/commit/6331dd125d8e8429480b2630f49781f3e1ed49cd) on July 13, 2017. [Ethereum GitHub repository](https://github.com/ethereum/ethereum-org/blob/master/solidity/token-advanced.sol) did not fix it until June 7, 2018: One member of SECBIT team [opened a pull request and got merged](https://github.com/ethereum/ethereum-org/commits/master/solidity/token-advanced.sol). If you accidentally followed two official code examples during this time period, please check your functions as soon as possible.

#### EIP20 Specification

So why the official versions are not compatible with Solidity compiler after updating? SECBIT team found that [EIP20 specification](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md#transfer) does not state anything about return value, thus causing confusion and contradiction. Now there are 3 cases of transfer(): 

1. return false when failed
2. revert when failed
3. although transfer() succeeded, revert due to missing return value

If this confusion remains unsolved, the developers could not establish a standard smart contract specification and non-standard smart contracts would bring more and more trouble when called externally. Can we state that EIP20 is fully responsible? The answer is no. Actually, debates on what value should transfer() return could be dated years ago. Some people vote for returning false while others think that reverting is better. Until now, no conclusion has been made in EIP20 specifications but reverting is more common today.

#### Solidity Compiler and EVM

Aside from this discussion, one member of the Solidity developing team, Christian Reitwiessner thinks that there are some good reasons to check the return value, even it could lead to incompatibilities. Take a look at an EVM assembly function: `call(g, a, v, in, insize, out, outsize)` - call contract at address `a` with input `mem[in..(in+insize)]` providing `g` gas and `v` wei, output area `mem[out..(out+outsize)]` returning 0 on error (e.g. out of gas) and 1 on success.

Before Solidity 0.4.22, the intermediate contract of the exchange would call a contract with address `a`. The address of input and output were set the same in order to save gas. If the function called has no return value, the caller would read the input as there was no output covering input, thus the `mem[out]` would contain some garbage data, which could possibly be some non-zero value standing for `true` in Solidity. That is why transfer() seems normal in previous Solidity versions. Also, if the garbage data is zero, it stands for `false` while the token contract transfers successfully. The external DAPP receives a false result and takes it as a transfer failure, causing new vulnerabilities.

After Solidity 0.4.22, introducing opcode `returndatasize` enabled checking return value read from the function rather than garbage data from a specific memory address. Without a return sentence to pass the `returndatasize` check, functions would throw an exception thus reverting all transactions in the contract: there is no return value, thus the `returndatasize` is zero, smaller than a boolean - `true` or `false`.

This check is generally useful, because now we have means to check the returned data we want in the first place, not some meaningless random data. Actually, the opcode was proposed long ago - the Byzantium Hard Fork, October, 2017. Ethereum took a lot of ideas from EIP, including `revert` and `returndatasize` in EVM. Finally the opcode comes into effect in Solidity 0.4.22. By this improvement, we could avoid the DAPP problem stated above so embracing the update is a great practice, with a little sacrifice of time fixing the incompatibility.

#### Proposed Solution

SECBIT team has some tips of avoiding the incompatibility:

1. Re-deploy the contract
2. DAPP developers use a safe calling function to access to the incompatible Token contracts
3. Ethereum hard fork

Thanks to Lukas Cremer's article (see Reference 4). Although the first method seems fine, much work needs to be done to re-deploy thousands of contracts. The third way is theoretically practical, while everyone is relevant and much discussion is yet to come. SECBIT team now offers a most rational solution - the second one and we have already published the code on GitHub: https://github.com/sec-bit/badERC20Fix/blob/master/badERC20Fix.sol, here is a snippet of our solution for transfer():

```js
library ERC20AsmFn {

    function isContract(address addr) internal {
        assembly {
            if iszero(extcodesize(addr)) { revert(0, 0) }
        }
    }

    function handleReturnData() internal returns (bool result) {
        assembly {
            switch returndatasize()
            case 0 { // not a std erc20
                result := 1
            }
            case 32 { // std erc20
                returndatacopy(0, 0, 32)
                result := mload(0)
            }
            default { // anything else, should revert for safety
                revert(0, 0)
            }
        }
    }

    function asmTransfer(address _erc20Addr, address _to, uint256 _value) internal returns (bool result) {

        // Must be a contract addr first!
        isContract(_erc20Addr);
        
        // call return false when something wrong
        require(_erc20Addr.call(bytes4(keccak256("transfer(address,uint256)")), _to, _value));
        
        // handle returndata
        return handleReturnData();
    }
```

Thanks to Brendan Chou's (see Reference 7) solution, SECBIT team completed the program referring to part of his code. Also, we updated the code with some minor improvements:

1. Get the function signature by using keccak256() - Brendan Chou's code used an interface with no return value: `function transfer(address to, uint256 value) external`. This brings another 'no return' compatibility issue so we changed the method.
2. Add the solution for missing return value in transferFrom().
3. Add the solution for missing return value in approve().

#### Conclusion

Ethereum is yet to grow robust, so we may face many changes in the future. The return value incompatibility has a long history background, and everyone should work together for better communication. However, there is around a month since the issue got raised, many DAPP and smart contract developers are still unaware. SECBIT Lab holds the view that the Ethereum community should build stronger bonds in technology and enhance safety consciousness.

#### Reference

1. Ethereum official GitHub repository: https://github.com/ethereum/ethereum-org/blob/master/solidity/token-advanced.sol#L85
2. EIP20 specification: https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20.md
3. Explaining Unexpected Reverts Starting with Solidity 0.4.22: <https://medium.com/@chris_77367/explaining-unexpected-reverts-starting-with-solidity-0-4-22-3ada6e82308c>
4. Missing Return Value Bug - At Least 130 Tokens Affected: https://medium.com/coinmonks/missing-return-value-bug-at-least-130-tokens-affected-d67bf08521ca
5. Solidity's GitHub Issue: https://github.com/ethereum/solidity/issues/4116
6. Ethereum Official Website: https://ethereum.org/token
7. Brendan Chou's Code: https://gist.github.com/BrendanChou/88a2eeb80947ff00bcf58ffdafeaeb61

