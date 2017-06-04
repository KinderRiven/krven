

def fun(*args):
   log = ""
   for each in args:
      log += "[" + str(each) + "]"
      print log

array = [1, 2, 3, 4]
fun("HELLO", "WORLD", "WELL", array)