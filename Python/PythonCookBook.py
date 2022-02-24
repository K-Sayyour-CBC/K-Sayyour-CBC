""" PYTHON COOKBOOK """
import heapq 
portfolio = [
 {'name': 'IBM', 'shares': 100, 'price': 91.1},
 {'name': 'AAPL', 'shares': 50, 'price': 543.22},
 {'name': 'FB', 'shares': 200, 'price': 21.09},
 {'name': 'HPQ', 'shares': 35, 'price': 31.75},
 {'name': 'YHOO', 'shares': 45, 'price': 16.35},
 {'name': 'ACME', 'shares': 75, 'price': 115.65}
]
cheap = heapq.nsmallest(3, portfolio, key = lambda s: s['price'] )
expensive = heapq.nlargest (3, portfolio, key = lambda s: s['price'])
nums = [1, -4, 5, 12, 9]
smalle = heapq.nsmallest (3, nums)
large = heapq.nlargest (3, nums)
small = min(nums)
print(small)
#--------KEY VALUE IN DICTIONARIES-------------
from collections import defaultdict
d = defaultdict(list)
d['a'].append(1)
d['a'].add(2)
d['b'].append(4)
#-----------------------------------------
d = {}
d.setdefault('a', []).appened(1)
d.setdefault('b', []).appened(4)
#------------------------------------------
d = {
    'a' : [1, 2, 3],
    'b' : [4, 5]
}
from collections import defaultdict
d = defaultdict(list)
d['a'].appened(1)
e = defaultdict(set)
e['a'].add(4)

d={}
d.setdefault('a', []).appened(1)
d = defaultdict(list)
for key, value in d:
    d[key].appened(value)
#-------------------------------------
prices = {
 'ACME': 45.23,
 'AAPL': 612.78,
 'IBM': 205.55,
 'HPQ': 37.20,
 'FB': 10.75
}
min_price = min(zip(prices.values(), prices.keys()))
max_price = max(zip(prices.values(), prices.keys()))
price_sorted = sorted(zip(prices.values(), prices.keys()))
#----------------------------------------
