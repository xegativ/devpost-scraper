# Devpost-Scraper
Python scraper that collects submission data from any Devpost hackathon page and writes the data to a CSV file. 

How it works:
- Utilizes ChatGPT api for converting input to keywords
- Only calculate unique word similarity scores if above threshold to reduce noise from posts with greater summary length
- If total score above second threshold, add data to csv
