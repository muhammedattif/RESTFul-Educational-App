# Description

This is an Educational application. This app is developed using Python/Django based on Django Rest Framework (RESTFul APIs).


# System requirements

* User
    * Register
    * Login
    * Search on course
* Courses
    * Has Content
        * Content may be Video or Audio
        * Description
        * Attachments
            * PDF
        * Has Privacy (public, private, give an access to a client) (Admin level)
        * Has Quiz
            * Add quiz  (Admin level)
            * Start a quiz
            * Retry
        * Add comment on Content
            * Pending  (Admin level)
            * Published  (Admin level)
        * Actions
            * Request to correct info
                * Minute - Minute
                * Scientific Evedence
            * Report a problem
        * Mark as Completed
        * Content will be tracked to be added in watch history playlist of the user in case opened it
    * Has Privacy (public, private, give an access to a client)  (Admin level)
    * Add feedback
        * Rating
        * Description
    * Add comment on Course
        * Pending  (Admin level)
        * Published  (Admin level)
    * Add to a Playlist
    * Add to Favorites
    * Has Quiz
        * Add quiz  (Admin level)
        * Start a quiz
        * Retry
    * Category
    * Course Acticity Tracking
    * Enroll a Course

# APIs Features

## Authentication

#### Based on RestFramework Token Authentication

- SignIn
- Signup
--------

## Courses

- List all Courses
- List Course Detail
- List Course's Content
- List content Detail
- List Enrolled courses
- Track Course Activity (Watched or not)
- Add Feedback to an enrolled Course
- List Course Feedbacks
- Add Comment on Course
- List Course's Comments
- Add Comment on Content
- List Content's Comments
- Get Course's Quiz
- Get Content's Quiz
- Submit Quiz's answers
- Get Quiz's results
- List Course's Attachments
- List Content's Attachments
--------

## Playlists

- Create a Playlist
- Delete a Playlist
- List all playlists
- Add content to a playlist
- Delete content from a playlist
- List playlist's Content
- List all contents in favorites
- Add content to favorite
- Remove content from favorite
- List all contents in watch history
--------


## Payment

- List all previous Enrollments of a User
--------

## Installation

All you have to do is:

1- Clone the project

2- Create Virtual environment

3- Run

```bash
$ pip install -r requirements.txt
```

4- Run

```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver
```

# APIs Examples

## Authentication

### POST /users/signin

**SignIn**

Example:
> **POST**  http://example.gov/api/users/signin

Request body:

      {
          "email_or_username": "jane.smith@example.gov",
          "password": "123",
      }
------------------------------


### POST /users/signup

**SignUp**

Example:
> **POST**  http://example.gov/api/users/signup

Request body:

      {
          "email": "jane.smith@example.gov",
          "username": "jane",
          "password": "123",
          "password2": "123",
          "user_type": "student"
      }
------------------------------

## Users

### List all enrolled courses

**GET /users/[user_id]/enrolled-courses**

Example:
> **GET** http://example.gov/api/users/[user_id]/enrolled-courses

------------------------------

### Get User Profile

**GET /users/[user_id]/profile**

Example:
> **GET** http://example.gov/api/users/[user_id]/profile

------------------------------

### Change Password

**PUT /users/change-password**

Example:
> **PUT** http://example.gov/api/users/change-password

Request body:

    {
    "old_password": "Old@123",
    "new_password": "New@123"
    }

------------------------------


### Reset Password

**POST /users/password_reset**

Example:
> **POST** http://example.gov/api/users/reset-password

Request body:

    {
    "email": [Email]
    }

------------------------------

### Reset Password Confirm

