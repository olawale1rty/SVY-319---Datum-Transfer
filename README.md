# Datum Transfer

An application that calculates datum transfer given the secondary and standard port in a csv format.

### Input Data

Each input data is a csv file with the following columns:

- Time_H
- HW
- Time_L
- LW

where Time_H is High Water Time, HW is High Water, Time_L is Low Water Time and LW is Low Water of the port.

E.g of an input data: Using the Lagos bar reading and the Calabar bar reading gotten from the Nigerian Ports Authority tidal table book.

The data was created into a csv file with the columns above for each port and the files are in the 'assets' directory.

### Output Data

The output data is also a csv file that can be saved into any directory after previewing the data.

An example of the output data is the 'Results.csv' file in the 'assets' directory which used the Lagos bar reading as standard port and the Calabar bar reading as secondary port.

### Installation

Binary executables for this project for windows, mac and linux can be found in the release section also.

### Development Setup

This project requires `python3.12` uses [poetry](https://python-poetry.org/) for its virtual environment and dependency
management.
It requires that you have `poerty` installed. If you don't have `poetry` on you development setup, you can
install it with `pip install poetry`.

#### Steps

- Clone this repository.
- Switch to the cloned repository and set up a virtual environment for the project with `poetry shell`
- Install the project's dependencies with `poetry install`
- Run the project. `python main.py`
