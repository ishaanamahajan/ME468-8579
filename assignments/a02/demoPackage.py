import numpy

import random
import pandas
from lucifer import ProgressBar
from time import sleep


bar = ProgressBar(total=100)

for i in range(10):
  sleep(0.5)
  bar.show(amount=i+1, text = "Implementing package in ME468 container")


