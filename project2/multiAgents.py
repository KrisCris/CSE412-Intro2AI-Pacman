# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import random

import util
from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
  """

    def getAction(self, gameState):
        """
    You do not need to change this method, but you're welcome to.

    getAction chooses among the best options according to the evaluation function.

    Just like in the previous project, getAction takes a GameState and returns
    some Directions.X for some X in the set {North, South, West, East, Stop}
    """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
    Design a better evaluation function here.

    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (newFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.

    Print out these variables to see what you're getting, then combine them
    to create a masterful evaluation function.
    """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = newFood.asList()

        if len(foodList) == 0:
            return 100

        fDist = 1000000
        for f in foodList:
            dist = util.manhattanDistance(newPos, f)
            if dist < fDist:
                fDist = dist + len(foodList) * 20

        for i in range(len(newGhostStates)):
            dist = util.manhattanDistance(newPos, newGhostStates[i].getPosition()) + newScaredTimes[i]
            if dist <= 1:
                return -1000000

        return -fDist


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
  """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
  """

    def getAction(self, gameState):
        """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
        "*** YOUR CODE HERE ***"
        from sys import maxint

        def _mini_max(state, agent_idx, depth):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            agent_idx = agent_idx % state.getNumAgents()
            if agent_idx == 0:
                depth += 1
                if depth > self.depth:
                    return self.evaluationFunction(state)
                else:
                    return _max_value(state, agent_idx, depth)
            else:
                return _min_value(state, agent_idx, depth)

        def _max_value(state, agent_idx, depth):
            value = -maxint
            optimal_action = None

            for action in state.getLegalActions(agent_idx):
                new_state = state.generateSuccessor(agent_idx, action)
                new_val = _mini_max(new_state, agent_idx + 1, depth)
                if new_val > value:
                    optimal_action = action
                    value = new_val
            return value if depth > 1 else optimal_action

        def _min_value(state, agent_idx, depth):
            value = maxint

            for action in state.getLegalActions(agent_idx):
                new_state = state.generateSuccessor(agent_idx, action)
                new_value = _mini_max(new_state, agent_idx + 1, depth)
                if new_value < value:
                    value = new_value
            return value

        act = _mini_max(gameState, 0, 0)
        return act


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
  """

    def getAction(self, gameState):
        """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
        "*** YOUR CODE HERE ***"
        from sys import maxint

        def _alpha_beta(state, agent_idx, depth, alpha, beta):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            agent_idx = agent_idx % state.getNumAgents()
            if agent_idx == 0:
                depth += 1
                if depth > self.depth:
                    return self.evaluationFunction(state)
                else:
                    return _max_value(state, agent_idx, depth, alpha, beta)
            else:
                return _min_value(state, agent_idx, depth, alpha, beta)

        def _max_value(state, agent_idx, depth, alpha, beta):
            value = -maxint
            optimal_action = None

            for action in state.getLegalActions(agent_idx):
                new_state = state.generateSuccessor(agent_idx, action)
                new_val = _alpha_beta(new_state, agent_idx + 1, depth, alpha, beta)
                if new_val > value:
                    optimal_action = action
                    value = new_val

                alpha = max(alpha, value)
                if alpha >= beta:
                    return value

            return value if depth > 1 else optimal_action

        def _min_value(state, agent_idx, depth, alpha, beta):
            value = maxint

            for action in state.getLegalActions(agent_idx):
                new_state = state.generateSuccessor(agent_idx, action)
                new_value = _alpha_beta(new_state, agent_idx + 1, depth, alpha, beta)
                if new_value < value:
                    value = new_value

                beta = min(beta, value)
                if alpha >= beta:
                    return value

            return value

        act = _alpha_beta(gameState, 0, 0, -maxint, maxint)
        return act


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
  """

    def getAction(self, gameState):
        """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
        "*** YOUR CODE HERE ***"
        from sys import maxint

        def _expecti_max(state, agent_idx, depth):
            if state.isWin() or state.isLose():
                return self.evaluationFunction(state)
            agent_idx = agent_idx % state.getNumAgents()
            if agent_idx == 0:
                depth += 1
                if depth > self.depth:
                    return self.evaluationFunction(state)
                else:
                    return _max_value(state, agent_idx, depth)
            else:
                return _exp_value(state, agent_idx, depth)

        def _max_value(state, agent_idx, depth):
            value = -maxint
            optimal_action = None

            for action in state.getLegalActions(agent_idx):
                new_state = state.generateSuccessor(agent_idx, action)
                new_val = _expecti_max(new_state, agent_idx + 1, depth)
                if new_val > value:
                    optimal_action = action
                    value = new_val
            return value if depth > 1 else optimal_action

        def _exp_value(state, agent_idx, depth):
            value = 0.0

            actions = state.getLegalActions(agent_idx)
            for action in actions:
                new_state = state.generateSuccessor(agent_idx, action)
                value += _expecti_max(new_state, agent_idx + 1, depth)

            if len(actions) == 0:
                return 0

            return float(value) / float(len(actions))

        act = _expecti_max(gameState, 0, 0)
        return act


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """

    "*** YOUR CODE HERE ***"
    from util import manhattanDistance as mDist

    # food - head to the closest food
    def _food_val(state):
        food_list = state.getFood().asList()
        pacman_pos = state.getPacmanPosition()
        value = []

        for food in food_list:
            value.append(1.0 / float(mDist(pacman_pos, food)))
        if len(value) > 0:
            return max(value)

        return 0

    # capsule - head to the closest capsule
    def _capsule_val(state):
        pacman_pos = state.getPacmanPosition()
        capsules = state.getCapsules()

        value = []
        for capsule in capsules:
            value.append(1.0 / float(mDist(pacman_pos, capsule)))
        if len(value) > 0:
            return max(value)

        return 0

    # ghost
    def _ghost_val(state):
        score = 0
        for ghost in state.getGhostStates():
            dist_ghost = mDist(state.getPacmanPosition(), ghost.getPosition())

            # ignore too far away target
            if ghost.scaredTimer > 0:
                # hunt target within 12 blocks
                # + 1 to prevent (val<1)^2 become too small
                # ** 2 to let pacman target on ghosts when getting closer
                score += (max(0, 12.0 - float(dist_ghost))) ** 2
            else:
                # to escape when ghost approaching
                # choose 7 assuming pacman can escape from C shape
                score -= (max(0, 7.0 - float(dist_ghost))) ** 2
        return score

    def _food_num_val(state):
        food_list = state.getFood().asList()
        if len(food_list) > 0:
            # make value big when food_list is small
            return 1 / len(food_list) ** 2
        return 0

    # 10 points for each food
    # 200 points for eat a white ghost
    # => 1:20
    weighted_food = _food_val(currentGameState) * 1
    weight_capsule = _capsule_val(currentGameState) * 20
    weight_ghost = _ghost_val(currentGameState)
    weighted_food_num = _food_num_val(currentGameState)

    return currentGameState.getScore() + weight_ghost + weighted_food + weight_capsule + weighted_food_num


