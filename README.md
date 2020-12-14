# DjangoEcommerce
Online gadget's shop with Django 3 + Bootstrap 4

---
Project setup (Windows):
1) `git clone https://github.com/IncomprehensibleGuy/DjangoEcommerce.git`
2) `cd DjangoEcommerce`
3) `python -m venv venv`
4) `cd venv/Scripts`
5) `activate`
6) `cd ../..`

Project setup (Linux / MacOS):
1) `git clone https://github.com/IncomprehensibleGuy/DjangoEcommerce.git`
2) `ls DjangoEcommerce`
3) `python -m venv venv`
4) `source venv/bin/activate`

* `pip install -r requirements.txt`
* `python manage.py migrate`
* `python manage.py runserver`

* Install redis and start server
* In 'base/' directory create file 'private_date.py' with string constants 'email_user' & 'email_password'
* In new terminal: `celery -A base worker -l info`
---

### ToDo
...
- [x] Отправка информации о заказе на почту при оплате (Celery+Redis)
- [ ] Регистрация по email с отправкой кода подтверждения на почту
- [ ] Регистрация через google аккаунт
- [ ] Генерация pdf с деталями заказа для отправки на email
- [ ] Добавить Vue.js: динамическая валидация форм
- [ ] Страница истории заказов
- [ ] Страница изменения аккаунта
