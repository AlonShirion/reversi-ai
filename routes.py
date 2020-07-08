from ast import literal_eval
from flask import Flask, json
from flask import request
from werkzeug.exceptions import HTTPException

import othello

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

api = Flask(__name__)


def get_choice(choice, options):
    if choice in options:
        return options[choice]

    return 'Invalid startegy has been sent!'


@api.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@api.route('/ai_play', methods=['POST'])
def ai_play():
    strategy = request.form.get('strategy').encode("utf-8")
    color = request.form.get('color').encode("utf-8")
    board = literal_eval(request.form.get('board').encode("utf-8"))

    options = {'random': othello.random_strategy(color, board),
               'max-diff': othello.maximizer(othello.score, color, board),
               'max-weighted-diff': othello.maximizer(othello.weighted_score, color, board),
               'minimax-diff': othello.minimax_searcher(3, othello.score, color, board),
               'minimax-weighted-diff':
                   othello.minimax_searcher(3, othello.weighted_score, color, board),
               'ab-diff': othello.alphabeta_searcher(3, othello.score, color, board),
               'ab-weighted-diff':
                   othello.alphabeta_searcher(3, othello.weighted_score, color, board)}

    result = get_choice(strategy, options)

    if not isinstance(result, basestring):
        result = result()

    return str(result)

    # return 'Invalid startegy has been sent!'
    # return json.dumps(companies)


if __name__ == '__main__':
    api.run()
