output = """
# SWISH format: 2.5.8
# Search words: bandung or makan
# Removed stopwords: 
# Number of hits: 17
"""
lines = output.split('\n')
search_words_line = [line for line in lines if '# Search words:' in line]
if search_words_line:
    search_words = search_words_line[0].split(':')[1].strip()

print(search_words)