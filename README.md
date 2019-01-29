ThirdLove Machine Learning Engineer Interview Exam
==================================================

This README contains all the information relevant to the interview process and
exam given at ThirdLove.

Section 1 Answers
-----------------

Please refer to the file `exam/SECTION1.txt` in order to check the answers to
the questions of Section 1.


Application README
------------------

### Description of the application

The selected project is a very simple algorithm for recommending movies
according to some metadata from the user: age, gender and occupation (from a
list of possible occupations).

For the purpose of this exam, the model trained for the task is not thoroughly
optimized, and is limited to the list of movies given by the dataset [movielens
ml-100k](http://files.grouplens.org/datasets/movielens/ml-100k/).

For the model I used a simple random forest regression algorithm trained with
the previously mentioned dataset that, given a list of user metadata and a movie
from the list tries to guess the rating the user would give to the movie. Based
on that, the API should retrieve a list of the top X movie recommendations for
that user.

### Design of the API

The API's specification is the following:

| Method   | URL               | Parameters                                                                | Response                                                                                                                        |
| -------- | ----------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `GET`    | `/`               |                                                                           | 200 - Welcome message                                                                                                           |
| `GET`    | `/protected`      |                                                                           | 200 - `{"message": "Protected"}` ; 401 - Unauthenticated session                                                                |
| `POST`   | `/api/login`      | `{"session_password": string}`                                            | 200 - `{"access_token": string}` ; 400 - Missing password ; 401 - Invalid password                                              |
| `POST`   | `/api/recommend`  | `{"age": int, "gender": string, "occupation": string , "max_recs"?: int}` | 200 - `{"recommendations": list of string}` ; 400 - Invalid age, gender, occupation or max_recs ; 401 - Unauthenticated session |

This API is quite simple as the main purpose is just to serve as an interface
for the served model, which is a simple one as well. There are 4 resources
available.

The first two URIs presented in the table are there for testing purposes. The
first is a basic test to see the application is effectively working.  The
second URI is only accessible after logging into the application, thus it is 
useful to test if the JWT Token Authentication is correctly working.

The third resource: `/api/login` is needed to authenticate the session, with
the password given when running the server (check section **Running the
application**).  It expects the `session_password` as parameter and returns the
`access_token`. 

Finally, the last resource: `/api/recommend` is the key resource for this
application, as is the one that effectively does the recommendation based on
user metadata. It takes three obligatory parameters and an optional parameter:

1. `age`: The age of the user. Must be a valid integer.
2. `gender`: The gender of the user. Must be one of the following:
    - `M`: Male.
    - `F`: Female.
    - `O`: Other.
3. `occupation`: The occupation of the user.
    - `administrator`
    - `artist`
    - `doctor`
    - `educator`
    - `engineer`
    - `entertainment`
    - `executive`
    - `healthcare`
    - `homemaker`
    - `lawyer`
    - `librarian`
    - `marketing`
    - `none`
    - `other`
    - `programmer`
    - `retired`
    - `salesman`
    - `scientist`
    - `student`
    - `technician`
    - `writer`
4. `max_recs`: Optional. Integer with the maximum number of movies to retrieve. 
    Defaults to 10.

Given those, it will retrieve a list of movie titles sorted by the model
scores. Once again, this model is not thoroughly optimized, so the titles may
not reflect the best performance available.

#### Note on the API implementation

This API structure is abstract enough to be almost model independent. However,
for this particular case, I decided it was simpler to let the API do some
minimal pre-processing work, thus, it will not work with any scikit-learn
model. In any case, as long as the model follows some kind of pattern, the API
could be easily adapted to a new model (e.g. if the model was trained with a
library other than scikit-learn, it would be easy enough to just get the
parameters and replicate those on a scikit-learn model and use in this API, or
just plug the model from another library into the `/api/recommend` view).

### Running the application

#### Running locally

To run the application locally first you need to create a [virtual
environment](https://virtualenv.pypa.io/en/latest/), and install the
requirements with:

    pip install -r requirements.txt

Then run the application with the following command:

    ML_MODEL_PATH=path/to/model.pkl SESSION_PASSWORD=test python ./main.py --port 5000 --debug

Where `path/to/model.pkl` must be the path to the pickle file with the model
and `SESSION_PASSWORD` is the password needed to access the service.

#### Running the application on Docker

To run the application you need [to install docker](https://docs.docker.com/install/).

Build the image with the following command:

    docker build -t <image_name> .

Instantiate the image in a container with the following command:

    docker run -d --rm -p 5000:80 -v path/to/model/dir:/model -e ML_MODEL_PATH="/model/model.pkl" -e SESSION_PASSWORD="test" --name <container_name> <image_name>

Where `path/to/model/dir` is the path tha holds the file `model.pkl`.

#### Testing the application

##### Manual test

Manual test of the application can be done via the cURL command. First you need
to authenticate to get an access token:

    curl -X POST -H "Content-type: application/json" -d '{"session_password": "test"}' http://0.0.0.0:5000/api/login

This will return an `access_token` that you need in order to fetch for
recommendations.  Once you have the token, let's assume you store it in a
variable `TOKEN`, you can retrieve recommendations using the following command:

    curl -X POST -H "Content-type: application/json" -H "Authorization: Bearer ${TOKEN}" -d '{"age": 30, "gender": "M", "occupation": "programmer"}' http://0.0.0.0:5000/api/recommend
    
##### Unit testing

The application can be tested locally with the following command (provided the
Python environment was correctly set):

    pytest

In case of a Docker container, the image is tested while being built. But, it
can be tested on a running container as well with the following command:

    docker exec -it <container_name> pytest
    
##### Troubleshoot while running the model on Docker

The image will be built and tested on build. If the tests fails, the image
might be dangling, check there's no container of the image with the following
command:

    docker ps -a

If there is a container remove it with:

    docker rm <container_id>
    
Finally, remove the dangling image with the following command:

    docker rmi $(docker images --filter "dangling=true" -q --no-trunc)

Check (and correct) the erroneous tests and build and run the image again.
