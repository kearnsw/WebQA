class Post:
	def __init__(self, text):
		self.text = text
	
	def print(self):
		print(self.text)

class Question(Post):
	def __init__(self, text):
		super().__init__(text)

class Answer(Post):
	def __init__(self, text):
		super().__init__(text)

