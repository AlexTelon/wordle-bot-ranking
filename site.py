from flask import Flask, request
from flask_restful import Resource, Api
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from statistics import mean
import shelve

import wordle

app = Flask(__name__)
api = Api(app)

@dataclass
class UserData():
    # Name of the user.
    user_name: str
    # The same user may attempt different runs. This indicate the run number.
    running_count: int = 1

    # Guesses on the current word
    guesses: List[str] = field(default_factory=list)

    # The guesses made on all previous words.
    results: List[Tuple[str, ...]] = field(default_factory=list)

    def __post_init__(self):
        # The current word that you need to guess on.
        self.correct = wordle.next_word(self.user_name, self.running_count, "")

    def guess(self, word):
        self.guesses.append(word)
        if word == self.correct:
            self.results.append(tuple(self.guesses))
            self.correct = wordle.next_word(self.user_name, self.running_count, self.correct)
            self.guesses = []
            return True
        return False

    def hint(self, word):
        result = []
        for a,b in zip(word, self.correct):
            if a == b:
                result.append('green')
            elif a in self.correct:
                result.append('yellow')
            else:
                result.append('gray')
        return result

    def average(self):
        data = [len(r) for r in self.results]
        return mean(data or [-1])

    def is_done(self):
        return len(self.results) == 2


class UserManagement(Resource):
    def put(self, user_name):
        if user_name in results:
            return {'error': 'User already exists!'}, 409
        results[user_name] = UserData(user_name)

class Wordle(Resource):
    def get(self, user_name: str):
        if user_name not in results:
            return {'error': f'User {user_name} does not exist, Make a PUT request to /users/{user_name} to add it!'}, 418
        user_data = results[user_name]
        return {
            'guesses': user_data.guesses,
            'guesses_on_previous_words': user_data.results,
            'guess_counts': [len(r) for r in user_data.results],
            'average': user_data.average(),
            'done': user_data.is_done()
            }

    def put(self, user_name):
        guess = request.form['guess']
        user_data = results[user_name]
        print(f'got guess {guess} correct is {user_data.correct}')
        was_correct = user_data.guess(guess)

        result = {'correct_guess': was_correct}
        if not was_correct:
            hint = user_data.hint(guess)
            result['hint'] = hint
        return result

api.add_resource(Wordle, '/<string:user_name>')
api.add_resource(UserManagement, '/users/<string:user_name>')

if __name__ == '__main__':
    db = shelve.open('simple.db')

    # Populate results from the db.
    results: Dict[str, UserData] = {}
    results.update(db)

    app.run(debug=False)

    # TODO we should update the server more often.
    db.update(results)
    db.close()