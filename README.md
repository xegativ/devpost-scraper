# Devpost Scraper
Python scraper that collects winning submission data from a Devpost hackathon page and writes the data to a CSV file. 

How it works:
- Converts input to keywords
- Only calculate unique word-similarity scores if above threshold to reduce noise from posts with greater summary length
- If total score above second threshold, add data to csv

WIP:
- Summarize descriptions via sentence extraction using spaCy
- Get keywords of a projects, and allow user to input keywords to filter projects by comparing 
