Title: Hello, Pelican!
Date: 2017-7-03
Tags: Misc
Category: misc
Slug: hello-pelican
Authors: Jim Fasarakis-Hilliard
Summary: First, post! Using pelican as the static site generator for my github.io personal page. Let's see how this goes.

Granted that `stork = 'pelican'` then, the stork has arrived with my blog.
I finally got through to setting up something I like that is also Python based.
Pelican, along with a nice little theme called voce, is powering up this place.

Let's see that code-snippet:

    :::python
    class MyMeta(type):
        def __new__(cls, name, bases, namespace):
            my_fancy_new_namespace = {....}
            if '__classcell__' in namespace:
                 my_fancy_new_namespace['__classcell__'] = namespace['__classcell__']
            return super().__new__(cls, name, bases, my_fancy_new_namespace)

Some simple disassembly:

    :::python
    from dis import dis
    dis(func)
      2           0 LOAD_CONST               1 (42)
                  2 STORE_FAST               0 (a)

      3           4 LOAD_FAST                0 (a)
                  6 RETURN_VALUE
