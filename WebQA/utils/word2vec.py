import os
import pickle as pkl
import sys
from multiprocessing import Pool, cpu_count

import pandas as pd
import spacy
from gensim.models import Word2Vec

nlp = spacy.load("en_core_web_lg")


def split_sentences(raw_text):
    doc = nlp(raw_text)
    return doc.sents


def tokenize(doc):
    return [token.text for token in doc]


def preprocess(text):
    return [tokenize(sentence.as_doc()) for sentence in split_sentences(text)]


def batch_tokenize(list_of_sentences):
    """

    :param list_of_sentences: a list of sentences
    :return: a list of t
    """
    sys.stdout.write("Tokenizing {0} questions...".format(len(list_of_sentences)))
    sys.stdout.flush()
    with Pool(10) as p:
        tokenized_sentences = p.map(preprocess, list_of_sentences)
    return flatten(tokenized_sentences)


def flatten(list_of_lists):
    return [item for l in list_of_lists for item in l]


if __name__ == "__main__":

    if os.path.isfile("tokens.out"):
        with open("tokens.out", "rb") as f:
            tokenized_sentences = pkl.load(f)
    else:
        qs = []
        for arg in sys.argv:
            print("Reading {0}...".format(arg))
            pages = pd.read_pickle(arg)
            questions = []
            answers = []
            for page in pages:
                if page and page.question != "":
                    if page.answers:
                        medical_answers = [answer for answer in page.answers]
                        questions.append(page.question.text.strip())
                        answers.append(medical_answers[0].text.strip())

            data = pd.DataFrame({"Question": questions, "Answer": answers})

            qs += list(data["Question"])

        tokenized_sentences = batch_tokenize(qs)
        with open("tokens.out", "wb") as f:
            pkl.dump(tokenized_sentences, f, protocol=4)

    num_cpus = cpu_count()
    sys.stdout.write("Training Word2Vec model...")
    sys.stdout.flush()
    model = Word2Vec(tokenized_sentences, size=100, window=3, sg=1, workers=num_cpus)
    model.save("webQA.bin")
