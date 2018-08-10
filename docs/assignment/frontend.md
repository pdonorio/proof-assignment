
# frontend development


## registration views

We have APIs on a Flask backend to register and verify a user into our mongo database.

We need to create frontend views with `React.js`:
1. A view to login.
2. A view for a base registration form. 
3. A view to assess a verification email was sent to the email specified.
4. A view for a logged user to see his profile (which is where the user is redirected if successfull at step 1). 

1. and 2. should be looking as close as possible to  the [attached design](data/images/login_design.png). 
The design is based on google material.
The suggested library to integrate it is [material-ui](LINKTOADD)


## APIs specifications

Here's the list of API calls to interact in the above request

### login

If a user is registered and activated they can login by calling:
```bash

# default account already existing after startup up of the framework
USER=user@nomail.org
PASSWORD=test

http POST localhost:8080/auth/login email=$USER password=$PASSWORD

HTTP/1.0 200 OK
        "data": {
            "token": "..."
        }
```


### register a profile

To request a registration the flow requires the following
```bash
USER=beta@tester.me
PASSWORD=verylongpassword
NAME=test
SURNAME=beta

http POST localhost:8080/auth/profile \
    email=$USER password=$PASSWORD name=$NAME surname=$SURNAME
```

This call above tries to send an email to the specified address.
To make that work you have to ensure you have the `SMTP` configuration in place (explained in another section of the documentation).

NOTE: this is not an authenticated request.


### activation

If you now login with the current profile which is not activated, you end up with:
```bash
http POST localhost:8080/auth/login email=test@test.test password=testtest

HTTP/1.0 401 UNAUTHORIZED
            "Sorry, this account is not active"
```

So let's activate the account. You received the token via email 
(or can find it in the logs of the backend server)

```bash
http PUT localhost:8080/auth/profile/activate/$ACTIVATION_TOKEN

HTTP/1.0 200 OK
[...]
    "Response": {
        "data": "Account activated",
        "errors": null
    }
}
```

If you try to activate with a wrong token:
```bash
http PUT localhost:8080/auth/profile/activate/blabla

HTTP/1.0 400 BAD REQUEST
            "Invalid activation token"
```

