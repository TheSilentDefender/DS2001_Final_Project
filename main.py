import pandas
from art import *


def read_data(file):
  data = pandas.read_csv(file)
  return data


def main():
  print(tprint("DS2001FINALPROJECT","rnd-xlarge"))
  print(read_data("SPCsv202211080904.csv"))


main()