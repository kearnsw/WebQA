from bs4 import BeautifulSoup
from WebQA.core.User import User
from WebQA.core.Post import Question, Answer
from WebQA.core.QA_Page import QA_Page
import pickle as pkl
import os
from multiprocessing import Pool, cpu_count
from argparse import ArgumentParser


class MedhelpPage(QA_Page):

    def __init__(self):
        super().__init__()
        self.question = ""
        self.answers = []

    def parse(self, input_file):
        # Parse HTML into BeautifulSoup object
        with open(input_file, "r") as f:
            soup = BeautifulSoup(f, "html.parser")

        # Extract the post content
        posts = soup.find_all("div", {'class': 'post_message_container'})
        if posts:
            for idx, post in enumerate(posts):
                # Get OP user ID
                try:
                    user_id = post.find("a").text
                except:
                    user_id = None

                # Check if user who submitted post is a medical professional
                if post.find("img", {'class': 'doctor_icon'}) or post.find("img", {'class': 'nurse_icon'}):
                    isMedical = True
                else:
                    isMedical = False
                user = User(user_id, isMedical)

                # Extract post text
                text = post.find("div", {'class': "post_message"}).text

                # First post is the question and subsequent posts are replies (could possibly improve this to look at
                # OP replies and subsequent thread discussion)
                if idx == 0:
                    self.question = Question(text, user)
                else:
                    self.answers.append(Answer(text, user))
            return self


def load(input_file):
    """
    Parses the HTML from Medhelp forum posts and extracts user questions and answers
    :param input_file: filename of post page to process
    :return: A QA_Page object that contains the post question and answers
    """
    return MedhelpPage().parse(input_file)


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
    cli_parser.add_argument("-d", "--input_dir", default="/data/common/www.WebQA.org/posts/",
                            help="directory containing Medhelp posts")
    cli_parser.add_argument("-o", "--output", default="qa.pkl", help="file to write QA data extracted from posts")
    args = cli_parser.parse_args()

    process_all(args.input_dir, args.output)


