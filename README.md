# VIRUS OPTIMIZATION

Project for the "Operational research: theory and applications" course, Politecnico of Turin, A.Y. 2020/2021



## Project

There are two main characteristics that make a virus lethal: infectivity and death rate. Let us consider a network represented by an undirected graph. Starting from a random node, the infection spreads across the network. Since the viral quantity of the virus in the human body follows an exponential trend over time as N<sub>t</sub>=N<sub>+&#8734;</sub>(1-e<sup>-&lambda; t</sup>), it is reasonable to assume that if person *i* has been infected at time 0, the probability of infecting each neighbour is defined as  p<sub>i</sub>=&alpha;<sub>i</sub>(1-e<sup>-&lambda; t</sup>), while the probability of his death is q<sub>i</sub>=&beta;<sub>i</sub>(1-e<sup>-&lambda; t</sup>), where both &alpha;~i~ and &beta;~i~ are distributed according to Beta distributions, characterized by different parameters. We can consider the following five states for each node:

- *Healthy*: the person was not infected with the virus;

- *Contagious*: the person was infected with the virus and has a viral quantity different from zero, therefore she/he can infect other people;

- *Ill*: as soon as the viral quantity exceeds the threshold value *h*, 1-e<sup>-&lambda;t</sup> &geq; h​, the person becomes ill and she/he is removed from the network, in this way the quarantine period is simulated;

- *Recovered*: the ill person survived for *T* timestamps, hence she/he is considered healed;

- *Dead*: the ill person could not recover within the *T* timestamps, therefore she/he is considered dead.


  

## Pseudocode
```pseudocode
set DURATION //maximum duration of the simulation, in timestamps
set lambda; //lambda that needs to be analysed
set T; //number of iterations necessary for a node to heal
set h; //threshold for the viral quantity to pass from CONTAGIOUS state to ILL state
set all counters equal to -1; //they keep track for how long a node has been contagious and ill
initialize nodes //list of nodes belonging to the network;
 
for t in DURATION do
	if t is equal to 0 then
        select randomly patient zero;
        set state of patient zero to CONTAGIOUS;
        initialize patient_zero.p;
        initialize patient_zero.viral_quantity;

	for node in nodes do

        if node.state is either HEALTHY, DEAD or RECOVERED then
        	continue;

        else if node.state is CONTAGIOUS then
        	update node.p;
        	update node.viral_quantity;

            if node.viral_quantity is greater or equal to h then
                update node.state to ILL;
                initialize node.q;
                increment node.ill_counter by 1;

            else
                for neighbor in node's neighborhood do
                    if neighbor is HEALTHY and random number less or equal to node.p then
                        set neighbor state to CONTAGIOUS;
                        initialize neighbor.p;
                        initialize neighbor.viral_quantity;

		else if node.state is equal to ILL then
			update node.q;
			increment node.ill_counter by 1;

            if random number less or equal to node.p then
            	update node.state to DEAD;

            else if node.ill_counter is greater than T then
            	set node.state to RECOVERED;

	if all nodes are either HEALTHY, DEAD or RECOVERED then
		break;
```




## Python packages:
If they are not already installed, please install the following Python packages.

```shell
pip3 install logging
pip3 install networkx
pip3 install pickle
pip3 install pandas
```



## Run the code:
Run the code by writing in the terminal

```shell
python3 main.py
```

