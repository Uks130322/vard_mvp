import matplotlib.pyplot as plt
import numpy as np


def get_data(key_x: str, key_y: str, chart_data: list) -> tuple:
    """Get two lists, x and y, from data by key_x and key_y"""
    x = []
    y = []
    for item in chart_data:
        x.append(item[key_x])
        y.append(item[key_y])
    return x, y


def make_plot(x: list, y: list, image_format='png', x_label='x', y_label='y', color='blue', title=''):

    plt.style.use('_mpl-gallery')

    # make data
    x = np.array(x)
    y = np.array(y)

    # plot
    plt.plot(x, y, linewidth=2.0, label=title, color=color)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    plt.show()


def make_scatter(x: list, y: list, image_format='png', x_label='x', y_label='y', color='blue', title=''):
    plt.style.use('_mpl-gallery')

    # make the data
    x = np.array(x)
    y = np.array(y)

    # size and color:
    sizes = np.random.uniform(15, 80, len(x))
    colors = np.random.uniform(15, 80, len(x))

    # plot
    plt.scatter(x, y, s=sizes, c=colors, vmin=0, vmax=100)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    plt.show()

def make_bar(x: list, y: list, image_format='png', x_label='x', y_label='y', color='blue', title=''):
    plt.style.use('_mpl-gallery')

    # make data:
    x = np.array(x)
    y = np.array(y)

    # plot

    plt.bar(x, y, width=1, edgecolor="white", linewidth=0.7)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    plt.show()


def make_stackplot(x: list, y: list, image_format='png', x_label='x', y_label='y', color='blue', title=''):
    plt.style.use('_mpl-gallery')

    # make data
    x = np.array(x)
    y = np.array(y)

    # plot
    plt.stackplot(x, y, labels=y)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    plt.show()


def make_pie(x: list, y: list, image_format='png', x_label='x', y_label='y', color='blue', title=''):
    plt.style.use('_mpl-gallery-nogrid')

    # make data
    x = np.array(x)
    colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(x)))

    # plot
    plt.pie(x, colors=colors, radius=3, center=(4, 4),
        wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

    plt.xlabel(x_label)
    plt.ylabel(y_label) # TODO rewrite this
    plt.title(title)

    plt.show()