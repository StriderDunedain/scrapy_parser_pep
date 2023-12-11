import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        # Находим раздел 'Numerical Index'...
        numerical_index_table = response.xpath(
            '//section[@id="numerical-index"]'
        ).xpath(
            '//table[@class="pep-zero-table docutils align-default"]'
        )
        # Находим все ссылки на страницы PEP'ов...
        pep_links = set(
            numerical_index_table.css('td a::attr(href)').getall()
        )
        for pep_link in pep_links:
            # Отправляем на парсинг ссылки на страницы PEP'ов...
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        # Находим тэги, в которых находится нужные данные...
        abbr_tag = response.xpath(
            '//dl[@class="rfc2822 field-list simple"]'
        ).css('abbr')
        title = response.xpath(
            '//section[@id="pep-content"]'
        ).css('h1::text').get()

        # Находим статус, название и номер PEP'а...
        status = abbr_tag[0].css('abbr::text').get()
        name = abbr_tag[1].css('abbr::attr(title)').get()
        number = int(title.split()[1])

        # Возвращаем Item из с данными...
        yield PepParseItem(
            {'number': number,
             'name': name,
             'status': status}
        )
