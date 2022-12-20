import unittest
from pricebasket.PriceBasket import Product, Basket, Util, PriceCalculator, PercentageDiscountOffer, BuyXGetYDiscountOffer

available_products_in_store = [
    Product('Apples', 1),
    Product('Bread', 0.8),
    Product('Milk', 1.3),
    Product('Soup', 0.65)
]

current_offers = [
    PercentageDiscountOffer('Apples', 10),
    BuyXGetYDiscountOffer('Bread', 50, 'Soup', 2)
]

apple_promo = current_offers[0]
bread_promo = current_offers[1]


class TestPriceBasket(unittest.TestCase):

    def test_format_price(self):
        self.assertEqual('£0.41', Util.format_price(0.41))
        self.assertEqual('£1.01', Util.format_price(1.01))
        self.assertEqual('£3.00', Util.format_price(3.00))

    def test_get_product_price(self):
        self.assertEqual(1, Util.get_product_price('Apples', available_products_in_store))
        self.assertEqual(0.8, Util.get_product_price('Bread', available_products_in_store))
        self.assertEqual(1.3, Util.get_product_price('Milk', available_products_in_store))
        self.assertEqual(0.65, Util.get_product_price('Soup', available_products_in_store))

    def test_get_item_quantity(self):
        basket = Basket(['Apples', 'Apples', 'Apples', 'Bread', 'Soup', 'Soup'])
        basket.add_to_basket(available_products_in_store)
        self.assertEqual(3, basket.get_product_quantity_in_basket('Apples'))
        self.assertEqual(2, basket.get_product_quantity_in_basket('Soup'))
        self.assertEqual(1, basket.get_product_quantity_in_basket('Bread'))

    def test_get_promotion_message(self):
        basket = Basket(['Bread', 'Apples', 'Apples', 'Apples', 'Bread', 'Soup', 'Soup', 'Soup', 'Soup'])
        basket.add_to_basket(available_products_in_store)
        self.assertEqual('  Apples 10% off: £0.30', apple_promo.get_promotion_message(basket, available_products_in_store))
        self.assertEqual('  50% off Bread when buying 2 Soups: £0.80', bread_promo.get_promotion_message(basket, available_products_in_store))

    def test_calculate_total_offer_discount_for_basket(self):
        basket = Basket(['Bread', 'Apples', 'Apples', 'Apples', 'Bread', 'Soup', 'Soup', 'Soup', 'Soup'])
        basket.add_to_basket(available_products_in_store)
        # promotion_discount = 3 (apple qty) * 0.1 (10% discount on Apples price)
        self.assertEqual(0.3, apple_promo.calculate_total_offer_discount_for_basket(basket, available_products_in_store))

        # promotion_discount = 2 (qualified bundle qty) * 0.4 (50% discount on Bread price)
        self.assertEqual(0.8, bread_promo.calculate_total_offer_discount_for_basket(basket, available_products_in_store))

    def test_update_customer_basket(self):
        basket = Basket(['Apples', 'Apples', 'Apples'])
        basket.add_to_basket(available_products_in_store)
        self.assertEqual({'Apples': 3}, basket.get_basket())

        basket = Basket(['Apples', 'Bread', 'Milk'])
        basket.add_to_basket(available_products_in_store)
        self.assertEqual({'Apples': 1, 'Bread': 1, 'Milk': 1}, basket.get_basket())

    def test_calculate_basket_subtotal(self):
        basket = Basket(['Apples', 'Soup', 'Bread'])
        basket.add_to_basket(available_products_in_store)
        self.assertEqual(2.45, basket.calculate_basket_subtotal(available_products_in_store))

        basket = Basket(['Apples', 'Bread', 'Milk'])
        basket.add_to_basket(available_products_in_store)
        self.assertEqual(3.1, basket.calculate_basket_subtotal(available_products_in_store))

        basket = Basket(['Soup', 'Bread', 'Milk'])
        basket.add_to_basket(available_products_in_store)
        self.assertEqual(2.75, basket.calculate_basket_subtotal(available_products_in_store))

    def test_offers_can_be_applied_to_basket(self):
        basket = Basket(['Soup', 'Bread', 'Milk'])
        basket.add_to_basket(available_products_in_store)
        self.assertFalse(PriceCalculator(basket, current_offers, available_products_in_store).offers_can_be_applied_to_basket())

        basket = Basket(['Apples', 'Bread', 'Milk'])
        basket.add_to_basket(available_products_in_store)
        self.assertTrue(PriceCalculator(basket, current_offers, available_products_in_store).offers_can_be_applied_to_basket())

        basket = Basket(['Soup', 'Bread', 'Soup'])
        basket.add_to_basket(available_products_in_store)
        self.assertTrue(PriceCalculator(basket, current_offers, available_products_in_store).offers_can_be_applied_to_basket())


if __name__ == '__main__':
    unittest.main()
