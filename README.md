# Devpost-Scraper-Filter
Python scraper that collects winning submission data from a Devpost hackathon page and writes the data to a CSV file only if it matches inputted prompt. 

How it works:
- Converts input to keywords
- Only calculate unique word-similarity scores if above threshold to reduce noise from posts with greater summary length
- If total score above second threshold, add data to csv
