import pandas as pd
import unicodedata
import re
from clean_number import normalize_all_numbers

emoji_map = {
    "🔼": "<PICKUP>", "⏫": "<PICKUP>", "⬆️": "<PICKUP>", "⤴️": "<PICKUP>", "⬆": "<PICKUP>", "👆" : "<PICKUP",
    "🔽": "<DROPOFF>", "⏬": "<DROPOFF>", "⬇️": "<DROPOFF>", "⤵️": "<DROPOFF>", "👇" : "<DROPOFF>"
}
# Parenthesis "emoji names"
paren_map = {
    "(red arrow up)": "<PICKUP>",
    "(red arrow curving up)": "<PICKUP>",
    "(red arrow curving down)": "<DROPOFF>",
    "(red arrow down)": "<DROPOFF>",
}

def remove_zero_width(text): #\u0020\u0027\ufe0f\u0027
    zw = r"[\u200B\u200C\u200D\u2060\uFEFF\u0020\u0027]"
    return re.sub(zw, "", text)

def clean_data(raw_text):
    # Emojis that should NOT be deleted and their tags
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
        "yes", "cross mark", "white triangle right"
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
        u"\U0001FA70-\U0001FAFF"  # newer emoji
        u"\U0001F000-\U0001F02F"  # Mahjong
        u"\U0001F0A0-\U0001F0FF"  # Playing cards
        u"\u2600-\u26FF"          # misc symbols
        u"\u2300-\u23FF"          # technical symbols
        u"\uFE0E-\uFE0F"          # variation selectors
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)
    
    text = remove_zero_width(text)

    
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

# Example usage
if __name__ == "__main__":
    # Test the clean_data function
    raw_text = input("Input Raw Text : ")
    print(clean_data(raw_text))