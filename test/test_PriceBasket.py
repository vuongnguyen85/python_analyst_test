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

def create_basket(products):
    basket = Basket(available_products_in_store)
    basket.add_to_basket(products)
    return basket


class TestPriceBasket(unittest.TestCase):

    def test_format_price(self):
        self.assertEqual('41p', Util.format_price(0.41))
        self.assertEqual('£1.01', Util.format_price(1.01))
        self.assertEqual('£3.00', Util.format_price(3))

    def test_get_product_price(self):
        basket = create_basket(['Apples', 'Bread', 'Soup', 'Milk'])
        self.assertEqual(1, basket.get_product_price('Apples'))
        self.assertEqual(0.8, basket.get_product_price('Bread'))
        self.assertEqual(1.3, basket.get_product_price('Milk'))
        self.assertEqual(0.65, basket.get_product_price('Soup'))

    def test_get_item_quantity(self):
        basket = create_basket(['Apples', 'Apples', 'Apples', 'Bread', 'Soup', 'Soup'])
        self.assertEqual(3, basket.get_product_quantity_in_basket('Apples'))
        self.assertEqual(2, basket.get_product_quantity_in_basket('Soup'))
        self.assertEqual(1, basket.get_product_quantity_in_basket('Bread'))
        self.assertEqual(0, basket.get_product_quantity_in_basket('Milk'))

    def test_get_promotion_message(self):
        basket = create_basket(['Bread', 'Apples', 'Apples', 'Apples', 'Bread', 'Soup', 'Soup', 'Soup', 'Soup'])
        self.assertEqual('  Apples 10% off: 30p', apple_promo.get_promotion_message(basket))
        self.assertEqual('  50% off Bread when buying 2 Soups: 80p', bread_promo.get_promotion_message(basket))

    def test_calculate_total_offer_discount_for_basket(self):
        basket = create_basket(['Bread', 'Apples', 'Apples', 'Apples', 'Bread', 'Soup', 'Soup', 'Soup', 'Soup'])
        # promotion_discount = 3 (apple qty) * 0.1 (10% discount on Apples price)
        self.assertEqual(0.3, apple_promo.calculate_total_offer_discount_for_basket(basket))

        # promotion_discount = 2 (qualified bundle qty) * 0.4 (50% discount on Bread price)
        self.assertEqual(0.8, bread_promo.calculate_total_offer_discount_for_basket(basket))

    def test_update_customer_basket(self):
        basket = create_basket(['Apples', 'Apples', 'Apples'])
        basket_with_quantity = {}
        for Product, quantity in basket.get_basket().items():
            basket_with_quantity.update({Product.get_name(): quantity})

        self.assertEqual({'Apples': 3}, basket_with_quantity)

        basket = create_basket(['Apples', 'Bread', 'Milk'])
        basket_with_quantity = {}
        for Product, quantity in basket.get_basket().items():
            basket_with_quantity.update({Product.get_name(): quantity})

        self.assertEqual({'Apples': 1, 'Bread': 1, 'Milk': 1}, basket_with_quantity)

    def test_calculate_basket_subtotal(self):
        basket = create_basket(['Apples', 'Bread', 'Soup'])
        self.assertEqual(2.45, basket.calculate_basket_subtotal())

        basket = create_basket(['Apples', 'Bread', 'Milk'])
        self.assertEqual(3.1, basket.calculate_basket_subtotal())
        #
        # basket = create_basket(['Milk', 'Bread', 'Soup'])
        # self.assertEqual(2.75, basket.calculate_basket_subtotal())

    def test_offers_can_be_applied_to_basket(self):
        # Need 2 soups to have discount on bread
        basket = create_basket(['Milk', 'Bread', 'Soup'])
        self.assertFalse(PriceCalculator(basket, current_offers).offers_can_be_applied_to_basket())

        basket = create_basket(['Apples', 'Bread', 'Milk'])
        self.assertTrue(PriceCalculator(basket, current_offers).offers_can_be_applied_to_basket())

        basket = create_basket(['Soup', 'Bread', 'Soup'])
        self.assertTrue(PriceCalculator(basket, current_offers).offers_can_be_applied_to_basket())


if __name__ == '__main__':
    unittest.main()
