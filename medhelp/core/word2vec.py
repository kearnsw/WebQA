from gensim.models import Word2Vec
from multiprocessing import Pool, cpu_count
import spacy
from medhelp.core.pages import QA_Page
import medhelp.core.posts
from medhelp.core import posts
from medhelp.core import user
import pandas as pd

nlp = spacy.load("en_core_web_lg")


def split_sentences(raw_text):
    doc = nlp(raw_text)
    return doc.sents


def tokenize(doc):
    return [token for token in doc]


def preprocess(question):
    sentences = split_sentences(question)
    return [tokenize(sentence.as_doc()) for sentence in sentences]


def batch_tokenize(iterable):
    with Pool(cpu_count()) as p:
        tokenized_sentences = p.map(preprocess, iterable)
    return flatten(tokenized_sentences)


def flatten(list_of_lists):
    return [item for l in list_of_lists for item in l]


if __name__ == "__main__":

    pages = pd.read_pickle("qa.pkl")
    questions = []
    answers = []
    for page in pages:
        if page and page.question != "":
            if page.answers:
                medical_answers = [answer for answer in page.answers]
                questions.append(page.question.text.strip())
                answers.append(medical_answers[0].text.strip())

    data = pd.DataFrame({"Question": questions, "Answer": answers})

    qs = list(data["Question"])
    print(len(questions))
    tokenized_sentences = batch_tokenize(qs)
    print(len(tokenized_sentences))
    num_cpus = cpu_count()
    model = Word2Vec(tokenized_sentences, size=100, window=3, sg=1, workers=num_cpus)
    model.save("webQA.bin")
