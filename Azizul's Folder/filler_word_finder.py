import re
from collections import Counter

def analyze_text(file_path):
    # Read the sample text from the file
    with open(file_path, 'r') as file:
        sample_text = file.read()

    # Your patterns
    crutch_words_pattern = r'\b(um|uh|ah|like|so|actually|basically|seriously|literally|okay|right|you\s*,*\s*know|honestly|' \
                           r'nevertheless|essentially|moreover|nonetheless|furthermore|consequently|i\s*mean|in\s*a\s*sense|' \
                           r'to\s*be\shonest|to\stell\s*you\sthe\struth|as\s*i\swas\ssaying|the\s*thing\sis|' \
                           r'at\s*the\send\sof\sthe\s*day|as\s*a\smatter\sof\s*fact|if\sy|will|as\s*far\s*as\s*i\s*know|' \
                           r'believe\s*me|to\s*be\s*fair|as\s*a\s*result|on\s*the\sother\shand|' \
                           r'to\s*put\s*it\sdifferently|to\s*some\s*extent|needless\s*to\s*say|in\s*any\s*case|' \
                           r'all\s*things\s*considered|to\s*my\s*knowledge|in\s*a\smanner\sof\sspeaking|mmm|hmm|uh-huh|mm-hmm|uh-oh|' \
                           r'huh|hmm-mm|uh-uh|erm|ahem|uhh|well,\s*you\s*see|oh|ooh|aha|duh|yikes)\b'

    repetition_pattern = r'\b(\w+)\s+\1\b'

    # Finding matches
    crutch_words_found = re.findall(crutch_words_pattern, sample_text.lower(), flags=re.IGNORECASE)

    # Count all word occurrences
    words = re.findall(r'\b\w+\b', sample_text.lower())
    word_counts = Counter(words)

    # Create a dictionary with words and their frequencies, removing entries with value 0
    word_frequency_dict = {word: frequency for word, frequency in word_counts.items() if word in set(crutch_words_found) and frequency > 0}

    return word_frequency_dict

# Get the file path from the user
file_path = input("Enter the path to the file: ")

# Call the function and get the results
result_dict = analyze_text(file_path)

# Print or use the results as needed
print("Crutch Words with Frequencies:")
for word, frequency in result_dict.items():
    print(f"{word}:{frequency}")
