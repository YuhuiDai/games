from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import unittest

class TestContactPage(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/views/contactPage.html")

    def test_title(self):
        self.assertTrue("Contact Me Page" in self.driver.title)

    def test_author(self):
        print (self.driver.find_element_by_name("author").getAttribute("content"))
        self.assertTrue("Yuhui" in self.driver.find_element_by_name("author"))


    def tearDown(self):
        self.driver.close();

if __name__ == '__main__':

    unittest.main()

#
# assert "Contact Me Page" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
