# Filecoin Research

<img src="https://lh3.googleusercontent.com/oe0fJWHIcpXy5eFcOYLA0YFjwXnXGz4lPQv4-szxhrdxeUBKZmJJHjwsveOvkqBBfT9koSOCw8TYoNd78h4zAcpeD4UL0olne2AgwEittt54xRj8sTWBsBi3Xx4SI8DAfz-0lyhA" width="150px"> 

---

This repository is the main hub leading to the various efforts in Filecoin Research and should provide you with the means to engage in this work.

**Disclaimer:** While we work hard to document our work as it progresses, research progress may not be fully reflected here for some time, or may be worked out out-of-band.

## Table of Contents

- [What is Filecoin Research?](#what-is-filecoin-research)
- [Filecoin Research Endeavours](#filecoin-research-endeavours)
  - [Overview](#overview)
  - [Area: Consensus](#area-consensus)
  - [Area: Filecoin Protocol Improvements](#area-filecoin-protocol-improvements)
  - [Area: Generic Blockchain Infrastructure](#area-generic-blockchain-infrastructure)
  - [Area: Primitives](#area-primitives)
  - [Area: Practical zk-SNARKs ](SNARK/SNARK.md)
  - [Area: Practial PoRep](porep/porep.md)
  - [Key Open Problems](#key-open-problems)
- [Contributing](#contributing)
- [Community](#community)
- [Useful Docs](#useful-docs)
- [License](#license)

## What is Filecoin Research?

- **Make breakthroughs in the Filecoin protocol**
- **Support devs to develop Filecoin**

The purpose of Filecoin Research is to design or build the predicates enabling Filecoin: a decentralized storage network. We work to prove Filecoin constructions correct, or to improve them. The work here should provide some motivations for decisions about how Filecoin works; its output is [the Filecoin spec](https://github.com/filecoin-project/specs), from which a filecoin network can be implemented.

## Filecoin Research Endeavours

Filecoin Research work is conducted by area of focus, with current efforts ongoing in:
- [Specs](https://github.com/filecoin-project/specs): The Filecoin Spec is the main interface between research and Filecoin development. Research work is only complete once it finds its way into the spec.
- General Research (you're already here): This repo generally regroups unsolved-problems with Filecoin Research and helps organize our research work.
- [Proofs](https://github.com/filecoin-project/rust-proofs): Dedicated to shaping and building out the Filecoin Proving Subsystem (FPS), whose API can be called by a Filecoin node to Seal disk sectors, or generate PoSTs for instance.
- [Consensus](https://github.com/filecoin-project/consensus): Dedicated to finalizing the construction and proving the security of Filecoin's Consensus protocol, through which leaders are elected to mine new blocks and extend the Filecoin blockchain.

#### Overview

Here is a list of the Filecoin project's research endeavours, we split them by projects for discoverability and further highlight select problems [below](#key-open-problems). We also specify scope and priority in this table, you can find exact definitions for these [here](problems-glossary.md).

- [Area: Consensus](#area-consensus)
- [Area: Filecoin Protocol Improvements](#area-filecoin-protocol-improvements)
- [Area: Generic Blockchain Infrastructure](#area-generic-blockchain-infrastructure)
- [Area: Primitives](#area-primitives)

### Area: Consensus

This endeavour deals with the Filecoin consensus layer broadly. It encompassed projects dealing with precise constructions Filecoin uses or could use (like Expected Consensus or Single Secret Leader Election) as well as the broader classification of Storage-Power-based Consensus in the field, for instance in relation to PoW and PoS. See the [consensus repo](https://github.com/filecoin-project/consensus) for more.

<table style="width:100%">
  <col width="15%">
  <col width="35%">
  <col width="40%">
  <col width="10%">
  <tr>
    <th><b>Project</b></th>
    <th><b>Description</b></th> 
    <th><b>Problems</b></th>
    <th><b>Status</b></th>
  </tr>
  <tr>
    <td><b>Expected Consensus (EC)</b></td>
    <td>Expected Consensus is a consensus protocol that includes a block proposer and a way to achieve agreement (PoS Nakamoto consensus) on a particular block. It yields one secret leader per round on expectation, but may yield 0 or multiple.</td> 
    <td>Short-term/Ongoing:<br>- Formal analysis of EC Security<br>- <a href="./open-problems.md#ec-attacks">Heuristic Security and attack simulations</a></td>
    <td>Working on/Collaboration</td>
  </tr>
  <tr>
    <td><b>Secret Single Leader Election (SSLE)</b></td>
    <td>SSLE is a leader election protocol that guarantees that at each round only a single leader is elected (as opposed to one on expectation) and its identity remains secret until announced.</td>
    <td>Short-term:<br>- A practical <a href="./open-problems.md#ssle">SSLE Construction</a><br><br>Medium-term:<br>- A consensus protocol that uses SSLE as leader election (and adaptation into Filecoin)</td>
    <td>Collaboration/RFP</td>
  </tr>
  <tr>
    <td><b>Storage Power Consensus (SPC)</b></td>
    <td>Storage Power Consensus is the intermediate layer of consensus in the Filecoin system, bridging the gap between a storage network and Proof of Stake consensus to elect leaders based on storage committed to the network.</td>
    <td>Short-term:<br>- <a href="open-problems.md#committing-power-to-a-particular-fork">Committing power to a particular fork</a> (e.g. through reseal)<br><br>Medium-term:<br>- Efficient 51% block signing via all-to-all communications<br>- Proof-of-Space before SEAL<br><br>Long-term:<br>- Formally defining the EC/SPC interface</td>
    <td>Working on/Collaboration/RFP</td>
  </tr>
  <tr>
    <td><b>Power Fault Tolerance (PFT)</b></td>
    <td>PFT is abstracted in terms of influence over the protocol rather than machines</td>
    <td>Medium-term:<br>- Formal framework for PFT in third gen blockchains</td>
    <td>Working on/Collaboration</td>
  </tr>
</table>

## Area: Filecoin Protocol Improvements

This area deals with the transaction layer of the Filecoin protocol and encompasses endeavours across the various parts that come together to make up Filecoin. We quickly present our research interests here.

<table style="width:100%">
  <col width="15%">
  <col width="35%">
  <col width="40%">
  <col width="10%">
  <tr>
    <th><b>Endeavour</b></th>
    <th><b>Description</b></th> 
    <th><b>Problems</b></th>
    <th><b>Status</b></th>
  </tr>
  <tr>
    <td><b>Mining</b></td>
    <td>Mining here refers to the work of storage miners in the Filecoin network, who use proofs to store files on a client's behalf. This section deals with the ways miners interact with proofs as part of storage and retrieval mining in Filecoin.</td>
    <td>Short-term/Ongoing:<br>- PoST difficulty adjustment<br>- Tolerating faults for honest miners<br><br>- Medium-term:<br>- PoSpace after Pledge (before SEAL)<br>- Mining Pools in Filecoin</td>
    <td>Working on/Collaboration (Curious for medium-term)</td>
  </tr>
  <tr>
    <td><b>Repair</b></td>
    <td>Repair miners ensure that as storage miners go offline, clients' orders remain secure. They are verifiers of the chain, catching faults and ensuring orders are re-assigned when storage miners fail.</td>
    <td>Medium-term:<br>- Repair proofs<br>- Scaling Repair<br><br>Long-term:<br>- Watchtowers for storage repair</td>
    <td>RFP/Curious</td>
  </tr>
  <tr>
    <td><b>Securing Filecoin</b></td>
    <td>Filecoin protocol security (to be distinguished from the security of an implementation) is a major endeavour of Filecoin research. It touches our consensus layer, primitives, and transaction layer more broadly. We break this work down into three broad categories: economic security (or incentive compatibility), formal security (provable guarantees), and heuristic security (attack analysis and parameter setting). We detail a few of our endeavours in the space here.</td>
    <td>Short-term:<br>- Cryptoeconomic simulator<br>- PoST security proofs<br>- Formally analyzing Filecoin through the lens of PoS and PoW<br>- Filecoin DoS analysis<br>- Formal analysis of Filecoin finality<br><br>Medium-term:<br>- Filecoin checkpointing</td>
    <td>Working on/Collaboration</td>
  </tr>
  <tr>
    <td><b>Storage Market</b></td>
    <td>The Filecoin's storage market refers to market dynamics around miners' monetization of disk space. Storage market questions concern the tools Filecoin provides miners to manage their disk in filling orders on the network.</td>
    <td>Short-term:<br>- Multiple Sector sizes<br><br>Medium-term:<br>- PoST alternatives for proving storage</td>
    <td>Working on/Collaboration, Curious for long-term</td>
  </tr>
</table>


### Area: Generic Blockchain Infrastructure

We plan to improve the state of the art of generic blockchain constructions. As part of developing Filecoin, we've uncovered open problems that may interest the community at large.

<table style="width:100%">
  <col width="15%">
  <col width="35%">
  <col width="40%">
  <col width="10%">
  <tr>
    <th><b>Endeavour</b></th>
    <th><b>Description</b></th> 
    <th><b>Problems</b></th>
    <th><b>Status</b></th>
  </tr>
  <tr>
    <td><b>Chain Scalability and Throughput</b></td>
    <td>Blockchain design is constrained by limitations of what data can be stored on-chain.</td>
    <td>Short-term/Ongoing:<br>- Signature Aggregation<br><br>Medium-term:<br>- Dedicated Nodes for transaction batching<br>- Accumulator-based chain state<br>Long-term:<br>- Snarking the chain</td>
    <td>Working on/Curious (for long-term)</td>
  </tr>
  <tr>
    <td><b>Blockchain VMs</b></td>
    <td>Filecoin will integrate smart contract functionality through a Filecoin VM. As we look towards this, we are interested in better models for VM execution in the context of a blockchain.</td>
    <td>Medium-term:<br>- WASM<br><br>Long-term:<br>- Privacy-supporting smart contracts<br>- Efficient VM execution model</td>
    <td>Working on/Curious</td>
  </tr>
  <tr>
    <td><b>Other Projects of Interest</b></td>
    <td>This endeavour regroups other insights or problems we've uncovered as part of our work on Filecoin that is likely relevant to other architects and developers working on blockchain-based systems.</td>
    <td>Short-term:<br>- Investigating the necessity of block delay for blockchains<br>- Trustless network joining/node bootstrapping<br><br>Medium-term:<br>- Formal treatment of the impact of cryptoeconomics on protocol security<br>- Exploration of transfer freezing for public keys as an alternative to slashing<br>- Off-chain random beacons<br></td>
    <td>Working on (short-term), Collaboration/RFP (medium-term), Curious (long-term)</td>
  </tr>
</table>


### Area: Primitives

Filecoin itself relies on the performance and security of cryptographic primitives. We quickly discuss the main open problems we are thinking about with regards to Filecoin primitives below.

<table style="width:100%">
  <col width="15%">
  <col width="35%">
  <col width="40%">
  <col width="10%">
  <tr>
    <th><b>Endeavour</b></th>
    <th><b>Description</b></th> 
    <th><b>Problems</b></th>
    <th><b>Status</b></th>
  </tr>
  <tr>
    <td><b>Proof of Replication (PoRep)/Proof of SpaceTime(PoST)</b></td>
    <td>Proof-of-Replication is a key component of Filecoin as a storage-based marketplace. PoReps are assembled into Proofs of SpaceTime to ensure that miners are indeed storing client data.</td>
    <td>Short-term:<br>- Reducing hardware costs for Porep/PoST<br>-<a href="open-problems.md#asic-resistant-porep-hash-functions">ASIC-resistant PoRep hash function</a><br/>- <a href="./open-problems.md#post-aggregation">PoST Aggregation</a><br/><br>Medium-term:<br>- Updateable PoRep<br>- Better PoRep: fast replication & verification, small & fast proof, flexible sector size<br>- <a href="./open-problems.md#porep-without-timing-assumptions">PoRep/PoST without timing assumptions</a><br>- <a href="./open-problems.md#vertical-porep-post-proving-system">Vertical PoRep/PoST proving system</a></td>
    <td>Working on/Collaboration/RFP</td>
  </tr>
  <tr>
    <td><b>SEALSTACK</b></td>
    <td>SEALSTACK refers to a specific attack that breaks PoRep by allowing a miner to cheat on space. The Filecoin team has a few candidate mitigations for SEALSTACK but is working to identify the optimal solution.</td>
    <td>Short-term:<br>- SEALSTACK: Symmetric Proof of replication construction<br>- SEALSTACK: Asymetric PoRep<br><br>Medium-term:<br>- SEALSTACK with fast decode</td>
    <td>Working on/RFP</td>
  </tr>
  <tr>
    <td><b>SNARKS and other key primitives</b></td>
    <td>Filecoin relies on SNARKS to aggregate PoSTs (proof compression of data going to the chain). We are looking into improvements in this space as well as alternative primitives we could use.</td>
    <td>Short-term:<br>- Practical Circuits<br/>- <a href="./open-problems.md#faster-snarks-on-gpu-and-off-the-shelf-hardware">Faster SNARKS on GPU and off-the-shelf hardware</a><br/><br>Medium-term:<br>- <a href="./open-problems.md#sector-aggregation">Sector Aggregation</a> (with aggregation nodes)<br>- ZK-cryptographic compression (with easy set membership verification for random variables)<br>- Succinct file inclusion proofs<br>- <a href="./open-problems.md#snark-friendly-accumulators">SNARK-friendly accumulators</a></td>
    <td>Collaboration/RFP</td>
  </tr>
  <tr>
    <td><b>VDFs</b></td>
    <td>One of Filecoin's PoST candidate constructions uses VDFs in order to ensure appropriate delay between various challenges to the miner. Thus, the security of a candidate construction for Filecoin (as well as Filecoin consensus) relies on certain guarantees provided by VDFs. As such, we are interested in advancements in the field, as well as alternative constructions.</td>
    <td>Short-term:<br>- Fastest Hash/VDF Function<br>- Removing VDFs from Filecoin<br>- Using a hash function that re-uses the same VDF hardware<br>- VDF pools</td>
    <td>Collaboration/RFP/Curious</td>
  </tr>
  <tr>
    <td><b>Other Primitives of Interest</b></td>
    <td>Other key primitives would prove highly useful to Filecoin's development. We detail a few here.</td>
    <td>Medium-term:<br>- Proof of data delivery to assure constrain assured price<br/>- Better Big Number Library<br>- <a href="./open-problems.md#weighted-threshold-signatures">Weighted Threshold Signatures</a><br><br>Long-term:<br>- Proof of Location</td>
    <td>Collaboration/RFP/Curious</td>
  </tr>
</table>

### Key Open Problems

We break down a few open problems of high priority for the team below. Some have open [RFPs](https://github.com/protocol/research-RFPs). For all, we welcome any collaborations (potentially leading to new constructions, discoveries and publications). Please reach out at [filecoin-research@protocol.ai](filecoin-research@protocol.ai). 

[See our open problems](./open-problems.md).

You can also check out slides from talks given about Research Problems in Filecoin:
- [Filecoin: Open Problems building storage-based consensus](https://drive.google.com/a/protocol.ai/file/d/1TeoRVRTDzMvPfYbty0WZ_V75zIyHinke/view?usp=sharing) given by Henri Stern at EPFL Crypto WinterSchool in February 2019.
- [Filecoin Research Problems](https://drive.google.com/a/protocol.ai/file/d/16-74tC09jJeMdgXgKukmTHtmyTGHFkI3/view?usp=sharing) given by Nicola Greco at IC3 Winter Retreat in February 2019.

## Contributing

The purpose of this repo is for Filecoin Research questions to be open to researchers around the world who may be interested in working on them.

If you want to dive into these topics, please see [CONTRIBUTING.md](CONTRIBUTING.md).

## Community

- Github over Google Docs!
- Join the [Public Filecoin Slack](https://github.com/filecoin-project/community#chat):
  - General Filecoin Research: #fil-research
  - Proofs development: #fil-proofs
  - General Filecoin: #general
- Our [Discussion Forum](discuss.filecoin.io)

## Useful docs

- [**Research Notes**](https://github.com/filecoin-project/research/tree/master/research-notes) that have not yet found a home
- [**Calculators**](https://github.com/filecoin-project/research/tree/master/calculators.md) used to estimate some results ahead of spending cycles on a construction
- [**Spec/Design docs**](https://github.com/filecoin-project/specs) for the Filecoin protocol

## License

The Filecoin Project is dual-licensed under Apache 2.0 and MIT terms:

- Apache License, Version 2.0, ([LICENSE-APACHE](https://github.com/filecoin-project/research/blob/master/LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](https://github.com/filecoin-project/research/blob/master/LICENSE-MIT) or http://opensource.org/licenses/MIT/)
