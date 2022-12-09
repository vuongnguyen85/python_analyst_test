import unittest
from pricebasket.PriceBasket import Product, Basket, format_price, PriceCalculator, PercentageDiscountOffer, BuyXGetYDiscountOffer

apple_promo = PercentageDiscountOffer('Apples', 10)
bread_promo = BuyXGetYDiscountOffer('Bread', 50, 'Soup', 2)

products = {
    'Apples': 1,
    'Bread': 0.8,
    'Milk': 1.3,
    'Soup': 0.65
}


class TestPriceBasket(unittest.TestCase):

    def test_format_price(self):
        self.assertEqual('£0.41', format_price(0.41))
        self.assertEqual('£1.01', format_price(1.01))
        self.assertEqual('£3.00', format_price(3.00))

    def test_get_product_price(self):
        self.assertEqual(1, Product.get_price('Apples'))
        self.assertEqual(0.8, Product.get_price('Bread'))
        self.assertEqual(1.3, Product.get_price('Milk'))
        self.assertEqual(0.65, Product.get_price('Soup'))
        self.assertEqual(0, Product.get_price('Banana'))

    def test_get_item_quantity(self):
        basket = Basket(['Apples', 'Apples', 'Apples', 'Bread', 'Soup', 'Soup'])
        basket.update_customer_basket()
        self.assertEqual(3, basket.get_item_quantity('Apples'))
        self.assertEqual(2, basket.get_item_quantity('Soup'))
        self.assertEqual(1, basket.get_item_quantity('Bread'))

    def test_get_promotion_message(self):
        basket = ['Bread', 'Apples', 'Apples', 'Apples']
        Basket(basket).update_customer_basket()
        self.assertEqual('  Apples 10% off: £0.30', apple_promo.get_promotion_message(apple_promo.calculate_total_offer_discount_for_basket(basket)))

        basket = ['Bread', 'Apples', 'Apples', 'Apples', 'Bread', 'Soup', 'Soup', 'Soup', 'Soup']
        Basket(basket).update_customer_basket()
        self.assertEqual('  50% off Bread when buying 2 Soups: £0.80', bread_promo.get_promotion_message(bread_promo.calculate_total_offer_discount_for_basket(basket)))

    def test_calculate_total_offer_discount_for_basket(self):
        basket = ['Bread', 'Apples', 'Apples', 'Apples']
        Basket(basket).update_customer_basket()
        # promotion_discount = 3 (apple qty) * 0.1 (10% discount on Apples price)
        self.assertEqual(0.3, apple_promo.calculate_total_offer_discount_for_basket(basket))

        basket = ['Bread', 'Apples', 'Apples', 'Apples', 'Bread', 'Soup', 'Soup', 'Soup', 'Soup']
        Basket(basket).update_customer_basket()
        # promotion_discount = 2 (qualified bundle qty) * 0.4 (50% discount on Bread price)
        self.assertEqual(0.8, bread_promo.calculate_total_offer_discount_for_basket(basket))

    def test_update_customer_basket(self):
        self.assertEqual({'Apples': 3}, Basket(['Apples', 'Apples', 'Apples']).update_customer_basket())
        self.assertEqual({'Apples': 1, 'Bread': 1, 'Milk': 1}, Basket(['Apples', 'Bread', 'Milk']).update_customer_basket())

    def test_calculate_basket_subtotal(self):
        self.assertEqual(2.45, PriceCalculator(['Apples', 'Soup', 'Bread']).calculate_basket_subtotal())
        self.assertEqual(3.1, PriceCalculator(['Apples', 'Bread', 'Milk']).calculate_basket_subtotal())
        self.assertEqual(2.75, PriceCalculator(['Soup', 'Bread', 'Milk']).calculate_basket_subtotal())


if __name__ == '__main__':
    unittest.main()
