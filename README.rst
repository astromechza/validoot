validoot - 1.2
==============

This module is designed to solve the most basic of argument validations:
types, clauses, and combinations of clauses. It is meant to remove some
of the boiler plate code used to check the input types and checks such
as between, or string lengths.

Github url: https://github.com/AstromechZA/validoot

Pypi url: https://pypi.python.org/pypi/validoot/1.2

Definitions
^^^^^^^^^^^

-  Clause - A function that takes in the value as a parameter and
   returns ``True`` or ``False``.
-  Operator - Allows you to “and” and “or” clauses together.

Basic example:
--------------

.. code:: python

    from validoot import validates, inst, typ, between

    @validates(inst(basestring), typ(int), between(0, 100))
    def do_something(name, id, age):
        pass

In the code above, a ``validoot.ValidationError`` will be thrown if the
``name`` is not a string or unicode, if the ``id`` is not an integer, or
if the ``age`` is not between 0 and 100.

Operators:
----------

We can extend the first example by adding an additional check for the
``name``: it must be between 5 and 40 characters. For this we use the
``validoot.And`` operator to combine the clauses.

.. code:: python

    from validoot import validates, inst, typ, between, len_between, And

    @validates(And(inst(basestring), len_between(5, 40)), typ(int), between(0, 100))
    def do_something(name, id, age):
        pass

An ``Or`` operator also exists. Both ``And`` and ``Or`` take in a
variable number of clauses and can be nested further.

Operator shortcuts are provided for joining clauses in a different
manner which reads differently (``._and(...)``, ``._or(...)``). So our
previous example can be changed to look like this:

.. code:: python

    from validoot import validates, inst, typ, between, len_between

    @validates(inst(basestring)._and(len_between(5, 40)), typ(int), between(0, 100))
    def do_something(name, id, age):
        pass

Operators can also be combined in more complicated ways:

.. code:: python

    inst(basestring)._and(len_between(5, 40))._or(typ(int))

Keyword arguments:
------------------

There is also support for keyword arguments:

.. code:: python

    from validoot import validates, inst, typ

    @validates(inst(basestring), something=typ(float))
    def do_something(name, something=1.0, anotherthing=2):
        pass

Here the ``something`` value must pass the validation checks as
specified in the decorator. No checks exist for ``anotherthing`` so it
has no restrictions.

Decorating Class/Static/Instance methods or Constructors:
---------------------------------------------------------

Methods belonging to classes can be validated as well in exactly the same way
as the examples above. Please make note of the order of the ``@validates``
decorator and other decorators such as ``@classmethod`` or ``@staticmethod``.

.. code:: python

    class SomeClass(object):

        # classmethod MUST be the innermost decorator!
        @validates(typ(int))
        @classmethod
        def some_class_method(cls, an_integer):
            return an_integer

        # staticmethod can be outer or inner decorator
        @staticmethod
        @validates(typ(float))
        def some_static_method(a_floater):
            return a_floater

        @validates(typ(string))
        def some_instance_method(self, a_string):
            return a_string

In order to validate arguments passed through to a constructor, the validates
decorator should be places on the class itself:

.. code:: python

    @validates(typ(string))
    class SomeClass(object):

        def __init__(self, username):
            self.username = username

Additional Clauses:
-------------------

There are some more complex clauses included with the package:

-  ``_`` : The underscore only allows ``NoneType``.
-  ``numeric`` : Only accepts ``int``, ``float``, or ``long`` types.
-  ``text`` : Only accepts instances of ``basestring`` (Python 2) or
   ``str`` (Python 3).
-  ``positive`` : Only positive numbers
-  ``negative`` : Only positive numbers
-  ``email_address`` : Simple regex email check (covers most basic examples)
-  ``ip_address`` : Only accept an IPv4 address
-  ``url`` : Simple regex url check (covers most basic examples)

These can be found in the ``validoot.builtins`` module.

FAQ:
----

What if I don’t want validation for one of the position arguments?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simple. Just use ``None``.

.. code:: python

    from validoot import validates, inst, between

    @validates(inst(basestring), None, between(0, 100))
    def do_something(name, id, age):
        pass

What validation clauses are built in?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``typ(t)`` - value must be of exact type ``t``
-  ``inst(t)`` - value must be of exact type ``t`` or of subclass
-  ``between(lower, upper, lower_inc=True, upper_inc=False)`` - the
   value must between ``lower`` and ``upper``. ``lower_inc`` and ``upper_inc``
   indicate range inclusivity.
-  ``len_between(...)`` - identical to ``between`` but uses
   ``len(value)``
-  ``regex(string)`` - value must match the regex string provided

How do I create my own validation clauses?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The built in clauses provided by Validoot are all subclasses of the
``validoot.clauses.Clause`` object. Check out its source code to see
how they work. Technically clauses can be any callable object so plain
functions or lambdas also work.
