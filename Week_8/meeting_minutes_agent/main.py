import sys
from agent import extract_meeting_minutes

file = sys.argv[1]

with open(file, "r") as f:
    text = f.read()

result = extract_meeting_minutes(text)
print(result)