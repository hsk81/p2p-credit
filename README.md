P2P Credit
==========

A peer-to-peer credit auction platform which facilitates fund raising for projects by addressing the crowd out there. People can offer each other credit, whereas the interest rate is determined through an auction mechanism. The more people bid the lower the interest rate goes down.

There are two problems with P2P funding: First, how do you ensure that a successful bid of an investor is actually delivered and second, how do you ensure that the credit is paid back properly by the credit taker?

There are multiple approaches to solve the first problem:

1. You don't address is at all, and simply trust that the bidders will live up to their commitment, which means they would transfer actual money from their bank account to the credit takers account. If they fail to do so within a set time period, you could punish them by banning such bidders from the platform.

2. Another approach would be, that they would be forced at bid time to send the money. The company running the P2P infrastructure would act as a bank and deliver the collected amount.

  There are several issues with this solution:

  1. The company, running the P2P funding infrastructure, would be required to have a banking license and also be a single point of failure (trust, security, regulation), 
  2. the technological implementation of the financial transaction at bid time would be expensive and 
  3. also eliminate certain desired features of the system like privacy and anonymity of the investors and credit takers.

  To solve all this problems we need a novel approach which leads us the the following proposals:

3. Instead of using traditional currency people would rely on an internet currency called **Bitcoins** (see http://en.wikipedia.org/wiki/Bitcoin). At bid time the investors would be required to send Bitcoins to the P2P company.

  This would eliminate issue (2.2), since Bitcoins rely on a fully distributed P2P protocol outflanking any current currency transaction system and therefore reducing implementation costs. It would also eliminate issue (2.3) since Bitcoins allow anonymous sender and receiver addresses, in stark contrast with current bank accounts.

  Still issue (2.1) would pose a huge risk to the system, since any entity with a monopoly on security could shut down the company, running the P2P funding infrastructure. This leads us to the final proposal:

4. The idea is to *eliminate* the company, running the P2P funding infrastructure, by turning the company itself into a distributed P2P software!

Each participant of the network would run the software on their own machines, and would bid and ask for credit. The underlying technology enabling such a novel approach would be Bitcoins.

In detail it would work in the following manner:

  * Credit receiver **RCV** would set up a project **P** for auction with an expiration date **E**, and would state his willingness to accept the credit amount **A** at a certain interest rate **R** between a *minimal* **MIN** and *maximal* **MAX** threshold;

    * it should also possible to distribute *shares* instead of taking a credit in exchange for interest;

  * if the rates **MIN** and **MAX** would appeal to investors, each of these credit senders **SND**s would bid a certain amount **S** for the project **P**;

  * each amount **S** would be split among *all* participants (playing here collectively the role of a *trusted* entity) of the credit funding network;

  * once the auction expires, because of the date **E** or because the **MIN** threshold has been reached, the *network* would collect all bids from the participants, transfer the winning bids (with a cumulative amount A) to the receiver **RCV** and the loosing bids to their originators; or

  * if the auction fails because the collected amount **C** was less then the targeted amount **A** or because the actual interest rate **R** was higher than the maximal rate **MAX**, then the *network* would collect and transfer all bids to their originators.

Each trusted node could charge a fee of trust, and the network would prefer nodes with a lower fee. Each node would have an opinion about the trustworthiness of other nodes, and nodes with a low level of trust would be less likely chosen for holding Bitcoins for others or for being asked about the trustworthiness of others.

Each credit receiver could choose to remain anonymous, but upon failure to pay the credit with the agreed on interest, his identity would be revealed by the network to his investors.