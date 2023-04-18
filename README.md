# BSV_15
***
Branch and Bound algorithm for solving the 15-Puzzle

## Description

This is a simple implementation of the Branch and Bound algorithm for solving the 15-Puzzle. The algorithm is implemented in Python and uses the following libraries:

* [copy](https://docs.python.org/3/library/copy.html)
* [matplotlib](https://matplotlib.org/)
* [os](https://docs.python.org/3/library/os.html)
* [pandas](https://pandas.pydata.org/)
* [Pygame](https://www.pygame.org/news)
* [random](https://docs.python.org/3/library/random.html)
* [sys](https://docs.python.org/3/library/sys.html)
* [threading](https://docs.python.org/3/library/threading.html)
* [time](https://docs.python.org/3/library/time.html)
* [tqdm](https://tqdm.github.io/)
* [\_\_future__](https://docs.python.org/3/library/__future__.html)

## Installation

To install the required libraries, run the following command:

    pip install -r requirements.txt


## Usage

To run the program, run the following command from the program's root directory:

    python3 main.py

### Options

The program has the following options:

* **1. Launch GUI**: Launches the GUI, allowing user to interact with the puzzle and solver.
* **2. Plot Timing Data**: Gathers and plots experimental timing data for the solver. 
       The results are stored as `.csv` files in the `dataframes` directory. 
       The plots are stored in the `plots` directory.
* **3. Import Test Puzzle**: Imports a test puzzle from the `test_boards` directory. 
       The puzzles are stored as a grid of whitespace separated integers in `.txt` files.

## Authors

* [**Bjarne Wilken**](https://github.com/B-DUB99)
* [**Sam Selesky**](https://github.com/samselesky)
* [**Von Scheffler**](https://github.com/vscheff)



