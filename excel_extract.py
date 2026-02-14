import pandas as pd
from clean_data import clean_data
from pythainlp import word_tokenize

def clean_text(text):
    """
    Clean a single text string.
    
    Args:
        text: Raw text string
        
    Returns:
        Cleaned text string
    """
    return clean_data(str(text))

def tokenize_text(text, engine='newmm', keep_whitespace=False):
    """
    Tokenize a text string into words.
    
    Args:
        text: Text string to tokenize
        engine: Tokenization engine (default: 'newmm')
        keep_whitespace: Whether to keep whitespace (default: False)
        
    Returns:
        List of tokens
    """
    return word_tokenize(str(text), engine=engine, keep_whitespace=keep_whitespace)

def process_text_pipeline(text, engine='newmm', keep_whitespace=False):
    """
    Complete pipeline: raw text -> clean -> tokenize -> return list.
    
    Args:
        text: Raw text string
        engine: Tokenization engine (default: 'newmm')
        keep_whitespace: Whether to keep whitespace (default: False)
        
    Returns:
        List of tokens
    """
    cleaned = clean_text(text)
    tokens = tokenize_text(cleaned, engine=engine, keep_whitespace=keep_whitespace)
    return tokens

def create_ner_format(df, sentence_col='Tokens', sentence_id_col='Sentence_ID'):
    """
    Convert tokenized dataframe to NER training format.
    
    Args:
        df: DataFrame with tokenized text
        sentence_col: Column name containing token lists
        sentence_id_col: Column name for sentence IDs (optional)
        
    Returns:
        DataFrame in NER format
    """
    ner_data = []
    
    for idx, row in df.iterrows():
        tokens = row[sentence_col]
        for token in tokens:
            ner_data.append({
                'Sentence_ID': idx,
                'Token': token,
                'Label': 'O'
            })
        # Add empty row between sentences
        ner_data.append({'Sentence_ID': '', 'Token': '', 'Label': ''})
    
    return pd.DataFrame(ner_data)

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
    
    # Process each row: clean and tokenize
    df['Processed'] = df[column_name].apply(clean_text)
    df['Tokens'] = df['Processed'].apply(tokenize_text)
    
    # Create NER training format dataframe
    ner_df = create_ner_format(df)
    
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
    # Example 1: Full pipeline on Excel file
    cleaned_df, ner_df = process_excel_file("new_input.xlsx", output_file="output.xlsx", column_name="Messages")
    
    print("\nFirst 5 rows of cleaned data:")
    print(cleaned_df.head())
    
    print("\nFirst 20 rows of NER format:")
    print(ner_df.head(20))
    
    # Example 2: Process single text
    raw_text = "Welcome !!"
    tokens = process_text_pipeline(raw_text)
    print(f"\nRaw text: {raw_text}")
    print(f"Tokens: {tokens}")
    
    # Example 3: Step-by-step processing
    raw_text2 = "Raw text :    "
    cleaned = clean_text(raw_text2)
    tokens2 = tokenize_text(cleaned)
    print(f"\nRaw: {raw_text2}")
    print(f"Cleaned: {cleaned}")
    print(f"Tokens: {tokens2}")