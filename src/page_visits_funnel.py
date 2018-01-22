import pandas as pd

visits = pd.read_csv('visits.csv',parse_dates=[1])
cart = pd.read_csv('cart.csv', parse_dates=[1])
checkout = pd.read_csv('checkout.csv',parse_dates=[1])
purchase = pd.read_csv('purchase.csv',parse_dates=[1])


# print(visits.head(100))
# print(cart.head(100))
# print(checkout.head(100))
# print(purchase.head(100))


visits_cart = pd.merge(visits,cart,how='left')

added_to_cart = (1 - (len(visits_cart[pd.notnull(visits_cart['cart_time'])])/float(len(visits_cart)))) * 100

# print(added_to_cart)

cart_checkout = pd.merge(cart,checkout,how='left')


cart_to_checkout = (1 - (len(cart_checkout[pd.notnull(cart_checkout['checkout_time'])])/float(len(cart_checkout)))) * 100

# print(cart_to_checkout)

all_data = pd.merge(visits,cart,how='left').merge(checkout,how='left').merge(purchase,how='left')

# print(all_data)

checkout_no_purchase = (1 - (len(all_data[(pd.notnull(all_data['visit_time'])) & (pd.notnull(all_data['cart_time'])) & (pd.notnull(all_data['checkout_time']))])/float(len(all_data)))) * 100

cart_df = all_data[pd.notnull(all_data['cart_time'])]
checkout_df = all_data[ (pd.notnull(all_data['cart_time'])) & (pd.notnull(all_data['checkout_time'])) ]
purchase_df = all_data[ (pd.notnull(all_data['cart_time'])) & (pd.notnull(all_data['checkout_time'])) & (pd.notnull(all_data['purchase_time'])) ]



cart_percentage = (1 - len(cart_df)/float(len(all_data))) * 100
checkout_percentage = (1 - len(checkout_df)/float(len(all_data))) * 100
purchase_percentage = (1 - len(purchase_df)/float(len(all_data))) * 100


print("cart: " ,cart_percentage)
print("checkout: " ,checkout_percentage)
print("purchase: " ,purchase_percentage)



all_data['time_to_purchase'] = all_data.purchase_time - all_data.visit_time

print(all_data.time_to_purchase)

print(all_data.time_to_purchase.mean())





#print(all_data.head(100))


