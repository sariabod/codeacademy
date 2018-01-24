import numpy as np

cupcakes = np.array([2,.75,2,1,.5])

recipes = np.genfromtxt('recipes.csv',delimiter=',')

print(recipes)

#print(recipes)

eggs = recipes[:,3]

print(eggs)

cookies = recipes[2]

print(cookies)

double_batch = cupcakes * 2

grocery_list = cookies + double_batch