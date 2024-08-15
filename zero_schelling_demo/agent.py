
from .imports import * 


class Agent:
    """Agent class

    This class models an agent to be put on a grid in a Schelling
    segregation simulation. The agent belongs to a specific group and
    has a minimum threshold of similar neighbors required to be
    satisfied or "happy". The agent can evaluate its neighbors,
    determine its happiness, and decide on a new position if unhappy.

    Parameters
    ----------
    min_like_neighbors_happy : int, optional
        The minimum number of like neighbors required for the agent to
        be happy (default is 1).
    position : tuple of int, optional
        The (x, y) coordinates of the agent's position on the grid
        (default is (0, 0)).
    group : int, optional
        The agent's group identifier, typically 0 or 1 (default is 0).
    id : str, optional
        A unique identifier for the agent. If not provided, a UUID is 
        generated automatically (default is None).

    Attributes
    ----------
    min_like_neighbors_happy : int
        The minimum number of like neighbors required for the agent to
        be happy.
    group : int
        The agent's group identifier.
    position : tuple of int
        The (x, y) coordinates of the agent's position on the grid.
    is_happy : bool
        Whether the agent is happy with its current neighbors.
    id : str
        The unique identifier for the agent.
    n_similar_neighbors : int
        The number of neighboring agents that belong to the same group.
    neighbor_locs : list of tuple of int
        The list of neighboring positions around the agent.

    Methods
    -------
    calculate_new_position(grid)
        Determine the agent's new position on the grid if it is unhappy.
    eval_neighbors(grid)
        Evaluate the number of neighboring agents that belong to the 
        same group.
    get_locs(grid)
        Retrieve the locations of neighboring slots around the agent's 
        position.
    __str__()
        Return a string representation of the agent's attributes.
    """
    def __init__(self, min_like_neighbors_happy=1, position=(0,0), group=0, 
                 id=None):
        self.min_like_neighbors_happy = min_like_neighbors_happy
        self.group = group
        self.position = position
        self.is_happy = False
        if not id:
            self.id = str(uuid())
        else:
            self.id = id

    def calculate_new_position(self, grid):
        """Determine new position

        This method evaluates the agent's neighbors and determines
        whether the agent is happy. If the agent is already happy, it
        returns its current position. Otherwise, it chooses a random
        adjacent empty location to move to.

        Parameters
        ----------
        grid : numpy.ndarray
            The grid representing the current state of the system, with 
            agents and empty spaces.

        Returns
        -------
        tuple
            The new position for the agent as a tuple (x, y). If the
            agent is already happy, it returns the current position.
        """
        self.eval_neighbors(grid)
        if self.n_similar_neighbors >= self.min_like_neighbors_happy:
            self.is_happy = True
            return self.position
        else:
            # randomly move to different location
            for x,y in self.neighbor_locs:
                if grid[x,y] == 0:
                    return (x, y)
                else:
                    pass

    def eval_neighbors(self, grid):
        """Evaluate number of similar neighbors"""
        self.get_locs(grid)
        self.n_similar_neighbors = 0
        for x,y in self.neighbor_locs:
            n = grid[x,y]
            if n != 0:
                if n.group == self.group:
                    self.n_similar_neighbors += 1
        if self.n_similar_neighbors >= self.min_like_neighbors_happy:
            self.is_happy = True

    def get_locs(self, grid):
        """Retrieve locations of neighbor slots.

        This method calculates the neighboring positions surrounding the
        agent's current position on the grid. The positions are adjusted
        to ensure they remain within the grid boundaries. The resulting
        list of neighboring locations is stored in `self.neighbor_locs`
        and randomized for later use.

        Parameters
        ----------
        grid : numpy.ndarray
            The grid representing the current state of the system.

        Returns
        -------
        list
            A list of tuples representing the positions of neighboring 
            slots, randomized in order.
        """
        locs = []
        pos = self.position
        n = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), 
             (-1, 1)] 
        for x,y in n:
            p = list(copy(pos)) 
            # position cannot be less than zero or greater than max index
            p[0] = min(max(0, p[0]+x), grid.shape[0]-1)
            p[1] = min(max(0, p[1]+y), grid.shape[1]-1)
            locs.append(p)
        self.neighbor_locs = list(set([tuple(x) for x in locs 
                                       if tuple(x) != pos]))
        # randomize order of locations
        self.neighbor_locs = (pd.Series(self.neighbor_locs).sample(frac=1)
                                .tolist())

        return self.neighbor_locs

    def __str__(self):
        return (f"Agent(min_like_neighbors_happy="
                f"{self.min_like_neighbors_happy}, position={self.position}, "
                f"group={self.group}, id='{self.id}')")
