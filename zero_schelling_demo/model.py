"""Model class

Model class that sets up the model and finds equilibrium. See docstring for
Model class. 

"""

from .init_grid import init as init_grid
from .graph import graph

from .imports import * 


class Model:
    """
    A model for simulating agent-based systems on a grid.

    This class implements a basic agent-based model where agents are 
    positioned on a grid, and each agent's happiness is evaluated based 
    on the number of like neighbors. The model can iterate through 
    steps, moving unhappy agents to new positions, until an equilibrium 
    is reached where all agents are happy or a maximum number of 
    iterations is achieved.

    Parameters
    ----------
    min_like_neighbors_happy : int, optional
        The minimum number of like neighbors required for an agent to be 
        happy (default is 1).
    size_grid : int, optional
        The size of the grid, which will be a square of dimensions 
        `size_grid` x `size_grid` (default is 25).
    n_agents : int, optional
        The number of agents to be placed on the grid (default is 100).

    Attributes
    ----------
    grid : numpy.ndarray
        A 2D array representing the grid, where each cell may contain an 
        agent or be empty.
    min_like_neighbors_happy : int
        The minimum number of like neighbors required for an agent to be 
        happy.
    size_grid : int
        The size of the grid.
    n_agents : int
        The total number of agents in the model.
    agents : list
        A list of agents currently in the grid.
    n_agents_happy : int
        The current number of happy agents in the grid.
    fig : matplotlib.figure.Figure
        The figure object used for plotting the grid.

    Methods
    -------
    plot(figsize=6, showgrid=False)
        Return a figure that represents the grid.
    solve(itermax=1500, graphs=False, fp_graphs='/l/tmp/')
        Find equilibrium by iteratively adjusting the system until all 
        agents are happy or a maximum number of iterations is reached.
    list_agents()
        Reshape the grid to a list of agents.
    archive_graph(fp_graphs, i='')
        Create and write out a graph of the current state of the grid.
    step(graphs=False, fp_graphs='/l/tmp', i='')
        Execute one iteration of the model, moving unhappy agents and 
        optionally saving a graphical representation of the grid.
    count_happy()
        Count and return the number of happy agents in the grid.
    __str__()
        Return a string representation of the model.
    """
    def __init__(self, min_like_neighbors_happy=1, size_grid=25, n_agents=100):
        self.grid = init_grid(min_like_neighbors_happy, size_grid=size_grid,
                              n_agents=n_agents)
        self.min_like_neighbors_happy = min_like_neighbors_happy
        self.size_grid = size_grid
        self.n_agents = n_agents
        self.count_happy()

    def plot(self, figsize=6, showgrid=False):
        """Return a figure that represents the grid"""
        self.fig = graph(self.grid, figsize=figsize, showgrid=showgrid)
        return self.fig

    def solve(self, itermax=500, graphs=False, fp_graphs='/l/tmp/'):
        """Find equilibrium

        This method iteratively adjusts the state of the system to reach
        an equilibrium where all agents are 'happy'. The process stops
        when all agents are happy or the maximum number of iterations
        (`itermax`) is reached.

        Put another way, this function "steps" the model repeatedly. In
        each step, unhappy agents move to an adjacent cell. This repeats
        until all agents are happy. 

        Parameters
        ----------
        itermax : int, optional
            The maximum number of iterations to attempt (default is
            1500).
        graphs : bool, optional
            If True, generate and save graphical outputs at each step
            (default is False).
        fp_graphs : str, optional
            File path where the graphs will be saved, if `graphs` is
            True (default is '/l/tmp/').

        Returns
        -------
        None
        """

        i = 0
        while self.n_agents_happy < self.n_agents:
            self.step(graphs=graphs, i=i, fp_graphs=fp_graphs)
            i += 1
            self.count_happy()
            if i >= itermax:
                break
        print(f"done, {self.n_agents_happy} out of {self.n_agents} are "
              f"happy. that took {i} out of iteration max {itermax} steps. ")

    def list_agents(self):
        """Reshape grid to list of agents

        This method flattens the grid and extracts all agents into a
        list, which is stored in `self.agents`. 

        Returns
        -------
        list
            A list of agents present in the grid.

        """
        self.agents = [x[0] for x in self.grid.reshape(-1, 1) if x[0]]
        return self.agents

    def archive_graph(self, fp_graphs, i=''):
        """Create and write out graph of current state"""
        d = pd.Timestamp.utcnow().timestamp()
        if i:
            fn = f"{d} - schelling step {i:.0f}.png"
        else:
            fn = f"{d} - schelling image.png"
        fp = join(fp_graphs, fn)
        fig = self.plot()
        fig.savefig(fp)

    def step(self, graphs=False, fp_graphs='/l/tmp', i=''):
        """Primary model stepping func

        Executes one iteration of the model by evaluating each agent's
        happiness and moving those who are not happy to a new position
        in the grid. Optionally, a graphical representation of the grid
        can be saved at each step.

        Parameters
        ----------
        graphs : bool, optional
            If True, generate and save a graph of the grid at each step
            (default is False).
        fp_graphs : str, optional
            File path where the graphs will be saved, if `graphs` is
            True (default is '/l/tmp').
        i : str or int, optional
            An identifier for the current step, used when saving the
            graph (default is '').

        Returns
        -------
        None
        """
        agents = self.list_agents()
        for a in agents:
            a.eval_neighbors(self.grid)
            if not a.is_happy:
                # if not happy, move. 
                xc, yc = a.position # current position 
                xn, yn = a.calculate_new_position(self.grid) # new position
                assert self.grid[xn, yn] == 0, 'must be empty'
                a.position = xn, yn
                self.grid[xn, yn] = copy(a)
                self.grid[xc, yc] = 0
        if graphs:
            self.archive_graph(fp_graphs, i=i)

    def count_happy(self):
        """Sum up number of happy agents in entire grid"""
        self.n_agents_happy = 0
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i, j] != 0:
                    if self.grid[i, j].is_happy:
                        self.n_agents_happy += 1
        return self.n_agents_happy

    def __str__(self):
        return f"Model"
