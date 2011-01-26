# CoxMediaGroup Code Challenge Entry

by Michael F. Lamb <mike@datagrok.org>

## Task

1. Fork this repo on github. (done)
2. Create an app that can interactively play the game of Tic Tac Toe against another player and never lose.
3. Commit early and often, with good messages.
4. Push your code back to github and send me a pull request.

### Assumptions

- "app" means "django app," does not include demonstration of Django project setup, admin api, etc.

- "never lose" means "wins or draws."

## Development plan

3. Minimal "simplest thing that works" implementation. Just satisfy requirements of task:

	- Django view imports and adapts generic tic-tac-toe algorithm to Django view
	- Stateless.
	- Logic in client.
	- No attempt to prevent user from cheating.
	- No user name, login, scoreboard, etc.
	- No database required.
	- No sessions required.
	- HTML-only implementation:
		- url?state=xox-xo--x etc.

4. (Tag, submit pull request, ask for feedback and further direction, continue as time allows with enhancements.)

5. Polish up docstrings and write additional tests.

6. Add jQuery / AJAX client implementation

7. Explore feature enhancements that could demonstrate use of database API,
Django session middleware, etc.

### Repository Layout

	Tic-Tac-Toe/            repo root
		tictactoe/          django app
			__init__.py
			tictac.py       General tic-tac-toe algorithm module
			models.py       \
			tests.py         } Django boilerplate
			views.py        /

### Design Decisions/Rationale

Directory layout: forked github repo name is "Tic-Tac-Toe." Dashes are invalid in python package and module names; django apps are python packages. Looking around at Django apps on github, there seems to be no strict standard for directory layout. Don't want to overwrite upstream README with my own.

tictac.py module: keep game logic decoupled from django framework. 'tictac' algorithm module to avoid possible name conflicts with 'tictactoe' django app. (Maybe there's a better way but refactoring is easy, go with this)

Algorithm ([minimax]): Tried [Randy Hyde's algorithm][1], initial tests showed it not to work well. Not going to waste time on any more arbitrarily specified algorithms, will just implement [minimax] and let the machine do the heavy lifting. Since tic-tac-toe has symmetries and users must take turns moving, there should be plenty of opportunity to reduce storage and processing load if needed.

Algorithm: [negamax] variant of [minimax] demonstrated itself to be appropriate for this task, because the game is alternate-player

[1]: http://webster.cs.ucr.edu/AsmTools/MASM/TicTacToe/ttt_1.html
[negamax]: http://en.wikipedia.org/wiki/Negamax

Pushing dev branch to github: normally, I would keep my development branch on my local machine and only push after a nice clean merge to master, but I want to show my progress to the reviewer.

State representation: As a string, for easy matching with python builtin regular expressions. 'x' for x, 'o' for o, '-' for empty position; ' ' makes for unsightly URLs.

## Implementation ideas

### Algorithm

- Implement [MiniMax] algorithm (more general, pretending requirements might change) Recursively determines best move given any game state.
	- Enhancement: employ deque rather than relying on recursive calls; if this were not tic-tac-toe we might need more tracking than Python's call stack could provide.
	- Enhancement: employ [alpha-beta pruning] to reduce storage requirement
	- Enhancement: create hashtable (dict) that stores game states with best move
	- Enhancement: tic-tac-toe board has dihedral symmetry of order 8; use this to decrease storage requirement for hashtable
		- Create function to find "canonical state" that can be looked up given any game state. (And a function to invert the stored best move back to symmetrical state)

[minimax]: http://en.wikipedia.org/wiki/Minimax#Minimax_algorithm_with_alternate_moves
[alpha-beta pruning]: http://en.wikipedia.org/wiki/Alpha-beta_pruning

### Server-side

- First iteration: simple, featureless.
- Later enhancements:
	- User login, ranking (req. sessions and database api)

### Client-side

- First iteration: plain HTML, stateless. Client click sends state in query string, server generates new state and renders page.
- Later enhancements:
	- jQuery / AJAX gameplay
	- nicer look+feel?
	- scoreboard?

<!-- vim: set ft=mkd: -->
