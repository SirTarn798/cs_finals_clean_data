import pandas as pd
from clean_data import clean_data

def process_excel_file(input_file, output_file=None, column_name=None):
    """
    Read an Excel file, process each row, and write results to second column.
    
    Args:
        input_file: Path to input Excel file
        output_file: Path to output Excel file (optional, defaults to input_file)
        column_name: Name of the column to process (optional, uses first column if None)
        
    Returns:
        DataFrame with original and processed data
    """
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Get the column to process
    if column_name is None:
        column_name = df.columns[0]
    
    # Process each row and store in new column
    df['Processed'] = df[column_name].apply(lambda x: clean_data(str(x)))
    
    # Save to output file
    if output_file is None:
        output_file = input_file
    
    df.to_excel(output_file, index=False)
    print(f"Processing complete. Results saved to {output_file}")
    
    return df

# Example usage
if __name__ == "__main__":
    result_df = process_excel_file("input.xlsx", output_file=None, column_name="Messages")
    print("\nFirst 5 rows:")
    print(result_df.head())