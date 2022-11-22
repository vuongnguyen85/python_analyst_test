import sys

products = {
    'Apples': 1.00,
    'Bread': 0.80,
    'Milk': 1.30,
    'Soup': 0.65
}

def getPrice(item):
    return products[item]

def listContainsApples(items):
    global appleDiscount
    appleDiscount = False
    for item in items:
        if item == 'Apples':
            appleDiscount = True
    return appleDiscount

def listContainsAtLeastTwoSoups(items):
    global soupCount
    soupCount = 0
    for item in items:
        if item == 'Soup':
            soupCount = soupCount + 1
    return soupCount >= 2

def listContainsBread(items):
    global breadCount
    breadCount = 0
    for item in items:
        if item == 'Bread':
            breadCount = breadCount + 1
    return breadCount >= 1

def calculateApplesDiscount(items):
    global appleDiscountValue
    appleDiscountValue = 0
    for item in items:
        if item == 'Apples':
            appleDiscountValue = appleDiscountValue + (products[item] * .1)
    return round(appleDiscountValue, 2)

def calculateBreadDiscount(items):
    global breadDiscountValue
    breadDiscountValue = 0
    if listContainsBread(items) and listContainsAtLeastTwoSoups(items):
        breadDiscountValue = breadDiscountValue + (products["Bread"] * .5)
    return round(breadDiscountValue, 2)

def calculateBasket(items):
    subtotal = 0
    for item in items:
        subtotal = subtotal + products[item]
    return round(subtotal, 2)

def formatPrice(price):
    return '£{:,.2f}'.format(price) # ':,' adds comma for thousand values and '.2f' rounds to 2dp

def priceBasket(item1, item2, item3):
    items = [item1, item2, item3]
    subtotal = calculateBasket(items)
    formattedSubtotal = formatPrice(subtotal)
    appleDiscountValue = calculateApplesDiscount(items)
    breadDiscountValue = calculateBreadDiscount(items)

    # check for special offers
    if listContainsApples(items):
        print(f'Subtotal: {formattedSubtotal}')
        formattedAppleDiscountValue = formatPrice(appleDiscountValue)
        print(f'Apples 10% off: {formattedAppleDiscountValue}')
        newTotal = subtotal - appleDiscountValue
        formattedNewTotal = formatPrice(newTotal)
    elif listContainsAtLeastTwoSoups(items) and listContainsBread(items):
        print(f'Subtotal: {formattedSubtotal}')
        formattedBreadDiscountValue = formatPrice(breadDiscountValue)
        print(f'Half price loaf of bread with 2 tins of Soup: {formattedBreadDiscountValue}')
        newTotal = subtotal - breadDiscountValue
        formattedNewTotal = formatPrice(newTotal)
    else:
        print(f'Subtotal: {formattedSubtotal} (No offers available)')

    # print total, reuse subtotal if no offers
    try:
        print(f'Total: {formattedNewTotal}')
    except:
        print(f'Total: {formattedSubtotal}')

if __name__ == '__main__':
    priceBasket(sys.argv[1], sys.argv[2], sys.argv[3])