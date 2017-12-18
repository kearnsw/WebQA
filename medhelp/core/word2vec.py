from gensim.models import Word2Vec
import multiprocessing
import spacy
import pickle as pkl
from medhelp.core.pages import QA_Page
import medhelp.core.posts
from medhelp.core import posts
from medhelp.core import user
import pandas as pd
import sys


nlp = spacy.load("en_core_web_lg")

def split_sentences(raw_text):
	doc = nlp(raw_text)
	return doc.sents

def tokenize(doc):
	return [token for token in doc]

if __name__ == "__main__":
	with open("qa.pkl", "rb") as f:
		pages = pd.read_pickle(f)
	questions = []
	answers = []
	for page in pages:
		if page and page.question != "":
			if page.answers:
				medical_answers = [answer for answer in page.answers]
				questions.append(page.question.text.strip())
				answers.append(medical_answers[0].text.strip())
			#answers.append(page.answers[0].text.strip())
	
	data = pd.DataFrame({"Question": questions, "Answer": answers})
	
	qs = list(data["Question"])
	print(len(questions))
	tokenized_sentences = []
	for q in qs:
		sentences = split_sentences(q)
		tokenized_sentences += [tokenize(sentence.as_doc()) for sentence in sentences]
	print(len(tokenized_sentences))
	num_cpus = multiprocessing.cpu_count()
	model = Word2Vec(tokenized_sentences, size=100, window=3, sg=1, workers=num_cpus)
	model.save("webQA.bin")	
