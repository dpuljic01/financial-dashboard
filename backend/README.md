# Masters Thesis - Financial Dashboard

Insert some description here :)


### Heroku

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

    - *locally* -> `python python manage.py runserver`
    - *staging* -> `heroku run python manage.py runserver --app financial-dashboard-stage`
    - *production* -> `heroku run python manage.py runserver --app financial-dashboard-prod`

* Create user manually
    - `heroku run python manage.py create_user --app app_name`
