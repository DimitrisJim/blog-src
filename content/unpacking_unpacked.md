Title: Unpacking Unpacking in Python
Date: 2018-7-26
Tags: Python
Category: Python, Iterables
Slug: python-unpackings-unpacked
Authors: Jim Fasarakis-Hilliard
Summary: This post describes the operation of unpacking in Python. From function definitions and calls to assignments and displays.

[comment]: # (Introduction)

By Python stars, I don't mean multiplication (`a*b`), exponentiation (`a**b`),
star imports (`import *`) or the bare `*` in function definitions for
[keyword only arguments][1]. This is about using `*` with *iterables* and `**`
with *mappings* in the, as will become clearer, context of assignments.

This post assumes using a recent Python version (`Python 3.6.4 ` on my machine). Also, since this is the best place to say this: Don't use Python 2 in *new* projects, get to the `__future__` and let 2.7 die in peace.

[comment]: # (Terminology)

Terminology
-----------

First, some terminology is needed for *Iterable*, *Mapping* and *Unpacking*. Since iterable is really short, I'll just dump a quote here:

> **Iterable**: An object capable of returning its members one at a time.
Pythons' built-in sequences (like `list`, `tuple`, `str`), sets and
mappings are all iterable. Any user defined class can also become
iterable by [implementing the appropriate special methods][2].

Similarly, using the [Python Glossary][14], we find that mapping is:

> A container object that supports arbitrary key look-ups and implements the methods specified in the Mapping or MutableMapping abstract base classes. Examples include dict, collections.defaultdict, collections.OrderedDict and collections.Counter.

Basically, it's a collection of distinct key to value pairs that implements `__contains__`, `keys`, `items`, `values`, `get`, `__eq__`, and `__ne__`. You shouldn't care much for these methods for now.

### Unpacking

Unpacking is a wee bit trickier. The problem is that the term *unpacking* is overloaded IMHO; it's used to describe two related but *different operations*.

#### Unpacking on RHS of assignments

The first operation, for which the term unpacking makes sense to me, is on the *Right Hand Side* (RHS) of an assignment; this is commonly found in function *calls*:

    :::python
    def spam(a, b):
      print(a, b)
    l = [1, 2]
    spam(*l)

A function call is basically an implicit assignment of the call arguments (RHS) to the function parameters (LHS) followed by an execution of the function body.

Here, we unpack the contents of the iterable `l` (a list) and get them assigned to the parameters `a` and `b`. `[1, 2]` becomes `1` and `2` basically, equivalent to doing `foo(1, 2)`: the iterable `l` had its elements *unpacked*.

#### 'Unpacking' on LHS of assignments

The second operation, for which the term unpacking doe *not* make sense to me, is in the *Left Hand Side* (LHS) of an assignment; this is commonly found in function *definitions*:

    :::python
    def spam(*args, **kwargs):
        print(args, kwargs)
    spam(1, 2, 3, a=4, b=5)

<sub>`*args` and `**kwargs` can be seen as the LHS of the implicit assignment
that happens with function calls.</sub>

So what's going on here? Using my great detective skills I deduce that it's pretty much the opposite operation than what we had before. Essentially `spam(1, 2, 3, a=4, b=5)` is equivalent to calling
`spam((1, 2, 3), {'a': 4, 'b': 5})`. We have *packed* the positional arguments in the iterable `*args` and the keyword arguments in the mapping `**kwargs`.

So I'll make these operations distinct by using the term **packing** for LHS stars from now on.

---

As you see, there's a couple of similarities between these: they are both found in assignments and both can use a single star and a double star to unpack/pack respectively. There are a couple of differences too of course:

  1. Positioning: Unpacking is found on the RHS of assignments, Packing on the LHS.

  2. Control: The result of packing items is set in stone by the language. There's no way to alter what the items get packed into unless you alter the Python implementation.

