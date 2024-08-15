
from . import agent
from .imports import * 


def init(min_like_neighbors_happy, size_grid, n_agents):
    """Initialize the grid with agents.

    This function creates a grid and populates it with two groups of
    agents, each with an initial position set to (0, 0). The agents are
    then randomly distributed across the grid, and their positions are
    updated accordingly.

    Note that the grid must be square. 

    Parameters
    ----------
    min_like_neighbors_happy : int
        The minimum number of like neighbors required for an agent to be 
        happy.
    size_grid : int
        The size of the grid, which will be a square of dimensions
        `size_grid` x `size_grid`.
    n_agents : int
        The total number of agents to be placed on the grid.

    Returns
    -------
    numpy.ndarray
        A grid of dimensions `size_grid` x `size_grid`, populated with 
        agents and empty slots.
    """

    # create grid with agents
    agents = []

    # add group 1 agents
    for _ in range(int(n_agents/2)):
        a = agent.Agent(min_like_neighbors_happy=min_like_neighbors_happy,
                        position=(0,0), group=1)
        agents.append(a)
        
    # add group 2 agents
    for _ in range(int(n_agents/2)):
        a = agent.Agent(min_like_neighbors_happy=min_like_neighbors_happy,
                        position=(0,0), group=2)
        agents.append(a)

    # add zeros to agents
    agents = agents + [0] * (size_grid**2 - n_agents)
    # create np.array from list, randomize starting locations
    grid = (pd.Series(agents).sample(frac=1).values
              .reshape(size_grid, size_grid))

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            a = grid[i, j]
            if a:
                # set agent position 
                a.position = (i,j)
                grid[i,j] = a

    return grid
