Key Open Problems
=====

We break down a few open problems of high priority for the team below. Some have open [RFPs](). For all, we welcome any collaborations (potentially leading to new constructions, discoveries and publications). Please reach out at [filecoin-research@protocol.ai](filecoin-research@protocol.ai).

**Disclaimer:** While we work hard to document our work as it progresses, research progress may not be fully reflected here for some time, or may be worked out out-of-band.

You can read more about what we mean by status or priority [here](./problems-glossary.md).

## Table of Contents

- [Area: Consensus](#area-consensus)
  - [EC attacks](#ec-attacks)
  - [SSLE](#ssle)
  - [Committing power to a particular fork](#committing-power-to-a-particular-fork)
- [Area: Primitives](#area-primitives)
  - [ASIC-resistant PoRep hash functions](#asic-resistant-porep-hash-functions)
  - [PoST aggregation](#post-aggregation)
  - [PoRep without timing assumptions](#porep-without-timing-assumptions)
  - [Vertical PoRep/PoST proving system](#vertical-porep-post-proving-system)
  - [Faster SNARKS on GPU and off-the-shelf hardware](#faster-snarks-on-gpu-and-off-the-shelf-hardware)
  - [Sector Aggregation](#sector-aggregation)
  - [SNARK-friendly accumulators](#snark-friendly-accumulators)
  - [Weighted Threshold Signatures](#weighted-threshold-signatures)



## Area: Consensus

### EC Security

**What:** *Expected Consensus* is a consensus protocol that includes a block proposer and a way to achieve agreement (*PoS Nakamoto consensus*) on a particular block. It is both *Secret Leader Election* and a set of chain selection rules that ensure convergence. It guarantees a leader will eventually be elected through the protocol, to be revealed only as they publish a block to the network (thereby preventing *DoS*ing). On expectation, one leader will be elected at every round.

*EC* takes in randomness from the chain along with a list of miners and their respective powers from the Filecoin power table. Miners are elected in proportion with the storage they have committed to the network. While we believe that *EC* security degrades to that of Snow White, Filecoin research is working toward a formal treatment of *EC* security.

In parallel, in integrating *EC* within a live system, we are running attack analyses and simulations to tune our parameters and ensure that *EC* provides Filecoin with incentive compatibility.

Current research focuses on the following attacks on Filecoin consensus (across *EC* and *SPC*):

- Block Withholding
- Fork Grinding
- Undetectable Nothing at Stake
- Exponential Forking
- Posterior Corruption
- VDF Delay Attack
- SPC Flooding Attack

**Why:** At a high-level, much of Filecoin’s motivation lies in building useful *Proof-of-Work*, replacing electricity consumption with file storage as the main mechanism for participating in network transactions, leader election and ultimately earning economic rewards. *Expected Consensus* is a *Proof-of-Stake* like protocol which sits atop *Storage Power Consensus* and helps realize this vision. Securing it is crucial to Filecoin's security as a persistent state machine on which people can persistently store data.

**Status:** Working on/Collaboration

**Priority:** Ongoing/Short-Term

**References:** 

- [Filecoin Research Consensus Repo](https://github.com/filecoin-project/consensus)
- [EC Simulations](https://github.com/filecoin-project/consensus/tree/master/code)
- [Filecoin Spec](https://github.com/filecoin-project/specs/)
- [Filecoin Whitepaper](https://filecoin.io/filecoin.pdf)

### SSLE

**What**: *Secret Single Leader Election* is a leader election mechanism that can be used in Filecoin consensus (and other consensus) protocols.

We are looking for a construction of SSLE with the following properties:

- *Fair* - Each miner’s chance of becoming the canonical block leader should to be proportional to their power.

- *Secret* - Only the canonical block leader at a round `r` can know that they are the leader until they broadcast a new block to the other miners.

- *Unpredictable* - No observer or collection of observers should be able to predict block leaders with any advantage greater than `eps`.

- *Verifiable* - All miners should be able to verify the canonical block leader non-interactively.

**Why**: Such a construction would have a great impact in improving Filecoin’s design. Unlike the *Expected Consensus* sortition which secretly elects one leader at every round *on expectation*, single secret leader election elects *at most one* leader, thereby significantly reducing the amount of forks in the chain and greatly simplifying the underlying system.

We are actively working on this problem as well as [soliciting proposals](https://github.com/protocol/research-RFPs/blob/master/RFPs/rfp-6-SSLE.md) for such a construction. We believe *SSLE* will:

- Lead to faster convergence in the Filecoin network
- Minimize fork grinding as a potential attack vector for Filecoin (as is the case with *EC*)
- Yield a simpler Filecoin protocol (removing allowances Filecoin makes for multiple winners in leader election)

**Status:** Ongoing Collaboration/RFP

**Priority**: Short/Mid-term

**References:** 

- [Filecoin Research Consensus Repo](https://github.com/filecoin-project/consensus)
- [SSLE RFP](https://github.com/protocol/research-RFPs/blob/master/RFPs/rfp-6-SSLE.md)

### Commiting Power to a Particular Fork

**What:** Like other *Proof-of-Stake* protocols, *Expected Consensus* is subject to *undetectable nothing-at-stake* attacks ([Formal Barriers](https://arxiv.org/pdf/1809.06528.pdf) by Brown-Cohen, Narayanan, et al.). In the context of *Storage Power Consensus*, this means that storage miners can mine multiple forks with the same underlying storage across forks. Recall that the computational requirements needed to generate a *Proof-of-Spacetime* is not the limiting factor in *SPC*.

There are mitigations:

- using a lookback parameter for randomness sampling leads to the same leader election outcomes for all forks descended from the head at which the seed is sampled, thereby reducing chain branching. 
- *SEAL*ing data forces a miner to commit to a given branch from the *SEAL* onwards, as all future *PoST*s refer back to the initial *SEAL*. Thus, Re*SEAL*ing data would effectively force miners to commit their power to a particular branch.

We are looking for the optimal strategy in having miners commit power to a particular fork without negatively affecting their potential earnings (i.e. with a high probability of finality).

**Why:** This is a key issue for *SPC* using *EC*. *SPC* approximates Proof-of-Work by using another limited resource (storage) to force consensus using a *Proof-of-Stake* consensus protocol. However, this ability to mine across forks at low cost is a precise way in which *SPC* poorly approximates *PoW* hardness. Proper mitigation to this issue will improve Filecoin as a useful *Proof-of-Work*.

**Status:** Working On/Collaboration

**Priority:** Medium-Term

**References:** 

- [Filecoin Research Consensus Repo](https://github.com/filecoin-project/consensus)
- [SEAL and PoST security hardness issue](https://github.com/filecoin-project/consensus/issues/30)

## Area: Primitives

### ASIC-Resistant PoRep Hash Functions

**What:** TODO

**Why:** 

**Status:** Future RFP

**Priority:** Short-Term

**References:** 



### PoST Aggregation

**What:** TODO

**Why:** 

**Status:** Working On/Collaboration

**Priority:** Short-Term

**References:** 



### Practical PoRep Without Timing Assumptions

**What:** A *Proof-of-Replication* is both a *Proof-of-Space* and a *Proof-of-Retrievability*. It is an interactive proof system in which a prover is able to demonstrate that they are dedicating unique resources to storing one or more retrievable replicas of some data.

While PoReps may unconditionally demonstrate possession of data, they cannot guarantee that the data is stored redundantly. Indeed, In order to make impossible for a storage provider to delete part of the replicas they are pretending to store and derive them on-the-fly upon request, current PoRep constructions rely on timing assumptions (under which the prover is assumed not to be able to generate a proper response).

The Damgård et. al construction of [Proof of Replication without timing assumption](https://eprint.iacr.org/2018/654) has expensive communication complexity in settings that would tolerate generation attacks: the prover has to sample a set of users and run a multi-party protocol where each user participates in the encoding. We are looking into improvements to this construction and new approaches to the problem considering location and network delays.

**Why:** Timing assumptions creates a need for specialized hardware (to give provers a level playing field). Getting rid of these timing assumptions would represent an elegant further step in the development of Proofs of Replication.

Filecoin makes direct use of PoReps through its use of *Proofs-of-Spacetime* to ensure that a file is stored over time by a storage provider.

**Status:** Collaboration/Future RFP

**Priority:** Medium-Term

**References:** 

- [Scaling Proof-of-Replication for Filecoin Mining](https://web.stanford.edu/~bfisch/porep_short.pdf)

- [PoReps: Proofs of Space on Useful Data](https://eprint.iacr.org/2018/678.pdf)

- [Tight Proofs of Space and Replication](https://eprint.iacr.org/2018/702.pdf)

- [Proofs of Replicated Storage Without Timing Assumptions](https://eprint.iacr.org/2018/654.pdf)

  

### Vertical PoRep/PoST proving system

**What:** 

**Why:** 

**Status:** Curious

**Priority:** Medium-Term

**References:** 



### Faster SNARKS on GPU and off-the-shelf hardware

**What:** 

**Why:** 

**Status:** Future RFP

**Priority:** Short-Term

**References:** 



### Sector Aggregation

**What:** 

A `sector` is a unit of storage over which a miner performs a *Proof-of-Replication* to convince the network and their clients that they are dedicating physical storage to the data they promised to store.

When the miner fills the sector with data from the storage market, they *seal* the sector sector. The miner then posts to the chain the the cryptographic commitments (1) of the original data, `commD`, and (2) of the sealed data, `commR`. In addition, the miner submits a convincing *proof* that the data behind `commR` is a correct encoding of the data behind `commD`. This process is called `Sector Commitment`.

Having each miner post commitments and proofs for each of their storage units results in a large on-chain footprint. 

**Why:** We want to reduce this footprint so as to:  (1) reduce the throughput for storage that Filecoin can on-board (note that for each sector sealed, the miner must submit a minimum of ~300 bytes composed by the proof, `commD` and `commR`), (2) Avoid having miners pay transaction fees for each storage submission (which could penalize particular storage patterns).

Can we batch storage submissions from the same miner into a single short proof? Can we batch storage submission from multiple miners?

**Status:** Working On/Collaboration

**Priority:** Medium-Term

**References:** https://github.com/filecoin-project/specs/pull/125



### SNARK-friendly accumulators

**What:** 

**Why:** 

**Status:** Future RFP/Curious

**Priority:** Medium-Term

**References:** 

### Weighted Threshold Signatures

**What:** A `(t, n)`-Weighted Threshold Signature allows a group of participants with different signing power to produce a valid signature when a subset of participants with a signing power which sums up to `t` (out of a total signing power on `n`) cooperates in the signing procedure.

Note that while `(t, n)`-Threshold Signatures already exist, a valid signature here is produced if any `t` (out of `n`) subgroup of participants cooperate in the signing procedure. In this sense, a `(t, n)`-Threshold Signature is a special case of a  `(t, n)`-Weighted Threshold Signature where all the participants have weight one. Note that the weight of each participant can be related to the collateral that a particular user is committing to.

**Why:** The straightforward way to get a `(t, n)`-Weighted Threshold Signature is to provide each participant with a number of keys equal to their weight. Namely, if participant `P` has weight `k`, they receive `k` different keys and can produce `k` valid signatures. Nevertheless, this strawman is highly inefficient, both in terms of keys size and signature size.

We would like a key sizes independent from weight and signature sizes independent from the threshold `t`. 

Promising directions include:

- Design an ad-hoc secret sharing scheme for key generation.
- Aggregate `k` multiple weight `1` signatures into a signature of the same size with weight `k`.

Such a cryptographic tool would be of great use to both PoS consensus protocols and any power-based voting systems.

**Status:** Curious

**Priority:** Medium-Term
