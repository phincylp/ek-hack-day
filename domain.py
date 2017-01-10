#!/usr/bin/python
import sys
sys.path.append('/usr/local/lib/python2.7/site-packages')
import selenium, time
import argparse
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
URL_VALUE = "http://www.domain.com"

class SiteConnect:
	def setUp(self):
		display = Display(visible=0, size=(1024, 768))
		display.start()
		fp = webdriver.FirefoxProfile()
		fp.set_preference("http.response.timeout", 5)
		fp.set_preference("dom.max_script_run_time", 5)
		self.driver = webdriver.Firefox(firefox_profile=fp)
	def tearDown(self):
		self.driver.close()
		self.display.stop()

	def searchFk(self, search_pattern):
		driver = self.driver
		driver.get(URL_VALUE)
		assert "Shop" in driver.title
		elem = driver.find_element_by_name("q")
		elem.send_keys(search_pattern)
		elem.send_keys(Keys.RETURN)
		assert "No results found." not in driver.page_source
	def userLogin(self, useremail, userpass):
		driver = self.driver
		driver.get(URL_VALUE + "/account/login")
		username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='fk-input login-form-input user-email']")))
		username.send_keys(useremail)
		password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='fk-input login-form-input user-pwd']")))
		password.send_keys(userpass)
		password.send_keys(Keys.RETURN)
		loggedin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='account-dropdown']")))

	def addtoCart(self, prducturl):
		driver = self.driver
		while True:
			try:
				driver.set_page_load_timeout(5)
				driver.get(prducturl)
				productpage = driver.find_element_by_xpath("//*[@action='https://www.domain.com/checkout/init'][1]")
				productpage.submit()
				break
			except selenium.common.exceptions.TimeoutException:
#				print "timed out"
				break
#		productpage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@value='Buy Now']")))
		productpage = driver.find_element_by_xpath("//*[@action='https://www.domain.com/checkout/init'][1]")
		productpage.submit()
		
	def getCart(self):
		driver = self.driver
		driver.get("http://www.domain.com/")
		cartpage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='item_count_in_cart_top_displayed']")))
		cartpage.click()
	def placeOrder(self, cvvnum):
		driver = self.driver
		self.getCart()
		place = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='btn btn-orange btn-buy-big place-order-button no-underline']")))
		place.submit()
		gotopay = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@class='btn btn-orange btn-large btn-continue no-underline']")))
		gotopay.click()
		time.sleep(10)
		codclick = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@bind-log='selected CreditCardPm payment']")))
		cod = driver.find_element_by_xpath("//*[@bind-log='selected CreditCardPm payment']")
		cod.click()









if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='This is the product url')
	parser.add_argument('-u','--ur',action='store',dest='url',default=None,help='<Required> url link',required=True)
	results = parser.parse_args()
	prducturl = results.url
#	print prducturl
	site = SiteConnect()
	site.setUp()
	useremail = "username"
	userpass = "somepass"
	site.userLogin(useremail, userpass)
	site.addtoCart(prducturl)
	site.tearDown()
#	site.getCart()
#	site.placeOrder(233)

