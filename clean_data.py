import unicodedata
import re

def clean_data(raw_text):

    # Emojis that should NOT be deleted and their tags
    emoji_map = {
        "🔼": "<PICKUP>", "⏫": "<PICKUP>", "⬆️": "<PICKUP>", "⤴️": "<PICKUP>", "⬆": "<PICKUP>",
        "🔽": "<DROPOFF>", "⏬": "<DROPOFF>", "⬇️": "<DROPOFF>", "⤵️": "<DROPOFF>",
    }

    # Parenthesis "emoji names"
    paren_map = {
        "(red arrow up)": "<PICKUP>",
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

    # Step 3: Remove all other parenthesis emojis (like "(one)(two)(seven)")
    text = re.sub(r'\((?!red arrow up\)|red arrow down\)).*?\)', '', text)

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
    text = re.sub(r'([0-9]+)', r' \1 ', text)
    text = re.sub(r'([,.!?])', r' \1 ', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Step 7: Split ThaiWords1234 cases
    text = re.sub(r'([ก-๙]+)([0-9]+)', r'\1 \2', text)
    text = re.sub(r'([0-9]+)([ก-๙]+)', r'\1 \2', text)

    # Step 8: Convert tags to real Thai words
    text = text.replace("<PICKUP>", "ขึ้น")
    text = text.replace("<DROPOFF>", "ลง")

    return text


if __name__ == "__main__":
    raw_text = input("Input Raw Text : ")
    print(clean_data(raw_text))
