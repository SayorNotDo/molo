import asyncio
import unittest
from device import *
from element import *

element = {
    'xpath': '',
    'id': '',
    'resource-id': '',
    'text': 'new UiSelector().text("游戏加速")'
}


class TestDevice(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    # async def test_find_element_by_id(self):
    #     try:
    #         self.driver = await initialize()
    #         print("----------------------start------------------------")
    #         res = await find_element_by_xpath(self.driver,
    #                                           elementXpath='//android.widget.RelativeLayout[@content-desc="遊戲加速"]/android.widget.FrameLayout[2]')
    #         print("----------------------end------------------------")
    #         print(res)
    #     except ElementNotFound as e:
    #         return

    async def test_find_element(self):
        self.driver = await initialize()
        res = await find_element(self.driver, element)
        print(res)

    def tearDown(self):
        self.loop.close()


if __name__ == '__main__':
    unittest.main()
