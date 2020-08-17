
# Masters Thesis - Financial Dashboard



NOTE: this is still WIP, here is the [LIVE DEMO](https://dp-finance.herokuapp.com/) of the current progress.

<sub>PS: If it's slow when first time opening app, that's because Heroku shuts down app after 30mins of inactivity, 
so it takes a while to run it again.</sub>



## Server

  

### Project setup



```

pip install -r requirements.txt

```



### Run

```
export FLASK_APP=wsgi.py
flask run
```


or


```
python manage.py runserver
```



## Client



### Project setup

```

npm install

```



### Compiles and hot-reloads for development

```

npm start

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

heroku config:set FLASK_APP=wsgi.py
...

```



* Deploy on Heroku by pushing to the `heroku` branch or some other branch you created



```bash

git push <heroku|staging|production> master

```

* Running the app

	-  *locally* -> `python manage.py runserver`

	-  *production* -> `heroku run python manage.py runserver --app app_name`



* Create user manually (these are automatically verified, no need for email confirmation)

	-  `heroku run python manage.py create_user --app app_name`