### Count your stars
[comment]: # (NOTE: Reread, see how it sounds.)

Before talking about Unpacking and Packing in more detail, let's get this out of the way.

*Any object that is iterable* can be used with a single star `*`. This means lists, sets, dictionaries and user defined iterables can be used with `*`.
Yes, dictionaries too; when iterated through dictionaries yield their keys. Trying to use it with an object that isn't iterable gets you shouted at. For
example, let's try and unpack an `int` into a list display:

    :::python
    >>> [*1]  # trying to unpack an int
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'int' object is not iterable

Only mappings can use the double star form though. Trying to use anything that
isn't a map with `**` gets you a well earned `TypeError`, for example:

    :::python
    >>> {**[]}
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: 'list' object is not a mapping

Don't worry about the syntax, especially if you get a `SyntaxError`. I'll explain it later.

Packing
-------

We're gonna start with packing since it's something most people have met. As previously stated, *you have no control over what the items are going to get packed into*. This is something the language defines. All you need to know for now is that it's packed into an iterable.

We'll break packing down into two cases (because functions are special):

 - Function definitions.
 - All other forms of assignment.

### Function Definitions
<sup>**Pythons: all**</sup>

This is the most common and the oldest form of Python star constructs. You'll
most commonly see them with the names `args` and `kwargs` in a function definition:

    :::python
    def spam(*args, **kwargs):
        print(args, kwargs)

The names `args` and `kwargs`, though common, are specified *by you* when defining the function. These both existed as far back as [Python 1.4][5] from what I was able to discover. **Fun fact:** using an old Python 1.0.1 I had around, `*args` works like a charm, `**kwargs` leads to a lovely  segmentation fault.

So what are these? Looking at the [appropriate section][6] in the Language Reference we find:

> If the form “`*identifier`” is present, it is initialized to a tuple receiving any excess positional parameters, defaulting to the empty tuple. If the form “`**identifier`” is present, it is initialized to a new ordered mapping receiving any excess keyword arguments, defaulting to a new empty mapping of the same type.

As you can see, the language defines what data structure is used; there's no way to change what the values get packed into. Specifically, when we call a function that has been defined with `*args` and `**kwargs`:

 - `*args`: `tuple` receiving **excess** positional arguments.
 - `**kwargs`: ordered mapping receiving **excess** keyword arguments.

So, when we call `spam` with `1, 2, 3, foo=30` we expect `1, 2, 3` to be packed into the tuple `args` while also expecting the mapping `kwargs` to have a key `foo` with the value `30`.

I've boldfaced the word excess in the quoted text because `*args` and `**kwargs` won't grab anything that can be assigned to positional or keyword parameter that has been defined for a function. For example, this new `spam_new` (woah naming conventions) function also defines a positional parameter named `spammy` and a keyword argument named `spam_key` with a default value. It then prints out everything:

    :::python
    def spam_new(spammy, *args, *, spam_key='spam', **kwargs):
      print(spammy, args, spam_key, kwargs)

Let's call it with a couple of different combinations:

    :::python
    spam_new(1, 2, 3, foo=30)                # 1 (2, 3) spam {'foo': 30}
    spam_new(1, 2, 3, foo=30, spam_key=30)   # 1 (2, 3) 30 {'foo': 30}

As you can see, in both calls, `*args` caught `(2, 3)` since `1` was assigned to the first positional parameter `spammy`. In the second call, `**kwargs` caught `foo=30` but not `spam_key=30` since `spam_key` corresponds to a keyword parameter with the same name.

Finally, some closing notes:

 1. You can only use `*args` and `**kwargs` once in a function definition. If you think about it, using them more than once is very ambiguous as to what exactly should happen.
 2. Positioning is important. `def foo(*args, b)` and `def foo(b, *args)` behave very differently. Using `def foo(*args, b)` you won't be able to supply a value for `b` (which you might be able to using the `inspect` module though I haven't tried that.)
 3. Any parameter that follows an `*args` parameter *must* be supplied as a keyword argument.

        :::python
        def foo(*args, c, d):
          """ c and d can only be passed as keyword arguments """

 This also makes sense. Any non-keyword argument would be grabbed by `*args`.

 4. If you supply a default value for a parameter before `*args` (i.e a positional parameter), all parameters that are defined after it must also have default values.

