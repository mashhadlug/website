webtastic
=========

a simple website html generator written by python with extensibility in mind.

TODOs
---------

* Write documentation
* Write tests (oops!)
* Add python 3 support(?)

Usage
---------

look at the source directory for getting the idea behind Webtastic before the arrival of the Documentation. 

    $ python webtastic

The above code will read the source files in the `source` directory and will render them by the corresponding template filename. the result will be put into a new directory named `html`. to compile the static pages for a directory in your webhost (for example http://example.com/myblog/) simple run the below command:

    $ python webtastic --base-url=myblog

How It Works?
---------

Webtastic is simply made of a jinja2 `template` directory and a `source` directory. when you run, it parse every `.md` file in your source directory with corresponding template file in `template/` and writes it to `html/` directory.

a source file is consists of two part. seperating by 10 dhashes. the above part is to define variables using YAML to be used by template engine and the below part is the actual content of the page using `Markdown`. it's really simple! just look at the source files.

    ----------
    author: Mashhadlug
    title: index page's title
    layout: index
    ----------
    # This is Heading one
    
    and some paragraph.

Demo
---------

currently using Webtastic

* [Mashhadlug LUG](http://next.mashhadlug.org)

LICENSE
---------
Webtastic is licensed under GPLv3 or any later version.
