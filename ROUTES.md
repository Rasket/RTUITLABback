Check routes:

http://127.0.0.1:80(8888)/getcheck/
	POST:
	used to add check to db,
	req json with next data - customer id, shop where products were buyed, names of products (dict) \
		, amount of products (dict), type of pay, data, cost and shop category (???)

http://127.0.0.1:80(8888)/getcheck/<int: id>
	GET:
	get all checks from user with this id
	return html file with all data 


Shop routes:

http://127.0.0.1:80(9998)/api/products/

	GET:
		used to buy products from shop
		req json with next data - customer id, shop to buy products, products (dict), amount (dict)  \
			, type of pay
		if all data correct send post request tocheck service, except write check into his own db
	POST:
		used to add products to shop
		req json with next data - shop, products, amounts


Factory routes:
None