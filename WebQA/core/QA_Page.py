class QA_Page:
    def __init__(self):
        self.question = ""
        self.answers = []

    def parse(self, input_file):
        pass

    def print(self):
        print("Question: {0}".format(self.question.text))
        for idx, answer in enumerate(self.answers):
            print("Answer #{0}: {1}".format(idx, answer.text))
        print("\n")
