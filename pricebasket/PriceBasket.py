import argparse

products = {}
current_offers = {}

def format_price(price):
    return '£{:,.2f}'.format(price)  # ':,' adds comma for thousand values and '.2f' rounds to 2dp

def get_price(product):
    return products[product]


class AddProduct:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        products.update({self.name: self.price})


class CreateOffer:
    def __init__(self, product, type, percentage_discount, additional_required_product = '', additional_required_product_qty = 0):
        self.product = product
        self.type = type
        current_offers.update({product: [self._type, percentage_discount, additional_required_product, additional_required_product_qty]})

class PercentageDiscountOffer(CreateOffer):
    _type = 'percentage_discount'
    def __init__(self, product, percentage_discount):
        super().__init__(product, self._type, percentage_discount)


class BuyXGetYDiscountOffer(CreateOffer):
    _type = 'buy_x_get_y_discount'
    def __init__(self, product, percentage_discount, additional_required_product, additional_required_product_qty):
        super().__init__(product, self._type, percentage_discount, additional_required_product, additional_required_product_qty)


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

    def check_if_item_on_offer(self, offer_product):
        return offer_product in self.offers

    def get_offer_details(self, offer_product):
        return self.offers[offer_product]

    def get_offer_type(self, offer_product):
        if self.check_if_item_on_offer(offer_product):
            return self.get_offer_details(offer_product)[0]
        else:
            print(f'item is not on offer')

    def get_percentage_amount(self, offer_product):
        if self.check_if_item_on_offer(offer_product):
            return self.get_offer_details(offer_product)[1]
        else:
            print(f'item is not on offer')

    def get_required_item(self, offer_product):
        if self.check_if_item_on_offer(offer_product):
            try:
                return self.get_offer_details(offer_product)[2]
            except:
                print(f'offer item doesn\'t have required item')
        else:
            print(f'item is not on offer')

    def get_required_item_quantity(self, offer_product):
        if self.check_if_item_on_offer(offer_product):
            try:
                return self.get_offer_details(offer_product)[3]
            except:
                print(f'offer item doesn\'t have required item')
        else:
            print(f'item is not on offer')

    def calculate_percentage_discount(self, offer_product):
        return get_price(offer_product) * self.get_percentage_amount(offer_product) * .01

    def calculate_buy_x_get_x_discount(self, basket, offer_product):
        if Basket(basket).get_item_quantity(self.get_required_item(offer_product)) >= self.get_required_item_quantity(offer_product):
            return self.calculate_percentage_discount(offer_product)
        else:
            return 0

    def get_product_discount_amount(self, basket, offer_product):
        if self.check_if_item_on_offer(offer_product):
            offer_product_quantity = Basket(basket).get_item_quantity(offer_product)
            if self.get_offer_type(offer_product) == 'percentage_discount':
                return round((self.calculate_percentage_discount(offer_product) * offer_product_quantity), 2)  # discount_amount can be multiplied by offer_product quantity
            elif self.get_offer_type(offer_product) == 'buy_x_get_y_discount':
                promo_limit = round(Basket(basket).get_item_quantity(self.get_required_item(offer_product)) / self.get_required_item_quantity(offer_product))
                return round((self.calculate_buy_x_get_x_discount(basket, offer_product) * min(promo_limit, offer_product_quantity)), 2)
                # discount_amount can be multiplied by multiple of (required set of products), dependent on no. of offer_product in basket
        else:
            return 0

    def get_promo_message(self, discount_amount, product):
        return f'  {product} {self.get_percentage_amount(product)}% off: {format_price(discount_amount)}'


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
            apples_discount_amt = round(offers.get_product_discount_amount(self.basket, 'Apples'), 2)
        if offers.check_if_item_on_offer('Bread'):
            print(offers.get_product_discount_amount(self.basket, 'Bread'))
            bread_discount_amt = round(offers.get_product_discount_amount(self.basket, 'Bread'), 2)

        if offers.check_if_item_on_offer('Soup'):
            milk_discount_amt = round(offers.get_product_discount_amount(self.basket, 'Soup'), 2)
        if offers.check_if_item_on_offer('Milk'):
            soup_discount_amt = round(offers.get_product_discount_amount(self.basket, 'Milk'), 2)

        # check for special offers
        if apples_discount_amt > 0 or bread_discount_amt > 0 or milk_discount_amt > 0 or soup_discount_amt > 0:
            print(f'Subtotal: {formatted_subtotal}')
            print('Offers applied:')
            try:
                if apples_discount_amt > 0:
                    print(offers.get_promo_message(apples_discount_amt, 'Apples'))
                    subtotal = subtotal - apples_discount_amt
                if bread_discount_amt > 0:
                    print(offers.get_promo_message(bread_discount_amt, 'Bread'))
                    subtotal = subtotal - bread_discount_amt
                if milk_discount_amt > 0:
                    print(offers.get_promo_message(milk_discount_amt, 'Milk'))
                    subtotal = subtotal - milk_discount_amt
                if soup_discount_amt > 0:
                    print(offers.get_promo_message(soup_discount_amt, 'Soup'))
                    subtotal = subtotal - soup_discount_amt
            except:
                'Exception if any discount_value is undefined'
        else:
            print(f'Subtotal: {formatted_subtotal} (No offers available)')

        print(f'Total: {format_price(subtotal)}')


# add products
apples = AddProduct('Apples', 1.00)  #  schema = (product, price)
bread = AddProduct('Bread', 0.80)
milk = AddProduct('Milk', 1.30)
soup = AddProduct('Soup', 0.65)

# add offers
apple_promo = PercentageDiscountOffer('Apples', 10)  #  schema = (offer_product, percentage_off)
bread_promo = BuyXGetYDiscountOffer('Bread', 50, 'Soup', 2)  #  schema = item: [offer_product, percentage_off, required_product, required_product_amount]


parser = argparse.ArgumentParser()
parser.add_argument("items", type=str, nargs='+')  # nargs='+' here means at least one value required with no limit of how many arguments (items) could be added
args = parser.parse_args()


if __name__ == '__main__':
    PriceCalculator(args.items).price_basket()
