import argparse

products = {
    'Apples': 1.00,
    'Bread': 0.80,
    'Milk': 1.30,
    'Soup': 0.65
}

current_offers = {
    'Apples': ['percentage_discount', 10],  #  schema = item: ['discount_type', percentage_off, required_product, required_product_amount]
    'Bread': ['buy_x_get_x_discount', 50, 'Soup', 2]
}


def get_price(item):
    return products[item]

def format_price(price):
    return '£{:,.2f}'.format(price)  # ':,' adds comma for thousand values and '.2f' rounds to 2dp


class Basket:
    def __init__(self, basket):
        self.basket = basket

    def get_item_quantity(self, item):
        item_quantity = 0
        for content in self.basket:
            if content == item:
                item_quantity = item_quantity + 1
        return item_quantity


class Offer:
    def __init__(self, offers):
        self.offers = offers

    def check_if_item_on_offer(self, product):
        return product in self.offers

    def get_promo_message(self, product):
        return f'  {product} {self.get_percentage_amount(product)}% off: {format_price(self.get_discount_amount(product))}'

    def get_offer_details(self, product):
        if (self.check_if_item_on_offer(product)):
            return self.offers[product]
        else:
            print(f'{product} is not currently on offer')

    def get_offer_type(self, product):
        if (self.check_if_item_on_offer(product)):
            return self.get_offer_details(product)[0]
        else:
            print(f'{product} is not currently on offer')

    def get_percentage_amount(self, product):
        if (self.check_if_item_on_offer(product)):
            return self.get_offer_details(product)[1]
        else:
            print(f'{product} is not currently on offer')

    def get_discount_amount(self, product):
        if (self.check_if_item_on_offer(product)):
            return self.get_offer_details(product)[1] * .01
        else:
            print(f'{product} is not currently on offer')

    def get_required_item(self, product):
        if (self.check_if_item_on_offer(product)):
            try:
                return self.get_offer_details(product)[2]
            except:
                print(f'{product} doesn\'t need required item for offer')
        else:
            print(f'{product} is not currently on offer')

    def get_required_item_quantity(self, product):
        if (self.check_if_item_on_offer(product)):
            try:
                return self.get_offer_details(product)[3]
            except:
                print(f'{product} doesn\'t need required item quantity for offer')
        else:
            print(f'{product} is not currently on offer')


class CalculateDiscount:
    def __init__(self, Offer, product):
        self.Offer = Offer
        self.product = product

    def calculate_percentage_discount(self):
        return get_price(self.product) * self.Offer.get_discount_amount(self.product)

    def calculate_buy_x_get_x_discount(self, basket):
        if (Basket(basket).get_item_quantity(self.Offer.get_required_item(self.product)) >= self.Offer.get_required_item_quantity(self.product)):
            return self.calculate_percentage_discount()
        else:
            return 0

    def get_discount_amount(self, basket):
        if (self.Offer.check_if_item_on_offer(self.product)):
            if self.Offer.get_offer_type(self.product) == 'percentage_discount':
                return self.calculate_percentage_discount()
            elif self.Offer.get_offer_type(self.product) == 'buy_x_get_x_discount':
                return self.calculate_buy_x_get_x_discount(basket)
        else:
            return 0


class PriceCalculator:
    def __init__(self, basket):
        self.basket = basket

    def calculate_basket(self):
        subtotal = 0
        for item in self.basket:
            subtotal = subtotal + get_price(item)
        return round(subtotal, 2)

    def price_basket(self):
        subtotal = self.calculate_basket()
        formatted_subtotal = format_price(subtotal)
        offers = Offer(current_offers)

        if offers.check_if_item_on_offer('Apples'):
            apples_discount = round(CalculateDiscount(offers, 'Apples').get_discount_amount(self.basket), 2)

        if offers.check_if_item_on_offer('Bread'):
            bread_discount = round(CalculateDiscount(offers, 'Bread').get_discount_amount(self.basket), 2)

        if offers.check_if_item_on_offer('Soup'):
            milk_discount = round(CalculateDiscount(offers, 'Soup').get_discount_amount(self.basket), 2)

        if offers.check_if_item_on_offer('Milk'):
            soup_discount = round(CalculateDiscount(offers, 'Milk').get_discount_amount(self.basket), 2)

        # check for special offers
        if apples_discount > 0 or bread_discount > 0 or milk_discount > 0 or soup_discount > 0:
            print(f'Subtotal: {formatted_subtotal}')
            print('Offers applied:')
            try:
                if apples_discount > 0:
                    print(offers.get_promo_message('Apples'))
                    subtotal = subtotal - apples_discount
                if bread_discount > 0:
                    print(offers.get_promo_message('Bread'))
                    subtotal = subtotal - bread_discount
                if milk_discount > 0:
                    print(offers.get_promo_message('Milk'))
                    subtotal = subtotal - milk_discount
                if soup_discount > 0:
                    print(offers.get_promo_message('Soup'))
                    subtotal = subtotal - soup_discount
            except:
                'Exception if any discount_value is undefined'
        else:
            print(f'Subtotal: {formatted_subtotal} (No offers available)')

        print(f'Total: {format_price(subtotal)}')


parser = argparse.ArgumentParser()
parser.add_argument("items", type=str, nargs='+')  # nargs='+' here means at least one value required with no limit of how many arguments (items) could be added
args = parser.parse_args()

if __name__ == '__main__':
    PriceCalculator(args.items).price_basket()
