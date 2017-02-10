from unittest import TestCase, main
from pickling import * 
from pickle import load, dump
from os import remove
from os.path import isfile

class TestWritePickle(TestCase):
  def test_pickling_list(self):
    obj = [1, 2, 3]
    write_pickle("test.pkl", obj)
    self.pickle_file = open("test.pkl", "rb")
    unpickled = load(self.pickle_file) 
    self.assertEqual(obj, unpickled)
    self.pickle_file.close()

  def tearDown(self):
    remove("test.pkl") 

class TestFBInfoToCSV(TestCase):
  def test_empty_list(self):
    list_of_dict = []
    write_fb_info_to_csv("test.csv", list_of_dict)
    self.assertEqual(False, isfile("test.csv"))
  
  def test_one_dict_list(self):
    list_of_dict = [{"id": "a", "name": "b", "category": "c"}]
    write_fb_info_to_csv("test.csv", list_of_dict)
    self.csv_file = open("test.csv", "r")
    self.assertEqual("name,id,category,url\nb,a,c,http://facebook.com/a\n", self.csv_file.read())
    self.csv_file.close()

  def test_multi_dict_list(self):
    list_of_dict = [{"id": "a", "name": "b", "category": "c"},
                    {"id": "d", "name": "e", "category": "f"}]
    write_fb_info_to_csv("test.csv", list_of_dict)
    self.csv_file = open("test.csv", "r")
    self.assertEqual("name,id,category,url\nb,a,c,http://facebook.com/a\ne,d,f,http://facebook.com/d\n", self.csv_file.read())
    self.csv_file.close()

  def tearDown(self):
    if isfile("test.csv"):
      remove("test.csv")

if __name__ == '__main__':
  main() 
