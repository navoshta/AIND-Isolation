"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

def custom_score_v1(game, player):
    """
    Heuristic based solely on available moves' distance from edges.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_score = 0
    opp_score = 0

    half_h = game.height / 2
    half_w = game.width / 2

    for r, c in game.get_legal_moves(player):
        own_score += half_h - abs(half_h - r)
        own_score += half_w - abs(half_w - c)

    for r, c in game.get_legal_moves(game.get_opponent(player)):
        opp_score += half_h - abs(half_h - r)
        opp_score += half_w - abs(half_w - c)

    return float(own_score - opp_score)

def custom_score_v2(game, player):
    """
    Heuristic based on available moves' weighted distance from edges.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_score = 0
    opp_score = 0

    half_h = game.height / 2
    half_w = game.width / 2

    for r, c in game.get_legal_moves(player):
        own_score += 1
        own_score += 0.5 * (half_h - abs(half_h - r)) / half_h
        own_score += 0.5 * (half_w - abs(half_w - c)) / half_w

    for r, c in game.get_legal_moves(game.get_opponent(player)):
        opp_score += 1
        opp_score += 0.5 * (half_h - abs(half_h - r)) / half_h
        opp_score += 0.5 * (half_w - abs(half_w - c)) / half_w

    return float(own_score - opp_score)

def custom_score_v3(game, player):
    """
    Heuristic based on available moves' dynamically weighted distance from edges.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own_score = 0
    opp_score = 0

    half_h = game.height / 2
    half_w = game.width / 2

    c_center = len(game.get_blank_spaces()) / (game.height * game.width)
    c_moves = (1 - c_center)
    c_center = c_center / 2 # Since we calculate them separately for width and height

    for r, c in game.get_legal_moves(player):
        own_score += c_moves
        own_score += c_center * (half_h - abs(half_h - r)) / half_h
        own_score += c_center * (half_w - abs(half_w - c)) / half_w

    for r, c in game.get_legal_moves(game.get_opponent(player)):
        opp_score += c_moves
        opp_score += c_center * (half_h - abs(half_h - r)) / half_h
        opp_score += c_center * (half_w - abs(half_w - c)) / half_w

    return float(own_score - opp_score)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    return custom_score_v3(game, player)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)  This parameter should be ignored when iterative = True.

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).  When True, search_depth should
        be ignored and no limit to search depth.

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            DEPRECATED -- This argument will be removed in the next release

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        if len(legal_moves) == 0:
            return (-1, -1)

        current_move = legal_moves[0]

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            if self.iterative:
                depth = 0
                while current_move != -1:
                    depth += 1
                    current_move = self.move_for_depth(game, depth)
            else:
                current_move = self.move_for_depth(game, self.search_depth)

        except Timeout:
            # Handle any actions required at timeout, if necessary
            return current_move

        # Return the best move from the last completed search iteration
        return current_move

    def move_for_depth(self, game, depth):
        if self.method == 'minimax':
            _, move = self.minimax(game, depth)
        elif self.method == 'alphabeta':
            _, move = self.alphabeta(game, depth)
        return move

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return (self.score(game, self), game.get_player_location(self))

        best_move = (-1, -1)
        best_score = float("-inf") if maximizing_player else float("inf")

        for current_move in game.get_legal_moves():
            current_score, _ = self.minimax(
                game.forecast_move(current_move),
                depth - 1,
                not maximizing_player
            )

            if maximizing_player:
                if current_score > best_score:
                    best_score = current_score
                    best_move = current_move
            else:
                if current_score < best_score:
                    best_score = current_score
                    best_move = current_move
        return (best_score, best_move)



    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        if depth == 0:
            return (self.score(game, self), game.get_player_location(self))

        best_move = (-1, -1)
        best_score = float("-inf") if maximizing_player else float("inf")

        for current_move in game.get_legal_moves():
            current_score, _ = self.alphabeta(
                game.forecast_move(current_move),
                depth - 1,
                alpha, beta,
                not maximizing_player
            )

            if maximizing_player:
                if current_score > best_score:
                    best_score = current_score
                    best_move = current_move
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    return best_score, best_move

            else:
                if current_score < best_score:
                    best_score = current_score
                    best_move = current_move
                beta = min(beta, best_score)
                if beta <= alpha:
                    return best_score, best_move

        return (best_score, best_move)
