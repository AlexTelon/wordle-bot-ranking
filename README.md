# What is this?

I think it will be a webserver serving a REST enpoint where some of my friends can compete with bots.

Should have a highscore also I guess..

Usees swedish words from https://ordlig.se/static/media/words_5_v2.cb6a80dc2d4c6a7692be.txt


# How to setup server

```bash
python -m venv .env
source .env/bin/activate
python -m pip install -r requirements.txt

# Only for development.
python site.py
```

# How to communicate with server

```bash
# Add user leroy.
curl http://localhost:5000/users/leroy -X PUT

# Make a first guess for the user leroy.
curl http://localhost:5000/leroy -d "guess=roman" -X PUT
```