That list wasn't exhaustive but it should encompass most of what you'd need to know.

#### Other callables

I might have been using the term 'function' in the previous section but, everything I said also applies to methods and anonymous, i.e lambda, functions.

Methods are basically functions attached to objects so as you'd expect the behavior is exactly the same. If you're using `*args` just be careful with the `self` parameter. You *will* catch that too if you don't define your method with at least one positional parameter.

Lambda functions too behave the same way, all they are are functions with the difference that the executable body is comprised of a single expression.

### LHS of Assignments:
<sup>[PEP 3132 -- Extended Iterable Unpacking][4] | **Pythons: >= 3.0**</sup>

Aaand PEP 3132 came along and extended the syntax (loosened it) allowing the
star to be used in other instances of assignment. The question now becomes,
where do we have assignments? As we'll see, apart from function calls, we have
a couple more instances of implicit assignment. Let's start with the explicit
case though which is the assignment statement.

Before doing that, a side-note: you can't have `**` on the LHS of the following assignments. I'm pretty sure this is because a) assignment is a statement and not an expression and b) even if it was an expression you'd get really ugly assignment statements.

#### Assignment Statement

[Assignment statements][7] are well known to most people. We have a list of target names on the LHS of the `=` symbol and an expression on the RHS. Prior to PEP 3132 and Python 3, we couldn't really do much with the LHS: specify the names to be bound to the values and be done. After PEP 3132 we have the opportunity to use `*` to catch all values that do not have a corresponding name to be assigned to.

Using this we can easily split iterables into parts:

    :::python
    head, *rest = [20, 30, 40, 50]
    print(head, rest)  # 20 [30, 40, 50]
    *rest, tail = [20, 30, 40, 50]
    print(rest, tail)  # [20, 30, 40] 50
    head, *middle, *tail = [20, 30, 40]
    print(head, middle, tail)  # 20 [30] 40

Pretty cool. As you can probably tell by the output of the `print` calls, the
result of packing here is a `list` object. This is stated in the documentation of the assignment statement:

> If the target list contains one target prefixed with an asterisk, called a “starred” target: The object must be an iterable with at least as many items as there are targets in the target list, minus one. The first items of the iterable are assigned, from left to right, to the targets before the starred target. The final items of the iterable are assigned to the targets after the starred target. A list of the remaining items in the iterable is then assigned to the starred target (the list can be empty).

Here, *target list* refers to the LHS of the assignment and *target* refers to each of the names found in the target list; *star target* is a target prefixed by a star; he's the one we're talking about.  *object* refers to the expression on the RHS. The key sentence that clarifies what the result is is the last one:

> A list of the remaining items in the iterable is then assigned to the starred target (the list can be empty).

The list is empty when the number of items in the iterable object on the RHS is one less than the number of targets on the LHS. Values are first assigned for the non-star targets on the LHS as the quoted text states. So, for example:

    :::python
    first, second, third, *rest, final = [1, 2, 3, 4]
    print(first, second, third, rest, final)  # 1 2 3 [] 4

First `first` was assigned to `1`, then `second` to `2`; `third` was assigned to `3` and then, finally, `final` to `4`. Python then sees that no more values from the object on the RHS exist and assigns `rest` to the empty list.

So, can you do a wild and freaky conversion from tuple to list by only using the star target in the LHS of the assignment? Let's experiment:

    :::python
    *values = (1, 2, 3, 4)

    SyntaxError: starred assignment target must be in a list or tuple

