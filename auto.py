'''
Basic:
ERC20 basic interface, ownable, SafeMath, Re-approval protection (approve, transfer, transferFrom)

Optional:
Burnable, Mintable, Pausable

Not Included:
Timelock
'''
import os
import sys

class AutoGenerate(object):
  def __init__(self, Name, Symbol, Sum, Dec, Burn, Mint, Pause, Mythril):
    self.ContractName = Name.replace(' ', '')
    self.ContractSymbol = Symbol
    self.InitialSum = Sum
    self.Decimal = Dec
    self.Has_Burn = Burn
    self.Has_Mint = Mint
    self.Has_Pause = Pause
    self.Has_Check = Mythril

  def generate(self):
    Contract_Name = self.ContractName
    Contract_Symbol = self.ContractSymbol
    Initial_Sum = self.InitialSum
    Decimals = self.Decimal
    Need_Burn = self.Has_Burn
    Need_Mint = self.Has_Mint
    Need_Pause = self.Has_Pause
    isPaused = ''
    pause = ' '
    if Need_Pause == 'y':
      isPaused = ', Pausable'
      pause = ' whenNotPaused '

    template = '\n\n\
/**\n\
 * @title Standard ERC20 token\n\
 *\n\
 * @dev Implementation of the basic standard token.\n\
 * @dev https://github.com/ethereum/EIPs/issues/20\n\
 * @dev Based on code by FirstBlood: https://github.com/Firstbloodio/token/blob/master/smart_contract/FirstBloodToken.sol\n\
 */\n\
contract ' + Contract_Name + ' is Ownable' + isPaused + '\n\
{\n\
  using SafeMath for uint256;\n\
  string name = ' + '\'' + Contract_Name + '\'' + ';\n\
  string symbol = ' + '\'' + Contract_Symbol + '\'' + ';\n\
  uint8 decimals = ' + Decimals + ';\n\
  uint256 totalSupply = ' + Initial_Sum + ' * 10 ** uint256(decimals);\n\
  mapping(address => uint256) balances;\n\
  mapping (address => mapping (address => uint256)) internal allowed;\n\n\
  event Transfer(address indexed from, address indexed to, uint256 value);\n\
  event Approval(address indexed owner, address indexed spender, uint256 value);\n\n\
  constructor() public\n\
  {\n\
    balances[msg.sender] = totalSupply;\n\
  }\n\n\
  function getTotalSupply() public view returns (uint256)\n\
  {\n\
    return totalSupply;\n\
  }\n\n\
  function transfer(address _to, uint256 _value)' + pause + 'public returns (bool)\n\
  {\n\
    require(_to != address(0));\n\
    require(_value <= balances[msg.sender]);\n\
    balances[msg.sender] = balances[msg.sender].sub(_value);\n\
    balances[_to] = balances[_to].add(_value);\n\
    emit Transfer(msg.sender, _to, _value);\n\
    return true;\n\
  }\n\n\
  function balanceOf(address _owner) public view returns (uint256)\n\
  {\n\
    return balances[_owner];\n\
  }\n\n\
  function transferFrom(address _from, address _to, uint256 _value)' + pause + 'public returns (bool)\n\
  {\n\
    require(_to != address(0));\n\
    require(_value <= balances[_from]);\n\
    require(_value <= allowed[_from][msg.sender]);\n\
    balances[_from] = balances[_from].sub(_value);\n\
    balances[_to] = balances[_to].add(_value);\n\
    allowed[_from][msg.sender] = allowed[_from][msg.sender].sub(_value);\n\
    emit Transfer(_from, _to, _value);\n\
    return true;\n\
  }\n\n\
  function approve(address _spender, uint256 _value)' + pause + 'public returns (bool)\n\
  {\n\
    require(_value == 0 || allowed[msg.sender][_spender] == 0);\n\
    allowed[msg.sender][_spender] = _value;\n\
    emit Approval(msg.sender, _spender, _value);\n\
    return true;\n\
  }\n\n\
  function allowance(address _owner, address _spender) public view returns (uint256)\n\
  {\n\
    return allowed[_owner][_spender];\n\
  }\n\n\
  function increaseApproval(address _spender, uint _addedValue)' + pause + 'public returns (bool)\n\
  {\n\
    allowed[msg.sender][_spender] = (allowed[msg.sender][_spender].add(_addedValue));\n\
    emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);\n\
    return true;\n\
  }\n\n\
  function decreaseApproval(address _spender, uint _subtractedValue)' + pause + 'public returns (bool)\n\
  {\n\
    uint oldValue = allowed[msg.sender][_spender];\n\
    if(_subtractedValue > oldValue)\n\
    {\n\
      allowed[msg.sender][_spender] = 0;\n\
    }\n\
    else\n\
    {\n\
      allowed[msg.sender][_spender] = oldValue.sub(_subtractedValue);\n\
    }\n\
    emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);\n\
    return true;\n\
  }\n'

    if not os.path.exists('./' + Contract_Name):
      os.makedirs('./' + Contract_Name + '/contracts')
      os.makedirs('./' + Contract_Name + '/build/contracts')
      os.makedirs('./' + Contract_Name + '/migrations')
      os.makedirs('./' + Contract_Name + '/test')

    base = '\
pragma solidity 0.4.24;\n\
\n\n\
/**\n\
 * @title SafeMath\n\
 * @dev Math operations with safety checks that throw on error\n\
 */\n\
library SafeMath {\n\n\
  /**\n\
  * @dev Multiplies two numbers, throws on overflow.\n\
  */\n\
  function mul(uint256 a, uint256 b) internal pure returns (uint256 c) {\n\
    // Gas optimization: this is cheaper than asserting \'a\' not being zero, but the\n\
    // benefit is lost if \'b\' is also tested.\n\
    // See: https://github.com/OpenZeppelin/openzeppelin-solidity/pull/522\n\
    if (a == 0) {\n\
      return 0;\n\
    }\n\n\
    c = a * b;\n\
    assert(c / a == b);\n\
    return c;\n\
  }\n\n\
  /**\n\
  * @dev Integer division of two numbers, truncating the quotient.\n\
  */\n\
  function div(uint256 a, uint256 b) internal pure returns (uint256) {\n\
    // assert(b > 0); // Solidity automatically throws when dividing by 0\n\
    // uint256 c = a / b;\n\
    // assert(a == b * c + a % b); // There is no case in which this doesn\'t hold\n\
    return a / b;\n\
  }\n\n\
  /**\n\
  * @dev Subtracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).\n\
  */\n\
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {\n\
    assert(b <= a);\n\
    return a - b;\n\
  }\n\n\
  /**\n\
  * @dev Adds two numbers, throws on overflow.\n\
  */\n\
  function add(uint256 a, uint256 b) internal pure returns (uint256 c) {\n\
    c = a + b;\n\
    assert(c >= a);\n\
    return c;\n\
  }\n\
}\n\n\n\
/**\n\
 * @title Ownable\n\
 * @dev The Ownable contract has an owner address, and provides basic authorization control\n\
 * functions, this simplifies the implementation of "user permissions".\n\
 */\n\
contract Ownable {\n\
  address public owner;\n\n\n\
  event OwnershipRenounced(address indexed previousOwner);\n\
  event OwnershipTransferred(\n\
    address indexed previousOwner,\n\
    address indexed newOwner\n\
  );\n\n\n\
  /**\n\
   * @dev The Ownable constructor sets the original `owner` of the contract to the sender\n\
   * account.\n\
   */\n\
  constructor() public {\n\
    owner = msg.sender;\n\
  }\n\n\
  /**\n\
   * @dev Throws if called by any account other than the owner.\n\
   */\n\
  modifier onlyOwner() {\n\
    require(msg.sender == owner);\n\
    _;\n\
  }\n\n\
  /**\n\
   * @dev Allows the current owner to relinquish control of the contract.\n\
   */\n\
  function renounceOwnership() public onlyOwner {\n\
    emit OwnershipRenounced(owner);\n\
    owner = address(0);\n\
  }\n\n\
  /**\n\
   * @dev Allows the current owner to transfer control of the contract to a newOwner.\n\
   * @param _newOwner The address to transfer ownership to.\n\
   */\n\
  function transferOwnership(address _newOwner) public onlyOwner {\n\
    _transferOwnership(_newOwner);\n\
  }\n\n\
  /**\n\
   * @dev Transfers control of the contract to a newOwner.\n\
   * @param _newOwner The address to transfer ownership to.\n\
   */\n\
  function _transferOwnership(address _newOwner) internal {\n\
    require(_newOwner != address(0));\n\
    emit OwnershipTransferred(owner, _newOwner);\n\
    owner = _newOwner;\n\
  }\n\
}\n\n\n\
/**\n\
 * @title Pausable\n\
 * @dev Base contract which allows children to implement an emergency stop mechanism.\n\
 */\n\
contract Pausable is Ownable {\n\
  event Pause();\n\
  event Unpause();\n\n\
  bool public paused = false;\n\n\n\
  /**\n\
   * @dev Modifier to make a function callable only when the contract is not paused.\n\
   */\n\
  modifier whenNotPaused() {\n\
    require(!paused);\n\
    _;\n\
  }\n\n\
  /**\n\
   * @dev Modifier to make a function callable only when the contract is paused.\n\
   */\n\
  modifier whenPaused() {\n\
    require(paused);\n\
    _;\n\
  }\n\n\
  /**\n\
   * @dev called by the owner to pause, triggers stopped state\n\
   */\n\
  function pause() onlyOwner whenNotPaused public {\n\
    paused = true;\n\
    emit Pause();\n\
  }\n\n\
  /**\n\
   * @dev called by the owner to unpause, returns to normal state\n\
   */\n\
  function unpause() onlyOwner whenPaused public {\n\
    paused = false;\n\
    emit Unpause();\n\
  }\n\
}'

    with open('./' + Contract_Name + '/contracts/' + Contract_Name + '.sol', 'w') as f:
      f.write(base)

      if Need_Burn == 'y':
        template += '\
  event Burn(address indexed burner, uint256 value);\n\n\
  /**\n\
   * @dev Burns a specific amount of tokens.\n\
   * @param _value The amount of token to be burned.\n\
   */\n\
  function burn(uint256 _value)' + pause + 'public\n\
  {\n\
    _burn(msg.sender, _value);\n\
  }\n\n\
  function _burn(address _who, uint256 _value)' + pause + 'internal\n\
  {\n\
    require(_value <= balances[_who]);\n\
    // no need to require value <= totalSupply, since that would imply the\n\
    // sender\'s balance is greater than the totalSupply, which *should* be an assertion failure\n\n\
    balances[_who] = balances[_who].sub(_value);\n\
    totalSupply = totalSupply.sub(_value);\n\
    emit Burn(_who, _value);\n\
    emit Transfer(_who, address(0), _value);\n\
  }\n'

      if Need_Mint == 'y':
        template += '\
  event Mint(address indexed to, uint256 amount);\n\
  event MintFinished();\n\
  bool public mintingFinished = false;\n\n\
  modifier canMint()\n\
  {\n\
    require(!mintingFinished);\n\
    _;\n\
  }\n\n\
  modifier hasMintPermission()\n\
  {\n\
    require(msg.sender == owner);\n\
    _;\n\
  }\n\n\
  function mint(address _to, uint256 _amount) hasMintPermission canMint' + pause + 'public returns (bool)\n\
  {\n\
    totalSupply = totalSupply.add(_amount);\n\
    balances[_to] = balances[_to].add(_amount);\n\
    emit Mint(_to, _amount);\n\
    emit Transfer(address(0), _to, _amount);\n\
    return true;\n\
  }\n\n\
  function finishMinting() onlyOwner canMint' + pause + 'public returns (bool)\n\
  {\n\
    mintingFinished = true;\n\
    emit MintFinished();\n\
    return true;\n\
  }\n\n'

      f.write(template + '}')

    print('Done!')
    os.system('solc --zkt-warnings ./result.json --overwrite -o . ' + './' + Contract_Name + '/contracts/' + Contract_Name + '.sol')
    if(self.Has_Check == 'y'):
      os.system('myth -x ' + './' + Contract_Name + '/contracts/' + Contract_Name + '.sol')

if __name__ == '__main__':
  contract = AutoGenerate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])
  contract.generate()
