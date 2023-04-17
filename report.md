# BSV_15

15 Puzzle Branch & Bound
***
## Description


Program Description
Our program starts by giving the user three options: 
1. Launch GUI
2. Plot Timing Data
3. Import Test Puzzle 

<br>When entering option 1, 
<br>the user is asked to enter their desired width for the puzzle. 
Following this, the program will open a graphical user interface to display a randomized solvable puzzle of the given size. 
The user can then move around puzzle pieces, while the program increments and displays the total moves taken. 
The GUI also contains a solve button which starts a new thread to find a solution path for the puzzle. 
Once this thread has completed, the GUI will display the moves taken to get to the solution while incrementing the total moves counter for each move taken. 
When the user wants to close the GUI, they can press Esc.

<br>When entering option 2, 
<br>the user is prompted to enter the minimum puzzle size, maximum puzzle size, and number of tests per puzzle size. 
After the user input, our program will begin solving puzzles from the minimum size to the maximum size. 
The program will generate and solve a number of puzzles equal to the user input number of tests for each size. 
Upon completion of the tests, the results will be saved in a CSV file.  
To visualize the experimental data, the program creates two plots: 
one plot for the individual’s data, and another plot that compares our individual data with each group member’s data. 
When running this Program as a new user, it will automatically compare the data to our group members data and plot it. 

Lastly, when entering option 3, 
<br>the user is prompted to enter a file path that contains a pre-generated puzzle and the desired number of tests. 
The program then imports the puzzle and solves it the desired number of times, recording the time taken to solve each puzzle. 
Upon completion, the average time to solve the given puzzle is displayed.


<br>When considering a cost function to compare board states, we chose to only use the number of misplaced non-blank tiles. If two tiles have the same cost (tiles out of place), then our program compares the number of inversions of each node. The node with the least number of inversions will be explored further. As a result of this cost function, our program does not find the optimal solution. This was a design choice, as finding the optimal solution takes significantly more time than finding a possible solution. To find the optimal solution, we must add the depth of the node into the cost. Doing this causes our main algorithm to do a breadth-first search amongst the state tree. For well randomized puzzles, this forces the algorithm to search through an excessive number of board states before finding moves that reduce the cost.


***
## Test Result Analysis


Below is a graph containing a comparison of our group's times for solving puzzles with grid width 1 through 5 testing each width 20 times. 
The x-axis has the grid width plotted linearly, and the y-axis has the time-required to solve in nanoseconds plotted logarithmically. 
The graph contains points for each individual test run, as well as a line plotting the mean time for each size.

![all.png](plots/all.png)

When analyzing the graph, incrementing the grid width drastically increases the time it takes to solve the puzzle. 
This is clear when looking at the algorithm to solve a puzzle and the time complexity.  
The time complexity for solving a puzzle with branch and bound is O (n^2 * n!) where n is the grid width of the given puzzle. 
Looking at the time complexity, it is easy to see how increasing n drastically increases the time to solve the (n^2)-1 puzzle.

***
## Installation

Reference the [README.md](README.md)

***
## Authors 

* [**Bjarne Wilken**](https://github.com/B-DUB99)
* [**Sam Selesky**](https://github.com/samselesky)
* [**Von Scheffler**](https://github.com/vscheff)
