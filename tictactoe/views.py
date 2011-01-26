# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
import tictac
import pprint

def index(request, state):
    '''The most basic tic-tac-toe view. Presents a plain, stateless, HTML-only
    UI. Assumes 'x' always moves first.

    '''

    # default template data
    t = {
        # new game starting with player
        'state': state,
        'score': 0,
        'nextstate': '---------',
    }

    if state:
        # continue game in progress
        tictac.validate_state(str(state))
        t['score'], t['nextstate'] = tictac.evaluate_state(state)

    # The game is over if
    # there are no open spaces left,
    # or the player has won this turn (score = 1)
    # or the computer will win on its turn (score = -.9)
    t['game_over'] = '-' not in t['nextstate'] or t['score'] == 1 or t['score'] <= -.9

    if t['game_over']:
        t['game_board'] = [(None, c) for c in t['nextstate']]
    else:
        t['game_board'] = _generate_board(t['nextstate'])

    return render_to_response('tictactoe/index.html', t)


def _generate_board(state):
    '''Generate a tuple of the form (next_state, piece) for each piece in
    state, where next_state is None if the square is occupied, otherwise it is
    the state that will result if the player moves to (clicks on) that
    position.
    
    This is useful in the creation of a UI of the current game board and
    available moves for the player.
     
    >>> _generate_board('-x-------')
    
    '''

    _player = tictac.opponent(tictac.lastplayer(state))

    for i, piece in enumerate(state):
        nextstate = None
        if piece == '-':
            nextstate = state[:i] + _player + state[i+1:]
        yield (nextstate, piece)
