## Coding style
Please follow these coding standards while writing code for this project.

### Python style
* Follow [pep:8](https://www.python.org/dev/peps/pep-0008/) guide unless it is specified.
* The python files use 4 spaecs for indentation and HTML files use 2 spaces.
* Use underscores, not camelcase for variable, function and method names. For example: ```person.get_address()``` instead of ```person.getAddress()```.
* Use 'IntialCaps' for class names or for factory functions that return classes.
* Use single quote for strings or a double quote if the string contains a single quote.

### Imports
* User convinience imports whenever available.

  Do this:
  ```python
  from module.views import View
  ``` 
  Don't do this:
  ```python
  from module.views.generic.base import View
  ```
### Django guidelines
Please follow these guidelines while using django framework.

#### Template Style
* In Django template code, put only one space between the curly brackets and the tag contents.

    Do this:
    ```python
    {{ foo }}
    ```

    Don't do this:
    ```python
    {{foo}}
    ```
#### View Style
* In Django views, the first parameter in a view function should be called ```request```.

    Do this:
    ```python
    def my_view(request, foo):
        # ...
    ```
        
    Don't do this:
    ```python
    def my_view(req, foo):
        # ...
    ```
 
#### Model Style
* Field names should be all lowercase and use underscores instead of camelCase.

    Do this:
    ```python
    class Person(models.Model):
        first_name = models.CharField(max_length=20)
        last_name = models.CharField(max_length=40)
    ```
    
    Don't do this:
    ```python
    class Person(models.Model):
        FirstName = models.CharField(max_length=20)
        Last_Name = models.CharField(max_length=40)
    ```
 * The ``class Meta`` should appear *after* the fields are defined, with
  a single blank line separating the fields and the class definition.
    
    Do this:
    ```python
    class Person(models.Model):
        first_name = models.CharField(max_length=20)
        last_name = models.CharField(max_length=40)
        
        class Meta:
           verbose_name_plural = 'people'
    ```
    
    Don't do this:
    ```python
    class Person(models.Model):
          first_name = models.CharField(max_length=20)
          last_name = models.CharField(max_length=40)
          class Meta:
              verbose_name_plural = 'people'
    ```
   
   Don't do this:
    ```python
    class Person(models.Model):
          class Meta:
              verbose_name_plural = 'people'

          first_name = models.CharField(max_length=20)
          last_name = models.CharField(max_length=40)
    ```
* The order of model inner classes and standard methods should be as follows (noting that these are not all required).
    * All database fields
    * Custom manager attributes
    * ``class Meta``
    * ``def __str__()``
    * ``def save()``
    * ``def get_absolute_url()``
    * Any custom methods
    
* If ``choices`` is defined for a given model field, define each choice as a
  list of tuples, with an all-uppercase name as a class attribute on the model.
  
  Example
    ```python
    class MyModel(models.Model):
        DIRECTION_UP = 'U'
        DIRECTION_DOWN = 'D'
        DIRECTION_CHOICES = [
            (DIRECTION_UP, 'Up'),
            (DIRECTION_DOWN, 'Down'),
        ]
    ```

### Miscellaneous
* Remove ```import``` statements that are no longer needed.
