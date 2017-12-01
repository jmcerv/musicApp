# musicApp

## How to set this on your system

First go to a specific location in your console to store the app localy and clone the repo:

```git clone git@github.com:jmcerv/musicApp.git```

Then, on projects root, create a `.env` and copy the variables from the `.env.example` file.
Fill each variable with the proper data so you can set up your DataBase.
For now, the project is directed to Postgresql. If you want to change, see how to in the [Django docs](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-DATABASES)

After all this is done, you can start the server locally with:
`python manage.py runserver`

## Web App
On this app you can add user and songs. Each of them have their own section.

When adding a song, you can choose a user who likes it, or not. If you just want to add a song, you can add it to a user's favorite list later at the user page.

When searching for new songs, the search bar will autocomplete has you input letters.

## API REST

This app has a API Rest that allows the input of users and songs through a `POST` request. You can algo retrieve user and song information through a `GET`.

For this i recomend the usage of [Postman](https://www.getpostman.com/).

### GET

#### Users
[Imgur](https://i.imgur.com/ptr2XAz.png)
#### Songs
[Imgur](https://i.imgur.com/apg7Vu6.png)

### POST

### Users
[Imgur](https://i.imgur.com/5ByFlfl.png)
### Songs
[Imgur](https://i.imgur.com/TTyzzxo.png)

The `POST` song request has this specific characteristics:
* The `user` field is not mandatory, but if you want to conenct a user to his favorite song, you must put his `id`
* The app has a `JSON Parser` that can filter through the key value names. If you write `title_name` instead of `title`, the api will still accept the input
