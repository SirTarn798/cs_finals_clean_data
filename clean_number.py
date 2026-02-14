import re

thai_nums = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")

wordnum_map = {
    "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
    "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    "0" : "0", "1" : "1", "2" : "2", "3" : "3", "4" : "4", "5" : "5", "6" : "6", "7" : "7", "8" : "8", "9" : "9",
}

emoji_num_map = {
    "0️⃣": "0", "1️⃣": "1", "2️⃣": "2", "3️⃣": "3", "4️⃣": "4",
    "5️⃣": "5", "6️⃣": "6", "7️⃣": "7", "8️⃣": "8", "9️⃣": "9",
    "➀": "1", "➁": "2", "➂": "3", "➃": "4", "➄": "5",
    "➅": "6", "➆": "7", "➇": "8", "➈": "9",
    "➊": "1", "➋": "2", "➌": "3", "➍": "4", "➎": "5",
    "➏": "6", "➐": "7", "➑": "8", "➒": "9",
    "⓵": "1", "⓶": "2", "⓷": "3", "⓸": "4", "⓹": "5",
    "⓺": "6", "⓻": "7", "⓼": "8", "⓽": "9",
    "/" : '/', 'เคาท์ดาวน์' : "$"
}

def replace_wordnums(text):
    for word, digit in wordnum_map.items():
        text = re.sub(rf"\({word}\)", digit, text, flags=re.IGNORECASE)
    return text

def normalize_thai_numbers(text):
    return text.translate(thai_nums)

def remove_hyphens_from_phone_numbers(text):
    """
    Remove hyphens from numbers that start with 0 (likely phone numbers).
    For example: 098-3214567 -> 0983214567
    """
    # Find all patterns that look like phone numbers starting with 0
    # This pattern matches: 0 followed by digits and hyphens
    def replace_hyphens(match):
        # Remove all hyphens from the matched phone number
        return match.group(0).replace('-', '')
    
    # Pattern to match numbers starting with 0 that contain hyphens
    # Matches: 0 + (digits or hyphens)
    text = re.sub(r'0[\d-]+', replace_hyphens, text)
    
    return text

def normalize_all_numbers(text):
    # First replace emoji numbers
    for emoji, digit in emoji_num_map.items():
        text = text.replace(emoji, digit)
    
    # Replace word numbers
    text = replace_wordnums(text)
    
    # Normalize Thai numbers
    text = normalize_thai_numbers(text)
    
    # Remove hyphens from phone numbers (numbers starting with 0)
    text = remove_hyphens_from_phone_numbers(text)
    
    return text