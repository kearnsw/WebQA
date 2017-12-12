class Post:
	def __init__(self, text, user):
		self.text = text
		self.user = user
	
	def print(self):
		print(self.text)

class Question(Post):
	def __init__(self, text, user):
		super().__init__(text, user)

class Answer(Post):
	def __init__(self, text, user):
		super().__init__(text, user)

