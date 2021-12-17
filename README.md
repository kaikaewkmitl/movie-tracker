# Movie Tracker

A GUI program built using tkinter. Allows user to conveniently keep track of the movies they've watched.

KMITL's Introduction To Computers And Programming project by Mahnun Saratunti (64011456)

All data related to movies are provided by [The Movie Database (TMDb) API](https://developers.themoviedb.org/3)

## Install

```
git clone https://github.com/kaikaewkmitl/movie-tracker.git
cd movie-tracker
pip install -r requirements.txt
python3 main.py
```

## Features

* Displays a list of trending movies on the program’s Main Page.
* Users can search for a specific movies via search bar.
* All information related to movie is fetched from TMDb API.
* Users can view information of a specific movie. The movie's information includes:
  * movie's overview
  * poster
  * genres
  * rating
  * release date
  * etc.
* Basic user authentication. Users' data are stored in Heroku Postgres (SQL database managed by Heroku).
* The users' password are encrypted using Python's bcrypt library.
* After login, users have a freedom the add movies to their 'watech list' or 'will-watch list'.
* Users can view thier list on User List Page, they can view all movies, or filter down to just 'watched list' or 'will-watch list'.
* Users can also sort their list by movies' name, rating.
* Toggle between dark and light theme.

## Previews

Main Page

<img src="./images/main_page.png" alt="drawing" width="500"/>

Login Page

<img src="./images/login_page.png" alt="drawing" width="500"/>

Signup Page

<img src="./images/signup_page.png" alt="drawing" width="500"/>

Movie Information Page

<img src="./images/movie_info_page.png" alt="drawing" width="500"/>

User's Movie List Page

<img src="./images/user_list_page.png" alt="drawing" width="500"/>

Searching For Movies

<img src="./images/main_page_searched.png" alt="drawing" width="500"/>

Enable Dark Theme

<img src="./images/main_page_dark.png" alt="drawing" width="500"/>

## Credits

<a href="https://developers.themoviedb.org/3">
<img src="https://www.themoviedb.org/assets/2/v4/logos/v2/blue_square_1-5bdc75aaebeb75dc7ae79426ddd9be3b2be1e342510f8202baf6bffa71d7f5c4.svg" width=200>
</a>
