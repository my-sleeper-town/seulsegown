from django.core.management.base import BaseCommand, CommandParser
from store.models import Jumpo, Brand, Category
from crawlers.cu import crawl_cu
from crawlers.emart_24 import crawl_emart_24
from crawlers.ministop import crawl_ministop
from crawlers.seven_eleven import crawl_seven_eleven
from crawlers.gs25 import crawl_gs25
 
class Command(BaseCommand):
    help = 'Retrieves the address and jumpo name of 7-Eleven stores in Seoul from 7-Eleven.co.kr.'
    valid_brands = ['cu', 'emart24', 'ministop', 'seveneleven', 'gs25']

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("--brand", type=str, help="specify a brand to crawl")
        parser.add_argument("--all", action="store_true", help="crawl all brands")
    
    def handle(self, *args, **options):
        if options["all"] and options["brand"]:
            return False
        if not options["brand"] in self.valid_brands:
            print("USAGE: python manage.py crawl --brand cu")
            print("> valid brands: {}".format(self.valid_brands))
            print("> to crawl all brand, use --all")
            return False

        jumpos = []
        category = Category.objects.get_or_create(category_name="편의점")[0]
        if options["brand"] == "cu":
            print("crawl cu stores...")
            brand = Brand.objects.get_or_create(brand_name="CU", category=category)[0]
            cu_jumpos = crawl_cu()
            cu_jumpos = [Jumpo(**j, brand=brand) for j in cu_jumpos]
            jumpos += cu_jumpos
            print("got {} jumpos".format(len(cu_jumpos)))

        if options["brand"] == "emart24":
            print("crawl emart24 stores...")
            brand = Brand.objects.get_or_create(brand_name="emart24", category=category)[0]
            emart_jumpos = crawl_emart_24()
            emart_jumpos = [Jumpo(**j, brand=brand) for j in emart_jumpos]
            jumpos += emart_jumpos
            print("got {} jumpos".format(len(emart_jumpos)))

        if options["brand"] == "ministop":
            print("crawl ministop stores...")
            brand = Brand.objects.get_or_create(brand_name="ministop", category=category)[0]
            ministop_jumpos = crawl_ministop()
            ministop_jumpos = [Jumpo(**j, brand=brand) for j in ministop_jumpos]
            jumpos += ministop_jumpos
            print("got {} jumpos".format(len(ministop_jumpos)))

        if options["brand"] == "seveneleven":
            print("crawl seveneleven stores...")
            brand = Brand.objects.get_or_create(brand_name="seveneleven", category=category)[0]
            seven_eleven_jumpos = crawl_seven_eleven()
            seven_eleven_jumpos = [Jumpo(**j, brand=brand) for j in seven_eleven_jumpos]
            jumpos += seven_eleven_jumpos
            print("got {} jumpos".format(len(seven_eleven_jumpos)))
        
        if options["brand"] == "gs25":
            print("crawl gs25 stores...")
            brand = Brand.objects.get_or_create(brand_name="gs25", category=category)[0]
            seven_eleven_jumpos = crawl_gs25()
            seven_eleven_jumpos = [Jumpo(**j, brand=brand) for j in seven_eleven_jumpos]
            jumpos += seven_eleven_jumpos
            print("got {} jumpos".format(len(seven_eleven_jumpos)))


        print("total {} jumpos crawled".format(len(jumpos)))
        objs = Jumpo.objects.bulk_create(jumpos)
