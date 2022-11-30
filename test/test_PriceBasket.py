import unittest
from pricebasket.PriceBasket import get_price, Basket, format_price, Offer

current_offers = {
    'Apples': ['percentage_discount', 10],  #  schema = item: ['discount_type', percentage_off, required_product, required_product_amount]
    'Bread': ['buy_x_get_y_discount', 50, 'Soup', 2]
}


class TestPriceBasket(unittest.TestCase):

    def test_item_prices(self):
        self.assertEqual(1, get_price('Apples'))
        self.assertEqual(0.8, get_price('Bread'))
        self.assertEqual(1.3, get_price('Milk'))
        self.assertEqual(0.65, get_price('Soup'))

    def test_get_item_quantity(self):
        self.assertEqual(3, Basket(['Apples', 'Apples', 'Apples']).get_item_quantity('Apples'))
        self.assertEqual(2, Basket(['Apples', 'Bread', 'Apples']).get_item_quantity('Apples'))
        self.assertEqual(1, Basket(['Apples', 'Bread', 'Milk']).get_item_quantity('Bread'))
        self.assertEqual(0, Basket(['Soup', 'Bread', 'Milk']).get_item_quantity('Apples'))

    def test_format_price(self):
        self.assertEqual('£0.41', format_price(0.41))
        self.assertEqual('£1.01', format_price(1.01))
        self.assertEqual('£3.00', format_price(3.00))

    def test_check_item_on_offer(self):
        self.assertEqual(True, Offer(current_offers).check_if_item_on_offer('Apples'))
        self.assertEqual(True, Offer(current_offers).check_if_item_on_offer('Bread'))
        self.assertEqual(False, Offer(current_offers).check_if_item_on_offer('Soup'))

    def test_get_offer_type(self):
        self.assertEqual('percentage_discount', Offer(current_offers).get_offer_type('Apples'))
        self.assertEqual('buy_x_get_x_discount', Offer(current_offers).get_offer_type('Bread'))
        self.assertEqual(None, Offer(current_offers).get_offer_type('Soup'))

    def test_get_percentage_amount(self):
        self.assertEqual(10, Offer(current_offers).get_percentage_amount('Apples'))
        self.assertEqual(50, Offer(current_offers).get_percentage_amount('Bread'))
        self.assertEqual(None, Offer(current_offers).get_percentage_amount('Soup'))

    def test_get_required_item(self):
        self.assertEqual(None, Offer(current_offers).get_required_item('Apples'))
        self.assertEqual('Soup', Offer(current_offers).get_required_item('Bread'))
        self.assertEqual(None, Offer(current_offers).get_required_item('Soup'))

    def test_get_required_item_quantity(self):
        self.assertEqual(None, Offer(current_offers).get_required_item_quantity('Apples'))
        self.assertEqual(2, Offer(current_offers).get_required_item_quantity('Bread'))
        self.assertEqual(None, Offer(current_offers).get_required_item_quantity('Soup'))

    def test_get_product_discount_amount(self):
        self.assertEqual(0.1, Offer(current_offers).get_product_discount_amount(['Bread', 'Apples', 'Soup'], 'Apples'))
        self.assertEqual(0.3, Offer(current_offers).get_product_discount_amount(['Bread', 'Apples', 'Apples', 'Apples'], 'Apples'))
        self.assertEqual(0.8, Offer(current_offers).get_product_discount_amount(['Bread', 'Apples', 'Apples', 'Apples', 'Bread', 'Soup', 'Soup', 'Soup', 'Soup'], 'Bread'))
        self.assertEqual(0.4, Offer(current_offers).get_product_discount_amount(['Bread', 'Apples', 'Apples', 'Apples', 'Soup', 'Soup', 'Soup', 'Soup'], 'Bread'))

if __name__ == '__main__':
    unittest.main()
