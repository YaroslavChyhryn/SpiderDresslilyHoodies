# SpiderDresslilyHoodies
 [Scrapy] Spider for collecting data about hoodies

## Задача
Собрать информацию о мужских худи с
сайта: https://www.dresslily.com/hoodies-c-181.html 

Требуемая информация
данные по продукту
* product_id
* product_url
* name
* discount (%)
* discounted_price (0 if no sale)
* original_price
* total_reviews
* product_info (formatted string, e.g. “Occasion:Daily;Style:Fashion” )

данные по отзывам (reviews)
* product_id
* rating
* timestamp (convert review date to Unix timestamp)
* text
* size
* color