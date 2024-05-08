import pandas as pd
from helper_functions import (extract_text_from_html, remove_special_characters_and_punctuation,
                              apply_lda, process_url)

# Read the URL dictionary from the CSV file
url_dict_file = "url_dict.csv"
url_df = pd.read_csv(url_dict_file)
url_dict = dict(zip(url_df['Document Name'], url_df['url']))

if __name__ == "__main__":
    preprocessed_texts = []  # List to store clean texts
    entities_list = []
    topics_list = []
    sentiment_scores_list = []

    for name, url in url_dict.items():
        print(f"Processing document: {name}")  # Informative message

        try:
            # Extract text from HTML
            html_content = extract_text_from_html(url)

            # Remove special characters and punctuation from HTML content
            clean_text = remove_special_characters_and_punctuation(html_content)
            preprocessed_texts.append(clean_text)

            # Primary analysis
            stemmed_tokens, entities, lda_model, sentiment_scores = process_url(clean_text)

            # Append results to respective lists
            entities_list.append(entities)
            sentiment_scores_list.append(sentiment_scores)
            lda_model = apply_lda([stemmed_tokens])
            topics = [topic for _, topic in lda_model.print_topics()]
            topics_list.append(topics)
            # topics_list.append(lda_model)  # Assuming lda_model is the list of topics

        except Exception as e:
            print(f"Error processing document {name}: {e}")

    # Save clean texts to a text file
    with open('clean_texts.txt', 'w') as file:
        for name, text in zip(url_dict.keys(), preprocessed_texts):
            file.write(f"Document Name: {name}\n")
            file.write(f"Clean Text: {text}\n\n")

    # Create and save DataFrame
    data = {
        'Document Name': list(url_dict.keys()),
        'Entities': entities_list,
        'Sentiment Scores': sentiment_scores_list,
        'Topics': topics_list
    }

    df = pd.DataFrame(data)
    df.to_csv('apt29_data.csv', index=False)

    print("Processing complete. Results saved to apt29_data.csv and clean_texts.txt")
