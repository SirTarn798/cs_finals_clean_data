import pandas as pd
from clean_data import clean_data
from pythainlp import word_tokenize

def process_excel_file(input_file, output_file=None, column_name=None):
    """
    Read an Excel file, process each row, tokenize, and save results.
    - First sheet: original data with cleaned text
    - Second sheet: tokens in NER training format
    
    Args:
        input_file: Path to input Excel file
        output_file: Path to output Excel file (optional, defaults to input_file)
        column_name: Name of the column to process (optional, uses first column if None)
        
    Returns:
        Tuple of (cleaned_df, ner_df)
    """
    # Read the Excel file
    df = pd.read_excel(input_file)
    
    # Get the column to process
    if column_name is None:
        column_name = df.columns[0]
    
    # Process each row and store cleaned text
    df['Processed'] = df[column_name].apply(lambda x: clean_data(str(x)))
    
    # Tokenize the cleaned text
    df['Tokens'] = df['Processed'].apply(lambda x: word_tokenize(str(x), engine='newmm'))
    
    # Create NER training format dataframe
    ner_data = []
    for idx, row in df.iterrows():
        tokens = row['Tokens']
        for token in tokens:
            ner_data.append({
                'Sentence_ID': idx,
                'Token': token,
                'Label': 'O'  # Default label, can be modified for actual NER labels
            })
        # Add empty row between sentences for better readability
        ner_data.append({'Sentence_ID': '', 'Token': '', 'Label': ''})
    
    ner_df = pd.DataFrame(ner_data)
    
    # Save to output file with two sheets
    if output_file is None:
        output_file = input_file
    
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Cleaned Data', index=False)
        ner_df.to_excel(writer, sheet_name='NER Format', index=False)
    
    print(f"Processing complete. Results saved to {output_file}")
    print(f"- Sheet 1: Cleaned Data with original and processed text")
    print(f"- Sheet 2: NER Format with tokenized text")
    
    return df, ner_df

# Example usage
if __name__ == "__main__":
    cleaned_df, ner_df = process_excel_file("input.xlsx", output_file=None, column_name="Messages")
    
    print("\nFirst 5 rows of cleaned data:")
    print(cleaned_df.head())
    
    print("\nFirst 20 rows of NER format:")
    print(ner_df.head(20))