VARD MVP
============
![start page + chat](https://github.com/Uks130322/vard_mvp/assets/101522861/04f81d59-4a76-4488-adce-157c28d1d962)

Site: https://vard.tech/  
Backend with API-endpoints (this project): https://natalietkachuk.pythonanywhere.com/api/  

Minimum viable product for collaboration feature allows teams to connect in real-time, enabling seamless data analysis and insights sharing.  
VARD provides a collaborative environment where you can easily share data, insights, and reports with your team. This fosters teamwork, ensures everyone is on the same page, and allows for effective collaboration.  
  


Requirements
---------------

- Python 3.8
- Django 4.2  

Setup
-------------

For Windows:
 ```bash
    git clone https://github.com/Uks130322/vard_mvp
    python -m venv venv
    cd vard
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py runserver
```

To create superuser (admin):
```bash
  python manage.py createsuperuser
```

For Linux:
```bash
  git clone https://github.com/Uks130322/vard_mvp
  python3.8 -m venv venv
  source venv/bin/activate
  cd vard
  pip install -r requirements.txt
  python3.8 manage.py migrate
  python3.8 manage.py runserver
```

To create superuser (admin):
```bash
  python3.8 manage.py createsuperuser
```
  
Implemented functionality
--------------
For authorizated users only  

  - Registration and authentithication
  - Uploading CSV and JSON Files from PC or by URL
  - Connection with MySQL databases
  - Sending queries to the database and receiving a response
  - Creating Chart from response data
  - Creating Dashboard with some Charts
  - Giving an Access to other Users to read, comment or edit your Files, Charts and Dashboards
  - Commenting Files, Charts and Dashboards in case having access
  - Filter by User and some others fields for datas
  - Internal Chat for all team members
  - Access to all datas for Admin
  - Sending Feedback to developers

ER diagram
--------------
https://github.com/Uks130322/vard_mvp/blob/main/ERD.jpg

Swagger
---------------
For superuser (admin) only  
  
   - https://natalietkachuk.pythonanywhere.com/swagger/  
   - or at localhost: http://127.0.0.1:8000/swagger/

Contributors
-----------
https://github.com/stds58  
https://github.com/Uks130322

Frontend
-----------
https://vard-project.vercel.app/connections  
https://github.com/MamedovShuxrat/vard-project  
Contributor https://github.com/MamedovShuxrat
