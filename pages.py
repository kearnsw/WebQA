from bs4 import BeautifulSoup
from posts import Question, Answer
import pickle as pkl
import os
import sys

class QA_Page:
	
	def __init__(self):
		self.question = ""
		self.answers = []
	
	def parse(self, input_file):
		
		with open(input_file, "r") as f:
			soup = BeautifulSoup(f, "html.parser")

		posts = soup.find_all("div", {'class': 'post_message'})
		if posts:
			post_text = [post.text for post in posts]
			self.question = Question(post_text[0])
			for answer in post_text[1:]:
				self.answers.append(Answer(answer))
			
			return self
	
def load(input_file):
	page = QA_Page()
	return page.parse(input_file)
		
def find_pages(path):
	list_of_files = {}
	for (dirpath, dirnames, filenames) in os.walk(path):
		for filename in filenames:
			if filename.endswith('.html'): 
				list_of_files[filename] = os.sep.join([dirpath, filename])
	return list_of_files.values()

def process_all():
	html_pages = find_pages("/data/common/www.medhelp.org/posts/")
	pages = []
	num_pages = len(html_pages)
	for idx, page in enumerate(html_pages):
		if idx % 500 == 0:
			sys.stdout.write("Processing page {0}/{1}...\n".format(idx, num_pages))
			sys.stdout.flush()
		pages.append(load(page))

	with open("pages.pkl", "wb") as f:
		pkl.dump(pages, f)

with open("pages.pkl", "rb") as f:
	pages = pkl.load(f)
	answer_count = 0
	question_count = 0
	for page in pages:
		if page:
			question_count += 1
			for a in page.answers:
				answer_count += 1
		else:
			continue

print(question_count, answer_count)
