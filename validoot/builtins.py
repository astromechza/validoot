from .clauses import typ, inst, at_least, at_most, between, regex

"""
The builtins provided in this module are simply useful complex clauses that are
built by combining the basic Clauses.
"""

# underscore : return True if the value is None
_ = lambda v: v is None

# numeric : return True if the value is a int, float, or long
try:
    long = long
    numeric = typ(int)._or(typ(float), typ(long))
except NameError:
    numeric = typ(int)._or(typ(float))

# text : return True if the value is a string type
try:
    basestring = basestring
    text = inst(basestring)
except NameError:
    text = inst(str)

# positive
positive = at_least(0, inclusive=True)

# negative
negative = at_most(0, inclusive=False)

# geo
latitude = numeric._and(between(-90, 90))
longitude = numeric._and(between(-180, 180))

# email : BASIC email checking
email_address = regex(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

# ip
ip_address = regex(r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
                   r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')

# url : BASIC url checking
url = regex(r'((https?|ftp)://)?(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?')
