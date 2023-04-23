import streamlit as st
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pyperclip

def scrape_trends(url):
    """
    This function scrapes the Twitter Trends webpage and returns a sorted
    dataframe of the top hashtags along with their tweet count.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    data = [] # list to store scraped data

    for li in soup.find_all('li'):
        a_tag = li.find('a')
        title = a_tag.text
        tweet_count_tag = li.find('span', class_='tweet-count')
        if tweet_count_tag:
            tweet_count = tweet_count_tag.text
        else:
            tweet_count = ''
        if title.startswith('#'):
            data.append({'Title': title, 'Tweet Count': tweet_count})

    # write data to CSV file
    with open('trends.csv', mode='w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Title', 'Tweet Count'])
        writer.writeheader()
        writer.writerows(data)

    df = pd.read_csv("trends.csv")
    df_sorted = df.sort_values('Tweet Count', ascending=False)
    df_sorted['Tweet Count'] = df_sorted['Tweet Count'].fillna(1)
    df_sorted = df_sorted.reset_index(drop=True)

    return df_sorted

def main():
    st.title("Twitter Trends")

    url = st.text_input("Enter the URL of Twitter Trends page:")

    if not url:
        st.warning("Please enter a valid URL!")
        return

    num_title = st.slider("How many titles to include in the output?", 1, 40, 5)

    df_sorted = scrape_trends(url)

    titles = df_sorted.iloc[:num_title, 0].tolist()

    user_text = st.text_input("Enter some text:")

    if not user_text:
        st.warning("Please enter some text!")
        return

    for i in range(num_title):
        output = user_text + ' ' + ' '.join(titles[:i+1])
        st.write(output)
        if st.button("Copy Output {}".format(i+1)):
            pyperclip.copy(output)
            st.success("Output {} copied to clipboard!".format(i+1))

if __name__ == "__main__":
    main()
