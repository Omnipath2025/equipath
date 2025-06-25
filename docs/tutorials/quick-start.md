# Quick Start: Your First EquiPath Interaction

Welcome to EquiPath! This guide will walk you through setting up the project and running your first on-chain verification test. This process validates that your environment is correctly configured and that the core smart contracts are functional.

### Prerequisites

-   **Node.js** (v16.0.0 or higher)
-   **npm** (v8.0.0 or higher)
-   **Git**

### Step 1: Clone and Install

First, clone the repository from GitHub and navigate into the project directory. Then, install all the required dependencies.

Clone the repository
git clone https://github.com/Omnipath2025/equipath.git

Navigate into the project directory
cd equipath

Install all dependencies
The --legacy-peer-deps flag is required for this specific Hardhat setup.
npm install --legacy-peer-deps

### Step 2: Compile the Smart Contracts

Before you can interact with the contracts, you need to compile them. This process converts the human-readable Solidity code into EVM bytecode.

npm run compile

You should see a success message like `Compiled 5 Solidity files successfully`. If you run it a second time, it will correctly report `Nothing to compile`, which also indicates success.

### Step 3: Run the Automated Tests

The quickest way to verify that everything is working is to run the built-in test suite. These tests deploy the `EquiPathVerifier` contract to a temporary local blockchain and check its core functions.

npm test


**Expected Output:**

You should see a report indicating that all tests have passed:

EquiPathVerifier
√ Should set the deployer as the owner
√ Should allow the owner to transfer ownership

2 passing

**Congratulations!** You have successfully set up the EquiPath project and verified its core functionality. You are now ready to move on to the `integration-guide.md` to learn how to use the protocol in your own applications.
