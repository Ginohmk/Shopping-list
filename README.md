# API Development and Documentation Collaboration Project

## Shopping List App

This app is to enable creating and managing shopping lists. The app is developed using Django Rest Framework (DRF).

### Features

1. User Registration - User should be able to register with the follwing details:

- First name
- Last name
- Email
- Password

2. User login: User can log in with:

   - Email
   - Password

3. Email verification: users receives email notification to confirm registered email.

4. User can perform CRUD operation on the shopping list belonging to them.

## Starting

##### Prerequisite

- Note: You need to have python3.x [installed](https://www.tutorialspoint.com/how-to-install-python-in-windows) on you machine.

##### Steps

1.  Clone the project into your machine.

    ```cmd
          git clone https://github.com/Ginohmk/Shopping-list.git
    ```

2.  Navigate into the project folder.

    ```cmd
       cd Shopping-list
    ```

3.  Start your virtual environment (mac/linux and windows)

    ```cmd
      source/bin/activate
    ```

    Or for windows

    ```cmd
      \venv\Scripts\activate.bat
    ```

4.  Install project dependencies.

    ```cmd
      pip install -r requirements.txt
    ```

5.  Start server

    ```
      ./manage.py runserver
    ```

    <br />

### Folder Structure

This are the folders and files relevant to this project.

```
├── shopping_list # Project file
 ├── settings.py
 ├── urls.py
├── shop # Shopping_list app <br>
 ├── admin.py
 ├── models.py
 ├── serializers.py
 ├── services.py
 ├── urls.py
 ├── views.py
├── user # User app
 ├── admin.py
 ├── user_authentications.py # Custom authentication
 ├── models.py
 ├── user_permissions.py # Custom permision
 ├── serializers.py
 ├── services.py
 ├── urls.py
 ├── views.py
├── manage.py
├── README.md
├── requirements.txt
```

  <br />

### Backend APIs ( Live `https://kanumikec.pythonanywhere.com/` )

##### User Apis

1. Registration `/api/users/register/` (Post)

   - Payload

   ```json
   {
     "id": "string",
     "first_name": "string",
     "last_name": "string",
     "email ": "string",
     "password": "string"
   }
   ```

   - Response 200

   ```json
   {
     "id": "string",
     "first_name": "string",
     "last_name": "string",
     "email ": "string"
   }
   ```

   <br />

2. Login `/api/users/login/` (Post)

   - Payload

   ```json
   {
     "email": "string",
     "password": "string"
   }
   ```

   - Response 200
     <br />

3. Logout `/api/users/logout/` (Post)

   - Payload `None`

   - Response 200

   ```json
   {
     "message": "Logged out Successfully"
   }
   ```

   <br />

4. Me `/api/users/me/` (Get)

   - Payload `None`

   - Response 200

   ```json
   {
     "id": "string",
     "first_name": "string",
     "last_name": "string",
     "email ": "string"
   }
   ```

  <br />

5. Email verification `/api/user/verify-email/` (Post)

`Note: Verification link is sent to user and  when clicked they can verify their email`

- Payload `None`

- Response 200

   <br />

##### Shopping_list Apis

1.  Create shop `/api/shops/` (Post)

- Payload

```json
{
 "description": "string",
 "priority": int,
 "title": "string",
 "due_date": "string datetime",
 "quantity": int,
 "is_complete": boolean
}
```

- Response 200

```json
{
 "id": "uuid string",
 "description": "string",
 "priority": int,
 "title": "string",
 "due_date": "string datetime",
 "quantity": int,
 "is_complete": boolean
 "user": {
   "id": "string",
   "first_name": "string",
   "last_name": "string",
   "email": "string"
 }
}
```

  <br />

2. Get All shop `/api/shops/` (Get)

   - Response 200

   ```json
    [
      {
        "id": "uuid string",
        "description": "string",
        "priority": int,
        "title": "string",
        "due_date": "string datetime",
        "quantity": int,
        "is_complete": boolean
        "user": {
          "id": "string",
          "first_name": "string",
          "last_name": "string",
          "email": "string"
        }
      }
    ]
   ```

     <br />

3. Delete shop `/api/shops/<id: str>/` (Delete)

   - Response 204
     <br />

4. Update shop `/api/shops/<id: str>/` (Put)

- Payload

  ```json
  {
  "description": "string",
  "priority": int,
  "title": "string",
  "due_date": "string datetime",
  "quantity": int,
  "is_complete": boolean
  }
  ```

- Response 200

```json
   {
     "id": "uuid string",
     "description": "string",
     "priority": int,
     "title": "string",
     "due_date": "string datetime",
     "quantity": int,
     "is_complete": boolean
     "user": {
       "id": "string",
       "first_name": "string",
       "last_name": "string",
       "email": "string"
     }
   }
```

5. Retreive sinfle shop `/api/shops/<id: str>/` (Get)

- Response 200

```json
   {
     "id": "uuid string",
     "description": "string",
     "priority": int,
     "title": "string",
     "due_date": "string datetime",
     "quantity": int,
     "is_complete": boolean
     "user": {
       "id": "string",
       "first_name": "string",
       "last_name": "string",
       "email": "string"
     }
   }
```

<br/>
### Author

👤 **Kanu Mike**

- GitHub: [@Ginohmk](https://github.com/Ginohmk)
- Twitter: [@michotall95](https://www.twitter.com/michotall95)
- LinkedIn: [@kanumike](https://www.linkedin.com/in/mike-kanu-dev/)
- Instagram: [@savy_kanu_mike](https/instagram.com/savy_kanu_mike)
- Facebook: [@mike.kanu](https://www.facebook.com/mike.kanu)

👤 **Evan Guma**

- GitHub: [@ayera-4](https://github.com/ayera-4)

### 🤝 Contribute

Contributions, issues, and feature requests are welcome!

Feel free to check the [issues page](https://github.com/Ginohmk/online-note-book-drf/issues)

### Acknowledgement

## Show your support

Give a ⭐️ if you like this project!

## 📝 License

This project is [MIT](./MIT.md) licensed.
