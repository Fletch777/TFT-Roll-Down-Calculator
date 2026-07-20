This is my TFT calculator!

I started this project because I've always loved the mathematical side of tft.  
I was always curious what the exact probability was of me hitting x amount of units on a rolldown, or the chance of 3 starring a 5 cost on level 10.  

This calculator uses a markov chain, a stochastic model.  At it's core, it is just doing matrix exponentiation and matrix-vector multiplication.  

How it works:

5 input parameters are gathered from command line args: gold, level, unit cost, enemies units (everyone elses), owned units (yours)

From these args, we determine the following:

Gold & effective gold (effective gold factors in the amount it would cost you to 3 star your unit from your current count) -> # of rolls
Level -> used to index into our table of level odds
Unit cost -> used to index into our table of unit totals (ex. how many total 3 costs there are, or how many copies of each 4 cost there are)
enemy units / owned units -> used to determine how many target units are actually left in the pool


Then based on this information, we fill out our transition matrix (10x10 row-stochastic matrix) this holds the chance of going from any given state to any other given state

The steps taken by the matrix will represent an individual slot in your shop (which has 5 total slots)

Rather than moving from entire shop to entire shop (5 at a time) and getting a horribly messy matrix, 
we step one slot at a time, and compensate by multiplying the exponent(rolls) by 5(since there are 5 slots in a shop)

Once the matrix has been exponentiated, the initial state vector is run through it

The output is a final state vector with the probability of ending up with 0-9 units



Performance

It is worth noting that I included a benchmark script to compare the markov chain method to a more brute forced monte carlo method

The results speak to the elegance of linear algebra:

PS C:\Users\mflet\Desktop\tftcalcevnv> & C:\Users\mflet\AppData\Local\Microsoft\WindowsApps\python3.11.exe c:/Users/mflet/Desktop/tftcalcevnv/benchmark.py
Markov Execution Time:      0.000112 seconds
Monte Carlo Time (100k):    1.053998 seconds
Performance Speedup:        9,377x faster
PS C:\Users\mflet\Desktop\tftcalcevnv> 

It is also worth noting that the resulting probabilities from the markov chain and the monte carlo were nearly identical, despite the drastic performance difference!
(see comparison.png)



Pytest results

I used pytest to try and stress test edge cases within this model, focusing on a few key things:

1.  Probability conservation - the transition matrix needs to remain row stochastic always
2.  Respecting Hard Pool Caps - the markov chain respects the number of target units in the pool as well as the hard cap 
3.  Insufficient gold - correctly catches when player has enough gold to roll but not enough to buy units

To run the tests:
1. Install pytest 
2. Run the command "python -m pytest" in your terminal (no quotes)

As you'll see, all 3 tests are a pass!




Overall:

This program is very cool to use, one very interesting thing I found with this is the S shape curve of the effectiveness of your gold in terms of chance of 3 starring a unit
Effectively: Your chance is 0, until you have enough gold to actually buy all the units you'd need, resulting in a big jump
The middle zone then becomes very linear
As your gold goes towards infinity, the chance caps out at 100%, as you approach 100% you experience dimimishing returns, hence the 'S' shaped curve!