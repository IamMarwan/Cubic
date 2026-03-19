import sys
from agent import summarize_document

file = sys.argv[1]

with open(file, "r") as f:
    text = f.read()

result = summarize_document(text)
print(result)