import argparse
import csv
from abc import abstractmethod


class Product:
    def __init__(self, product_name, price):
        self.product_name = product_name
        self.price = float(price)

    def get_name(self):
        return self.product_name

    def get_price(self):
        return self.price


class Basket:
    basket_with_qty = {}
    def __init__(self, available_products_in_store):
        self.basket = {}
        self.available_products_in_store = available_products_in_store

    def get_basket(self):
        return self.basket

    def add_to_basket(self, products=[]):
        # get quantity of each product in basket (also check that they are available in store
        for product in products:
            for item in self.available_products_in_store:
                if item.get_name() == product:
                    self.basket_with_qty.update({item.product_name: int(products.count(product))})

        # create dict of Product class with quantity
        for product, quantity in self.basket_with_qty.items():
            for item in self.available_products_in_store:
                if item.get_name() == product:
                    self.basket.update({Product(item.get_name(), item.get_price()): quantity})

    def check_product_is_available(self, product):
        for item in self.available_products_in_store:
            if item.get_name() == product:
                return True
        return False

    def get_product_quantity_in_basket(self, product_name):
        try:
            for product, quantity in self.get_basket().items():
                if product_name == product.get_name():
                    return quantity
        except KeyError:
            return 0

    def calculate_basket_subtotal(self):
        subtotal = 0
        for product, quantity in self.get_basket().items():
            subtotal += product.get_price() * quantity
        return round(subtotal, 2)

    def get_product_price(self, product_name):
        for product, quantity in self.get_basket().items():
            if product_name == product.get_name():
                return product.get_price()


class Offer:
    def __init__(self, offer_product, percentage_off):
        """ All Offers need to have offer_product and percentage_off."""
        self.offer_product = offer_product
        self.percentage_off = int(percentage_off)

    def calculate_offer_discount(self, basket):
        return basket.get_product_price(self.offer_product) * self.percentage_off * .01

    @abstractmethod
    def get_promotion_message(self, basket):
        # print promotion message base on offer type
        pass

    @abstractmethod
    def calculate_total_offer_discount_for_basket(self, basket):
        # calculate the total discount available based on offer and basket
        pass


class PercentageDiscountOffer(Offer):
    """ Offer here is get a percentage discount on product if product is in basket."""
    def __init__(self, offer_product, percentage_off):
        super().__init__(offer_product, percentage_off)
        self.offer_product = offer_product

    def get_promotion_message(self, basket):
        return f'  {self.offer_product} {self.percentage_off}% off: {Util.format_price(self.calculate_total_offer_discount_for_basket(basket))}'

    def calculate_total_offer_discount_for_basket(self, basket):
        return round((super().calculate_offer_discount(basket) * basket.get_product_quantity_in_basket(self.offer_product)), 2)
        # discount_amount can be multiplied by offer_product quantity


class BuyXGetYDiscountOffer(Offer):
    """ Offer here is get a percentage discount on a product if we have required quantity of additional_product_required in basket."""
    def __init__(self, offer_product, percentage_off, additional_product_required, additional_product_quantity_required):
        super().__init__(offer_product, percentage_off)
        self.offer_product = offer_product
        self.additional_product_required = additional_product_required
        self.additional_product_quantity_required = int(additional_product_quantity_required)

    def get_promotion_message(self, basket):
        return f'  {self.percentage_off}% off {self.offer_product} when buying ' \
               f'{self.additional_product_quantity_required} {self.additional_product_required}s: {Util.format_price(self.calculate_total_offer_discount_for_basket(basket))}'

    def calculate_total_offer_discount_for_basket(self, basket):
        additional_product_quantity = basket.get_product_quantity_in_basket(self.additional_product_required)
        if additional_product_quantity >= self.additional_product_quantity_required:
            # get multiple of (required combination of products), in basket
            promo_limit = round(additional_product_quantity / self.additional_product_quantity_required)
            # discount_amount can be multiplied by minimum value between multiple of (required combination of products) and quantity of offer_product in basket
            return round((super().calculate_offer_discount(basket) * min(promo_limit, basket.get_product_quantity_in_basket(self.offer_product))), 2)
        else:
            return 0


class PriceCalculator:
    def __init__(self, Basket, list_of_available_offers):
        self.basket = Basket
        self.current_offers = list_of_available_offers

    def offers_can_be_applied_to_basket(self):
        for offer in self.current_offers:
            if offer.calculate_total_offer_discount_for_basket(self.basket) > 0:
                return True
        else:
            return False

    def calculate_basket_with_offers_applied(self, subtotal):
        print(f'Subtotal: {Util.format_price(subtotal)}')
        print('Offers applied:')
        for offer in self.current_offers:
            if offer.calculate_total_offer_discount_for_basket(self.basket) > 0:
                offer_discount = offer.calculate_total_offer_discount_for_basket(self.basket)
                print(offer.get_promotion_message(self.basket))
                subtotal -= offer_discount
        print(f'Total: {Util.format_price(subtotal)}')

    def calculate_basket_with_no_offers_applied(self, subtotal):
        print(f'Subtotal: {Util.format_price(subtotal)} (No offers available)')
        print(f'Total: {Util.format_price(subtotal)}')

    def calculate_customer_basket(self):
        subtotal = self.basket.calculate_basket_subtotal()

        if self.offers_can_be_applied_to_basket():
            self.calculate_basket_with_offers_applied(subtotal)
        else:
            self.calculate_basket_with_no_offers_applied(subtotal)


class Util:
    @staticmethod
    def format_price(price):
        if price < 0:
            return 'price can\'t be less than 0.'
        elif price < 1:
            price_in_pence = round(price * 100)
            return f'{price_in_pence}p'
        else:
            return '£{:,.2f}'.format(price)  # ':,' adds comma for thousand values and '.2f' rounds to 2dp

    @staticmethod
    def read_csv(path):
        with open(path, 'r') as f:
            return list(csv.reader(f))

    @staticmethod
    def get_available_products_in_store():
        available_products_in_store = []
        for row in Util.read_csv('data/products.csv')[1:]:
            available_products_in_store.append(Product(row[0], row[1]))
        return available_products_in_store

    @staticmethod
    def get_current_offers():
        current_offers = []
        for row in Util.read_csv('data/current_offers.csv')[1:]:
            try:
                current_offers.append(BuyXGetYDiscountOffer(row[0], row[1], row[2], row[3]))
            except Exception:
                current_offers.append(PercentageDiscountOffer(row[0], row[1]))
        return current_offers


if __name__ == '__main__':
    available_products_in_store = Util.get_available_products_in_store()
    current_offers = Util.get_current_offers()

    parser = argparse.ArgumentParser()
    parser.add_argument("items", type=str, nargs='+')  # nargs='+' here means at least one value required with no limit of how many arguments (products) could be added
    args = parser.parse_args()

    basket = Basket(available_products_in_store)
    basket.add_to_basket(args.items)

    PriceCalculator(basket, current_offers).calculate_customer_basket()
