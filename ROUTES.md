Check routes:

http://check:81(8888)/getcheck/
	POST:
	json с полными данными чека (
	id покупателя,
	магазин,
	продукты,
	кол-во,
	тип оплаты,
	дата,
	общая стоимость,
	категория покупки
	)
	пример:
	{
	"shop":"First",
	"id_buy":1,
	"products":"first",
	"amounts":1,
	"category":"Tanks",
	"cost":15,
	"type_pay":"money",
	"date":"2021-03-04 10:38:42.124681",
	}

http://check:81(8888)/getcheck/<int: id>
получить html страницу с информацией о покупателе с номером id


Shop routes:

http://shop:82(9998)/api/products/

	GET:
	купить в магазине
	id покупателя, магазин, продукты, кол-во, тип оплаты
	пример:
	{
    "id":"1",
    "shop":"First",
    "products":{
        "1":"second"
        },
    "amounts":{
        "1":1
    },
    "type_pay":"bill"
}

	POST:
	Отправка продуктов из фабрики
	Магазин, Продукты, Кол-во
	пример:
	{
    "shop":"First",
    "products":{
        "1":"second"
        },
    "amounts":{
        "1":1
    }
	}

http://shop:82(9998)/api/getcheck

	GET:
	Возвращает все чеки из БД


Factory routes:
None