That didn't go so well. So, what's the issue here? Thankfully, the syntax error is pretty illuminating: *The starred assignment target must be in a `list` or `tuple`*.. hm, ok:

    :::python
    [*values] = [1, 2, 3]  # put it in a list
    print(values)  # [1, 2, 3]
    *values, = [1, 2, 3]   # NOTE: trailing comma puts it in a tuple
    print(values)  # [1, 2, 3]

I'm not sure nor have I been able to find out why this is the way it is but, I'm confident there was a solid reason.

Before moving on, there's an additional nice feature which is a result of assignment being recursively defined. Lets say you have a list of lists and you'd like to split the first two sub-lists of this list into head-rest parts and assign the untouched sub-lists to another name. How would you go about doing it? Why you'd want to do this is another question. One obvious solution would be to just index and slice it:

    :::python
    ll = [[1, 2, 3, 4], [4, 6, 7], [22, 21], [22, 24]]
    head1, *rest1 = ll[0]  # split first
    head2, *rest2 = ll[1]  # split second
    rest = ll[2:]          # keep rest

This does the trick but StackOverflow has taught me that if you can do this in a single line (a one-liner) you get extra internet points. So, let's do just that:

    :::python
    # equivalent to the snippet above.
    (head1, *rest1), (head2, *rest2), *rest = ll

I'm not really advocating using this in assignment statements since indexing and slicing is arguably much more clear. It might be more useful in other contexts such as for loops. Either way, this just goes to show how packing can also be nested. If you want to do this for showing-off purposes then just remember that you need to match the *structure* of the iterable on the RHS in order to pack successfully on the LHS; using a very extreme example:

    :::python
    l = [[[[[[[[[[10, 10, 10]]]]]]]]]]
    [[[[[[[[[[head, *rest]]]]]]]]]] = l
    # or, using tuples instead of lists to match the structure:
    ((((((((((head, *rest),),),),),),),),),) = l

isn't that pretty? Both statements do the same thing, `head` is assigned to `10` while `rest` has a list with `[10, 10]`. `[]` or `()` can be both be used with the same effect though using `()` leads to this quirky syntax because `(a) == a`, you need to use the comma's to indicate that you have single element tuples. (Try removing the commas, you won't get a `SyntaxError` but you also won't get the 'expected' result.)

#### The for statement

For loops are another well known statement. Besides their looping abilities, what's interesting about them is that they also contain an assignment, an implicit one, but there nonetheless. `for` loops can be simplistically viewed as follows:

    :::python
    for LHS in RHS:
      # do things with LHS names

When Python executes a `for` loop it binds values from the elements of the `RHS` iterable to the names on the `LHS`. This basically means that all the things presented in the previous section apply here too:

    :::python
    for head, *rest in [[20, 30, 40, 50]]:
      print(head, tail)
    for *rest, tail in [[20, 30, 40, 50]]:
      print(rest, tail)
    for head, *middle, tail in [[20, 30, 40]]:
      print(head, middle, tail)

These all print the *same thing* their assignment statement counterparts do.

Why the extra square brackets you might be wondering? Well, for loops are based on iterables, they work by going through each element on the RHS iterable and performing an assignment to the names on the LHS. Translating them to a slightly equivalent while loop can make this operation clearer. Lets take the first `for` loop from the previous code snippet where the LHS is `head, *rest`:

    :::python
    def for_loop(RHS):
      """
      Not a strict translation of a for-loop but
      close enough to get the point across
      """
      index = 0
      while True:
        try:
          value = RHS[index]
        except IndexError as e:
          break
        # LHS
        head, *rest = value
        print(head, tail)
        index += 1

Now think about what happens when we pass in `RHS = [20, 30, 40, 50]` versus passing in `RHS = [[20, 30, 40, 50]]`. Try executing this function and see the error message.

