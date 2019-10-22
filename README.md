# WebQA

## Installation

```shell
git clone https://github.com/kearnsw/WebQA.git && cd WebQA
python setup.py develop
```

## Preprocess Forum Posts

`python -m WebQA.pages.Medhelp -d "/data/www.medhelp.org" -o "qa.pkl"`
`python -m WebQA.pages.Healthtap -d "/data/www.healthtap.com" -o "qa.pkl"`

## QA_Page

A QA Page is the main class of WebQA that consists of Question and Answers. Supported parsers are found in the pages
module and can be instantiated as below. To create a new page parser just override the parse method.

```python
from WebQA.pages.Healthtap import HealthtapPage

page = HealthtapPage()
page.parse("www.healthtap.com/user_questions/example.html")
print(page.question)
for answer in page.answers:
    print(answer)
```

## Posts

Questions and Answers are both subclasses of Post and contain text and a user as attributes.
```python
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
```
