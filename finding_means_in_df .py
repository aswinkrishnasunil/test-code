import pandas as pd

# Sample DataFrame
'''data = {
    'Row Labels': ['1/1/2015', '1/2/2015', '1/3/2015', '1/4/2015', '1/5/2015', '1/6/2015'],
    'AL': [0.43, 0.41, 0.41, 0.43, 0.47, 0.46],
    'AR': [3.02, 3.02, 3.01, 3.01, 3.00, 2.98],
    'ave': [0, 0, 0, 0, 0, 0],
    'Central TX': [4.88, 4.88, 4.88, 4.88, 4.88, 4.88],
    'Colorado SJ': [3.30, 3.31, 3.28, 3.27, 3.26, 3.32],
    'ave.1': [0, 0, 0, 0, 0, 0]
}'''

data = {
    'Row Labels': ['1/1/2015', '1/2/2015', '1/3/2015', '1/4/2015', '1/5/2015', '1/6/2015'],
    'AL': [1, 2, 3, 4, 5, 6],
    'AR': [0, 0, 0, 1, 2, 0],
    'ave': [0, 0, 0, 0, 0, 0],
    'Central TX': [7, 8, 9, 10, 11, 12],
    'TX ave': [0, 0, 0, 3, 4, 1],
    'ave.1': [0, 0, 0, 0, 0, 0]
}

df = pd.DataFrame(data)

# Determine the number of columns for each pair
columns_per_pair = 3

# Calculate the total number of pairs
total_pairs = len(df.columns) // columns_per_pair


#columns = df.columns[1:]  # Exclude 'Row Labels'
column_names = [col for col in df.columns if col != 'Row Labels']

calculation_pairs = [(column_names[i], column_names[i + 1], column_names[i + 2]) for i in range(0, len(column_names) - 2, 3)]



print(calculation_pairs)
# Iterate through column pairs
'''for col1, col2, result_col in calculation_pairs:
    # Iterate through rows starting from the second row
    for i in range(1, len(df)):
        # Perform the calculation based on column pairs
        df.at[i, result_col] = df.at[i, col1] * df.at[i-1, col2]'''

for pair in calculation_pairs:
    col0, col1, col2 = pair
    
    # Start from index 2 and perform the calculation
    for i in range(1, len(df)):
        # Check if 'col1' has any number greater than 0
        if df.at[i, col1] > 0:
            # Multiply 'col0' (current index) and 'col0' (previous index) and store the result in 'col2'
            #df.at[i, col2] = df.at[i, col0] * df.at[i - 1, col0]
            #df.at[i, col2] = df.at[i - 1, col0] + df.at[i - 2, col0] + df.at[i - 3, col0] + df.at[i, col0]
            mean_value = df.loc[i-4:i, col0].mean()
            df.at[i, col2] = mean_value


print(df)

# Display the resulting DataFrame
print(df)
