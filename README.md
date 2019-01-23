ThirdLove Machine Learning Engineer Interview Exam
==================================================

This README contains all the information relevant to the interview process and
exam given at ThirdLove.

Section 1
---------

Please refer to the file SECTION1.txt in order to check the answers to the
exam's questions.


Section 2
---------

### Design of the API 

The selected project is a very simple algorithm for recommending movies
according to some metadata from the user: age, gender and occupation (from a
list of possible occupations).

For the purpose of this exam, the model trained for the task is not thoroughly
optimized, and is limited to the list of movies given by the dataset [movielens
ml-100k](http://files.grouplens.org/datasets/movielens/ml-100k/).

For the model I used a simple linear regression algorithm trained with the
previously mentioned dataset that, given a list of user metadata and a movie
from the list tries to guess the rating the user would give to the movie. Based
on that, the API should retrieve a list of the top X movie recommendations for
that user.

The API's specification is the following:

| Method | URL                     | Parameters                                                                                                                                                                                                                                    | Response                                                                                          |
| ------ | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| POST   | /api/authenticate       | {"key": string}                                                                                                                                                                                                                               | 200 - Authentication token   ; 401 - Wrong key                                                    |
| POST   | /api/recommend          | {"age": int, "gender": M|F|O, "occupation": administrator|artist|doctor|educator|engineer|entertainment|executive|healthcare|homemaker|lawyer|librarian|marketing|none|other|programmer|retired|salesman|scientist|student|technician|writer} | 200 - [List of movie titles] ; 400 - Invalid gender or occupation ; 401 - Unauthenticated session |


### Deployment pipeline for machine learning cycle

The idea behind this pipeline is to merge the traditional ci/cd pipeline for
development and add a layer to setup and check the new models are working
before deployment.

In this case, the idea of a model correctly "working" means that the API has to
pass the unit tests assigned to it plus that the model should be tested against
some known baseline and check that there was not any accuracy lost in the
deployment process.

The best solution I came accross while building this pipeline was the use of a
Docker image that would ensure the environment compatibility with the one given
by the model, thus the developtment cycle would follow this pattern:

- Introduce the changes to the code or the new model.
- Build a docker image based on these changes.
- Run traditional integration and unit tests over the new model built.
- Run accuracy tests over the model and some given test data.

The workflow can be pictured in the following image:

![Deployment Workflow](deployment-flow.png "Deployment Workflow")

