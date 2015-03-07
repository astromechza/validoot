from .clauses import typ, inst

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
