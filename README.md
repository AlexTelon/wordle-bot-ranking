# What is this?

I think it will be a webserver serving a REST enpoint where some of my friends can compete with bots.

Should have a highscore also I guess..

Usees swedish words from https://ordlig.se/static/media/words_5_v2.cb6a80dc2d4c6a7692be.txt


# how to setup

```bash
python -m venv .env
source .env/bin/activate
python -m pip install -r requirements.txt

# Only for development.
python site.py
```