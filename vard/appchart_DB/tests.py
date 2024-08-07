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
# make_plot(*get_data('product_id', 'price', TEST_JSON))
# make_scatter(*get_data('product_id', 'price', TEST_JSON))
# make_bar(*get_data('product_id', 'price', TEST_JSON))
make_pie(*get_data('product_id', 'price', TEST_JSON))
# make_stackplot(*get_data('product_id', 'price', TEST_JSON))