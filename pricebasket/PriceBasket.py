import argparse
import csv


class Product:
    def __init__(self, product_name, price):
        self.product_name = product_name
        self.price = float(price)

    def get_name(self):
        return self.product_name

    def get_price(self):
        return self.price


class Basket:
    def __init__(self, products):
        self.basket = {}
        self.products = products

    def get_basket(self):
        return self.basket

    def add_to_basket(self, available_products_in_store):
        for product in self.products:
            for item in available_products_in_store:
                if item.get_name() == product:
                    self.basket.update({product: int(self.products.count(product))})

    def get_product_quantity_in_basket(self, product_name):
        try:
            return self.get_basket()[product_name]
        except KeyError:
            return 0

    def calculate_basket_subtotal(self, available_products_in_store):
        subtotal = 0
        for product_name, quantity in self.get_basket().items():
            subtotal += Util.get_product_price(product_name, available_products_in_store) * quantity
        return round(subtotal, 2)


class Offer:
    def __init__(self, offer_product, percentage_off):
        """ All Offers need to have offer_product and percentage_off."""
        self.offer_product = offer_product
        self.percentage_off = int(percentage_off)

    def calculate_offer_discount(self, available_products_in_store):
        return Util.get_product_price(self.offer_product, available_products_in_store) * self.percentage_off * .01

    def get_promotion_message(self, basket, available_products_in_store):
        # each new promotion is required to have this method
        pass

    def calculate_total_offer_discount_for_basket(self, basket, available_products_in_store):
        # each new promotion is required to have this method
        pass


class PercentageDiscountOffer(Offer):
    """ Offer here is get a percentage discount on product if product is in basket."""
    def __init__(self, offer_product, percentage_off):
        super().__init__(offer_product, percentage_off)
        self.offer_product = offer_product

    def get_promotion_message(self, basket, available_products_in_store):
        return f'  {self.offer_product} {self.percentage_off}% off: {Util.format_price(self.calculate_total_offer_discount_for_basket(basket, available_products_in_store))}'

    def calculate_total_offer_discount_for_basket(self, basket, available_products_in_store):
        return round((super().calculate_offer_discount(available_products_in_store) * basket.get_product_quantity_in_basket(self.offer_product)), 2)
        # discount_amount can be multiplied by offer_product quantity


class BuyXGetYDiscountOffer(Offer):
    """ Offer here is get a percentage discount on a product if we have required quantity of additional_product_required in basket."""
    def __init__(self, offer_product, percentage_off, additional_product_required, additional_product_quantity_required):
        super().__init__(offer_product, percentage_off)
        self.offer_product = offer_product
        self.additional_product_required = additional_product_required
        self.additional_product_quantity_required = int(additional_product_quantity_required)

    def get_promotion_message(self, basket, available_products_in_store):
        return f'  {self.percentage_off}% off {self.offer_product} when buying ' \
               f'{self.additional_product_quantity_required} {self.additional_product_required}s: {Util.format_price(self.calculate_total_offer_discount_for_basket(basket, available_products_in_store))}'

    def calculate_total_offer_discount_for_basket(self, basket, available_products_in_store):
        additional_product_quantity = basket.get_product_quantity_in_basket(self.additional_product_required)
        if additional_product_quantity >= self.additional_product_quantity_required:
            # get multiple of (required combination of products), in basket
            promo_limit = round(additional_product_quantity / self.additional_product_quantity_required)
            # discount_amount can be multiplied by minimum value between multiple of (required combination of products) and quantity of offer_product in basket
            return round((super().calculate_offer_discount(available_products_in_store) * min(promo_limit, basket.get_product_quantity_in_basket(self.offer_product))), 2)
        else:
            return 0


class PriceCalculator:
    def __init__(self, Basket, list_of_available_offers, available_products_in_store):
        self.basket = Basket
        self.current_offers = list_of_available_offers
        self.available_products_in_store = available_products_in_store

    def offers_can_be_applied_to_basket(self):
        for offer in self.current_offers:
            if offer.calculate_total_offer_discount_for_basket(self.basket, self.available_products_in_store) > 0:
                return True
        else:
            return False

    def calculate_basket_with_offers_applied(self, subtotal):
        print(f'Subtotal: {Util.format_price(subtotal)}')
        print('Offers applied:')
        for offer in self.current_offers:
            if offer.calculate_total_offer_discount_for_basket(self.basket, self.available_products_in_store) > 0:
                offer_discount = offer.calculate_total_offer_discount_for_basket(self.basket, self.available_products_in_store)
                print(offer.get_promotion_message(self.basket, self.available_products_in_store))
                subtotal -= offer_discount
        print(f'Total: {Util.format_price(subtotal)}')

    def calculate_basket_with_no_offers_applied(self, subtotal):
        print(f'Subtotal: {Util.format_price(subtotal)} (No offers available)')
        print(f'Total: {Util.format_price(subtotal)}')

    def calculate_customer_basket(self):
        subtotal = self.basket.calculate_basket_subtotal(self.available_products_in_store)

        if self.offers_can_be_applied_to_basket():
            self.calculate_basket_with_offers_applied(subtotal)
        else:
            self.calculate_basket_with_no_offers_applied(subtotal)


class Util:
    @staticmethod
    def format_price(price):
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

    @staticmethod
    def get_product_price(product_name, available_products_in_store):
        for item in available_products_in_store:
            if item.get_name() == product_name:
                return item.get_price()


if __name__ == '__main__':
    available_products_in_store = Util.get_available_products_in_store()
    current_offers = Util.get_current_offers()

    parser = argparse.ArgumentParser()
    parser.add_argument("items", type=str, nargs='+')  # nargs='+' here means at least one value required with no limit of how many arguments (products) could be added
    args = parser.parse_args()

    basket = Basket(args.items)
    basket.add_to_basket(available_products_in_store)

    PriceCalculator(basket, current_offers, available_products_in_store).calculate_customer_basket()
