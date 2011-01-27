'''Algorithms for playing the game of tic-tac-toe.

    http://en.wikipedia.org/wiki/Tic-tac-toe

This is an implementation of a Negamax algorithm to play a "perfect" game of
tic-tac-toe.

    http://en.wikipedia.org/wiki/Negamax

We represent the game board (state) as a string of exactly nine characters from
'x', 'o', and '-'. The characters in the state correspond to the board
position examined from top-left to bottom-right. Example:

>>> state = (
...     '---'
...     '---'
...     '---')
>>> validate_state(state)
>>> # (no exceptions indicates successful validation)
>>> while True:
...     score, nextstate = evaluate_state(state)
...     printboard_small(nextstate)
...     print 'Score: %.2f' % score
...     if score == 1:
...         print 'Win'
...         break
...     if score == -1:
...         print 'Lose'
...         break
...     if score == 0 and '-' not in state:
...         print 'Tie game.'
...         break
...     state = nextstate
x--
---
---
Score: -0.00
x--
-o-
---
Score: 0.00
xx-
-o-
---
Score: -0.00
xxo
-o-
---
Score: 0.00
xxo
-o-
x--
Score: -0.00
xxo
oo-
x--
Score: 0.00
xxo
oox
x--
Score: -0.00
xxo
oox
xo-
Score: 0.00
xxo
oox
xox
Score: -0.00
xxo
oox
xox
Score: 0.00
Tie game.


'''
import re

# My very trivial memoization module. Python 3 also has functools.lrucache.
from datagrok.misc import memoized

__author__ = 'Michael F. Lamb <mike@datagrok.org>'
__date__ = 'Thu, 20 Jan 2011 01:15:05 -0500'


class TTTStateError(StandardError):
    pass


# TODO: The majority of these functions employ a state variable as their first
# argument. It would make sense to pack them up into a class and keep the state
# there. Also, code might read easier.

# TODO: The negamax algorithm is useful in general; we could refactor it out of
# evaluate_state, and make it a general-purpose function that takes a state
# evaluation and a children-generating function as arguments. 
#
# evaluate = create_negamax(evaluate_terminal_state, children)
# state.evaluate()

# TODO: Add alpha-beta pruning to negamax algorithm.

# TODO: Improve memoization of negamax by recognizing symmetrical states and
# storing only one canonical representation.


def get_win_patterns():
    '''Creates a dict mapping players to regular expression objects that will
    match on a game state they have won.
   
    >>> win_patterns = get_win_patterns()
    >>> win_patterns['o'].match('xxx------') and 'O Wins'
    >>> win_patterns['x'].match('xxx------') and 'X Wins'
    'X Wins'
    >>> win_patterns['o'].match('x-x---ooo') and 'O Wins'
    'O Wins'

    '''
    win_pattern = '|'.join([
        'xxx......',
        '...xxx...',
        '......xxx',
        'x..x..x..',
        '.x..x..x.',
        '..x..x..x',
        'x...x...x',
        '..x.x.x..',
    ])

    return {
        'x': re.compile(win_pattern),
        'o': re.compile(win_pattern.replace('x','o')),
    }


def validate_state(state):
    '''Raises an error if state is invalid. Otherwise returns None.
    
    >>> validate_state('xxxooxoox')
    >>> validate_state('xxx------')
    Traceback (most recent call last):
    ...
    TTTStateError: Tic Tac Toe state indicates a player moved out-of-turn.
    
    '''
    if not isinstance(state, str) and not isinstance(state, unicode):
        raise TTTStateError('Tic Tac Toe state %s must be a string instance.' % repr(state))
    if len(state) != 9:
        raise TTTStateError('Tic Tac Toe state must be exactly 9 characters long.')
    if state.strip('xo-') != '':
        raise TTTStateError('Tic Tac Toe state must contain only the characters x, o, or -.')
    if state.count('x') - state.count('o') not in [0, 1]:
        raise TTTStateError('Tic Tac Toe state indicates a player moved out-of-turn.')


def printboard(state):
    '''Utility function to display the state as an ascii-art game board.'''
    print '\n'.join([
        ' %s | %s | %s',
        '-----------',
        ' %s | %s | %s',
        '-----------',
        ' %s | %s | %s',
    ]) % tuple(state.upper().replace('-', ' '))


def printboard_small(state):
    '''Utility function to display the state as an ascii-art game board.'''
    print '\n'.join([state[0:3], state[3:6], state[6:9]])


def opponent(player):
    '''Returns the player opposite the player given as the argument.'''
    if player == 'x':
        return 'o'
    return 'x'


def lastplayer(state):
    '''Returns the player who moved last in the given state.'''
    if state.count('x') - state.count('o'):
        return 'x'
    return 'o'


@memoized
#@notifying
def evaluate_state(state, _re_win=get_win_patterns()):
    '''Returns a float between 1 and -1 representing the greatest possible loss
    for the player about to move in this particular state, and the new state
    after making that move. Against a perfect opponent, a negative value
    guarantees a loss and a 0 value guarantees a tie.

    Given a tictactoe board state, compute and return a tuple indicating the
    win status and a new state that includes the computer's choice of the
    optimal next move.

    If the game is already won by the computer, the state will not change.

    A win status of -1 indicates a win by the player. (Game over)
    A win status of 1 indicates a win by the computer. (Game over)
    A win status of 0 indicates a draw

    Arguments:
        _re_win -- internal, do not override.

    >>> state = 'x-----o--'
    >>> evaluate_state(state)
    >>> for s in possible_moves(state, 'x'):
    ...    score = evaluate_state(s)
    ...    print '%s %5.2f %5s' % (repr(s), score,
    ...        score>0 and 'win' or score<0 and 'loss' or 'draw')
    'xx----o--'  0.66   win
    'x-x---o--'  0.66   win
    'x--x--o--' -0.59  loss
    'x---x-o--'  0.00  draw
    'x----xo--'  0.00  draw
    'x-----ox-'  0.00  draw
    'x-----o-x'  0.66   win

    '''
    # figure out who moved last
    player = lastplayer(state)

    win = _re_win[player].match(state)
    loss = _re_win[opponent(player)].match(state)

    if win and loss:
        raise TTTStateError('It is impossible for both players to have won.')

    elif win:
        return 1, state

    elif loss:
        return -1, state

    # neither win nor loss means either game continues, or draw. check for draw
    elif '-' not in state:
        return 0, state

    # recurse
    else:
        score, state = max([(evaluate_state(s)[0], s) for s in possible_moves(state, opponent(player))])
        return -.9 * score, state


def possible_moves(state, player=None):
    '''Generate all possible moves for the next player, given state.
 
    player -- optional, the player who will move next.

    Example:
    >>> for s in possible_moves(state='xox--x-o-', player='x'):
    ...     print repr(s)
    'xoxx-x-o-'
    'xox-xx-o-'
    'xox--xxo-'
    'xox--x-ox'

    '''
    if player is None:
        player = opponent(lastplayer(state))

    for i in range(len(state)):
        if state[i] == '-':
            yield state[:i] + player + state[i+1:]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
