import json
import logging
from typing import Dict, List
import re
import inspect

from flask import request

from routes import app

logger = logging.getLogger(__name__)

def getNextProbableWords(classes: List[Dict],
                         statements: List[str]) -> Dict[str, List[str]]:
  # assumption "statements" is no empty element, class keys in the classes list are unique,  type names used in the classes list are valid and can be recognized as either built-in types or custom types and there is no key in "classes" that is named with character '<' ahd '>'

  output = {}

  def is_custom_type(type_name):
    try:
      class_object = globals()[type_name]
      return inspect.isclass(class_object)
    except KeyError:
      return False

  def check_polymorphic(input_value, item):
    # Get the first type of the input
    if not is_custom_type(input_value[0]):
      for i in item:  #  assumes that i is a dictionary with only one key-value pair
        if input_value[0] == list(i.keys())[0]:
          first_type = type(i[input_value[0]])
          break
    else:
      print(input_value[0])
      first_type = type(input_value[0])

    for value in input_value[1:]:
      if not is_custom_type(value):
        for i in item:
          if value == list(i.keys())[0]:
            if type(i[value]) != first_type:
              return True
            break
      elif type(value) != first_type:
        return True

    return False

  def extract_class_member(class_name, condition=None):
    if condition is None:
      for item in classes:
        if class_name in item:
          return list(item[class_name].keys(
          ) if isinstance(item[class_name], dict) else item[class_name])
    else:
      for item in classes:
        if class_name in item:
          class_obj = item[class_name]
          output = []
          for member in list(
              class_obj.keys() if isinstance(class_obj, dict) else class_obj):
            if re.match(condition.lower(), member.lower()):
              if isinstance(class_obj, dict):
                match = re.findall(r'<(.*?)>', class_obj[member])
                if match:
                  temp = extract_class_member(match[0])
                  if check_polymorphic(temp, classes):
                    member = ""
                  else:
                    member = temp

              output.append(member)
          if output:
            return output
    return ""

  target = []
  for statement in statements:
    s_class = statement.split('.')[0]
    target.append(s_class)

  for statement in statements:
    num_layer = statement.count('.')  # handle class key ends with '.' only

    s_class = statement.split('.')[0]

    member = None
    if num_layer == 1:
      if statement.split('.')[1] == '':
        member = extract_class_member(s_class)
      else:
        member = extract_class_member(s_class, statement.split('.')[1])
    else:
      if len(statement.split('.'))>1:
        member = extract_class_member(s_class, statement.split('.')[1])

    if s_class in target:
      if member == []:
        member = [""]
      output[statement] = sorted(member)[:5] if member is not None else [""]

  return output

@app.route('/lazy-developer', methods=['POST'])
def lazy_developer():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = getNextProbableWords(data.get("classes"), data.get("statements"))
    logging.info("My result :{}".format(result))
    return json.dumps(result)
