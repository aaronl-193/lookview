# LookView
*(Made as a student project)*
Lookview is a self-hosted application that enables you to add and review films!
(in prototype)

Made by BINUS University Students:
1. Aaron Lawrence
2. Darren Alfian Riady
3. Khoiri Davin Nayaka
4. Muhammad Bagas Wicaksana
5. Richie Nathan Hermanto
6. Jorell Ozora Tjandranegara

### Build instructions
1. Install dependencies using `pip install -r requirements.txt`.
2. Generate migrations using `python lookview/manage.py makemigrations`.
3. Migrate changes using `python lookview/manage.py migrate`.
4. Run `python lookview/manage.py runserver` to run the server.

### Running Instructions
1. Go to the link instructed in terminal.
2. Create a super user by using `python manage.py createsuperuser`
3. Go to `http://[IP]:[PORT]/admin` to add a `SiteUser`, `Algorithm`, and `Watchlist` object to the superuser.
4. Add films in the same manner.

Consult [https://docs.djangoproject.com/en/5.2/ref/contrib/admin/] regarding the admin site management.