There's some other minor differences between the RHS in for loops with those found in assignment statements but that's beyond the scope of this post. All you need to care about is that you can pack in for-loops the same way you pack in assignment statements, you just add an extra pair of brackets or a trailing comma (making it a single element tuple) to the RHS:

    :::python
    # Note extra comma in ll (why is it there?)
    for (head1, *rest1), (head2, *rest2), *rest in ll,:
        print(head1, rest1, head2, rest2, rest)

and this prints out:

    :::python
    1 [2, 3, 4] 4 [6, 7] [[22, 21], [22, 24]]

as you'd expect it to.

#### The with statement

Let me preface this by saying don't do this. I really have never seen this being done someplace in the wild and can't think of a reason why it should. Having said that, let's go ahead and abuse the `as` clause of `with` statements.

I won't go ahead and explain what exactly context managers are for, that is also a topic for another post. If you aren't really familiar with them, just skip this section and move on. Those who know and want to see something stupid being done, keep on reading.

The `with` statement offers a restricted form of assignment. I won't get into too much detail here too because explaining the difference between `expression` and `expression_list` in the context of Pythons grammar will result in too much of a sideshow. With that being said, let's create a mentally challenged context manager:

    :::python
    class SillyContext:
      def __enter__(*_, **__):
        """
        Use '_' and '__' to indicate we ignore all
        arguments passed, positional and keyword
        """
        return ['Yes,', 'It is']

      def __exit__(*_, **__):
        return True

So we have this absolutely amazing context manager that returns a list when you enter it. Marvelous. Let's now abuse the syntax:

    :::python
    with SillyContext() as [this, *is_very_stupid]:
      print(this, "".join(is_very_stupid))

Which, if you execute it, prints out `Yes, It is`; so, SO useful. The gist of what goes on here is exactly the same. We write out the names we want to keep, which is `this` here, and pack the rest in a list `is_very_stupid` which we denote by prefixing it with a star.

Anyway, that's all I've found for packing. If you stumble upon any other cases that I might have missed, don't be shy to shout them at me through electronic means.

[comment]: # (Done with packing (?) Num of times read text: 1)

Unpacking
---------

Let us now move on to unpacking. Unpacking is basically the evil twin of packing if that evil twin wasn't really so evil, just misunderstood. Sillyness aside, I wasn't able to find a PEP that introduced unpacking. Knowing that it first appeared in [call expressions][10], I was able to use my [great detective skills][8] to see that it must have appeared in Python 2.2 for the first time. That release was a pretty significant one if you take a look at [what was added][9] so, this finding isn't surprising.

As in the case of packing, we will first look at functions, specifically, calling them. Then, we'll take a look at what PEP 448 gave us for the RHS of assignments and more generally, displays. Finally, a small note about the future of unpacking.

### Function calls

So, after looking at function definitions and the packing that is done when you prefix a parameter with a single or double star, lets shift our attention to the unpacking that you can perform when you call a function. The information presented here obviously applies for methods, lambdas and generally, callables.

First, let's take a look at what the [language reference][10] says about these. Regarding `*iterable` unpacking during calls:

> If the syntax `*expression` appears in the function call, expression must evaluate to an iterable. Elements from these iterables are treated as if they were additional positional arguments. For the call `f(x1, x2, *y, x3, x4)`, if y evaluates to a sequence y1, …, yM, this is equivalent to a call with M+4 positional arguments x1, x2, y1, …, yM, x3, x4.

This is pretty straight-forward: `expression` *must* evaluate to an iterable and, what happens, is that the elements of that iterable are treated as if they were additional positional arguments; the call `f(x1, x2, *y, x3, x4)` where `y=[y1, y2, ..., yM]` for example, is equivalent to `f(x1, x2, y1, y2, ..., yM, x3, x4)`. If the expression isn't an iterable, catastrophe will befall you.

