# attendance_system
School system for attendance test

Requirements:
1. Design architecture - overall picture of system with description 
2. Data flow 
3. Scalability
4. Clear requirements - state we have no parallel classes
5. Make active classes for student - possible parallel classes 
6. Internet connection falls down 


Steps how to build django app 

1. Create virtual env in your project folder
2. Install django -> pip install django==2.0.7 -this version used for project 
3. Make database connection in setting.py
4. Make admin user by -> python manage.py createsuperuser
5. Create app -> python manage.py createapp name_of_the_app
6. Make models from database -> python manage.py inspectdb > name_of_the_app/models.py
7. Make migrations with models -> python manage.py makemigrations
                               -> python manage.py migrate 
    This should create migrate file in app folder with structure of models. 
    Also models.py needs to have models form database
8. Create admin access to models -> 
    /admin folder 
    from .models import name_of_the_model 
    admin.site.register(name_of_the_model)
9. See admin site to see the models. This way new data can be inserted into the database
10. 
