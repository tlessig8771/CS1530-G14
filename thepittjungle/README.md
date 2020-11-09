To run in Windows
1. cd thepittjungle
2. py -3 -m venv venv
3. venv\Scripts\activate
4. pip install -r requirements.txt -> do this only once. postgres must be installed
5. set FLASK_APP=pittjungle.py
6. set MAIL_USERNAME=thepittjungle
7. set MAIL_PASSWORD=CS1630Project
In order to set admin account:
set FLASKY_ADMIN=email@example.com  ==> email of the user to be set as admin
it needs to set before the admin registers as user.
8. flask deploy
9. flask run

To run in MacOS:
1. cd thepittjungle
2. python3 -m venv venv
3. . venv/bin/activate
4. pip install -r requirements.txt -> do this only once. postgres must be installed
5. export FLASK_APP=pittjungle.py
6. export MAIL_USERNAME=thepittjungle
7. export MAIL_PASSWORD=CS1630Project
export FLASKY_ADMIN=email@example.com  ==> email of the user to be set as admin
it needs to set before the admin registers as user.
8. flask deploy
9. flask run