A simple example using most of the available built-in iterables:

    :::python
    def it_unpacked(a, b, c):
      print(a, b, c)
    # all equivalent to: it_unpacked(1, 2, 3)
    # 1 assigned to a, 2 to b, 3 to c.
    it_unpacked(*[1, 2, 3])  # unpack list
    it_unpacked(*(1, 2, 3))  # unpack tuple
    it_unpacked(*{1, 2, 3})  # unpack set
    d = {1:1, 2:2, 3:3}
    it_unpacked(*d)          # unpack dict

The last case is noteworthy: A dictionary is also iterable and when iterated through it yields its keys. Using `*d` is shorthand for `*d.keys()` which results in the values `1`, `2` and `3` being assigned to `a`, `b` and `c` respectively. Mappings are the only data structures that can use both `*` and `**` unpacking.

Obviously if you unpack an iterable that has more or less elements than the function expects, you get barked at:

    :::python
    it_unpacked(*[1, 2])        # missing 1 required positional arg
    it_unpacked(*[1, 2, 3, 4])  # unpacked takes 3 pos. args but got 4

Unless, of course, if you use a function that has a star `*` parameter defined. In this case, passing in *more* arguments is fine, they are simply caught by the star parameter:

    :::python
    def it_unpacked2(a, b, c, *excess_args):
      print(a, b, c, excess_args)

    l = list(range(20))
    it_unpacked2(*l)  # a is 0, b is 1, c is 2, excess_args is (3, 4, ..., 19)

That's pretty much it for `*` unpacking in function calls. This is basically `*` on the RHS of an assignment and all it does is expands the values of an iterable having them intepreted as single units instead of as part of a collection.

Moving on to `**`, the reference manual has this to say for `**mapping` unpacking:

> If the syntax `**expression` appears in the function call, expression must evaluate to a mapping, the contents of which are treated as additional keyword arguments. If a keyword is already present (as an explicit keyword argument, or from another unpacking), a `TypeError` exception is raised.

Again, straight-forward: `expression` must be a mapping and the mappings' key-value pairs are treated as additional keyword arguments to the function. The `**expression` must follow any `*expression` unpackings. Also, as noted here, if you supply a keyword argument explicitly and then provide one with the same name by unpacking a mapping you get a `TypeError`. That is:

    :::python
    def dummy(a): pass

    dummy(a=20, **{'a': 30})      # got multiple values for keyword argument 'a'
    # or, with PEP 448
    dummy(**{'a':1}, **{'a': 2})  # got multiple values for keyword argument 'a'

This does makes some sense, what value should finally be assigned for `a`? To be honest though, I wouldn't *really* mind if the behavior used in dictionary displays was used here: the final, rightmost keyword argument is used. Anyhow.

A `dict`, an `OrderedDict` or `ChainMap` from the `collections` library and any other user-defined mapping object can be used with `**` to unpack keyword arguments for a function. A couple of examples with these should illustrate the
point:

    :::python
    def kw_function(foo, bar=20, spam=30):
        print(foo, bar, spam)

    # equivalent to kw_function(foo=20)
    kw_function(**{'foo': 20})                   # 20 20 20
    # equivalent to kw_function(20, bar=1, spam=3)
    kw_function(20, **{'bar':1, 'spam':3})       # 20 1 3
    # other mapping structures
    from collections import OrderedDict, ChainMap
    od = OrderedDict([('bar', 'bar')])
    # chain map is initialized by other mappings
    cm = ChainMap(od, {'spam': 'spam'})
    # equivalent to kw_function(1, bar='bar')
    kw_function(1, **od)                         # 1 bar 30
    # equivalent to kw_function(1, bar='bar', spam='spam')
    kw_function(1, **cm)                         # 1 bar spam

As with the single star unpacking case, if you unpack a mapping that contains a key value that does not match a parameter name, you get an error unless you define your function with a `**kwargs` parameter to catch it. You can play around and do this yourself :-)

