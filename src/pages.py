from bs4 import BeautifulSoup
from posts import Question, Answer
import pickle as pkl
import os
import sys
from random import randint
from user import User
from tqdm import tqdm

class QA_Page:
	
	def __init__(self):
		self.question = ""
		self.answers = []
	
	def parse(self, input_file):
		
		with open(input_file, "r") as f:
			soup = BeautifulSoup(f, "html.parser")

		posts = soup.find_all("div", {'class': 'post_message_container'})
		if posts:
			for idx, post in enumerate(posts):
				try:
					user_id = post.find("a").text
				except:
					user_id = None

				if post.find("img", {'class': 'doctor_icon'}) or post.find("img", {'class': 'nurse_icon'}):
					isMedical = True
				else:
					isMedical = False
				user = User(user_id, isMedical)	
				text = post.find("div", {'class': "post_message"}).text
				if idx == 0:
					self.question = Question(text, user)
				else:
					self.answers.append(Answer(text, user))
			return self
	
	def print(self):
		print("Question: {0}".format(self.question.text))
		for idx, answer in enumerate(self.answers):
			print("Answer #{0}: {1}".format(idx, answer.text))
		print("\n")	

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
	for idx, page in enumerate(tqdm(html_pages)):
		pages.append(load(page))

	with open("qa.pkl", "wb") as f:
		pkl.dump(pages, f)
if __name__ == "__main__":
	# process_all()

	with open("qa.pkl", "rb") as f:
		pages = pkl.load(f)
		answer_count = 0
		question_count = 0
		is_medical_count = 0
		for page in pages:
			if page:
				question_count += 1
				for a in page.answers:
					answer_count += 1
					if a.user.isMedical:
						is_medical_count += 1
						print(page.question.text, a.text)
			else:
				continue

	print(question_count, answer_count, is_medical_count)

	rand_page = pages[randint(0, len(pages)-1)]
	rand_page.print()

	page = load("/data/common/www.medhelp.org/posts/Diabetes/headache/show/2163033.html")
	page.question.print()
	print(page.answers[0].user.isMedical)
	print(page.answers[0].text)

