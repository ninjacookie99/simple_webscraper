from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
# import numpy as np
# import pandas as pd 

# URL to scrape
my_url = 'https://www.newegg.com/global/ae-en/p/pl?d=graphics+card&PageSize=36'

# opening up connection, grabbing the page
uClient = uReq(my_url)

# off-load the content into a variable
page_html = uClient.read()

# close the web client after use
uClient.close()

# call the soup function and parse using HTML
page_soup = soup(page_html,"html.parser")

# grabs each product
containers = page_soup.find_all("div",{"class":"item-container"})

pages = page_soup.find_all("span",{"class":"list-tool-pagination-text"})[0].text.strip()

total_pages = pages.replace('Page 1/',"")

filename = "products.csv"
f = open(filename,"w")

headers = "brand, product_name, shipping_cost, current_price\n"

f.write(headers)

count = 0
# for page in range()
for container in containers:
	try:
		brand = container.div.div.a.img["title"].title()
	except:
		brand = ""
		print("No brand name found")

	# all the product title containers
	title_container = container.find_all("a",{"class":"item-title"})

	# find the text that includes the product name
	product_name = title_container[0].text.strip()

	# all shipping price containers
	shipping_container = container.find_all("li",{"class":"price-ship"})
	if shipping_container[0].text == 'Free Shipping':
		shipping_cost = 0

	elif shipping_container[0].text =='Special Shipping':
		shipping_cost = shipping_container[0].text

	else:
		shipping_cost = shipping_container[0].text.replace("Dh Shipping","")

	# all the current price containers
	price_container = container.find_all("li",{"class":"price-current"})
	current_price = price_container[0].text.replace("Dh","").strip().replace("-", "")

	print(brand,end = "\n")
	print(product_name, end = "\n")
	print(shipping_cost, end = "\n")
	print(current_price, end = "\n")

	f.write(brand + ',' + product_name.replace(",","|") + ',' + str(shipping_cost) + ',' +  current_price.replace(",","") + "\n")
	count+=1
	print(count)
f.close()