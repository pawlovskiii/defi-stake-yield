# The Stake-Yield DeFi protocol

## Table of contents

- [General info](#general-info)
- [Setup](#setup)
  - [Installing dependencies](#installing-dependencies)
  - [Run the project](#run-the-project)

## General info

## Setup

These are the crucial steps to configuring and running the project.

### Installing dependencies

To clone and run this application, you'll need [Git](https://git-scm.com) and [Node.js](https://nodejs.org/en/download/) (which comes with [npm](http://npmjs.com)) installed on your computer. In this case, Node.js is only needed for installing a prettier-plugin for Solidity. Furthermore, you'll have to download [Python](https://www.python.org/downloads/) 3.6+ version to install all the required packages via pip. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/pawlovskiii/stake-yield-defi-protocol

# Go into the repository
$ cd stake-yield-defi-protocol

# Install ganache-cli
$ npm install -g ganache-cli

# Install dependencies (not required)
$ npm install
```

To download all the necessarily Python packages needed for the project

```bash
$ pip install -r requirements.txt
```

### Recommended commands to use for the project

The crucial step in order to do any action with the contracts.

```bash
$ brownie compile
```

#### Deploying contracts via Ganache Local Chain

```bash
# without specific flags, it defaults to ganache-cli
$ brownie run .\scripts\main.py
```

#### Brownie testing variations command

```bash
# testing all the functions
$ brownie test

# single function testing
$ brownie test -k test_set_price_feed_contract
```
