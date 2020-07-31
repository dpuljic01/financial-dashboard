# Masters Thesis - Financial Dashboard

Insert some description here :)


# Backend

## Project setup

```
pip install -r requirements.txt
```

## Run
```
flask run

or

python manage.py runserver
```

# Frontend

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).


# Heroku

* Set environmental variables (change `SECRET_KEY` value)

    ```bash
    heroku config:set SECRET_KEY=not-so-secret
    heroku config:set FLASK_APP=autoapp.py
    ```

* Deploy on Heroku by pushing to the `heroku` branch or some other branch you created

    ```bash
    git push <heroku|staging|production> master
    ```
  
* Running the app

    - *locally* -> `python manage.py runserver`
    - *staging* -> `heroku run python manage.py runserver --app financial-dashboard-stage`
    - *production* -> `heroku run python manage.py runserver --app financial-dashboard-prod`

* Create user manually
    - `heroku run python manage.py create_user --app app_name`
