# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


class Node(object):
    _state = None
    _parent = None
    _direction = None
    _cost = None

    def __init__(self, state, direction, cost, parent):
        self._state = state
        self._direction = direction
        self._cost = cost
        self._parent = parent

    def __str__(self):
        return "[" + str(self._state) + "]"

    def trace(self):
        route = ""
        this = self
        while not this.isHead():
            route += str(this) + "->"
            this = this.getParent()
        route += str(this)
        return route

    def isHead(self):
        if self._parent is None:
            return True
        else:
            return False

    def getParent(self):
        return self._parent

    def getState(self):
        return self._state

    def getDirection(self):
        return self._direction

    def getCost(self):
        return self._cost

    def getActions(self):
        actions = []
        this = self
        while not this.isHead():
            actions.append(this.getDirection())
            this = this.getParent()
        actions.reverse()
        return actions

    def getAccumCost(self):
        cost = 0
        this = self
        while not this.isHead():
            cost += this.getCost()
            this = this.getParent()
        return cost


# i don't use this methods anymore... see search()
# def genericSearch(problem, container):
#     # keep track of already expanded states
#     expanded = []

#     # init state

#     parent = Node(state=problem.getStartState(), direction=None, cost=None, parent=None)

#     while True:
#         # print parent.trace()
#         # check goal state
#         if problem.isGoalState(parent.getState()):
#             return parent.getActions()

#         # expanding
#         states = problem.getSuccessors(parent.getState())
#         # mark parent node as expanded
#         expanded.append(parent.getState())

#         # if no solution
#         if len(states) == 0 and container.isEmpty():
#             print "No feasible solution."
#             return None

#         # each sub-node
#         for state, direction, cost in states:
#             # skip expanded node (parent of some nodes)
#             if state in expanded:
#                 continue

#             # warp newly generated state as Node
#             node = Node(state=state, direction=direction, cost=cost, parent=parent)
#             # push to stack/queue, or some appropriate data structure
#             container.push(node)

#         # pop nodes of states been regenerated and expanded (When re-generation is allowed)
#         while parent.getState() in expanded:
#             parent = container.pop()


# implementation of exactly the pseudo code in course slides
def search(problem, container):
    expanded_states = []
    container.push(Node(state=problem.getStartState(), direction=None, cost=None, parent=None))

    while True:
        current_state = container.pop()
        if current_state.getState() in expanded_states:
            continue

        if problem.isGoalState(current_state.getState()):
            return current_state.getActions()

        for state, direction, cost in problem.getSuccessors(current_state.getState()):
            container.push(Node(state=state, direction=direction, cost=cost, parent=current_state))

        expanded_states.append(current_state.getState())

        if container.isEmpty():
            print 'no solution'
            return None


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    return search(problem, util.Stack())
    # # legacy code
    # # store unexpanded nodes
    # stk = util.Stack()
    # # keep track of already expanded states
    # expanded = []
    #
    # parent = Node(state=problem.getStartState(), direction=None, cost=None, parent=None)
    #
    # while True:
    #     # check goal after expansion
    #     if problem.isGoalState(node.getState()):
    #         return node.getActions()
    #
    #     states = problem.getSuccessors(parent.getState())
    #     expanded.append(parent.getState())
    #
    #     if len(states) == 0 and stk.isEmpty():
    #         print "No feasible solution."
    #         return None
    #
    #     for state, direction, cost in states:
    #         # states duplicated in the stack are not checked since we want to regenerate states.
    #         # thus we do stk.pop() iteratively to remove expanded nodes in the end.
    #
    #         # From Course video:
    #         # No states re-generation may produce a better solution,
    #         # but the algorithm might get stuck in some super deep subtrees.
    #         if state in expanded:
    #             continue
    #
    #         node = Node(state=state, direction=direction, cost=cost, parent=parent)
    #         # print node.trace() + "\n"
    #
    #         # push
    #         stk.push(node)
    #
    #     # pop nodes of states regenerated and expanded.
    #     while parent.getState() in expanded:
    #         parent = stk.pop()


def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    return search(problem, util.Queue())
    # # legacy code
    # # store unexpanded nodes
    # q = util.Queue()
    # # keep track of already expanded states
    # expanded = []
    #
    # parent = Node(state=problem.getStartState(), direction=None, cost=None, parent=None)
    #
    # while True:
    #     # check after expansion
    #     if problem.isGoalState(parent.getState()):
    #         return parent.getActions()
    #
    #     states = problem.getSuccessors(parent.getState())
    #     expanded.append(parent.getState())
    #
    #     if len(states) == 0 and q.isEmpty():
    #         print "No feasible solution."
    #         return None
    #
    #     for state, direction, cost in states:
    #         # skip parent nodes
    #         if state in expanded:
    #             continue
    #
    #         node = Node(state=state, direction=direction, cost=cost, parent=parent)
    #         # print node.trace() + "\n"
    #
    #         # check after expansion
    #         if problem.isGoalState(node.getState()):
    #             return node.getActions()
    #         q.push(node)
    #
    #     # pop nodes of states regenerated and expanded.
    #     while parent.getState() in expanded:
    #         parent = q.pop()


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    return search(problem, util.PriorityQueueWithFunction(lambda node: node.getAccumCost()))
    # # legacy code
    # pq = util.PriorityQueue()
    #
    # # keep track of already expanded states
    # expanded = []
    #
    # parent = Node(state=problem.getStartState(), direction=None, cost=0, parent=None)
    #
    # while True:
    #     # Difference to DFS & BFS():
    #     # For DFS & BFS, you can either check the goal state right after the state is generated
    #     # or the state is ready for expansion (After getting out of the stack/queue).
    #     #
    #     # But in UCS, we have to care about the cost.
    #     # Checking goal after the node popped out from the PQ
    #     # ensures that we are always dealing with the node with lowest cost first,
    #     # so we won't get tricked by a path to the goal in very short distance but with huge cost in the last edge.
    #     #
    #     # like:
    #     # %%% A -- 1 --> B -- 1 --> C -- 1 --> D %%%
    #     # %%% |                                ^ %%%
    #     # %%% |                                | %%%
    #     # %%%  --------------- 10 -------------  %%%
    #     #
    #     # If the node is checked right after its generation,
    #     # it would be troublesome comparing its cost to other unfinished routes.
    #
    #     if problem.isGoalState(parent.getState()):
    #         return parent.getActions()
    #
    #     # Some standard operation, lol
    #     states = problem.getSuccessors(parent.getState())
    #     expanded.append(parent.getState())
    #
    #     if len(states) == 0 and pq.isEmpty():
    #         print "No feasible solution."
    #         return None
    #
    #     for state, direction, cost in states:
    #         # skip parent (expanded) nodes.
    #         # "Do not gen expanded states" <- it is generated by the game, we just ignore them.
    #         if state in expanded:
    #             continue
    #
    #         node = Node(state=state, direction=direction, cost=cost, parent=parent)
    #         # print node.trace() + "\t" + str(node.getAccumCost()) + "\n\n"
    #
    #         pq.push(node, node.getAccumCost())
    #
    #     # pop nodes of states regenerated and expanded.
    #     # "Do not re-expand states" <- we doing the following to avoid expanded states being re-expanded
    #     while parent.getState() in expanded:
    #         parent = pq.pop()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    return search(
        problem,
        util.PriorityQueueWithFunction(
            lambda node: node.getAccumCost() + heuristic(node.getState(), problem)
        )
    )


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