#### Unpacking multiple times
<sup>[PEP 448 -- Additional Unpacking Generalizations][11] | **Pythons: >= 3.5**</sup>

This is one of the features PEP 448 brought to the party. Basically, prior to Python 3.5 you could only have one `*` unpacking and one `**` unpacking when performing a function call. Something like this:

    :::python
    def f(*__, **__): pass

    f(*[1], *[2])
    # or
    f(**{1:1}, **{2:2})

raised a `SyntaxError`. This means that, if you have values you need to pass along to a function that are contained in two different iterables or mappings, you'd need to join these together before unpacking them. This was deemed unnecessary and rightfully so. Since Python 3.5 those calls now execute as expected.

For those interested, you can unpack as many times as you want as long as the total number of arguments supplied to the function don't exceed `255`. I know, that sucks. `255` is just too small of a number for some functions that need to do absolutely everything in the world all at once including emailing themselves to the author of Clean Code in order to haunt him with their existence.

### Unpacking in list, tuple and dict displays.
<sup>[PEP 448 -- Additional Unpacking Generalizations][11] | **Pythons: >= 3.5**</sup>

PEP 448's contributions weren't only limited to allowing multiple unpackings in function calls. The additional feature we got was being able to unpack on the RHS of assignment expressions. Well, the exact feature we got was being able to unpack inside *displays* which will be explained shortly. The distinction between RHS and LHS is a convenient one because we are in full control over what happens at the RHS. Also, you'll mostly encounter unpackings in displays at the RHS of assignments.

Moving on to displays now. [Displays are special syntax Python][13] provides in order for us to create lists, sets, dictionaries and tuples. You've probably seen these but let's enumerate them here for completeness:

 1. `[v1, v2, ..., vN]` for list displays. For example: `[1, 2, 3]`.

 2. `{v1, v2, ..., vN}` for set displays. For example: `{1, 2, 3}`

 3. `{k1:v1, k2:v2, ..., kN:vN}` for dictionary displays. For example: `{1:1, 2:2, 3:3}`. Dictionaries and sets share the same bracket form but you can tell them apart from what they contain. A series of key/value pairs creates a dictionary, a series of values creates a set.

 4. `v1, v2, v3` or, optionally, `(v1, v2, v3)` for tuple displays. For example: `1, 2, 3` or `(1, 2, 3)`. Parentheses do not create tuples, commas do. This can be seen by checking the type of the variable `a` after the assignment `a = 1,`.

Displays also have a second flavor called *comprehensions* but these were not altered with PEP 448; see the **Future** section of this post for a bit more on them.