# Abbreviation
better = betterEvaluationFunction


class ContestAgent(MultiAgentSearchAgent):
    """
    Your agent for the mini-contest
  """

    def getAction(self, gameState):
        """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
        "*** YOUR CODE HERE ***"
        from sys import maxint
        from util import manhattanDistance as mDist

        def _expecti_max(state, agent_idx, depth):
            if state.isWin() or state.isLose():
                return better(state)
            agent_idx = agent_idx % state.getNumAgents()
            if agent_idx == 0:
                depth += 1
                if depth > self.depth:
                    return better(state)
                else:
                    return _max_value(state, agent_idx, depth)
            else:
                return _exp_value(state, agent_idx, depth)

        def _max_value(state, agent_idx, depth):
            value = -maxint
            optimal_action = None

            for action in state.getLegalActions(agent_idx):
                new_state = state.generateSuccessor(agent_idx, action)
                new_val = _expecti_max(new_state, agent_idx + 1, depth)
                if new_val > value:
                    optimal_action = action
                    value = new_val
            return value if depth > 1 else optimal_action

        def _exp_value(state, agent_idx, depth):
            value = 0.0

            pacman_direction = state.data.agentStates[0].configuration.direction
            pacman_pos = state.data.agentStates[0].configuration.pos
            ghost_direction = state.data.agentStates[agent_idx].configuration.direction
            ghost_pos = state.data.agentStates[agent_idx].configuration.pos

            actions = state.getLegalActions(agent_idx)

            if mDist(pacman_pos, ghost_pos) > 7:
                # we can not know what far away ghosts are going to do without large cose
                # so simply use equal possibility
                accumWeight = 0
                for action in actions:
                    if action == 'Stop':
                        continue
                    weight_dict = {
                        'West': 25,
                        'East': 25,
                        'North': 25,
                        'South': 25
                    }
                    if ghost_direction != 'Stop':
                        weight_dict[ghost_direction] += 15

                    new_state = state.generateSuccessor(agent_idx, action)
                    accumWeight += weight_dict[action]
                    value += _expecti_max(new_state, agent_idx + 1, depth) * weight_dict[action]
                if accumWeight == 0:
                    return 0

                return float(value) / float(accumWeight)

            else:
                # when ghost is approaching, the action that made ghost running toward pacman has higher possibility
                # so lower the possibility that ghosts running opposite direction
                accumWeight = 0
                for action in actions:
                    if action == 'Stop':
                        continue
                    weight_dict = {
                        'West': 25,
                        'East': 25,
                        'North': 25,
                        'South': 25
                    }

                    if pacman_pos[0] > ghost_pos[0]:
                        weight_dict['East'] = 45
                        weight_dict['West'] = 10
                    else:
                        weight_dict['East'] = 10
                        weight_dict['West'] = 45

                    if pacman_pos[1] > pacman_pos[1]:
                        weight_dict['North'] = 45
                        weight_dict['South'] = 10
                    else:
                        weight_dict['North'] = 10
                        weight_dict['South'] = 45

                    if ghost_direction != 'Stop':
                        weight_dict[ghost_direction] += 10

                    new_state = state.generateSuccessor(agent_idx, action)
                    accumWeight += weight_dict[action]
                    value += _expecti_max(new_state, agent_idx + 1, depth) * weight_dict[action]
                if accumWeight == 0:
                    return 0
                return float(value) / float(accumWeight)

        act = _expecti_max(gameState, 0, 0)
        return act