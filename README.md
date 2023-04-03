# Nelder-Mead-Market-Modelling

This repository contains code and data for applying the Nelder-Mead optimization algorithm to market modelling. The Nelder-Mead algorithm is a popular optimization method for finding the minimum or maximum of an objective function in multidimensional space, and has been successfully applied to a wide range of problems in finance and economics.

In this repository, I provide a set of Python scripts for implementing the Nelder-Mead algorithm on financial market data, with the goal of estimating parameters for various market models. I also include several datasets for testing and benchmarking the code, as well as example Jupyter notebooks that demonstrate how to use the code for common use cases.

Some of the key features of this repository include:

- Implementation of the Nelder-Mead algorithm in Python, optimized for financial market modelling
- Example Jupyter notebooks demonstrating how to use the code

I hope that this repository will be useful for researchers and practitioners interested in applying the Nelder-Mead algorithm to financial market modelling. Please feel free to use the code and data for your own research, and to contribute to the repository by submitting bug reports or pull requests.

# How to Use the Code

- Clone the repository to your local machine.

- Make sure you have all the necessary data files in the correct folder. Specifically, you should have all the indicator CSV files downloaded from https://fred.stlouisfed.org in a folder called "Data" that is located on your desktop.

- Open the "data_unifier.py" script located in this repository.

- Change the pathname to the one of the folder on your desktop where the indicator CSV files are located.

```
#Username/path will change depending on install locaiton
/Users/yourusername/Desktop/Market Analysis/Market Price/NASDAQCOM.csv
```

-Change the "start_date" variable to the date from which you want to start your analysis.

-Run the "data_unifier.py" script. This will read in all the CSV files in the specified folder, resample the data to monthly frequency, and save the resampled data to a new CSV file called "resampled_data.csv" in the same folder.

-Check the output of the script to ensure that all files were included in the final resampled data. If any files were not included, double-check that they are in the correct folder and that the file name matches the column name in the resampled data.

To run the program, you will need Python 3 and the following Python packages: pandas, numpy, matplotlib, and scipy.

To install the packages, you can use pip:

```
pip install pandas numpy matplotlib scipy
```

- Update the pathname as mentioned previously

- Run the following command to analyze the data:

```
python Data-Analysis.py
```

- The program will output the best correlation value and the corresponding weights for each indicator. It will also generate a plot of the NASDAQ composite index and the final weighted average of the indicators.
- The program will also generate a file named output.txt in the Market Analysis directory, which contains the following information:
-- The weights for each indicator.
-- The best correlation value.
-- The weights and correlation value for each processor.
