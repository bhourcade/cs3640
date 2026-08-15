import json
import pandas as pd
# from readability import Readability
import textstat
from textblob import TextBlob

# Returns 1 true or 0 false based on whether the text mentions CCPA or CPRA
def analyze_ccpa(text: str) -> int:
    text = text.upper()
    includes_ccpa = "CCPA" in text or "CALIFORNIA CONSUMER PRIVACY ACT" in text
    includes_cpra = "CPRA" in text or "CALIFORNIA PRIVACY RIGHTS ACT" in text or "PROPOSITION 24" in text

    if includes_ccpa or includes_cpra:
        return 1
    return 0


# Returns 1 true or 0 false based on whether the text mentions FERPA
def analyze_ferpa(text: str) -> int:
    text = text.upper()
    includes_ferpa = "FERPA" in text or "FAMILY EDUCATIONAL RIGHTS AND PRIVACY ACT" in text

    if includes_ferpa:
        return 1
    return 0


# Returns 1 true or 0 false based on whether the text mentions GDPR
def analyze_gdpr(text: str) -> int:
    text = text.upper()
    includes_gdrp = "GDPR" in text or "General Data Protection Regulation" in text

    if includes_gdrp:
        return 1
    return 0


# Returns word length
# Note: If time permits, we should find a more accurate way to measure word length.
def analyze_word_length(text: str) -> int:
    return len(text.split())


# Returns a number between 0-100 that indicates the reading ease of the provided text.
# 0 is very confusing and 100 is very easy.
# Uses the Flesch Reading Ease Formula
def analyze_reading_level(text:str) -> float:
    reading_level = textstat.flesch_reading_ease(text)
    return reading_level


# Returns a number between -1 and 1, where -1 is super negative and 1 is super positive.
# Used TextBlob to determine the sentiment.
def analyze_sentiment(text:str) -> float:
    res = TextBlob(text)
    sentiment_score = res.sentiment.polarity
    return sentiment_score

def main():

    # Uncomment below line and comment other if having path issues.
    # with open('..data/sample_data.json', 'r') as file:
    with open('data/output.json', 'r', encoding = 'utf-8') as file:
        # Returns a list of python dictionaries
        data = json.load(file)

    # Create each row for the table
    rows = []
    for item in data:
        #do not analyze data if the status is False
        if item.get('status') == True:
            url = item.get('url')
            university_class = item.get('class')
            # If it cant retrieve privacy_policiy_text, it returns empty string
            privacy_policy_text = item.get('privacy_policy_text') or ''
            # If it cant retrieve dnsmpi_text, it returns empty string
            dnsmpi_text = item.get('dnsmpi_text') or ''
            dnsmpi_url = item.get('dnsmpi')
            if dnsmpi_url is not None and dnsmpi_url != '':
                dnsmpi = 1
            else:
                dnsmpi = 0

            # Perform all analysis functions
            ccpa_or_cpra = analyze_ccpa(privacy_policy_text)
            ferpa = analyze_ferpa(privacy_policy_text)
            gdpr = analyze_gdpr(privacy_policy_text)
            word_length = analyze_word_length(privacy_policy_text)
            reading_level = analyze_reading_level(privacy_policy_text)
            sentiment_index = analyze_sentiment(privacy_policy_text)

            # Append the data to the list
            row = {
                'University link': url,
                'Kind of university': university_class.replace('_', ' ').title(),
                'CCPA or CPRA': ccpa_or_cpra,
                'FERPA': ferpa,
                'GDPR': gdpr,
                'DNSMPI': dnsmpi,
                'Word length': word_length,
                'Reading level': reading_level,
                'Sentiment index': sentiment_index
            }
            rows.append(row)


    # Saves the rows and saves the table as a csv file.
    df = pd.DataFrame(rows)

    # Uncomment these if having path issues (depends on OS/environment setup)
    # df.to_csv('../data/data_analysis.csv', index=False) 
    # df.to_excel("../data/data_analysis.xlsx", index=False) 

    df.to_csv('./data/data_analysis.csv', index=False) # saves to csv
    df.to_excel("./data/data_analysis.xlsx", index=False) # saves to xlsx workbork for analyis later

main()