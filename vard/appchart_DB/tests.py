from django.test import TestCase

from plot_utils import get_data, make_plot, make_scatter, make_bar, make_pie, make_stackplot


TEST_JSON = [
            {
                "product_id": 1,
                "menu_name": "GOJIRA ROLL",
                "price": 12.6
            },
            {
                "product_id": 2,
                "menu_name": "VIVA LAS VEGAS ROLL",
                "price": 15.7
            },
            {
                "product_id": 3,
                "menu_name": "FUTOMAKI",
                "price": 14.4
            }
        ]

# print('menu_name', 'price', TEST_JSON)
# make_plot(*get_data('menu_name', 'price', TEST_JSON),
#           x_label='menu_name', y_label='price', title='menu_name vs price', color='red')
# make_scatter(*get_data('menu_name', 'price', TEST_JSON),
#              x_label='menu_name', y_label='price', title='menu_name vs price', color='red')
# make_bar(*get_data('menu_name', 'price', TEST_JSON),
#          x_label='menu_name', y_label='price', title='menu_name vs price', color='red')
print(make_pie(*get_data('price', 'menu_name', TEST_JSON),
         x_label='price', y_label='menu_name', title='price vs menu_name', color='yellow', image_format='svg'))
# make_stackplot(*get_data('menu_name', 'price', TEST_JSON),
#                x_label='menu_name', y_label='price', title='product_id vs price', color='green')