from test.test_word_dict import is_neutral
from utils.positive_words import positive_words
from utils.negative_words import negative_words
from utils.neutral import neutral_words
import sqlite3
from pymongo import MongoClient

client = MongoClient("mongodb+srv://saaniashaik:Atlas%40123@cluster0.gr3pnpm.mongodb.net/myDatabase?retryWrites=true&w=majority&appName=Cluster0")
database = client.get_database("textminer")
sentences_collection = database.get_collection("sentences")
words_collection = database.get_collection("words")


def score_paragraph(paragraph):
    con = sqlite3.connect("./utils/tutorial.db", check_same_thread=False)  # like mongodb connection !
    cur = con.cursor()
    paragraph_score = 0
    sentences = paragraph.split(".")
    for i, sentence in enumerate(sentences):
        sentence_score = score_sentence(sentence)
        sentiment = "Negative"
        if sentence_score > 0:
            sentiment = "Positive"
        if sentence_score == 0:
            sentiment = "Neutral"
        mydict = {"sentence": sentence, "score": sentence_score, "sentiment": sentiment}
        sentences_collection.insert_one(mydict)
        paragraph_score += sentence_score
    return paragraph_score


def score_sentence(sentence: str):
    """
    Analyze score for given sentence.
    :param sentence: Sentence to be analyzed
    :return: sentiment score for the sentence
    """
    res = 0
    words = sentence.split()
    for i, word in enumerate(words):
        word_score = analyze_word(word)
        available_in_dict = is_available_in_dict(word)
        word_dict = {"word": word, "score": word_score, "is_available_in_dict": available_in_dict}
        words_collection.insert_one(word_dict)
        res += word_score
    return res


def analyze_word(word):
    """
    Analyze score for given word.
    :param word: word to be analyzed
    :return: sentiment score for the word
    """
    is_positive = positive_check(word)
    is_negative = negative_check(word)
    if is_positive:
        return 1
    if is_negative:
        return - 1
    return 0  # if neutral


def positive_check(word):
    return word in positive_words


def negative_check(word):
    return word in negative_words


def neutral_check(word):
    return word in neutral_words


def is_available_in_dict(word):
    is_in_positive = positive_check(word)
    is_in_negative = negative_check(word)
    is_in_neutral = neutral_check(word)
    return is_in_positive or is_in_negative or is_in_neutral
keep