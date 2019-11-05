## Deployment Guide for Django

* First, run a check against production settings by:
    ```shell script
    python manage.py check --deploy
    ```
  
* SECRET_KEY:
    * It must be a large random value and must be kept secret.
    * Don't use the production's key elsewhere.
    * Avoid committing it to the source control.
    * Instead of hardcoding a key in `settings.py` file,
        * Consider using it from a file:
            ```python
            with open('/etc/secret_key.txt') as f:
              SECRET_KEY = f.read().strip()
            ``` 
          
        * Consider loading it from environment variable:
            ```python
            import os
            SECRET_KEY = os.environ['SECRET_KEY']
            ``` 
* DEBUG:
    * Never enable it in production as it gives full tracebacks in browser and leaks informations about project.