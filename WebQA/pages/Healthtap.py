from bs4 import BeautifulSoup
from WebQA.core.User import User
from WebQA.core.Post import Question, Answer
from WebQA.core import QA_Page
import pickle as pkl
import os
from multiprocessing import Pool, cpu_count
from argparse import ArgumentParser


class HealthtapPage(QA_Page):
    def __init__(self):
        super().__init__()
        self.question = ""
        self.answers = []

    def parse(self, input_file):

        # Parse HTML into BeautifulSoup object
        with open(input_file, "r") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Extract the post content
        question_container = soup.find("div", {'class': 'question-text'})
        if question_container:
            self.question = Question(question_container.h1.text, None)
        answer_containers = soup.find_all("div", {'class': 'answer clearfix'})
        if answer_containers:
            for answer in answer_containers:
                self.answers.append(Answer(answer.text, None))
        return self

    def print(self):
        print("Question: {0}".format(self.question.text))
        for idx, answer in enumerate(self.answers):
            print("Answer #{0}: {1}".format(idx, answer.text))
        print("\n")


def load(input_file):
    """
    Parses the HTML from Medhelp forum posts and extracts user questions and answers
    :param input_file: filename of post page to process
    :return: A QA_Page object that contains the post question and answers
    """
    page = HealthtapPage()
    return page.parse(input_file)


def find_pages(path):
    """
    Walk path and collect all html file names
    :param path: Directory to start walk
    :return: All html file names in the directory and subdirectories
    """
    list_of_files = {}
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename.endswith('.html'):
                list_of_files[filename] = os.sep.join([dirpath, filename])
    return list_of_files.values()


def process_all(input_dir, output_file):
    """
    Parallel process all posts  
    :param dir: Directory that contains Medhelp posts
    :return: None, saves all files to output dir
    """
    html_pages = find_pages(input_dir)
    
    with Pool(cpu_count()) as p:
        pages = p.map(load, html_pages)

    with open(output_file, "wb") as f:
        pkl.dump(pages, f)


if __name__ == "__main__":

    cli_parser = ArgumentParser()
    cli_parser.add_argument("-d", "--input_dir", 
                            default="/data/common/www.healthtap.com/user_questions",
                            help="directory containing Medhelp posts")
    cli_parser.add_argument("-o", "--output", default="healthtap.pkl", help="file to write QA data extracted from posts")
    args = cli_parser.parse_args()

    process_all(args.input_dir, args.output)


