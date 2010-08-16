from textwrap import dedent
from setuptools import setup

setup(
        name = "lojbantools",
        version = "0.2.2",

        # metadata for PYPI
        author = "Timo Paulssen",
        author_email = "timo+lojbantools@wakelift.de",
        description = "This package offers access to a bunch of lojban tools.",
        license = "BSD",
        download_url = "http://wakelift.de/lojban/software/python/lojbantools-0.2.2.tar.gz",

        py_modules = ["camxes"],

        classifiers = [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Text Processing :: Linguistic", # this *is* correct, yeah?
        ],
        long_description = dedent("""\
            ============
            Lojban Tools
            ============

            This library most notably wraps camxes, a lojban parser generated by Rats!
            as a java jarfile.
            It also wraps vlatai from the jbofihe package, which does morphological
            analysis of lojban words.
            The third thing it wraps is makfa, which is a word lookup tool.

            Additional Dependencies
            -----------------------

            Since camxes is a java file, you need a **Java** virtual machine or something
            else that lets you run jarfiles. In addition to that, you also need the
            **jbofihe** package to get vlatai for morphological analysis and **makfa** for
            selma'o lookup (and more in the future).""")
)
