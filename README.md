# twopassword
A super simple password manager.

**Note:** Do not use this to store your real passwords. This is a very basic password manager that uses basic security to store the passwords.

## Setting up the Project

### Requirements
The following is required to setup this project:
- `python3.6+`

### Setup
1. Clone this repository & `cd` into it.
```
# Run this command if you have ssh enabled in GitHub
git clone git@github.com:parthsharma2/twopassword.git

# Else run this command to clone the repository
git clone https://github.com/parthsharma2/twopassword.git
```

```
cd twopassword
```

2. (Optional, but *recommended*) Create a python virtual environment & activate it.
```
python3 -m venv .venv
```
```
source .venv/bin/activate
```
*Note:* To exit out of the virtual environment, run the following command: `deactivate`

3. Install python dependencies.
```
pip install -r requirements.txt
```

4. Make & apply migrations.
```
python manage.py makemigrations
```
```
python manage.py migrate
```

5. Now you are ready to run the server.
```
python manage.py runserver
```

## Tests
To run the unit tests run the following command:
```
python manage.py test
```

## Settings
This section refers to custom settings that have been added to `twopassword/settings.py`
- `FERNET_SECRET_KEY`: This is a 44 character key that is used for encrypting & decrypting passwords stored by the user. Feel free to change it & make sure to keep it safe. I suggest using [Fernet.generate_key](https://cryptography.io/en/latest/fernet/#cryptography.fernet.Fernet.generate_key) to generate this key. **Please note:** If you change the key after passwords have been added to the database, you will have to first decrypt all those added passwords using the old key & then re-encrypt them using the new key.
