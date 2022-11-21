import sys

products = {
    'Apples': 1.00,
    'Bread': 0.80,
    'Milk': 1.30,
    'Soup': 0.65
}

appleDiscount = False
soupCount = 0
breadCount = 0

def getPrice(item):
    return products[item]

def calculateBasket(items):
    subtotal = 0
    for item in items:
        if item == 'Apples':
            global appleDiscountValue
            global appleDiscount
            appleDiscount = True
            appleDiscountValue = products[item] * .1
        elif item == 'Soup':
            global soupCount
            soupCount = soupCount + 1
        elif item == 'Bread':
            global breadCount
            global breadDiscountValue
            breadCount = breadCount + 1
            breadDiscountValue = products[item] * .5
        subtotal = subtotal + products[item]
    return subtotal

def formatPrice(price):
    return '£{:,.2f}'.format(price)

def priceBasket(item1, item2, item3):
    items = [item1, item2, item3]
    subtotal = calculateBasket(items)
    formattedSubtotal = formatPrice(subtotal) # ':,' adds comma for thousand values and '.2f' rounds to 2dp
    if appleDiscount or soupCount >= 2:
        if appleDiscount:
            print(f'Subtotal: {formattedSubtotal}')
            formattedAppleDiscountValue = formatPrice(appleDiscountValue)
            print(f'Apples 10% off: {formattedAppleDiscountValue}')
            newTotal = subtotal - appleDiscountValue
            formattedNewTotal = formatPrice(newTotal)
            print(f'Total: {formattedNewTotal}')
        elif soupCount >= 2 and breadCount >= 1:
            print(f'Subtotal: {formattedSubtotal}')
            formattedBreadDiscountValue = formatPrice(breadDiscountValue)
            print(f'Half price loaf of bread with 2 tins of Soup: {formattedBreadDiscountValue}')
            newTotal = subtotal - breadDiscountValue
            formattedNewTotal = formatPrice(newTotal)
            print(f'Total: {formattedNewTotal}')
        else:
            print(f'Subtotal: {formattedSubtotal} (No offers available - No bread in basket for bread offer)')
            print(f'Total: {formattedSubtotal}')
    else:
        print(f'Subtotal: {formattedSubtotal} (No offers available)')
        print(f'Total: {formattedSubtotal}')

if __name__ == '__main__':
    priceBasket(sys.argv[1], sys.argv[2], sys.argv[3])