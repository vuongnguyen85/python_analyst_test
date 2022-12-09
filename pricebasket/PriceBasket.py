import argparse

products_in_customers_basket = {}
available_products_in_store = {
    'Apples': 1,
    'Bread': 0.8,
    'Milk': 1.3,
    'Soup': 0.65
}


def format_price(price):
    return '£{:,.2f}'.format(price)  # ':,' adds comma for thousand values and '.2f' rounds to 2dp


class Product:
    @staticmethod
    def get_price(product):
        try:
            return available_products_in_store[product]
        except Exception:
            print(f'\'{product}\' is not currently available in store')
            return 0


class Offer:
    def __init__(self, offer_product, percentage_off):
        """ All Offers need to have offer_product and percentage_off."""
        self.offer_product = offer_product
        self.percentage_off = percentage_off

    def calculate_offer_discount(self):
        return Product.get_price(self.offer_product) * self.percentage_off * .01

    def get_promotion_message(self, discount_amount):
        # each new promotion is required to have this method
        pass

    def calculate_total_offer_discount_for_basket(self, basket):
        # each new promotion is required to have this method
        pass


class PercentageDiscountOffer(Offer):
    """ Offer here is get a percentage discount on product if product is in basket."""
    def __init__(self, offer_product, percentage_off):
        super().__init__(offer_product, percentage_off)
        self.offer_product = offer_product

    def get_promotion_message(self, discount_amount):
        return f'  {self.offer_product} {self.percentage_off}% off: {format_price(discount_amount)}'

    def calculate_total_offer_discount_for_basket(self, basket):
        return round((super().calculate_offer_discount() * Basket(basket).get_item_quantity(self.offer_product)), 2)
        # discount_amount can be multiplied by offer_product quantity


class BuyXGetYDiscountOffer(Offer):
    """ Offer here is get a percentage discount on a product if we have required quantity of additional_product_required in basket."""
    def __init__(self, offer_product, percentage_off, additional_product_required, additional_product_quantity_required):
        super().__init__(offer_product, percentage_off)
        self.offer_product = offer_product
        self.additional_product_required = additional_product_required
        self.additional_product_quantity_required = additional_product_quantity_required

    def get_promotion_message(self, discount_amount):
        return f'  {self.percentage_off}% off {self.offer_product} when buying ' \
               f'{self.additional_product_quantity_required} {self.additional_product_required}s: {format_price(discount_amount)}'

    def calculate_total_offer_discount_for_basket(self, basket):
        additional_product_quantity = Basket(basket).get_item_quantity(self.additional_product_required)
        if additional_product_quantity >= self.additional_product_quantity_required:
            # get multiple of required product in basket
            promo_limit = round(additional_product_quantity / self.additional_product_quantity_required)
            # discount_amount can be multiplied by multiple of (required combination of products), dependent on no. of offer_product in basket
            return round((super().calculate_offer_discount() * min(promo_limit, Basket(basket).get_item_quantity(self.offer_product))), 2)
        else:
            return 0


class Basket:
    def __init__(self, basket_products):
        self.basket_products = basket_products

    @staticmethod
    def get_item_quantity(item):
        try:
            return products_in_customers_basket[item]
        except Exception as e:
            print(e.type())
            print(f'\'{item}\' is not in Customer\'s basket')
            return 0

    def update_customer_basket(self):
        products_in_customers_basket.clear()
        distinct_basket_products = set(self.basket_products)
        for item in distinct_basket_products:
            products_in_customers_basket.update({item: self.basket_products.count(item)})
        return products_in_customers_basket


class PriceCalculator:
    def __init__(self, basket):
        self.basket = Basket(basket)
        self.basket.update_customer_basket()

    def calculate_basket_subtotal(self):
        subtotal = 0
        for item in products_in_customers_basket:
            subtotal += Product.get_price(item) * self.basket.get_item_quantity(item)
        return round(subtotal, 2)

    def calculate_basket_with_promotions_applied(self, offers):
        subtotal = self.calculate_basket_subtotal()

        offer_discount_available = False
        for offer in offers:
            if offer.calculate_total_offer_discount_for_basket(self.basket) > 0:
                offer_discount_available = True

        if offer_discount_available:
            print(f'Subtotal: {format_price(subtotal)}')
            print('Offers applied:')
            for offer in offers:
                if offer.calculate_total_offer_discount_for_basket(self.basket) > 0:
                    promotion_discount = offer.calculate_total_offer_discount_for_basket(self.basket)
                    print(offer.get_promotion_message(promotion_discount))
                    subtotal -= promotion_discount
        else:
            print(f'Subtotal: {format_price(subtotal)} (No offers available)')

        print(f'Total: {format_price(subtotal)}')


# add offers
offer_1 = PercentageDiscountOffer(offer_product='Apples', percentage_off=10)
offer_2 = BuyXGetYDiscountOffer(offer_product='Bread', percentage_off=50, additional_product_required='Soup', additional_product_quantity_required=2)

available_offers = [offer_1, offer_2]

parser = argparse.ArgumentParser()
parser.add_argument("items", type=str, nargs='+')  # nargs='+' here means at least one value required with no limit of how many arguments (items) could be added
args = parser.parse_args()

if __name__ == '__main__':
    PriceCalculator(args.items).calculate_basket_with_promotions_applied(available_offers)
    print(products_in_customers_basket)
