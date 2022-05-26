// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Burnable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Royalty.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/security/PullPayment.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "./ContextMixin.sol";
import "./@rarible/royalties/contracts/impl/RoyaltiesV2Impl.sol";
import "./@rarible/royalties/contracts/LibPart.sol";
import "./@rarible/royalties/contracts/LibRoyaltiesV2.sol";

/**
 * https://github.com/maticnetwork/pos-portal/blob/master/contracts/common/ContextMixin.sol
 */


contract NFT is ERC721, PullPayment, Ownable, ContextMixin, ERC721Burnable, RoyaltiesV2Impl {
  using Counters for Counters.Counter;

  // Constants
  uint256 public constant TOTAL_SUPPLY = 12000;

  Counters.Counter private currentTokenId;

  /// @dev Base token URI used as a prefix by tokenURI().
  string public baseTokenURI;

  constructor() ERC721("It's Mookie", "ITSMOOKIE") {
    baseTokenURI = "";
  }

  function mintTo(address recipient) public returns (uint256) {
    uint256 tokenId = currentTokenId.current();
    uint256 newItemId = 0;
    require(tokenId < TOTAL_SUPPLY, "Max supply reached");

    if (tokenId < TOTAL_SUPPLY) {
      currentTokenId.increment();
      newItemId = currentTokenId.current();
      _safeMint(recipient, newItemId);
      tokenId = currentTokenId.current();
    }

    return newItemId;
  }

  function mintTo(uint256 mintCount, address recipient) public returns (uint256) {
    uint256 tokenId = currentTokenId.current();
    uint256 newItemId = 0;
    uint256 count = 0;
    require(tokenId < TOTAL_SUPPLY, "Max supply reached");

    while (count < mintCount && tokenId < TOTAL_SUPPLY) {
      currentTokenId.increment();
      newItemId = currentTokenId.current();
      _safeMint(recipient, newItemId);
      tokenId = currentTokenId.current();
      count += 1;
    }

    return newItemId;
  }

  /// @dev Returns an URI for a given token ID
  function _baseURI() internal view virtual override returns (string memory) {
    return baseTokenURI;
  }

  /// @dev Sets the base token URI prefix.
  function setBaseTokenURI(string memory _baseTokenURI) public {
    baseTokenURI = _baseTokenURI;
  }

  /// @dev Overridden in order to make it an onlyOwner function
  function withdrawPayments(address payable payee) public override onlyOwner virtual {
      super.withdrawPayments(payee);
  }

  /**
  * Override isApprovedForAll to auto-approve OS's proxy contract
  */
  function isApprovedForAll(
      address _owner,
      address _operator
  ) public override view returns (bool isOperator) {
      // if OpenSea's ERC721 Proxy Address is detected, auto-return true
      if (_operator == address(0x58807baD0B376efc12F5AD86aAc70E78ed67deaE)) {
          return true;
      }
      
      // otherwise, use the default ERC721.isApprovedForAll()
      return ERC721.isApprovedForAll(_owner, _operator);
  }

  /**
    * This is used instead of msg.sender as transactions won't be sent by the original token owner, but by OpenSea.
    */
  function _msgSender()
      internal
      override
      view
      returns (address sender)
  {
      return ContextMixin.msgSender();
  }

  function setRoyalties(uint _tokenId, address payable _royaltiesReceipientAddress, uint96 _percentageBasisPoints) public onlyOwner {
      LibPart.Part[] memory _royalties = new LibPart.Part[](1);
      _royalties[0].value = _percentageBasisPoints;
      _royalties[0].account = _royaltiesReceipientAddress;
      _saveRoyalties(_tokenId, _royalties);
  }

  function supportsInterface(bytes4 interfaceId) public view virtual override(ERC721) returns (bool) {
      if(interfaceId == LibRoyaltiesV2._INTERFACE_ID_ROYALTIES) {
          return true;
      }
      return super.supportsInterface(interfaceId);
  }
}
