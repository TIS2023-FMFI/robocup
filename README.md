# robocup
Prihlasovanie účastníkov na RoboCup Junior Slovensko


## Django structure
```
robocup/robocup-reg/  (env files, docker, etc)  
└── web/  (django app main settings, urls, etc)
    ├── registration/   (folder of a module)
    │   ├── migrations/	(database migrations)
    │   ├── templates/	(static templates)
    │   ├── urls.py
    │   └── views.py
    ├── another_module/
    │   ├── migrations/
    │   ├── templates/
    │   ├── urls.py
    │   └── views.py
    ├── settings.py
    └── urls.py
```

### What do you need to contribute to the codebase
#### Set-up pipenv
**Python 3.10 is necessary**
Open project in pycharm and create a proper pipenv interpreter (https://www.jetbrains.com/help/pycharm/pipenv.html#pipenv-existing-project)
#### Set-up pre-commit
`pip install pre-commit`

`cd robocup-reg`

`pre-commit install`

and then

`git add . [or particular files]`

`git commit -m "your message"`

and repeat :) 

## Running the project
Project can be run failry easily with the use of docker compose. You can get docker with all the components [here](https://docs.docker.com/get-docker/).
1. Clone the repository
2. Fill the `.env` file with your environmental variables.
3. run `docker compose build`
4. run `docker compose up -d`

Hooray! You have successfully deployed your own instance of robocup registration!
