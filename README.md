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
Open project in pycharm and create a proper pipenv interpreter (https://www.jetbrains.com/help/pycharm/pipenv.html#pipenv-existing-project)
#### Set-up pre-commit
`pip install pre-commit`

`cd robocup-reg`

`pre-commit install`

and then

`git add . [or particular files]`

`git commit -m "your message"`

and repeat :) 
