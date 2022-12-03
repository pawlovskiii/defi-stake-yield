# The Stake-Yield DeFi protocol

## Table of contents

- [General info](#general-info)
- [Setup](#setup)
  - [Installing dependencies](#installing-dependencies)
  - [Recommended commands to use for the project](#recommended-commands-to-use-for-the-project)

## General info

Application is about reward system protocol within staking certain tokens. It uses ERC20 standards from OpenZeppelin, Oracles from ChainLink, and all different kinds of Mocks. It's well tested, especially within unit and integration tests.

## Setup

These are the crucial steps to configuring and running the project.

### Installing dependencies

To clone and run this application, you'll need [Git](https://git-scm.com) and [Node.js](https://nodejs.org/en/download/) (which comes with [npm](http://npmjs.com)) installed on your computer. In this case, Node.js is only needed for installing a prettier-plugin for Solidity. Furthermore, you'll have to download [Python](https://www.python.org/downloads/) 3.6+ version to install all the required packages via pip. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/pawlovskiii/stake-yield-defi-protocol

# Go into the repository
$ cd stake-yield-defi-protocol

# Install dependencies (not required)
$ npm install
```

To download all the necessarily Python packages needed for the project

```bash
$ pip install -r requirements.txt

$ pip install eth-brownie
```

### Recommended commands to use for the project

- Every command with **npm** at the beginning has it's a more detailed path script in the script section within **package.json** file.

The crucial step in order to do any action with the contracts.

```bash
$ npm run compile
```

#### Deploying contracts via Ganache Local Chain

```bash
# Most used command, because takes the lowest amount of time to execute all the transactions
$ npm run ganache
```

#### Deploying contracts via various TestNets

Users can decide which TestNet they prefer. I only want to inform you that Rinkeby will be deprecated soon, but it's way easier to get test ether in it within various faucets than from the Goerli.

```bash
# Preferably way, because Goerli will be maintained
$ npm run goerli

# Only if you got trouble with getting test ether within Goerli
$ npm run rinkeby
```

#### Brownie testing variations commands

```bash
# Tests all the functions within every script
$ npm test

# Tests whole single script
$ brownie test -k test_staked_amount

# Test single function
$ brownie test -k test_set_price_feed_contract
```
