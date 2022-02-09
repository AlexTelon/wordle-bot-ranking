# What is this?

I think it will be a webserver serving a REST enpoint where some of my friends can compete with bots.

Should have a highscore also I guess..

Using english source of words. Tried swedish first but åäö was a pain to get right for me, and I guess for bots that would talk to this api as well. So lets skip that and keep to english ascii letters and let everyone focus on the fun stuff.

Using https://github.com/AllValley/WordleDictionary/blob/main/wordle_solutions.txt as a source.


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
curl http://localhost:5000/leroy -d "guess=crane" -X PUT

# See your results
curl http://localhost:5000/users/leroy
# Or visit http://localhost:5000/users/leroy in your browser.

# Visit http://localhost:5000/leaderboard for the current leaderboard!
```

# TODO
 * Dont allow to leaderboard unless n > 100?