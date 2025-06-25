const { expect } = require("chai");
const { ethers } = require("hardhat");

// Test suite for the EquiPathVerifier smart contract
describe("EquiPathVerifier", function () {
  let verifierContract;
  let owner;
  let addr1;

  // This block runs before each test, deploying a fresh contract instance
  beforeEach(async function () {
    // Get signers (accounts) from Hardhat's testing environment
    [owner, addr1] = await ethers.getSigners();

    // Get the contract factory and deploy the contract
    const EquiPathVerifierFactory = await ethers.getContractFactory("EquiPathVerifier");
    verifierContract = await EquiPathVerifierFactory.deploy();
    
    // The deprecated "await verifierContract.waitForDeployment()" line has been removed.
    // In modern Hardhat, .deploy() already waits for the transaction to be mined.
  });

  // Test case 1: Verifies that the contract deployer is set as the owner
  it("Should set the deployer as the owner", async function () {
    // Check if the owner of the contract matches the address of the deployer
    expect(await verifierContract.owner()).to.equal(owner.address);
  });

  // Test case 2: Verifies that the owner can successfully transfer ownership
  it("Should allow the owner to transfer ownership", async function () {
    // We expect this transaction *not* to fail (be reverted)
    await expect(verifierContract.transferOwnership(addr1.address)).to.not.be.reverted;
    // We then expect the new owner to be addr1
    expect(await verifierContract.owner()).to.equal(addr1.address);
  });
});
