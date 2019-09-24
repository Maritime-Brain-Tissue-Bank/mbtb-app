## Design Philosophies

* Overall
    * **Loose Coupling**  
        The various layers shouldn't know about each other unless absolutely necessary.
        
    * **Don't Repeat Yourself (DRY)**  
        Every distinct concept and/or piece of data should live in one, and only one, place. Redundancy is bad. Normalization is good.
        
    * **Explicit is better than implicit**  
        It means it shouldn't do too much magic unless there is a good requirement.  
        
        Do this: 
        ```python
        def make_dict(x, y):
          return {'x':x, 'y': y}
        ```
        
        Don't do this:
        ```python
        def make_dict(*args):
          x, y = args
          return dict(**locals())
        ```
    * **Consistency**  
        It applies to everything from low-level (Python code) to high-level (experience using it).
        
    * **Separe Logic from Presentation**  
        The presentation layer should't support any functionality.
        
* Database
    * **SQL Efficiency**  
        It should optimize SQL statements and use it few times as possible.
        
    * **Option to drop into raw SQL easily, when needed**  
        There should be a provision to write custom SQL statements, or just `WHERE` clauses as custom parameters.
    