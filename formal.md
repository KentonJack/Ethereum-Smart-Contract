# Formal Verification: a Silver Bullet for Smart Contract Security

*SECBIT Lab cooperates with Consensys China and Qingxin Tech in formal verification of smart contract security.*

--------------------

Vulnerabilities in smart contracts are threatening digital currency project teams, developers and investors for a long time. A growing number of security teams are putting efforts in this field with plenty of approaches to secure contracts. SECBIT Lab proposes a powerful solution - combining the traditional way of 'test plus audit' with formal verification.

On July 7th, SECBIT Lab published the source code of ERC20 contract formal verification. The contract came from the official ERC20 template by ConsenSys and we have already pushed the formal verification code to GitHub repository(tokenlibs-with-proofs) at the address:

>  https://github.com/sec-bit/tokenlibs-with-proofs

We proved common issues and features of ERC20 contracts in the following properties

* Overflow/Underflow
* Sum of tokens in the contract
* Transferring results on accounts

By this project, we would like to demonstrate applying formal verification to smart contracts, also help more people learn this method and join us.

To avoid buggy contracts and filter out less secure contract templates by formal verification is our goal as well.

Meanwhile, SECBIT Lab would contribute to build more reliable smart contracts via formal verification in aspects of business implementation, security and economy.

## What is Formal Verification

