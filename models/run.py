#!/usr/bin/env python
import logging
import os
import sys

if os.environ.get("ALLENNLP_DEBUG"):
    LEVEL = logging.DEBUG
else:
    LEVEL = logging.INFO

sys.path.insert(0, os.path.dirname(os.path.abspath(os.path.join(__file__, os.pardir))))
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
                    level=LEVEL)

from memory_profiler import profile
import cProfile

@profile
def profWrap():
    cProfile.run('from allennlp.commands.train import train_model_from_file')
    cProfile.run('train_model_from_file("./model/baseline.json", "./result")')



if __name__ == "__main__":
    profWrap()
