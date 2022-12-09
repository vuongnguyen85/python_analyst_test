Python Analyst Exercise
===============

This app is used to calculate a shopping basket. We currently have the following items:
- Apples
- Bread
- Milk
- Soup

### Managing products
Inside PriceBasket.py, we can add as many products from line 4 by adding to current list, giving 'product_name' and 'product_price'.

### Managing Offers
We currently have 2 types of Offers created. We can amend the following from line 135 for the existing offers:
* offer_product
* percentage_off
* additional_product_required
* additional_product_quantity_required

If we want to create new offers, see next section. 

### Creating new offers
- To create a new offer type, we need to make use of the Offer class (see line 44 and 58 for details). 
- We need to define functions for get_promotion_message and calculate_total_offer_discount_for_basket.  

## Running Instructions
We can run the price basket app by entering the following input in the command line:

```
python3 main/PriceBasket.py item1 item2 item3
```

e.g. 
```
python3 main/PriceBasket.py Apples Bread Soup
```

Note: We can add as many items as we want, separated by a space. The only requirement is that we need to have at least one item.
