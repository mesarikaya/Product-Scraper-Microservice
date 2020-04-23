import sys
import unittest

from djangowebscraperapp.webcrawler.webcrawler import load_properties


class TestCrawler(unittest.TestCase):
    """def setUp(self):
        self.proxyList = ProxyList.get_proxies_from_scraper_api(5)
        self.proxyList = ['45.86.15.208:80',
        '166.159.90.56:53281','94.158.22.142:8085','173.44.227.86:12345','102.164.205.239:47190',
        '193.8.94.181:80','124.112.177.2:28803','85.208.86.214:8085','117.57.74.76:28803',
        '31.40.253.211:8085','37.44.255.156:8085','45.137.60.196:80','45.92.247.26:80',
        '193.233.149.211:4045','45.138.101.92:8085','5.62.158.242:8085','183.164.240.229:28803',
        '193.202.80.45:8085','192.186.151.222:80','195.88.242.209:4045','182.202.220.68:32609',
        '182.100.68.161:28803','117.102.81.6:53281','83.171.252.100:8085']"""

    @unittest.skip
    def test_scraper_api(self):
        self.proxyList = ProxyList.get_proxies_from_scraper_api(5)
        print("Resulting proxy list is:", self.proxyList)
        self.assertTrue(len(self.proxyList))

    @unittest.skip
    def test_proxy_list_exists(self):
        print("Resulting proxy list is:", self.proxyList)
        self.assertTrue(len(self.proxyList))

    @unittest.skip
    def test_rotate_proxies(self):
        proxies = ProxyList.rotate_proxies(self.proxyList)
        print("Retrieved proxy: ", proxies)
        self.assertTrue(len(proxies))

    @unittest.skip
    def test_ah_product_call(self):
        print("runnind ah product call test function")
        try:
            AHProductIdSpider.get_product_id()
            print("Success")
        except:
            # Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work.
            # We will just skip retries and we are only downloading a single url
            print("Skipping. Connection error")
            print("Unexpected error:", sys.exc_info()[0])
            # raise

        self.assertTrue(True)

    def test_load_properties(self):
        properties = load_properties.load_properties()
        self.assertTrue(properties.properties['Scraper_secret'])
        self.assertTrue(len(properties.properties.values()))
        self.assertTrue(len(properties))


if __name__ == '__main__':
    unittest.main()