Moving on, what PEP 448 gave us with displays, is the ability to unpack *inside* them. Say you have a list `l1` with a couple of elements and another list `l2` with some other elements. What you would usually do if you wanted to add these together (in an eager way -- I'm looking at you person who is thinking of `itertools`) is:

    :::python
    l3 = l1 + l2

What you can now magically do in order to join these is just unpack in a list display:

    :::python
    l3 = [*l1, *l2]

and this does get some points because it does execute faster than its counterpart and it's also a bit more clear what is going on: we know both `l1` and `l2` are iterable objects and that we want a list with their elements.

What sets it apart, though, is seen in the case where you have one iterable of type `A` (say, a list) and another of type `B` (say, a set). In this case, using `+` blows up because you're trying to add two objects of different types. Unpacking works just fine though because all it cares about is if the objects in question are iterable. For example:

    :::python
    l = [1, 2, 3]
    s = {4, 5, 6}
    l3 = l + s      # TypeError, hope you enjoy it
    l3 = [*l, *s]   # [1, 2, 3, 4, 5, 6]

So you can basically unpack any object as long as *it supports iteration*.

Depending on the type of brackets you use (or their absence) you get different objects back. As seen previously, using `[]` results in a list object. As you'd expect, for sets, the curly brackets `{}` are used. Finally, tuples are created if you don't use `[]` or `{}`. For example:

    :::python
    l = [1, 2, 3, 4]
    l1 = [*l]  # list (shallow copy of list l)
    s1 = {*l}  # set  (filter out duplicates)
    t1 = *l,   # tuple (w/o parentheses)
    t2 = (*l,) # tuple (with parentheses)

Remember the fourth line (`t1 = *l,`) because it generally confuses people. A single trailing comma will create a tuple which you then unpack *into*. The result is `(1, 2, 3, 4)` which is then assigned to `t1`.

What about `t = *1,`? Any idea what this might do? If you guessed a `TypeError` then congrats, hope you're happy. This is one of the cases where you need to use parentheses to group things because `*` is applied to `1` and not `1,` so:

    :::python
    t = *(1,)

Which is also an error. What's missing here? Why, an extra comma! `*(1,)` on its own is *not* a display. A display needs to use `[]` or `{}` or commas, you unpack *in* displays. The following all will work:

    :::python
    t = [*(1,)]  # list  [1]
    t = {*(1,)}  # set   {1}
    t = *(1,),   # tuple (1,)

Finally, let's talk about dictionary displays. Like we previously talked, when it comes to using the double star you'll need to provide a mapping. Anything else simply fails and makes you feel bad. As you'd expect, all this does is add the key/value pairs from the unpacked dictionary into the new dictionary:

    :::python
    d = {1: 1, 2: 2}
    d1 = {3:3, **d}
    print(d1)   # {3: 3, 1: 1, 2: 2}

You can, of course, unpack as many mappings as you'd like. If there's one or more keys with the same hash value the rightmost key will be retained:

    :::python
    d = {1: 1, 2: 2}
    d1 = {1: 2, **d}         # 1:2 gets replaced
    d2 = {**d, **d1, 2: 3}   # 1:2 and 2:2 get replaced.

And that's basically it for dictionaries; once you get the gist of `*` they are really a logical equivalent.

### Future

While discussing PEP 448, the question of unpacking in comprehensions was brought up. That is, should the language allow this to be done:

    :::python
    l = [[*range(10)], [*range(10)]]
    l2 = [*subl for subl in l]

If you execute this with Pythons <= 3.7 (at the time of writing), you'll find out that no, this can't be done. A `SyntaxError` telling you off is seen instead. If you need a bit of detail you can take a look at [this answer][12] I gave on Stack Overflow.

Take note that, as I point out in that answer, this feature has not been ruled out for future Pythons. It's something we might see later on when it's clarified what unpacking in comprehensions should mean.

---

### Check it

This is an easy way to see if you've understood what goes on. Take a look at the snippet and try and describe what happens in each of these cases.

    :::python
    it = [*range(10)]
    *elements, = it
    elements2 = *it,

Before executing see if you can correctly identify what the resulting types of `elements` will be.

[comment]: # (###### LINKS ######)

[1]: https://www.python.org/dev/peps/pep-3102/
[2]: https://docs.python.org/3/library/stdtypes.html#iterator-types
[3]: https://docs.python.org/3/reference/datamodel.html#the-standard-type-hierarchy
[4]: https://www.python.org/dev/peps/pep-3132/
[5]: https://docs.python.org/release/1.4/ref/ref7.html#REF27502
[6]: https://docs.python.org/3/reference/compound_stmts.html#function-definitions
[7]: https://docs.python.org/3/reference/simple_stmts.html#assignment-statements
[8]: https://www.python.org/doc/versions/
[9]: https://www.python.org/dev/peps/pep-0251/#new-features-for-python-2-2
[10]: https://docs.python.org/3/reference/expressions.html#calls
[11]: https://www.python.org/dev/peps/pep-0448/
[12]: https://stackoverflow.com/a/41251957/4952130
[13]: https://docs.python.org/3/reference/expressions.html#displays-for-lists-sets-and-dictionaries
[14]: https://docs.python.org/3/glossary.html
