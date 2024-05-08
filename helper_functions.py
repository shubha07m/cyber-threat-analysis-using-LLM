import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import re
import spacy
from gensim.models import LdaModel
from gensim.corpora import Dictionary
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# Function to extract text from HTML content
def extract_text_from_html(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()
    return text


# Function to tokenize the text
def tokenize_text(text):
    tokens = word_tokenize(text)
    return tokens


# Function to remove special characters and punctuation
def remove_special_characters_and_punctuation(text):
    # Define patterns to exclude (special characters, punctuation, numbers, common words)
    pattern1 = r"[^\w\s\-']"  # Removes special characters, punctuation except hyphen and apostrophe
    pattern2 = (r"\b(January|February|March|April|May|June|July|August|September|October|November|December|\b[A-Z]["
                r"a-z]+\b|\bFirst|Second|Third|Fourth|Fifth|Sixth|Seventh|Eighth|Ninth|Tenth)\b")  # Removes month
    # names, full day names, and ordinal numbers (First-Tenth)

    # Remove special characters and punctuation except hyphen and apostrophe
    clean_text = re.sub(pattern1, "", text)
    # Remove month names, full day names, and ordinal numbers
    clean_text = re.sub(pattern2, "", clean_text)
    # Remove all occurrences of \u00a0 (including multiple)
    clean_text = re.sub(r"\u00a0+", "", clean_text)
    # This pattern removes various newline characters
    clean_text = re.sub(r"(?:\r?\n|\r|\u0085|\u2028|\u2029)", "", clean_text)
    # Remove words longer than 20 characters
    clean_text = re.sub(r"\b\w{21,}\b", "", clean_text)
    return clean_text


# Function to remove stopwords
def remove_stopwords(tokens):
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
    return filtered_tokens


# Function to stem tokens
def stem_tokens(tokens):
    porter = PorterStemmer()
    stemmed_tokens = [porter.stem(word) for word in tokens]
    return stemmed_tokens


# Function to extract entities using spaCy NER
def extract_entities(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


# Function to apply LDA for topic modeling
def apply_lda(texts, num_topics=5):
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(doc) for doc in texts]
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary)
    return lda_model


# Function to perform sentiment analysis
def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(text)
    return sentiment_scores


def process_url(clean_text):
    tokens = tokenize_text(clean_text)
    filtered_tokens = remove_stopwords(tokens)
    stemmed_tokens = stem_tokens(filtered_tokens)

    # Extract entities
    entities = extract_entities(clean_text)
    # Apply LDA for topic modeling if needed
    lda_model = apply_lda([stemmed_tokens])  # Passing tokens as list
    # Perform sentiment analysis
    sentiment_scores = analyze_sentiment(clean_text)

    return stemmed_tokens, entities, lda_model, sentiment_scores
