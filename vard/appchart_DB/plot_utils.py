import matplotlib.pyplot as plt
import numpy as np

def make_plot():

    plt.style.use('_mpl-gallery')

    # make data
    x = np.linspace(0, 10, 100)
    y = 4 + 2 * np.sin(2 * x)

    # plot
    fig, ax = plt.subplots()

    ax.plot(x, y, linewidth=2.0)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
           ylim=(0, 8), yticks=np.arange(1, 8))

    plt.show()


def make_scatter():
    plt.style.use('_mpl-gallery')

    # make the data
    np.random.seed(3)
    x = 4 + np.random.normal(0, 2, 24)
    y = 4 + np.random.normal(0, 2, len(x))
    # size and color:
    sizes = np.random.uniform(15, 80, len(x))
    colors = np.random.uniform(15, 80, len(x))

    # plot
    fig, ax = plt.subplots()

    ax.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
           ylim=(0, 8), yticks=np.arange(1, 8))

    plt.show()

def make_bar():
    plt.style.use('_mpl-gallery')

    # make data:
    np.random.seed(3)
    x = 0.5 + np.arange(8)
    y = np.random.uniform(2, 7, len(x))

    # plot
    fig, ax = plt.subplots()

    ax.bar(x, y, width=1, edgecolor="white", linewidth=0.7)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        ylim=(0, 8), yticks=np.arange(1, 8))

    plt.show()


def make_stackplot():
    plt.style.use('_mpl-gallery')

    # make data
    x = np.arange(0, 10, 2)
    ay = [1, 1.25, 2, 2.75, 3]
    by = [1, 1, 1, 1, 1]
    cy = [2, 1, 2, 1, 2]
    y = np.vstack([ay, by, cy])

    # plot
    fig, ax = plt.subplots()

    ax.stackplot(x, y)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        ylim=(0, 8), yticks=np.arange(1, 8))

    plt.show()


def make_pie():
    plt.style.use('_mpl-gallery-nogrid')

    # make data
    x = [1, 2, 3, 4]
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))

    # plot
    fig, ax = plt.subplots()
    ax.pie(x, colors=colors, radius=3, center=(4, 4),
        wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
        ylim=(0, 8), yticks=np.arange(1, 8))

    plt.show()