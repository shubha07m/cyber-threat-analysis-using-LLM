import pandas as pd
from wordcloud import WordCloud
from collections import Counter
import re
import matplotlib.pyplot as plt
import os
import ast

# Read the data
df = pd.read_csv('apt29_data.csv')

# Create a directory to store plot images
plot_dir = 'plot_images'
os.makedirs(plot_dir, exist_ok=True)


def generate_word_cloud(df, max_entity_length=20):
    # Initialize an empty list to store all entities
    all_entities = []

    # Iterate over each row in the DataFrame
    for _, row in df.iterrows():
        entities_list = ast.literal_eval(row['Entities'])

        # Check if entities_list is not empty and structured correctly
        if isinstance(entities_list, list) and all(isinstance(entity, tuple) and len(entity) == 2 for entity in entities_list):
            # Flatten the list of entities and filter out entities based on criteria
            for entity, _ in entities_list:
                # Exclude entities that are only numbers
                if not entity.isdigit():
                    # Exclude entities containing 'microsoft'
                    if 'microsoft' not in entity.lower():
                        # Exclude entities with length greater than max_entity_length
                        if len(entity) <= max_entity_length:
                            # Exclude entities that match date patterns
                            if not re.match(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}', entity):  # Date pattern (e.g., 12/31/2023)
                                all_entities.append(entity)

    # Generate word cloud from the filtered entities
    entity_counts = Counter(all_entities)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(entity_counts)

    # Save the word cloud image
    wordcloud_path = os.path.join(plot_dir, 'wordcloud.png')
    wordcloud.to_file(wordcloud_path)

    # Select top 10 entities for pie chart
    top_entities = dict(entity_counts.most_common(10))

    # Generate pie chart for entity distribution
    fig, ax = plt.subplots(figsize=(8, 8))
    labels = list(top_entities.keys())
    sizes = list(top_entities.values())
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Entity Distribution (Top 10)')
    entity_pie_path = os.path.join(plot_dir, 'entity_pie_chart.png')
    fig.savefig(entity_pie_path, format='png')
    plt.close()

    return wordcloud_path, entity_pie_path


def generate_sentiment_plots(df):
    # Plot sentiment distribution
    sentiment_scores = df['Sentiment Scores'].apply(ast.literal_eval)
    sentiment_df = pd.DataFrame(sentiment_scores.tolist()).mean()

    # Save the sentiment plot image
    sentiment_path = os.path.join(plot_dir, 'sentiment_plot.png')
    sentiment_df.plot(kind='bar', color='blue')
    plt.title('Average Sentiment Scores')
    plt.xlabel('Sentiment')
    plt.ylabel('Score')
    plt.xticks(rotation=0)
    plt.savefig(sentiment_path, format='png')
    plt.close()

    # Find the mode sentiment category
    mode_sentiment = sentiment_df.idxmax()

    return sentiment_path, mode_sentiment


def generate_topic_distribution_plots(df):
    combined_topics = []

    for _, row in df.iterrows():
        topics = ast.literal_eval(row['Topics'])
        for topic in topics:
            topic_words = [word.split('"')[1] for word in topic.split('+') if 'microsoft' not in word.lower()]
            combined_topics.extend(topic_words)

    # Filter out dates and convert to lowercase
    combined_topics = [topic.lower() for topic in combined_topics if not topic.isdigit()]

    # Count frequency of each topic
    topic_counts = Counter(combined_topics)

    # Select top 10 topics
    top_topics = dict(topic_counts.most_common(10))

    # Generate word cloud from top topics
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(top_topics)

    # Save the word cloud image
    topic_wordcloud_path = os.path.join(plot_dir, 'topic_wordcloud.png')
    wordcloud.to_file(topic_wordcloud_path)

    # Generate pie chart for top 10 topics
    fig, ax = plt.subplots(figsize=(8, 8))
    labels = list(top_topics.keys())
    sizes = list(top_topics.values())
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title('Top 10 Topic Distribution')
    topic_pie_path = os.path.join(plot_dir, 'topic_pie_chart.png')
    fig.savefig(topic_pie_path, format='png')
    plt.close()

    return topic_wordcloud_path, topic_pie_path


def generate_summary_html():
    wordcloud_img, entity_pie_img = generate_word_cloud(df)
    sentiment_img, mode_sentiment = generate_sentiment_plots(df)
    topic_wordcloud_img, topic_pie_img = generate_topic_distribution_plots(df)

    html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Visualization Summary</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                }}

                h1 {{
                    text-align: center;
                    font-size: 2em;
                    margin-bottom: 20px;
                }}

                h2 {{
                    font-size: 1.5em;
                    margin-bottom: 10px;
                }}

                h3 {{
                    font-size: 1.2em;
                    margin-top: 10px;
                }}

                img {{
                    max-width: 800px;
                    width: 100%;
                    display: block;
                    margin: 10px auto;
                }}

                p {{
                    margin-bottom: 10px;
                }}
            </style>
        </head>
        <body>
            <h1>Visualization Summary</h1>

            <h2>Word Cloud of Entities</h2>
            <img src="{wordcloud_img}" alt="Word Cloud of Entities" />
            <h3>Pie Chart of Entity Distribution (Top 10)</h3>
            <img src="{entity_pie_img}" alt="Pie Chart of Entity Distribution (Top 10)" />

            <h2>Average Sentiment Scores</h2>
            <p>Most common sentiment category: {mode_sentiment}</p>
            <img src="{sentiment_img}" alt="Average Sentiment Scores" />

            <h2>Top 10 Topic Distribution</h2>
            <h3>Word Cloud of Topics</h3>
            <img src="{topic_wordcloud_img}" alt="Word Cloud of Topics" />
            <h3>Pie Chart of Top 10 Topic Distribution</h3>
            <img src="{topic_pie_img}" alt="Pie Chart of Top 10 Topic Distribution" />
        </body>
        </html>
        """

    with open('visualization_summary.html', 'w') as file:
        file.write(html_content)


if __name__ == "__main__":
    generate_summary_html()
