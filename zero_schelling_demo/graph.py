from copy import deepcopy as copy
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt


def graph(grid, figsize=7, showgrid=False):
    """Create a visual representation of the grid"""
    grid_viz = copy(grid)

    for i in range(grid_viz.shape[0]):
        for j in range(grid_viz.shape[1]):
            a = grid_viz[i,j]
            if a:
                grid_viz[i,j] = a.group
    grid_viz = grid_viz.astype(int)

    matrix = grid_viz

    colors = ['#D3D3D3', '#9E8257', '#E6A067']
    cmap = ListedColormap(colors)

    fig = plt.figure(figsize=(figsize, figsize))
    plt.imshow(matrix, cmap=cmap, vmin=0, vmax=2)
    plt.xticks([x-0.5 for x in range(grid.shape[0])])  
    plt.yticks([y-0.5 for y in range(grid.shape[1])])  
    plt.gca().set_xticklabels([])  
    plt.gca().set_yticklabels([])
    plt.grid(showgrid)

    plt.close(fig)

    return fig
