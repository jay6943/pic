import json
import ezdxf

doc = ezdxf.new()
msp = doc.modelspace()


layers = []
points = []


libs = '../../mask/libs'


def jload(filename):
  fp = open(f'{filename}.json', 'r', encoding='utf-8')
  data = json.load(fp)
  fp.close()
  return data


def jdump(filename, data):
  fp = open(f'{filename}.json', 'w', encoding='utf-8')
  json.dump(data, fp, indent=4, ensure_ascii=False)
  fp.close()


def jput(filename, title, value):
  data = jload(filename)
  data[title] = value
  jdump(filename, data)
