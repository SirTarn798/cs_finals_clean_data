import pandas as pd
import unicodedata
import re
from clean_number import normalize_all_numbers

def clean_data(raw_text):
    # Emojis that should NOT be deleted and their tags
    emoji_map = {
        "🔼": "<PICKUP>", "⏫": "<PICKUP>", "⬆️": "<PICKUP>", "⤴️": "<PICKUP>", "⬆": "<PICKUP>",
        "🔽": "<DROPOFF>", "⏬": "<DROPOFF>", "⬇️": "<DROPOFF>", "⤵️": "<DROPOFF>",
    }
    # Parenthesis "emoji names"
    paren_map = {
        "(red arrow up)": "<PICKUP>",
        "(red arrow curving up)": "<PICKUP>",
        "(red arrow curving down)": "<DROPOFF>",
        "(red arrow down)": "<DROPOFF>",
    }
    text = unicodedata.normalize("NFC", raw_text)
    text = text.lower()
    
    # Step 1: Replace allowed emojis
    for k, v in emoji_map.items():
        text = text.replace(k, v)
    
    # Step 2: Replace allowed parenthesis expressions
    for k, v in paren_map.items():
        text = text.replace(k, v)
    
    # Step 2.5 : Normalize Numbers
    text = normalize_all_numbers(text)
    
    # Step 3: Remove only specific parenthesis emojis
    emoji_patterns = [
        "yes", "cross mark"
        # Add more emoji names as needed
    ]
    escaped_patterns = [re.escape(pattern) for pattern in emoji_patterns]
    pattern = r'\((?:' + '|'.join(escaped_patterns) + r')\)'
    text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    # Remove any single character in parentheses
    text = re.sub(r'\(.\)', '', text)
    
    # Step 4: Remove ALL emojis except ones converted
    emoji_pattern = re.compile(
        "[" 
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F6FF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002700-\U000027BF"
        u"\U0001F900-\U0001F9FF"
        u"\U00002600-\U000026FF"
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)
    
    # Step 5: Normalize spacing
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Step 6: Separate numbers
    # text = re.sub(r'([0-9]+)', r' \1 ', text)
    # text = re.sub(r'([,.!?])', r' \1 ', text)
    # text = re.sub(r'\s+', ' ', text).strip()
    
    # # Step 7: Split ThaiWords1234 cases
    # text = re.sub(r'([ก-๙]+)([0-9]+)', r'\1 \2', text)
    # text = re.sub(r'([0-9]+)([ก-๙]+)', r'\1 \2', text)
    
    # Step 8: Convert tags to real Thai words
    text = text.replace("<PICKUP>", "ขึ้น")
    text = text.replace("<DROPOFF>", "ลง")
    
    return text

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
    # Test the clean_data function
    raw_text = input("Input Raw Text : ")
    print(clean_data(raw_text))