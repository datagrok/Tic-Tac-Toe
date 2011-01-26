'''Algorithms for playing the game of tic-tac-toe.

    http://en.wikipedia.org/wiki/Tic-tac-toe

This is an implementation of a Negamax algorithm to play a "perfect" game of
tic-tac-toe.

    http://en.wikipedia.org/wiki/Negamax

We represent the game board (state) as a string of exactly nine characters from
'x', 'o', and '-'. The characters in the state correspond to the board
position examined from top-left to bottom-right. Example:

>>> state = (
...     '-x-'
...     'o--'
...     '--x')
>>> state
'-x-o----x'
>>> validate_state(state)
>>> # (no exceptions indicates successful validation)
>>> printboard(state)
   | X |  
-----------
 O |   |  
-----------
   |   | X
>>> state = move(state)
>>> state = move(state)
>>> state = move(state)
>>> state = move(state)
>>> state = move(state)
>>> printboard(state)
   | X | O
-----------
 O | O | X
-----------
 X | O | X
>>> state = move(state)
>>> printboard(state)
 X | X | O
-----------
 O | O | X
-----------
 X | O | X

'''
import re

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

# TODO: Memoize negamax.

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


def evaluate_state(state, player=None, _re_win=get_win_patterns()):
    '''Returns a float between 1 and -1 representing the greatest possible loss
    for the player about to move in this particular state. Against a perfect
    opponent, a negative value guarantees a loss and a 0 value guarantees a
    tie.

    player -- optional, the player who moved last.
    _re_win -- internal, do not override.

    >>> state = 'x-----o--'
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
    if player is None:
        player = lastplayer(state)

    # check for a win
    if _re_win[player].match(state):
        return 1
    # check for a loss
    elif _re_win[opponent(player)].match(state):
        return -1

    # check for a draw
    elif '-' not in state:
        return 0

    # recurse
    else:
        return -.9 * max([evaluate_state(s) for s in possible_moves(state, opponent(player))])


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


def move(state):
    '''Given a tictactoe board state, compute and return a new state that
    includes the computer's choice of the optimal next move.
    
    >>> state = 'x-x-o---o'
    >>> printboard(state)
     X |   | X
    -----------
       | O |  
    -----------
       |   | O
    >>> printboard(move(state))
     X | X | X
    -----------
       | O |  
    -----------
       |   | O
    '''

    my_player = opponent(lastplayer(state))
    states = [(evaluate_state(s, my_player), s) for s in possible_moves(state, my_player)]
    states.sort()
    states.reverse()

    return states[0][1]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
