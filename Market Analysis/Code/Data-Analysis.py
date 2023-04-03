import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from multiprocessing import Pool, cpu_count

# Set time offset in unit of time (m or q)
t_frame = 'M'
t_offset = 2
graph_timeframe = '2021'  # calculation start date

# Read the stock market data
market_df = pd.read_csv('/Users/yourusername/Desktop/Market Analysis/Market Price/NASDAQCOM.csv', parse_dates=['DATE'])
market_df = market_df[['DATE', 'NASDAQCOM']]
market_df = market_df.set_index('DATE')

# Convert any non-numeric values to NaN, and then forward-fill the NaN values
market_df['NASDAQCOM'] = pd.to_numeric(market_df['NASDAQCOM'], errors='coerce')
market_df = market_df.fillna(method='ffill')

# Resample the market data to monthly or quarterly based on t_frame variable
market_df = market_df.resample(t_frame).mean()

# Load the resampled data
df_resampled = pd.read_csv('/Users/yourusername/Desktop/Market Analysis/resampled_data.csv', parse_dates=['DATE'])
df_resampled = df_resampled.set_index('DATE')

# Resample the data to monthly or quarterly based on t_frame variable
df_resampled = df_resampled.resample(t_frame).mean()

# Fill missing values with the previous non-missing value
df_resampled = df_resampled.fillna(method='ffill')

# Shift the market data by one quarter (three months) to simulate a one quarter advance
market_df = market_df.shift(-t_offset, freq=t_frame)

# Create a list of indicator names
indicator_names = list(df_resampled.columns)

# Set the bounds for the coefficients (between 0 and 1)
bounds = [(0, 1)] * len(indicator_names)

# Set the initial guesses for the coefficients (random values between 0 and 1)
x0_list = [np.random.rand(len(indicator_names)) for _ in range(cpu_count())]

def weighted_avg(coeffs):
    """
    Calculates the weighted average of all indicators using the given coefficients.
    """
    return df_resampled[indicator_names].mul(coeffs).sum(axis=1)


def objective_function(coeffs):
    """
    Calculates the negative correlation between the market data and the weighted average of indicators
    using the given coefficients.
    """
    weighted_avg_price = weighted_avg(coeffs)
    market_price = market_df['NASDAQCOM']
    #corr = market_price.corr(weighted_avg_price)
    corr = market_price[graph_timeframe:].corr(weighted_avg_price[graph_timeframe:])
    return -corr


def optimize_single_instance(x0):
    """
    Optimizes the objective function using the Nelder-Mead algorithm with a single initial guess.
    """
    result = minimize(objective_function, x0, method='Nelder-Mead', bounds=bounds, options={'maxiter': 10000000})
    return (result.x, -result.fun)


if __name__ == "__main__":
    # Run multiple instances of the optimization algorithm with different initial guesses in parallel
    with Pool() as pool:
        results = pool.map(optimize_single_instance, x0_list)

    # Select the solution with the best correlation value
    best_coeffs, best_corr = max(results, key=lambda x: x[1])

    # Normalize the coefficients so that they sum to 1
    best_coeffs = best_coeffs / np.sum(best_coeffs)

    # Print the best correlation and the corresponding coefficients
    print(f'Best correlation: {best_corr}')
    # print(f'Best coefficients: {best_coeffs}')

    print("Best values found by each processor:")
    for i, (coeffs, corr) in enumerate(results):
        coeffs = coeffs / np.sum(coeffs)
        print(f"Processor {i+1}: correlation={corr}")
    # Calculate the final weighted average using the best coefficients and plot it against the market data

    final_weighted_avg = weighted_avg(best_coeffs)

    # Create a dictionary to store indicator coefficients
    indicator_dict = {}

    # Set the output file path
    output_file = '/Users/yourusername/Desktop/Market Analysis/output.txt'

    # Write the output to the file
    with open(output_file, 'w') as f:
        
        # Write the indicator coefficients to the file
        for indicator, coefficient in zip(indicator_names, best_coeffs):
            f.write(f'{indicator}: {coefficient}\n\n')
            indicator_dict[indicator] = coefficient
        
        # Add spacing between sections
        f.write('\n')
        
        # Write the best correlation to the file
        f.write(f'Best correlation: {best_corr}\n')
        
        # Add spacing between sections
        f.write('\n')
        
        # Write the best values found by each processor to the file
        f.write("Best values found by each processor:\n")
        for i, (coeffs, corr) in enumerate(results):
            coeffs = coeffs / np.sum(coeffs)
            f.write(f"Processor {i+1}: correlation={corr}  values={coeffs}\n")


    #Plot the final weighted average and the market data
    # Plot the market data and the weighted average of indicators
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    #market_df = market_df.shift(t_offset, freq=t_frame)
    market_df.loc[graph_timeframe:].plot(ax=ax1, label='NASDAQCOM', color='blue')
    final_weighted_avg.loc[graph_timeframe:].plot(ax=ax2, label='Weighted Average', color='red')
    ax1.set_title('Market Data vs Weighted Average of Indicators')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('NASDAQCOM', color='blue')
    ax2.set_ylabel('Weighted Average', color='red')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax1.grid(True)
    # Set x-axis limits to the specified timeframe
    ax1.set_xlim(pd.Timestamp(graph_timeframe), pd.Timestamp.now())
    plt.show()