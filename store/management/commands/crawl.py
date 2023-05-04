from django.core.management.base import BaseCommand, CommandParser
from store.models import Jumpo, Brand, Category
from crawlers.cu import crawl_cu
from crawlers.emart_24 import crawl_emart_24
from crawlers.ministop import crawl_ministop
from crawlers.seven_eleven import crawl_seven_eleven
from crawlers.gs25 import crawl_gs25

def save_crawled_jumpos(jumpos, brand):
    '''
    jumpo를 표현한 딕셔너리를 받아 DB에 저장합니다. 중복인 데이터는 건너뜁니다.

    Args:
        jumpos (dict): 크롤링한 jumpo dict 리스트
        brand (store.models.Brand): Brand 객체
    '''
    print("{} jumpo crawled for {}".format(len(jumpos), brand.brand_name))
    jumpos = [Jumpo(**j, brand=brand) for j in jumpos]
    failed = 0
    for jumpo in jumpos:
        try:
            jumpo.save()
        except Exception as e:
            failed += 1
            print(e)
    print("{}/{} saved. {} failed.".format(len(jumpos) - failed, len(jumpos), failed))

class Command(BaseCommand):
    help = 'Crawl the informations of the jumpos by brand, and save into DB.'
    valid_brands = ['cu', 'emart24', 'ministop', 'seveneleven', 'gs25']

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--brand", type=str, help="specify a brand to crawl")
        parser.add_argument("--all", action="store_true", help="crawl all brands")
    
    def handle(self, *args, **options):
        if options["all"] and options["brand"]:
            return False
        if options["brand"] is not None and not options["brand"] in self.valid_brands:
            print("USAGE: python manage.py crawl --brand cu")
            print("> valid brands: {}".format(self.valid_brands))
            print("> to crawl all brand, use --all")
            return False

        category = Category.objects.get_or_create(category_name="편의점")[0]
        if options["brand"] == "cu" or options["all"]:
            brand = Brand.objects.get_or_create(brand_name="CU", category=category)[0]
            print("crawling {}...".format(brand.brand_name))
            save_crawled_jumpos(crawl_cu(), brand)

        if options["brand"] == "emart24" or options["all"]:
            brand = Brand.objects.get_or_create(brand_name="이마트24", category=category)[0]
            print("crawling {}...".format(brand.brand_name))
            save_crawled_jumpos(crawl_emart_24(), brand)

        if options["brand"] == "ministop" or options["all"]:
            brand = Brand.objects.get_or_create(brand_name="미니스톱", category=category)[0]
            print("crawling {}...".format(brand.brand_name))
            save_crawled_jumpos(crawl_ministop(), brand)

        if options["brand"] == "seveneleven" or options["all"]:
            brand = Brand.objects.get_or_create(brand_name="세븐일레븐", category=category)[0]
            print("crawling {}...".format(brand.brand_name))
            save_crawled_jumpos(crawl_seven_eleven(), brand)
        
        if options["brand"] == "gs25" or options["all"]:
            brand = Brand.objects.get_or_create(brand_name="GS25", category=category)[0]
            print("crawling {}...".format(brand.brand_name))
            save_crawled_jumpos(crawl_gs25(), brand)
            
        print("Done!")
