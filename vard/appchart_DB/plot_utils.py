import matplotlib.pyplot as plt
import numpy as np
import base64
import tempfile


def get_data(key_x: str, key_y: str, chart_data: list) -> tuple:
    """Get two lists, x and y, from data query by key_x and key_y"""
    x = []
    y = []
    for item in chart_data:
        x.append(item[key_x])
        y.append(item[key_y])
    return x, y


def plot_to_base64(plot, image_format='png'):
    """Convert plot from required format to base64 string"""
    plot_file = tempfile.NamedTemporaryFile(suffix=f'.{image_format}')
    plot.savefig(plot_file, format=image_format)
    plot_file.seek(0)
    plot_data = base64.b64encode(plot_file.read())
    plot_file.close()
    return plot_data


def create_plot(key_x: str, key_y: str, chart_data: list, image_format='png', x_label='x', y_label='y',
                color='blue', title='', plot_type='plot'):
    """Create plot in required format"""
    x, y = get_data(key_x, key_y, chart_data)
    image_format = image_format.lower()
    plot_type = plot_type.lower()
    color = color.lower()
    switcher = {
        'plot': make_plot,
        'scatter': make_scatter,
        'bar': make_bar,
        'pie': make_pie,
        'stackplot': make_stackplot
    }
    return switcher[plot_type](x, y, image_format, x_label, y_label, color, title)


def make_plot(x: list, y: list, image_format='png', x_label='x', y_label='y', color='blue', title=''):
    """Simple plot, one line"""

    plt.style.use('_mpl-gallery')

    # make data
    x = np.array(x)
    y = np.array(y)

    # plot
    plt.plot(x, y, linewidth=2.0, label=title, color=color)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # plt.show()
    return plot_to_base64(plt, image_format)


def make_scatter(x: list, y: list, image_format='png', x_label='x', y_label='y', color='blue', title=''):
    """Scatter plot, many points"""
    plt.style.use('_mpl-gallery')

    # make the data
    x = np.array(x)
    y = np.array(y)

    # size and color:
    sizes = np.random.uniform(15, 80, len(x)) # for different sizes

    # plot
    plt.scatter(x, y, s=sizes, vmin=0, vmax=100, color=color)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # plt.show()
    return plot_to_base64(plt, image_format)

def make_bar(x: list, y: list, image_format='png', x_label='x', y_label='y', color='blue', title=''):
    """Bar chart"""
    plt.style.use('_mpl-gallery')

    # make data:
    x = np.array(x)
    y = np.array(y)

    # plot

    plt.bar(x, y, width=1, edgecolor="white", linewidth=0.7, color=color)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # plt.show()
    return plot_to_base64(plt, image_format)


def make_stackplot(x: list, y: list, image_format='png', x_label='x', y_label='y', color='blue', title=''):
    """Stackplot, line with fill"""
    plt.style.use('_mpl-gallery')

    # make data
    x = np.array(x)
    y = np.array(y)

    # plot
    plt.stackplot(x, y, labels=y, colors=color)

    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # plt.show()
    return plot_to_base64(plt, image_format)


def make_pie(x: list, y: list, image_format='png', x_label='x', y_label='y', color='blue', title=''):
    """Pie chart, round diagram, x must be numbers"""
    plt.style.use('_mpl-gallery-nogrid')

    # make data
    x = np.array(x)
    if color.lower() == 'yellow':
        color = 'orange'
    colors = plt.get_cmap(f'{color.capitalize()}s')(np.linspace(0.2, 0.7, len(x)))


    # plot
    plt.pie(x, colors=colors, radius=3, center=(4, 4),
        wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, labels=y)

    plt.title(title)
    # plt.show()
    return plot_to_base64(plt, image_format)