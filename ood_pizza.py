"""
Problem:
Write a program that will take the order of a pizza and calculate the total cost of the pizza.

Requirements:
The initial setup involves a pizza with toppings, base, and size.
1. Prompt the user for the size of the pizza they would like to order.
2. Prompt the user for the number of toppings they would like to add to the pizza.
3. Calculate the total cost of the pizza based on the size and number of toppings.
4. Display the total cost of the pizza to the user.

Follow-Up: 
1. [!]]Add support for other items on the menu such as wings, drinks, etc.
2. How to implement a coupon system for the entire order
3. How to implement a buy-one-get-one-free coupon system
4. How to handle free toppings and where to place this logic
5. How to handle different store configurations with varying prices

Reference: 
https://leetcode.com/discuss/interview-question/6222043/OOD-Question-Design-a-Pizza-Shop-in-Amazon-interview./
https://www.1point3acres.com/bbs/thread-1107792-1-1.html

"""

"""
objects in this problem:
- BasePizza
- Topping
- Size 
- Order

workflow/actions:
- start an order
- choose a base pizza
- choose a size
- choose toppings
- calculate total cost
- ordering another pizza

clarifications:
- how many pizzas in one order?

Design Ideas:
1. PizzaSize, Item -> Pizza, Topping, Order, Menu
2. Size, Topping, Pizza, PizzaOrder, OrderCenter

Size, Item, Pizza, Order(manager of all items)
- Topping and Size can't exist without a Pizza
- Pizza must be initiated with a Size
- Pizza: {Topping -> count} since Topping can't exist without a Pizza, no need to have an id
- Order: {pizza_id -> Pizza} / [Pizza]

"""

import collections

class Topping:
    def __init__(self, id, price, name):
        self._id = id
        self._price = price
        self._name = name

        @property
        def price(self):
            return self._price

        @property
        def name(self):
            return self._name

class Size:
    def __init__(self, price, name):
        self._price = price
        self._name = name

        @property
        def price(self):
            return self._price

        @property
        def name(self):
            return self._name

class Pizza:
    def __init__(self, id, size):
        self._id = id
        self._size = size
        self._toppings = collections.defaultdict(Topping) # {topping: count}       

    @property
    def id(self):
        return self._id
    
    @property
    def size(self):
        return self._size
    
    @property
    def toppings(self):
        return self._toppings
    
    def choose_size(self, size):
        self._size = size

    def add_topping(self, topping):
        self._toppings[topping] += 1

    def remove_topping(self, topping):
        count = self._toppings.get(topping, 0)
        if count > 0:
            self._toppings[topping] = count - 1
            if self._toppings[topping] == 0:
                del self._toppings[topping]
        else:
            raise ValueError("Topping not found")

    def calculate_pizza_price(self):
        if not self._size:
            raise Exception("Size not chosen")
        
        base_price = self._size.price
        topping_price = 0
        for topping in self._toppings:
            topping_price += topping.price * self._toppings[topping]
       
        return base_price + topping_price
    
class Order:
    def __init__(self):
        self._pizzas = {} # {pizza_id: pizza}
        # FOLLOW-UP: add support for other items on the menu       

    def add_pizza(self, pizza_id, size):
        new_pizza = Pizza(pizza_id, size)
        self._pizzas[pizza_id] = new_pizza

    def add_topping(self, pizza_id, topping):
        if pizza_id in self._pizzas:
            self._pizzas[pizza_id].add_topping(topping)
        else:
            raise Exception("Pizza not found")
    
    def remove_topping(self, pizza_id, topping):
        try:
            if pizza_id not in self._pizzas:
                raise Exception("Pizza not found")
            
            self._pizzas[pizza_id].remove_topping(topping)

        except ValueError as e:
            print(f"Error: {e}")

    def remove_pizza(self, pizza_id):
        if pizza_id in self._pizzas:
            del self._pizzas[pizza_id]
        else:
            raise Exception("Pizza not found")

    def calculate_total_price(self):
        total_price = 0
        for pizza in self._pizzas:
            total_price += pizza.calculate_pizza_price()
        return total_price
        



        
    



        
        
        

        
