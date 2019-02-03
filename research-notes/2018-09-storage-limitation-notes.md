# Filecoin Storage Limitations

- Author: Brian Vohaska
- Comments: [#20](https://github.com/filecoin-project/research/issues/20)


As @whyrusleeping has shown in his analysis ([1], [2], [3], [4]), we currently have a limitation on the total storage that FIL can support. In part this limitation is due to the number of signatures and other associated data posted to the blockchain [2]; our choice of a ~400KB block; because we have well-defined blocks; and because we are storing deals, et al. on the FIL blockchain. 

### What is a storage limitation

FIL is a blockchain which means that when an epoch `E` has passed, a block is generated and *committed* to the blockchain. We can think of epoch as the amount of time it takes for a reasonable set of FIL participants to agree that a set of transactions (or block) is (1) valid and (2) well distributed to the network. When that reasonable set of FIL participants has agreed during the epoch, we say that the block was *committed*. Or in other words, we agree that this block is now a shared truth. This process is called *consensus*.

Storage limitations come in to play because we have chosen (1) a fixed consensus model and (2) a fixed blocks size (~400KB). This means that only a certain number of transactions can be included in a block. The number of transactions in a block chooses how many storage transactions we can perform per block [1] and as a result how much storage we can maintain in FIL with economic incentives. Note that the network could store more data but there would be no economic incentive to do so.

There there are some reasons that we have chosen this size [4].  We strongly welcome argument for/against.

In fact, there are many disjoint and related reasons why we have a total FIL storage limitation. This issue is meant to point out and explore how we can (1) increase FIL total storage or remove the storage limit completely (2) understand all components that lead to a storage limitation AND how those components relate to each other. I propose that by understanding how each component relates to each other we can perform a logical principal component analysis ([PCR](https://en.wikipedia.org/wiki/Principal_component_analysis)) and better solve FIL's storage limitation issue.

### Why do we care?

FIL is a global storage and communication system with the mission of providing secure, reliable, and  affordable storage to any party. As a result we need to be able to scale FIL globally AND at a global growth rate. Any fixed limitations we encounter, may lead to out not meeting our vision in the future.

### Let's look at some examples

1. (Large transaction size) Suppose transactions were each 400KB.This would mean that we can only include one transaction per block and would require that consensus happen very quickly (we we are able to include every participants transaction). We know that consensus requires an epoch to occur which means a reasonable set of participants needs to agree that this transaction is valid, and so forth. We also know that this means there's a lot of communication to many participants...which is typically pretty slow.

2. (Small transaction size) Suppose our transactions were 0KB (not realistic but good for argument). This would mean that we can include every transaction that will every be generated BUT consensus wouldn't occur until we decided that some condition has been met and we want an epoch to end. If we waited too long for an epoch to end, this might lead to an unstable economic system where soo many transactions have occurred that a transaction history becomes unverifiable (read as cheaters could sneak in and perform attacks) and there may no longer be string economic incentives to return data to a client. Nevertheless, being able to choose an epoch on consensus speed and not block size could be ideal. Note that having 0KB transactions is equivalent to having infinite block sizes (where communication is free and physics is kind-of broken).

3. (Maybe realistic transaction size) Now, suppose our transactions were each on the order of 2KB. This would mean that we can include 200 transactions per block. Consensus will still need to happen and we would still need to do all of the normal work to achieve consensus BUT we would be able to ensure that (1) waiting-too-long attacks don't happen, (2) economic incentives to return data efficiently still exist, (3) we can accommodate many transactions <-- we still aren't sure what a reasonable amount is yet.

Note that we have not looked at improving consensus in the above cases. This is because consensus is currently an open question though we will note it as an area of research for the storage limitation problem. In each of these cases, we notice that for some fixed consensus model, we would like to increase the number of transactions. Currently, decreasing the size of the transactions is the only means by which doing so.

### So what can we do about the limitation

In one sentence, increase the number of transactions. PLEASE CORRECT THIS IF IT IS WRONG. THIS IS A BIG ASSUMPTION. Given the above explanation, we might be able to:

- Increase consensus convergence? Can we modify expected consensus (EC) to help us increase the number of transactions

- Change what a transactions means / off-chain actions? Maybe we can perform some of the trans-actions off-chain?

- Decrease transaction sizes? Maybe there exists some means by which to decrease the size of transactions? Compression?

- Decrease the number of headers or header size? If headers exist, maybe we can compress them or aggregate them?

### Current components contributing to the FIL storage limitation

- Signatures ([detail spec](please fill me in with the spec address))

- Bids/Deals ([detail spec](https://github.com/filecoin-project/specs/blob/master/drafts/storage-market.md))

- **please edit/add/remove**

### Current Issues:

- [Signature aggregations](https://github.com/filecoin-project/research/issues/19)

---

References:

[1 - observable/visual analysis of storage limitations](https://beta.observablehq.com/d/37ff2d55942d1354)
[2 - specs/storage market draft](https://github.com/filecoin-project/specs/blob/master/drafts/storage-market.md)
[3 - specs/thoughts on aggregation](https://github.com/filecoin-project/specs/pull/93)
[4 - aq/issue on size constraints](https://github.com/filecoin-project/aq/issues/113)
