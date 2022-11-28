import unittest
from pricebasket.PriceBasket import get_price, Basket, format_price, Offer

current_offers = {
    'Apples': ['percentage_discount', 10],  #  schema = item: ['discount_type', percentage_off, required_product, required_product_amount]
    'Bread': ['buy_x_get_x_discount', 50, 'Soup', 2]
}

class TestPriceBasket(unittest.TestCase):

    def test_item_prices(self):
        self.assertEqual(get_price('Apples'), 1)
        self.assertEqual(get_price('Bread'), 0.8)
        self.assertEqual(get_price('Milk'), 1.3)
        self.assertEqual(get_price('Soup'), 0.65)

    def test_get_item_quantity(self):
        self.assertEqual(Basket(['Apples', 'Apples', 'Apples']).get_item_quantity('Apples'), 3)
        self.assertEqual(Basket(['Apples', 'Bread', 'Apples']).get_item_quantity('Apples'), 2)
        self.assertEqual(Basket(['Apples', 'Bread', 'Milk']).get_item_quantity('Bread'), 1)
        self.assertEqual(Basket(['Soup', 'Bread', 'Milk']).get_item_quantity('Apples'), 0)

    def test_format_price(self):
        self.assertEqual(format_price(0.41), '£0.41')
        self.assertEqual(format_price(1.01), '£1.01')
        self.assertEqual(format_price(3.00), '£3.00')

    def test_check_item_on_offer(self):
        self.assertEqual(Offer(current_offers).check_if_item_on_offer('Apples'), True)
        self.assertEqual(Offer(current_offers).check_if_item_on_offer('Bread'), True)
        self.assertEqual(Offer(current_offers).check_if_item_on_offer('Soup'), False)

    def test_get_offer_type(self):
        self.assertEqual(Offer(current_offers).get_offer_type('Apples'), 'percentage_discount')
        self.assertEqual(Offer(current_offers).get_offer_type('Bread'), 'buy_x_get_x_discount')
        self.assertEqual(Offer(current_offers).get_offer_type('Soup'), None)

    def test_get_discount_amount(self):
        self.assertEqual(Offer(current_offers).get_percentage_amount('Apples'), 10)
        self.assertEqual(Offer(current_offers).get_percentage_amount('Bread'), 50)
        self.assertEqual(Offer(current_offers).get_percentage_amount('Soup'), None)

    def test_get_discount_amount(self):
        self.assertEqual(Offer(current_offers).get_discount_amount('Apples'), 0.1)
        self.assertEqual(Offer(current_offers).get_discount_amount('Bread'), 0.5)
        self.assertEqual(Offer(current_offers).get_discount_amount('Soup'), None)

    def test_get_required_item(self):
        self.assertEqual(Offer(current_offers).get_required_item('Apples'), None)
        self.assertEqual(Offer(current_offers).get_required_item('Bread'), 'Soup')
        self.assertEqual(Offer(current_offers).get_required_item('Soup'), None)

    def test_get_required_item_quantity(self):
        self.assertEqual(Offer(current_offers).get_required_item_quantity('Apples'), None)
        self.assertEqual(Offer(current_offers).get_required_item_quantity('Bread'), 2)
        self.assertEqual(Offer(current_offers).get_required_item_quantity('Soup'), None)

if __name__ == '__main__':
    unittest.main()
