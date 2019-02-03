# Idea: use consistent hashing to avoid miner-monopoly and greedy-miner attacks (broken)

- Author: Nicola Greco

---

This is an intuition of how we could go about solving the two following attacks using ideas from consistent hashing.

This solution is actualy broken, I am posting this here since:
- This is something that we should investigate more (later!), since this could get us two birds with one stone!
- This is also a greaaaat interview question!

We discussed this solution about a year and a half ago, but didn't make progress on this.

### (Storage) Miner Monopoly Attack
A miner `M*` stores all the copies of a file `f`, such that they are the only storage miner and they have monopoly for `f`. This is #15

Bad things about miner monopoly attacks:
- `M*` can do *data witholding attacks*: never serving data on get requests
- `M*` can do *data extortion attacks*: ask for an insanely high price to return the data

### (Storage) Greedy Miner Attack
A *greedy* miner `M*` is a miner that doesn't care about storage rewards, it only cares about the block reward. For this reason, they hire themselves to store their own data 


### Proposed solution
The proposed solution here is to use consistent hashing (similarly to how this is used in Chord (I think Kadamlia as well)). The intuition is:
- to put all miners in a circle
- every miner gets assigned a range in the hash namespaces for files to store. (e.g. say that there are three miners A, B, C, A stores all the data from hash 000000..-999999.., B from 999999..-GGGGGG.., C from GGGG..-ZZZZ...).
- miners can only take the orders if hash of the file in the order is in their range
	- note: for each redundant copy of a file, we consider the hash of the file to be `H(file || number of the copy)`, such that each copy is assigned to a different miner

Ideally, this would solve:
- miner monopoly attacks: `M*` can only store the copies in their range (say the miner has 50% of storage, for each copy, there is 1/2 of probability for `M*` to store it)
- greedy miner attacks: (assuming that we have a way to break a file in pieces from a single ask order) `M*` can only store some of their data, since some others will be assigned to other miners

#### Problems with this solution
- Grinding: a greedy miner can generate some random data and split it in ways for which they would be always be selected. This is actually trivial: (1) get the data, hash it, if it's assigned to you, great, if not, add a nonce and on expectation after `total power/M* power` they find it)
- Miners now cannot really participate in the market since there will be some orders that match their prices, which they can't get, since the hash of the file in the order is not in their range - this screws up the market (not sure how much of a problem this is)
- On expectations, miners can only get a proportion of the orders in the market and no more than that proportion (while today miners can really store as much as they want - there is nothing preventing them)
- We don't have proofs for storage that is not in use, so a miner can just lie about having A LOT of fake empty storage, just so that their key space is large enough. A fix would not make the key space proportional to the storage (but then we can have a lot of sybils spreading around the circle)
- I am sure there are other problems but can't recall
