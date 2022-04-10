from src.es import run
from sys import argv

text = open(argv[1],'r').read()
run(text)