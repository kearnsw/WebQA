from bs4 import BeautifulSoup
from WebQA.core.Post import Question, Answer
from WebQA.core.QA_Page import QA_Page
from WebQA.utils.processing import process_all
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
    return HealthtapPage().parse(input_file)


if __name__ == "__main__":

    cli_parser = ArgumentParser()
    cli_parser.add_argument("-d", "--input_dir", 
                            default="/data/common/www.healthtap.com/user_questions",
                            help="directory containing Medhelp posts")
    cli_parser.add_argument("-o", "--output", default="healthtap.pkl", help="file to write QA data extracted from posts")
    args = cli_parser.parse_args()

    process_all(args.input_dir, args.output, load)


