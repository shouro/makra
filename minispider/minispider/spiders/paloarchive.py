"""
@author: Shouro <sourogts@gmail.com>
"""
import scrapy
from scrapy_splash import SplashRequest
from datetime import datetime, date
from minispider.items import MinispiderItem
from minispider.utils import date_gen, bangla_number_to_en
import dateutil.parser
from scrapy.exceptions import CloseSpider
import hashlib


TODAY = datetime.utcnow()
START_DATE = date(TODAY.year, TODAY.month, TODAY.day)
END_DATE = date(TODAY.year, TODAY.month, TODAY.day)

class PaloarchiveSpider(scrapy.Spider):
    name = 'paloarchive'
    allowed_domains = ['prothomalo.com']

    # itarate over main url list
    def start_requests(self):
        # date arg must be in iso8601 format
        start_date = getattr(self, 'startdate', None) 
        end_date = getattr(self, 'enddate', None)
        try:
            start_date = dateutil.parser.parse(start_date) if start_date is not None else START_DATE
            end_date = dateutil.parser.parse(end_date) if end_date is not None else END_DATE
        except Exception:
            raise CloseSpider('Invalid date, parsing failed')

        if start_date > end_date:
            raise CloseSpider('Start date must be small then end date')

        urlgen = ('https://www.prothomalo.com/archive/{}'.format(d.isoformat()) for d in date_gen(start_date, end_date))
        for url in urlgen:
            yield SplashRequest(url=url, endpoint='render.html', args={'wait': 0.5}, callback=self.parse)

    # Parse article list page
    def parse(self, response):
        # find all links in a page
        for relative_article_link in response.css('div.listing a.link_overlay::attr(href)').extract():
            url = response.urljoin(relative_article_link)
            yield SplashRequest(url=url, endpoint='render.html', args={'wait': 3.0}, callback=self.parse_article)

        # follow next page
        next_page = response.css('div.pagination > a.next_page::attr(href)')
        if next_page:
            yield SplashRequest(url=next_page.extract_first(), endpoint='render.html', args={'wait': 0.5}, callback=self.parse)

    # grab data from the article page
    def parse_article(self, response):
        article = MinispiderItem()
        article['uid'] = hashlib.sha256(response.url.encode()).hexdigest()
        article['url'] = response.url
        article['status'] = response.status
        article['domain'] = spider.allowed_domains[0]
        article['indexing_timestamp'] = datetime.utcnow()
        article['lang_detected'] = 'bangla'
        article['images'] = [{'url': div.css('b::attr(data-image)').extract_first().replace('//',''), 'caption': div.css('i::text').extract_first()} for div in response.css('div.pop-main div.info')]
        article['videos'] = []
        article['title'] = response.css('h1.title::text').extract_first()
        article['category'] = response.css('a.category_name::text').extract_first()
        article['author'] = response.css('div.author.each_row > span.name::text').extract_first()
        article['date_published'] = response.css('div.time.each_row > span:nth-of-type(1)::attr(content)').extract_first()
        article['date_modified'] = response.css('div.time.each_row > span:nth-of-type(2)::attr(content)').extract_first()
        article['article'] = f"{' '.join(response.css('article div.palo_web_news_div *::text').extract())} {' '.join(response.css('article p::text').extract())}".strip()
        article['tags'] = response.css('div.topic_list strong::text').extract()

        # Comments
        article_comments = response.css('div.comments_holder > div > ul > li')
        comments_container = []
        for comment in article_comments:
            for i, individual_comment in enumerate(comment.css('div.individual_comment')):
                if i == 0:
                    individual_comment_data = {
                        'uname': individual_comment.css('a.uname::text').extract_first(),
                        'comment': individual_comment.css('div.comment_portion > p::text').extract_first(),
                        'likes': bangla_number_to_en(individual_comment.css('div.comment_data > div > span::text').extract_first()),
                        'sub_comments': []
                    }
                else:
                    sub_comment = {
                        'uname': individual_comment.css('a.uname::text').extract_first(),
                        'comment': individual_comment.css('div.comment_portion > p::text').extract_first(),
                        'likes': bangla_number_to_en(individual_comment.css('div.comment_data > div > span::text').extract_first())
                    }
                    individual_comment_data['sub_comments'].append(sub_comment)
            comments_container.append(individual_comment_data)

        article['comments'] = comments_container
        yield article
