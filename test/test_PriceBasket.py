import unittest
from main.PriceBasket import getPrice, calculateBasket, listContainsApples, \
    listContainsAtLeastTwoSoups, calculateApplesDiscount, calculateBreadDiscount, listContainsBread, formatPrice

class TestPriceBasket(unittest.TestCase):

    def test_itemPrices(self):
        self.assertEqual(getPrice('Apples'), 1)
        self.assertEqual(getPrice('Bread'), 0.8)
        self.assertEqual(getPrice('Milk'), 1.3)
        self.assertEqual(getPrice('Soup'), 0.65)

    def test_containsApples(selfs):
        selfs.assertEqual(listContainsApples(['Apples', 'Apples', 'Apples']), True)
        selfs.assertEqual(listContainsApples(['Apples', 'Bread', 'Apples']), True)
        selfs.assertEqual(listContainsApples(['Apples', 'Bread', 'Milk']), True)
        selfs.assertEqual(listContainsApples(['Soup', 'Bread', 'Milk']), False)

    def test_containsTwoSoups(selfs):
        selfs.assertEqual(listContainsAtLeastTwoSoups(['Soup', 'Soup', 'Soup']), True)
        selfs.assertEqual(listContainsAtLeastTwoSoups(['Soup', 'Bread', 'Soup']), True)
        selfs.assertEqual(listContainsAtLeastTwoSoups(['Apples', 'Bread', 'Soup']), False)
        selfs.assertEqual(listContainsAtLeastTwoSoups(['Apples', 'Bread', 'Milk']), False)

    def test_containsBread(selfs):
        selfs.assertEqual(listContainsBread(['Apples', 'Apples', 'Apples']), False)
        selfs.assertEqual(listContainsBread(['Apples', 'Bread', 'Apples']), True)
        selfs.assertEqual(listContainsBread(['Bread', 'Bread', 'Milk']), True)
        selfs.assertEqual(listContainsBread(['Bread', 'Bread', 'Bread']), True)

    def test_calculateApplesDiscount(selfs):
        selfs.assertEqual(calculateApplesDiscount(['Apples', 'Apples', 'Apples']), 0.3)
        selfs.assertEqual(calculateApplesDiscount(['Apples', 'Bread', 'Apples']), 0.2)
        selfs.assertEqual(calculateApplesDiscount(['Apples', 'Bread', 'Milk']), 0.1)
        selfs.assertEqual(calculateApplesDiscount(['Soup', 'Bread', 'Milk']), 0)

    def test_calculateBreadDiscount(selfs):
        selfs.assertEqual(calculateBreadDiscount(['Bread', 'Soup', 'Soup']), 0.4)
        selfs.assertEqual(calculateBreadDiscount(['Soup', 'Bread', 'Soup']), 0.4)
        selfs.assertEqual(calculateBreadDiscount(['Apples', 'Bread', 'Milk']), 0)
        selfs.assertEqual(calculateBreadDiscount(['Soup', 'Bread', 'Milk']), 0)

    def test_formatPrice(self):
        self.assertEqual(formatPrice(0.41), '£0.41')
        self.assertEqual(formatPrice(1.01), '£1.01')
        self.assertEqual(formatPrice(3.00), '£3.00')

    def test_calculateBasket(selfs):
        selfs.assertEqual(calculateBasket(['Apples', 'Bread', 'Milk']), 3.1)
        selfs.assertEqual(calculateBasket(['Milk', 'Apples', 'Bread']), 3.1)
        selfs.assertEqual(calculateBasket(['Apples', 'Bread', 'Soup']), 2.45)

if __name__ == '__main__':
    unittest.main()