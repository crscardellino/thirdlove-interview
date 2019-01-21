ThirdLove Machine Learning Engineer Interview Exam
==================================================

This file contains the answers to the questions asked in the ThirdLove interview
exam.

Questions
---------

1. What is the difference between a Python tuple, list, and dictionary? Are they
sorted?

The three of them are collections of elements. Tuple a lists are a collection of
sorted elements given by the position they hold. The difference between them is
that lists are mutable whilst a tuples are not (i.e. once created their content
cannot be changed in place, only by creating a new tuple). A dictionary is an
unordered collection of items that maps a set of keys to a set of values.

2. What are the benefits of writing multi-threaded programs?

The benefits of multithreading can be summarised in four aspects:
  a. Responsiveness: A program can execute multiple actions even if part of it
      blocked or slowed down by a lengthy and time consuming operation, thus
      making it more responsive to the user (less waiting time).
  b. Resource sharing: Threads, unlike process (i.e. the ones spawned by
      parallel computations), share the memory and resources of the process
      they belong.
  c. Economy: As the resources are shared between threads, this makes for a
      more efficient way of working since process creation requires memory and
      resources allocation which is costly.
  d. Scalability: Multithreading can be done in one or multiple processors,
      thus it benefits from multiprocessors architectures. That means that
      multithreading on multicore CPUs machines increases parallelism.

3. What is a decorator?

Decorators are an object-oriented programming pattern, where the key idea is to
dinamically alter the functionality of a function, method or class without
having to modify the source code of the function being decorated.  In Python
language, these are a syntax sugar useful to modify a function or method.

4. What is PEP8?

PEP8 is a coding style convention for the Python programming language in order
to make the syntax more clear to read.

5. What are the differences between iterator, generator, iterable, callable?

An iterator is a factory of values, that is something you can iterate over it,
i.e. get a next element in a collection or stream of data.

A generator is a special kind of iterator (i.e. all generator is an iterator
but this is not true the other way around) that produces values in a _lazy_
fashion. That is, the values are produced as they are required by a _consumer_
(e.g. some algorithm iterating over the generated values). As it is lazy, thus
does not load everything into memory, a generator is a good way to retrieve
arbitrary streams of data (e.g. large files).

An iterable is any object that can return an iterator with the purpose of
returning all the iterator's elements. Generally, a collection of elements
(e.g. a tuple or a list) are iterables.

A callable is any object that can be _called_, that is it has a `__call__`
method (e.g. being an instance of a class with such method) or is a
function/method itself. Call, in this case, means you can retrieve a value if
you use the correct syntax (i.e. with the parenthesis).

6. How would you test an API?. What testing tools have you used?

There are two ways to test a REST API:
  a. Manually: Although impractical, sometimes it is beneficial in order to
      understand how an API works. In this case there are many different tools,
      although I know [Postman](https://www.getpostman.com/).
  b. Unit testing: This is an automated way of testing an API, and is an
      excellent way to check that everything is in order when new features are
      added to the API.  For this, there are different tools depending on the
      framework using.  Python, by itself has the `unittest` library, which,
      combined with some library like
      [`request`](http://www.python-requests.org/) can create a simple but
      powerful unittest scheme (this is the one I know).  Sometimes the
      framework has a tool for testing written like is the case for
      [Django](https://docs.djangoproject.com/en/2.1/topics/testing/) (I am
      also familiar with this one) and some other apps require an extra package
      like is the case for [Flask](http://flask.pocoo.org/docs/1.0/testing/)
      which requires [pytest](https://www.pytest.org/) (not familiar with this
      one, but it does not look so different from the usual unit testing
      pattern.

7. What are the differences between Flask and Django?

While both of them are frameworks, Flask is considered a _microframework_, i.e.
is more oriented in building small applications that sometimes have only one
clearly defined task (e.g. microservices that serves as API interfaces to a
Machine Learning algorithm). Also, Flask is better suited to write web APIs as
it is defined like so, while Django needs some [extra
packages](https://www.django-rest-framework.org/) in order to achieve this.
Django is better as a full featured framework.

8. What common package have you used with Flask?

- gunicorn: although is not exclusive to flask, is the better solution to serve
  a Flask application.
- flask-pewee: now is only in manteinance mode, but it provided an integration
  with pewee orm.
- Flask-Login: User session management.
- Flask-Oauthlib: Support for OAuth integration.

9. Where do you save sensitive data, i.e. secret keys?

There are a couple of ways to save it:

  a. One is in a file in the production server only, that will be only
      accessible by the user that needs it (in this case user, can be a user
      specific to an application like in PostgreSQL).
  b. The other possibility is in an _environment variable_.

10. Could you name some cloud technologies that you had the chance of use?

I don't really have much experience on this area. Most of the work I have done
is directly on dedicated servers. But I have use Heroku to deploy a couple of
toy examples.

11. What are the differences between Docker and Docker Compose?<Paste>

Docker is a _containerization_ tool that provides operating system level
virtualization. Docker compose is a wrapper around the docker CLI that is used
mostly to manage multiple docker containers more easily than what the docker
native CLI does.

12. Did you have the chance to use CI/CD tool? If yes, name one example setup.

Not really. I know of jenkins, but never had the chance to setup it by myself.