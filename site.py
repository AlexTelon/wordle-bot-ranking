from flask import Flask, request
from flask_restful import Resource, Api
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from statistics import mean

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
        self.generator = wordle.gen_words(self.user_name, self.running_count)

        # The current word that you need to guess on.
        self.correct = next(self.generator)

    def guess(self, word):
        self.guesses.append(word)
        if word == self.correct:
            self.results.append(tuple(self.guesses))
            self.correct = next(self.generator)
            self.guesses = []

            return True
        return False

    def average(self):
        data = [len(r) for r in self.results]
        return mean(data or [-1])

    def is_done(self):
        return len(self.results) == 2


results: Dict[str, UserData] = {}

class UserManagement(Resource):
    def put(self, user_name):
        if user_name in results:
            return {'error': 'User already exists!'}, 409
        results[user_name] = UserData(user_name)

class Wordle(Resource):
    def get(self, user_name: str):
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
        was_correct = user_data.guess(guess)

        return {user_name: f'added {guess} it was {was_correct} correct should be {user_data.correct}'}

api.add_resource(Wordle, '/<string:user_name>')
api.add_resource(UserManagement, '/users/<string:user_name>')

if __name__ == '__main__':

    # Im lazy so while we dont have persistence lets initialize with a user for me for now.
    results['altel1'] = UserData('altel1')

    app.run(debug=False)