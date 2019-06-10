# Idea: Proof of Delivery and Guaranteed Retrieval Price

- Author: Nicola Greco

- Historical note: Proposal written in 2017Q4 based on some work that Nicola did at MIT on Jury Trials/Probabilistic trust. The main purpose of this document is to try to answer the question "how do we guarantee retrieval price in Filecoin?". Just for reference, we call Jury Trial any protocol that samples from a population of 51% honesty.

---

The plan:
- In order to have guaranteed retrieval price in Filecoin, we need to be able to write "file contracts" that mentions an agreed upon price and penalization in case the storage provider is not serving the file.
- In order to penalize miners, we need to have a proof that they have not delivered a file to a client that is requesting it (or a proof that the file was delivered).
- So, we will explain in order:
  - the problem of guaranteed delivery and how we go around in filecoin
  - how to extend guaranteed delivery to guaranteed delivery with penalties
  - how to solve guaranteed delivery with a new primitive "fair delivery" which requires a trusted third party
  - how to remove the trusted third party with a blockchain and then with a set of randomly sampled validators
  - how you can write contracts once you have this primitive

---

# Data Availability Problem (or *Guaranteed Delivery Problem*)

**Data Availability Problem**: There is some data that is available on request.

**Guaranteed Delivery Problem**: A client stores some data with a storage provider (or more) and they want to have a guarantee that the data can be retrieved on request. 

**Guaranteed Retrieval Price Problem**: A client stores some data with a storage provider and they want to have a guarantee that the data can be retrieved on request and at an pre-established price.

## Naive solution: 1-of-m honest(or rational) provider assumption

A way to solve the data availability problem is to rely on the following assumption: a client will distribute the data to a sufficiently large set of providers `m`, such that there is at least `1-of-m` honest (or rational) providers that is willing (or incentivized) to serve the data.

**Problems**
- **Large m**: To guarantee availability, the client must store the data with multiple providers (at least `m`), and this might be have a high cost.
- **Unknown retrieval cost**: In a rational setting, there is no guarantee on the cost that will incentivize the rational provider.
- **monopoly attack**: a miner can have a monopoly over a file and perform an [extortion attack](https://github.com/filecoin-project/aq/issues/67)!

**Remark**: This is the current way the data availability problem is solved in Filecoin.

## New Proposal: Fair Delivery

### Data Availability with penalties

We now need to provide a different notion of data availability:

A client stores the data with a storage provider (or more) and they want to have a guarantee that **either the data is available (can be retrieved at the time of request), or the storage provider is penalized**. 

### Fair Delivery
A delivery of a file between a client and a provider is fair if there are two valid outcomes of the protocol:
- Output 1: the client receives the file
- Output 2: the client does not receive the file and the provider is penalized
- (Output 3: the client aborts, the client does not receive the file and the provider is not penalized)

**Problem with fair delivery!**:
This problem reduces to the fair exchange problem! There is no way we can achieve a fair delivery as described, without a trusted third party! Note: the fair delivery protocol can only be initiated by the client.

### Fair Delivery with Third Third Party (TTP)

We describe an optimistic "Fair Delivery" protocol with a trusted third party (TTP) in an optimistic setting (this means that the client or the provider invoke the trusted third party only in case of conflicts).

**Protocol**:
- Setup:
  - Client sends a file to Provider
  - Client sends a hash of the file to TTP
  - Provider deposits collateral with TTP
- Honest Delivery:
  - Client sends a file request to Provider
  - Provider sends the file to Client
  - Client verify
  - **Output 1: Client has the file, provider is not penalized (great!)**
- Delivery with conflicts:
  - Client sends a file request
  - Conflict!
    - either the client did not receive the file or,
    - the provider did not receive the requests, or
    - either are lying!
  - Conflict resolution:
    - client asks TTP to check if there are conflicts
    - TTP requests the file from provider with a timeout
      - if Provider sends the file to TTP before the timeout
		- TTP sends file to client
	    - **Output 1: Client has the file, provider is not penalized (great!)**
      - if Provider doesn't send the file before timeout:
        - TTP penalizes the collateral of the provider
        - **Output 2: Client doesn't have the file, provider is penalized**

#### Going around TTP using the blockchain

The way we have gone around Trusted Third Party in decentralized systems, is by replacing them with a distributed network and a consensus algorithm - in other words, we replace the TTP with a smart contract on a blockchain. Every time, clients or prover interact with the TTP, they would now post transactions to the smart contract. Instead of trusting a single TTP, we now trust that the majority of the consensus protocol is honest.

**Problem!** In our setting, in case of conflict, the provider must have to post on chain the entire file(!). Can we avoid posting the entire data on chain?

#### Jury Trial: Going around TTP by sampling validators

Instead of relying on the majority of the consensus in being the TTP, we can have a smaller set of users which we call "validators". Validators are sampled via a sampling strategy, and they act as a validator.

**Sampling validators for the jury trial**: If we assume that the majority of the consensus is honest, then we can sample a random set of users from the miners (proportionally to their power in the consensus) - e.g. using cryptographic sortition. If we assume that the majority of "money at stake for becoming a validator" is honest, then we can do the same here.

### Fair Delivery with Jury Trial on a blockchain

**Protocol**:
- Setup:
  - Client sends a file to Provider
  - Client creates a contract for a special file hash
  - Provider deposits collateral in the contract (officially commits to serve the file once)
- Honest Delivery:
  - Client sends a file request to Provider
  - Provider sends the file to Client
  - Client verify
  - **Output 1: Client has the file, provider is not penalized (great!)**
- Delivery with conflicts:
  - Client sends a file request
  - Conflict!
    - either the client did not receive the file or,
    - the provider did not receive the requests, or
    - either are lying!
  - Conflict resolution:
    - client asks a random sample of validators to help solving the conflict
    - Validator set requests the file from provider with a timeout
      - if Provider sends the file to validators before the timeout
		- Validators sends file to client
	    - **Output 1: Client has the file, provider is not penalized (great!)**
      - if Provider doesn't send the file before timeout:
        - Validators sign a penalization transaction and submit it to the smart contract, which penalizes provider
        - **Output 2: Client doesn't have the file, provider is penalized**

## From Fair Delivery to File Contracts with guarantee retrieval price

Once we have the fair delivery primitive, then we can have more expressive smart contracts which enforce retrieval of a file X times a price X for some amount of time.

A contract would look more and less like this


### RetrievalContract()

- `RetrievalContract.Setup(collateral, hash, clientAddrs, minerAddr, times, expiry)`
  - miner deposits a collateral for serving a hash at most `times`
  - when block time `expiry` is reached, collateral is given back
  - minerAddr is the retrieval miner and clientAddrs are the set of clients allow to retrieve the file
- `RetrievalContract.Penalize(signatures)`
  - `signatures` from a valid set of validators prove that the file was not given, collateral is now lost!
- `RetrievalContract.Close(tickets)`
  - miner posts tickets signed by the `clientAddrs` proving that they have done the work correctly
  - miner gets their collateral back

Open questions:
- how much collateral should a retrieval miner be request to put down (e.g. if collateral is too low, then they can do a Miner Monopoly Attack (where a miner is the only miner storing a particular file) again!)
- can we use "reputation" instead of collateral?
- how do we incentivize validators?