**POST /users/password_reset/confirm/**

Example:
> **POST** http://example.gov/api/users/reset-password/confirm/

Request body:

    {
    "password": [Email],
    "Token": [Token]
    }

------------------------------

## Courses

### List all courses

**GET /courses**

Example:
> **GET** http://example.gov/api/courses

------------------------------

### List of all featured courses

**GET /courses/featured**

Example:
> **GET** http://example.gov/api/courses/featured

------------------------------

### List Course Detail

**GET /courses/[course_id]**

Example:
> **GET** http://example.gov/api/courses/[course_id]

------------------------------

### List all courses

**GET /courses**

Example:
> **GET** http://example.gov/api/courses

------------------------------

### List Course's Contents

**GET /courses/[course_id]/contents**

Example:
> **GET** http://example.gov/api/courses/[course_id]/contents

------------------------------

### List Content's Detail

**GET /courses/[course_id]/contents/[content_id]**

Example:
> **GET** http://example.gov/api/courses/[course_id]/contents/[content_id]

------------------------------

### Mark Content as Read

**GET /courses/[course_id]/contents/[content_id]/mark_as_read**

Example:
> **GET** http://example.gov/api/courses/[course_id]/contents/[content_id]/mark_as_read

------------------------------

### Add Feedback

**POST /courses/[course_id]/feedbacks**

Example:
> **POST** http://example.gov/api/courses/[course_id]/feedbacks

Request body:

      {
          "rating": "[from 1 to 5]",
          "description": "Nice!"
      }

------------------------------

### List all feedbacks on a course

**GET /courses/[course_id]/feedbacks**

Example:
> **GET** http://example.gov/api/courses/[course_id]/feedbacks

------------------------------

### Add Comment to a Course

**POST /courses/[course_id]/comments**

Example:
> **POST** http://example.gov/api/courses/[course_id]/comments

Request body:

      {
          "comment_body": "Nice"
      }

------------------------------

### List all comments on a Course

**GET /courses/[course_id]/comments**

Example:
> **GET** http://example.gov/api/courses/[course_id]/comments

------------------------------

### Add Comment to a Content

**POST /courses/[course_id]/contents/[content_id]/comments**

Example:
> **POST** http://example.gov/api/courses/[course_id]/contents/[content_id]/comments

Request body:

      {
          "comment_body": "Nice"
      }

------------------------------

### List all comments on a Content

**GET /courses/[course_id]/contents/[content_id]/comments**

Example:
> **GET** http://example.gov/api/courses/[course_id]/contents/[content_id]/comments

------------------------------

### Get Course's Quiz

**GET /courses/[course_id]/quiz?retake=1**

Example:
> **GET** http://example.gov/api/courses/[course_id]/quiz?retake=1

------------------------------

### Get Content's Quiz

**GET /courses/[course_id]/contents/[content_id]/quiz?retake=0**

Example:
> **GET** http://example.gov/api/courses/[course_id]/contents/[content_id]/quiz?retake=0

------------------------------

### Submit question answer for course's quiz

**PUT /courses/[course_id]/quiz/answer**

Example:
> **PUT** http://example.gov/api/courses/[course_id]/quiz/answer

Request body:
    {
        "quiz_answers": [
            {
                "question_id": 1,
                "selected_choice_id": 4
            },
            {
                "question_id": 2,
                "selected_choice_id": 55
            }
        ]
    }

------------------------------


### Submit question answer for content's quiz

**PUT /courses/[course_id]/contents/[content_id]/quiz/answer**

Example:
> **PUT** http://example.gov/api/courses/[course_id]/contents/[content_id]/quiz/answer

Request body:

    {
        "quiz_answers": [
            {
                "question_id": 1,
                "selected_choice_id": 4
            },
            {
                "question_id": 2,
                "selected_choice_id": 55
            }
        ]
    }

------------------------------


### Get quiz result for Course

**GET /courses/[course_id]/quiz/result**

Example:
> **GET** http://example.gov/api/courses/[course_id]/quiz/result

------------------------------


### Get quiz result for Content

**GET /courses/[course_id]/contents/[content_id]/quiz/result**

Example:
> **GET** http://example.gov/api/courses/[course_id]/contents/[content_id]/quiz/result

------------------------------


### List Course's Attachments

**GET /courses/[course_id]/attachments**

Example:
> **GET** http://example.gov/api/courses/[course_id]/attachments

------------------------------

### List Content's Attachments

**GET /courses/[course_id]/contents/[content_id]/attachments**

Example:
> **GET** http://example.gov/api/courses/[course_id]/content/[content_id]/attachments

------------------------------



## Playlists


### Create a playlist

**POST /playlists**

Example:
> **POST** http://example.gov/api/playlists

Request body:

      {
          "name": "Python Vids"
      }
------------------------------

### List all playlists

**GET /playlists**

Example:
> **GET** http://example.gov/api/playlists

------------------------------

### List playlist's Contents

**GET /playlists/[playlist_id]**

Example:
> **GET** http://example.gov/api/playlists/[playlist_id]

------------------------------

### Add Content to a playlist

**PUT /playlists/[playlist_id]**

Example:
> **PUT** http://example.gov/api/playlists/[playlist_id]


Request body:

      {
          "content_id": [content_id]
      }
------------------------------

### Delete Content from a playlist

**DELETE /playlists/[playlist_id]/contents/[content_id]**

Example:
> **DELETE** http://example.gov/api/playlists/[playlist_id]/contents/[content_id]

------------------------------

### List all contents in favorites

**GET /playlists/favorites**

Example:
> **GET** http://example.gov/api/playlists/favorites

------------------------------

### Add Content to favorites

**PUT /playlists/favorites**

Example:
> **PUT** http://example.gov/api/playlists/favorites

Request body:

      {
          "content_id": [content_id]
      }

------------------------------


### Remove Content from favorites

**DELETE /playlists/favorites/[content_id]**

Example:
> **DELETE** http://example.gov/api/playlists/favorites/[content_id]

------------------------------

### List all contents in watch history

**GET /playlists/favorites/watch_history**

Example:
> **GET** http://example.gov/api/playlists/watch_history

------------------------------


## Payment


### List all previous Enrollments of a User

**GET /users/[user_id]/enrollments**

Example:
> **GET** http://example.gov/api/users/[user_id]/enrollments

------------------------------

### Enroll a free course

**POST /users/[user_id]/enrollments**

Example:
> **POST** http://example.gov/api/users/1/enrollments

Request body:

      {
          "course": [course_id]
      }

------------------------------

**Note**:

This project is built using Sqlite3 Database.

This commands is working for MacOS
