Title: Python Easter Eggs
Date: 2018-6-24
Tags: Python, CPython
Category: Python,  Easter, Eggs
Slug: python-easter-eggs
Authors: Jim Fasarakis-Hilliard
Summary: Some hidden easter eggs found in the CPython implementation of Python.

This is a small list of eggs found so far in the CPython implementation of Python. Do note that all these might not be present in other Python implementations.

Feel free to notify me if you find something that isn't here.

What is `this`?
---------------

Probably the most famous of the bunch is `this`. Importing `this` will get you the Zen of Python which provides a nice set of rules you can obnoxiously drop on people during code reviews.

    :::python
    import this
    The Zen of Python, by Tim Peters

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!

Go ahead and check out the [source for `this`][1]. It uses one of the most well known encryption techniques.

Antigravity!
------------

I won't spoil this, go open your terminal and type:

    :::python
    import antigravity

If you're on Python 3, don't close your terminal. There's an additional gem here for you:

    :::python
    from antigravity import geohash

To find out more about this, see the source of [`antigravity.py`][2].

Hello World [...|!]
-------------------

The output here differs slightly if you run it under Python 2 or Python 3, seems like the Python 3 version is merrier than its Python 2 counterpart:

    :::python
    # Under Python 3
    >>> import __phello__
    Hello world!
    >>> from __phello__ import spam  # module in package __phello__
    Hello world!
    >>> import __hello__
    Hello world!

That's a lot of hellowing! Under Python 2, the message uses a trailing ellipsis, how suspenseful:

    :::python
    # Python 2
    >>> import __hello__
    Hello world...

These (`__hello__` and `__phello__`) are used to test frozen modules/packages from what I've understood.

Brace yourself
--------------

This just speaks for itself:

    :::python
    >>> from __future__ import braces
      File "<stdin>", line 1
    SyntaxError: not a chance

Of course, these are not really needed because Python boasts one of the most [sophisticated parsers][4] around.

Friendly Language Uncle For Life
--------------------------------

For some of the backstory here, take a look at [PEP 401][3]. One of the official acts of the FLUFL was to reinstate the `<>` comparison operator which existed in Python 2 and was remove in Python 3:

    :::python
    >>> 1 <> 3
      File "<stdin>", line 1
        1 <> 3
           ^
    SyntaxError: invalid syntax
    >>> from __future__ import barry_as_FLUFL
    >>> 1 <> 3
    True

Don't do this.

[comments]: # (Links)
[1]: https://github.com/python/cpython/blob/master/Lib/this.py
[2]: https://github.com/python/cpython/blob/master/Lib/antigravity.py
[3]: https://www.python.org/dev/peps/pep-0401/
[4]: https://www.python.org/doc/humor/#python-block-delimited-notation-parsing-explained
