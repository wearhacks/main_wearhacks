[![Stories in Ready](https://badge.waffle.io/wearhacks/main_wearhacks.png?label=ready&title=Ready)](https://waffle.io/wearhacks/main_wearhacks)
# Wearhacks HQ Website
# Installation

## Requirements

* `pip` - instructions [here](https://pip.pypa.io/en/latest/installing.html)
* `virtualenvwrapper` - instructions [here](https://virtualenvwrapper.readthedocs.org/en/latest/install.html)
* `npm` - instructions [here](https://docs.npmjs.com/getting-started/installing-node)

## Quick setup


```bash
$ mkvirtualenv main_wearhacks
$ workon main_wearhacks
(main_wearhacks) $ pip install -r requirements.txt
(main_wearhacks) $ bower install
(main_wearhacks) $ cp main_wearhacks/settings/example_private_settings.py main_wearhacks/settings/private.py
(main_wearhacks) $ python manage.py makemigrations
(main_wearhacks) $ python manage.py migrate
(main_wearhacks) $ python manage.py generate_registrations 3
(main_wearhacks) $ python manage.py runserver
```

Now, open <http://127.0.0.1:8000/>.

## Usage

* To run on [localhost](http://127.0.0.1:8000/):

    ```bash
    $ workon wearhacks-website
    (wearhacks-website) $ python manage.py runserver
    ```
    
