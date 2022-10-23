from django import template

register = template.Library()

@register.filter(name='split')
def split(value, key):
  """
    Returns the value turned into a list.
  """
  return value.split(key)[2]

@register.filter(name='split_plus')
def split(value, key):
  """
    Returns the value turned into a list.
  """
  url = value.split(key)
  city = url[2]
  number = int(url)[3]
  new_number = number + 1
  output = city + "/" + str(new_number)

  return output