# robocup
Prihlasovanie účastníkov na RoboCup Junior Slovensko



## Django structure
robocup/web/  (env files, docker, etc)  
└── web/  (django app main settings, urls, etc)
    ├── registration/   (folder of a module)
    │   ├── migrations
    │   ├── templates
    │   ├── urls.py
    │   └── views.py
    ├── another_module/
    │   ├── migrations
    │   ├── templates
    │   ├── urls.py
    │   └── views.py
    ├── settings.py
    └── urls.py