Here is a definition of formal verification from Wikipedia:
> In the context of hardware and [software systems](https://en.wikipedia.org/wiki/Software_system), **formal verification** is the act of [proving](https://en.wikipedia.org/wiki/Mathematical_proof) or disproving the [correctness](https://en.wikipedia.org/wiki/Correctness_(computer_science)) of intended [algorithms](https://en.wikipedia.org/wiki/Algorithms) underlying a system with respect to a certain [formal specification](https://en.wikipedia.org/wiki/Formal_specification) or property, using [formal methods](https://en.wikipedia.org/wiki/Formal_methods) of [mathematics](https://en.wikipedia.org/wiki/Mathematics).
>
> The verification of these systems is done by providing a [formal proof](https://en.wikipedia.org/wiki/Formal_proof) on an abstract [mathematical model](https://en.wikipedia.org/wiki/Mathematical_model) of the system, the correspondence between the mathematical model and the nature of the system being otherwise known by construction. Examples of mathematical objects often used to model systems are: [finite state machines](https://en.wikipedia.org/wiki/Finite_state_machine), [labelled transition systems](https://en.wikipedia.org/wiki/Labelled_transition_system), [Petri nets](https://en.wikipedia.org/wiki/Petri_net), [vector addition systems](https://en.wikipedia.org/wiki/Vector_addition_system), [timed automata](https://en.wikipedia.org/wiki/Timed_automaton), [hybrid automata](https://en.wikipedia.org/wiki/Hybrid_automata), [process algebra](https://en.wikipedia.org/wiki/Process_algebra), formal semantics of programming languages such as [operational semantics](https://en.wikipedia.org/wiki/Operational_semantics), [denotational semantics](https://en.wikipedia.org/wiki/Denotational_semantics), [axiomatic semantics](https://en.wikipedia.org/wiki/Axiomatic_semantics) and [Hoare logic](https://en.wikipedia.org/wiki/Hoare_logic).

We could infer from the definition above that formal verification actually consists of different theoretical verifying techniques, while the principle is that formal verification is, in short, **a verification process based on mathematical models**. The process ensures that models satisfy given **properties**.

The formal verification technique involved in this article views smart contract code as the math model and the requirements of the contract as the **properties** to conduct a proof. Generally, it describes contract code by mathematical language and proves its positive properties, e.g. no integer overflow.

When talking about any formal verification theories or technologies, we must take three key points into consideration:

1. **All proofs must have certain assumptions;**
2. **The proving process is a correct reasoning depending on formal logic theory;**
3. **The result(theorem) is a consensus;**

The formal verification employed by SECBIT satisfies these points in the following way: the first point requires correctness of basic definitions; the second demands a legal proof - we use a popular proving assistant Coq to express and satisfy the procedure; the last one is met in that our conclusion states common ERC20 properties correctly.

Please notify that these three points are prerequisites of formal verification we rely on to secure contracts and the trusted computing base of smart contract formal verification. Security depends on certain trusted computing base. The smaller the base is, the safer the system would be. *The formal verification in this article reduces the base to a minimum set.*

## Why Formal Verification is Necessary to Smart Contracts

After blockchain technologies such as Bitcoin implemented the smart contract concept, Ethereum carried this idea forward. It turned scripts in Bitcoin transactions into a universal Turing complete programming language(note: Turing completeness means making a programming language expressing ability to the maximum extent), while the excessive freedom in Ethereum programming caused smart contracts being prone to vulnerabilities and bugs, leading to billions of economic losses since the beginning of Ethereum.

SECBIT Lab has carried out a scanning and analysis on all deployed token contracts on Ethereum regarding to reported vulnerabilities and risks. Astoundingly, the number of buggy contracts is 4,172 and 101 of them are on CoinMarketCap. The list of buggy contracts has been indexed into [Ethereum Developer Tools List](https://github.com/ConsenSysLabs/ethereum-developer-tools-list) by ConsenSys Labs.

SECBIT Lab has found that the security issues in smart contracts are much thornier and critical than traditional softwares after auditing numerous smart contracts:

1. Smart contracts' reliability comes from immutability that after deploying a smart contract Ethereum, we cannot modify code anymore. Anyone could attack the contract once finding vulnerabilities and the situation could worse up if no defending option is available, undermining both the contract's economic value(e.g. Token value) and the public trust.
2. Some projects would publish the source code after deployment. In one way, it enhances the public credibility; in another way, it decreases sharply the attack cost. Any tiny problem could get caught and made use of by hackers.
3. Lots of areas are related to smart contract developing, which contains deficiencies due to a short history; in the mean time, professional developers are insufficient to help avoid man-made trouble, thus a second of carelessness might cause a critical risk.

At present, two approaches are available for smart contract security issues: test and audit of contract code. These methods are necessary for avoiding most vulnerabilities, while contain limitations as well.

* Test

  The security team develops a automatic testing tool to generate a great quantity of test cases to examine the correctness under conditions as many as possible, while it cannot ensure a 100% coverage. We cannot state that the implementation is bug-free even if the test result is perfect.

* Audit

  Security auditors assess the source code in implementation and logic. The team uncovers most vulnerabilities and risks via professional means and offers implementation tips. Although an audit could reveal a majority of common security issues, the assessment is subject to auditors' experience and cannot eradicate every problem.

Formal verification, however, is a strict proof by reasoning over formal logical code expression. This process relies on rigor of mathematical logical reasoning, therefore ensures a perfect code coverage and an absolute exactness to an extent. It makes up the limitations above, hence is heavily applied in security-sensitive fields, e.g. astronautics, high-speed rail, nuclear power and aeronautics.

Smart contracts also demand extreme security, as many assets are in concern. Other problems regarding to complex business logic and high-level properties such as economy and game theory are not likely to avoid only by testing or auditing. Thus, formal verification is no doubt an efficient way to secure smart contracts with small scale and complex design.

## How to Build Formal Verification for Smart Contracts

Despite the fact that formal verification is effective for securing smart contracts, relevant research and tools at present are in short. SECBIT Lab published the ERC20 contract formal verification in order to filter out risky contract templates and attract more people to learn and join the formal verification of smart contracts.

### Structure

Token formal verification could be generally divided into four parts: source code, specifications, properties, proof.

![struct](./img1.png)

We need to follow a formal method procedure for verification.

* Source Code: Solidity source code, the code we are going to prove.

* Specifications: defines expected behavior of every contract function.

* Properties: the assured contract nature, e.g. immutability of token sum.

* Proof: prove certain qualities based on specifications.

### Properties Involved

The project mainly involves proof of the following properties in Token contracts:

* *nat_nooverflow_dsl_nooverflow*: no overflow in transfer() and transferFrom()

  ```ocaml
  Lemma nat_nooverflow_dsl_nooverflow:
      forall (m: state -> a2v) st env msg,
        (_from = _to \/ (_from <> _to /\ (m st _to <= MAX_UINT256 - _value)))%nat ->
        ((from == to) ||
         ((fun st env msg => m st (to st env msg)) <= max_uint256 - value))%dsl st env msg = otrue.
  ```

* *Property_totalSupply_equal_to_sum_balances*: totalSupply equals the sum of all balances after executing any steps in contracts

  ```ocaml
  (* Prop #1: total supply is equal to sum of balances *)
  Theorem Property_totalSupply_equal_to_sum_balances :
    forall env0 env msg ml C E C' E',
      create env0 msg C E
      -> env_step env0 env
      -> run env C ml C' E'
      -> Sum (st_balances (w_st C')) (st_totalSupply (w_st C')).
  ```

* *Property_totalSupply_fixed_transfer* : Token sum remains unchanged after executing transfer()

  ```ocaml
  (* Prop #2: total supply is fixed with transfer *)
  Theorem Property_totalSupply_fixed_transfer:
    forall env C C' E'  msg to v spec preP evP postP,
      spec = funcspec_transfer to v (w_a C) env msg
      -> preP = spec_require spec
      -> evP = spec_events spec
      -> postP = spec_trans spec
      -> preP (w_st C) /\ evP (w_st C) E' /\ postP (w_st C) (w_st C')
      -> (st_totalSupply (w_st C)) =  (st_totalSupply (w_st C')).
  ```

* *Property_totalSupply_fixed_after_initialization*: Token sum remains unchanged after initialization

  ```ocaml
  (* Prop #3: total supply is fixed after initialization *)
  Theorem Property_totalSupply_fixed_after_initialization:
    forall env0 env msg C E C' E',
      create env0 msg C E
      -> step env C msg C' E'
      -> (st_totalSupply (w_st C)) =  (st_totalSupply (w_st C')).
  ```

* *Property_totalSupply_fixed_delegate_transfer*: Token sum remains unchanged after executing transferFrom()

  ```ocaml
  (* Prop #4: total supply is fixed with delegate transfer *)
  Theorem Property_totalSupply_fixed_delegate_transfer1:
     forall env C C' E' from  msg to v spec,
      spec = funcspec_transferFrom_1 from to v (w_a C) env msg
      -> (spec_require spec) (w_st C) /\ (spec_events spec) (w_st C) E' /\ (spec_trans spec) (w_st C) (w_st C')
      -> (st_totalSupply (w_st C)) =  (st_totalSupply (w_st C')).
  
  Theorem Property_totalSupply_fixed_delegate_transfer2:
     forall env C C' E' from  msg to v spec,
      spec = funcspec_transferFrom_2 from to v (w_a C) env msg
      -> (spec_require spec) (w_st C) /\ (spec_events spec) (w_st C) E' /\ (spec_trans spec) (w_st C) (w_st C')
      -> (st_totalSupply (w_st C)) =  (st_totalSupply (w_st C')).
  
  ```

* *Property_from_to_balances_change*: Transferring only affects balances of accounts involved, other accounts remain unchanged

  ```ocaml
  (* Prop #5: only balances of from and to changed by transfer*)
  Theorem Property_from_to_balances_change_only:
    forall env C C' E' to addr msg v spec,
      spec = funcspec_transfer to v (w_a C) env msg
      -> (spec_require spec) (w_st C) /\
         (spec_events spec) (w_st C) E' /\
         (spec_trans spec) (w_st C) (w_st C')
      -> m_sender msg <> to
      -> m_sender msg <> addr
      -> to <> addr
      -> (st_balances (w_st C') to = (st_balances (w_st C) to) + v)
         /\ (st_balances (w_st C') (m_sender msg) = (st_balances (w_st C) (m_sender msg)) - v)
         /\ st_balances (w_st C') addr = st_balances (w_st C) addr.
  ```

### Procedure Summary

1. **Source Code**

   Standard ERC20 contract code, including six functions: constructor, transfer(), transferFrom(), balanceOf(), approve(), allowance().

2. **Specifications**

   > A **specification language** is a [formal language](https://en.wikipedia.org/wiki/Formal_language) in [computer science](https://en.wikipedia.org/wiki/Computer_science) used during [systems analysis](https://en.wikipedia.org/wiki/Systems_analysis), [requirements analysis](https://en.wikipedia.org/wiki/Requirements_analysis) and [systems design](https://en.wikipedia.org/wiki/Systems_design) to describe a system at a much higher level than a [programming language](https://en.wikipedia.org/wiki/Programming_language), which is used to produce the executable code for a system.

   *Spec.v* defines specifications of six functions in an ERC20 contract.

   The execution of every function could touch multiple cases and the behavior of each case could be described by a rule, therefore a specification usually compose of one or multiple rules. Take the specification of `transferFrom()` as an example: it consists of two rules- ```funspec_transferFrom_1``` and ```funcspec_transferFrom_2```, corresponding to situations that the approved value is smaller than ```2**256-1``` and equal to ```2**256-1```.

   Using ```funcspec_transferFrom_1``` as an example, every specification is composed of following parts.

   * ```spec_require``` defines prerequisites in this case:

     ```ocaml
     Definition funcspec_transferFrom_1
                (from: address)
                (to: address)
                (value: value) :=
       fun (this: address) (env: env) (msg: message) =>
         (mk_spec
            (fun S : state =>
            (* require(balances[_from] >= _value); *)
               st_balances S from >= value /\
            (* require(_from == _to || balances[_to] <= MAX_UINT256 - _value); *)
               ((from = to) \/ (from <> to /\ st_balances S to <= MAX_UINT256 - value)) /\
            (* require(allowance >= _value); *)
               st_allowed S (from, m_sender msg) >= value /\
            (* allowance < MAX_UINT256 *)
               st_allowed S (from, m_sender msg) < MAX_UINT256
            )
         ...
     ```

   * ```spec_events``` defines all events after executing the function successfully:

     ```ocaml
     Definition funcspec_transferFrom_1
                (from: address)
                (to: address)
                (value: value) :=
       fun (this: address) (env: env) (msg: message) =>
         (mk_spec
            (* require omitted *)
          
            (* emit Transfer(_from, _to, _value); *)
            (* return True; *)
            (fun S E => E = (ev_Transfer (m_sender msg) from to value) :: (ev_return _ True) :: nil)
     ```

     two sample events:

     * ```ev_Transfer``` is equivalent to event ```Transfer```;
     * ```ev_return``` is a pseudo event for marking function returning and the return value.

   * ```spec_trans``` defines state changes after a successful function execution, e.g. changes in storage variables:

     ```ocaml
     Definition funcspec_transferFrom_1
                (from: address)
                (to: address)
                (value: value) :=
       fun (this: address) (env: env) (msg: message) =>
         (mk_spec
            (* require omitted *)
            (* events omitted *)
            
            (* State transition: *)
            (fun S S' : state =>
            (* Unchanged. *)
               st_totalSupply S' = st_totalSupply S /\
               st_name S' = st_name S /\
               st_decimals S' = st_decimals S /\
               st_symbol S' = st_symbol S /\
            (* balances[_from] -= _value; *)
               st_balances S' = (st_balances S) $+{ from <- -= value }
            (* balances[_to] += _value; *)
                                                $+{ to <- += value } /\
            (* allowed[_from][msg.sender] -= _value; *)
               st_allowed S' = (st_allowed S) $+{ from, m_sender msg <- -= value }
            )
     ```

     which works that, correspondent items with ```balances``` and ```allowed``` change as expected and other storage variables remain the same.

3. **Proof of Contract Satisfying Specifications**

   Proving high-level properties is based on specifications defined above, and we need to make sure that Solidity source code meets with our specifications before proving properties. First we need to replace the Solidity contract code with Coq. Thus we implemented a Domain Specific Language(DSL) in Coq to represent Solidity code. *DSL.v* shows that ERC20 ```transfer()``` could be represented in this way:

   ```js
     (* DSL representation of transfer(), generated from solidity *)
     Definition transfer_dsl : Stmt :=
       (@require(balances[msg.sender] >= value) ;
        @require((msg.sender == to) || (balances[to] <= max_uint256 - value)) ;
        @balances[msg.sender] -= value ;
        @balances[to] += value ;
        (@emit Transfer(msg.sender, to, value)) ;
        (@return true)
       ).
   ```

   Then we would prove that every function in DSL satisfy specifications, e.g. we could prove that ```transfer()``` meets with ```funcspec_transfer``` via the lemma in *DSL.v*:

   ```js
   Lemma transfer_dsl_sat_spec:
   forall st env msg this,
       spec_require (funcspec_transfer _to _value this env msg) st ->
       forall st0 result,
           dsl_exec transfer_dsl st0 st env msg this nil = result ->
               spec_trans (funcspec_transfer _to _value this env msg) st (ret_st result) /\
               spec_events (funcspec_transfer _to _value this env msg) (ret_st result) (ret_evts result).
   ```

4. **Definition and Proof of High-Level Properties**

   The specification above describes each execution in one function, while high-level properties are those kept when accepting arbitrary message call as a whole entity, such as properties defined in *Prop.v* that all accounts would not lose tokens and sum of balances equals to totalSupply:

   ```ocaml
   (* Prop #1: total supply is equal to sum of balances *)
   Theorem Property_totalSupply_equal_to_sum_balances :
     forall env0 env msg ml C E C' E',
       create env0 msg C E
       -> env_step env0 env
       -> run env C ml C' E'
       -> Sum (st_balances (w_st C')) (st_totalSupply (w_st C')).
   ```

   Please refer to *Spec.v* for detailed definition and proof of all high-level properties.

## Future Plans

Contrary to traditional ones, security issues in smart contracts would lead to much more critical consequences with a broader range and much losses. Formal verification is definitely a silver bullet for resolving problems in smart contracts.

Given a scope, formal verification could assure the reliability of the code and get rid of some vulnerabilities from the root. This repository applies a few simple properties of ERC20 token contracts for a brief introduction to smart contract formal verification, which, however, does not reveal its full potential. With the growth of smart contracts, more and more achievements are on the way by applying the comprehensive mathematical theories and philosophy inside formal verification on challenges of economy and game theory.

Although formal verification is highly efficient in securing smart contracts, there is a lack of relevant experts, research and tools around the world. SECBIT team is on a campaign to apply this technology widely in smart contract security, backed by our research experience in the formal verification field for more than ten years. 

* We would prove more common properties for avoiding vulnerabilities and risks.
* We would prove token contracts with more features, e.g. freezing, upgrading, authority manipulating, adding ownerships.
* We would research on proof of high-level properties regarding to game theory, e.g. fairness, optimistic strategy, Nash equilibrium.

Meanwhile, we call for more people joining us to build formal verification and smart contracts together. If you have any questions or ideas, please join our [Gitter](https://gitter.im/sec-bit/Lobby) for discussion.

> Gitter Address: <https://gitter.im/sec-bit/Lobby>

`Special thanks to Yi Tang(ConsenSys China), Yuhui Wu(Qingxin Tech), Zhong Zhuang(DEx.top) and others for editing this article.`

## References

* [1] DSLs for Ethereum Contracts https://www.michaelburge.us/2018/05/15/ethereum-chess-engine.html
* [2] Formal verification https://en.wikipedia.org/wiki/Formal_verification 
* [3] Domain-specific language https://en.wikipedia.org/wiki/Domain-specific_language
* [4] 安⽐（SECBIT）实验室携⼿路印（Loopring）共同发布智能合约风险列表 https://mp.weixin.qq.com/s/XbXlrmt0fi9IgxicmdAF0w
* [5] CHAINB:【推荐】王健：说说形式化验证（Formal Verification）吧 http://chainb.com/?P=Cont&id=1957
* [6] C. A. R. Hoare. An axiomatic basis for computer programming. *Communications of the ACM*, 26(1):53-56, Jan. 1983.
* [7] L. Lamport. Proving the correctness of multiprocess programs. *IEEE Transactions on Software Engineering* SE-3, 2 (March 1977), 125-143.
* [8] G. Necula. Proof-carrying code. In *Proc.24th ACM* *symposium on Principles of programming languages (POPL’97)*. pages 106-119, New York, Jan. 1997.
* [9] Inria: The Coq Proof Assistant. https://coq.inria.fr/ 
* [10] Cadar, C., Dunbar, D., Engler, D.R., et al.: Klee: Unassisted and automatic generation of high-coverage tests for complex systems programs. In: OSDI. Volume 8. (2008) 209–224 
* [11] Gaudel, M.C.: Testing from formal specifications, a generic approach. In: International Conference on Reliable Software Technologies, Springer (2001) 35–48 
* [12] Nielson, F., Nielson, H.R., Hankin, C.: Principles of program analysis. Springer (2015) 
* [13] Gaudel, M.C.: Testing from formal specifications, a generic approach. In: International Conference on Reliable Software Technologies, Springer (2001) 35–48 
* [14] Inria: The Gallina specification language. https://coq.inria.fr/distrib/current/refman/language/gallina-specification-language.html 
* [15] Acta Scientiarum Naturalium Universitatis Pekinensis: Logic Based Formal Verification Methods: Progress and Applications  http://xbna.pku.edu.cn/html/2016-2-363.htm

