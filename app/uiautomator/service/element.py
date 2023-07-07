from typing import List, Union

import appium.webdriver.webdriver
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.webdriver import MobileWebElement, WebDriver

from exceptions import *

METHOD = {
    "xpath": AppiumBy.XPATH,
    "id": AppiumBy.ID,
    "resource-id": AppiumBy.ID,
    "text": AppiumBy.ANDROID_UIAUTOMATOR
}


async def find_elements(driver: appium.webdriver.webdriver.WebDriver = None,
                        element: str = None) -> Union[List[MobileWebElement], List]:
    pass


async def find_element(driver: WebDriver = None, element: dict = None) -> MobileWebElement | None:
    byMethod = element.keys()
    if not byMethod:
        raise MethodMissing
    for k in byMethod:
        if k in METHOD.keys() and element[k] != "":
            driver.find_element(by=METHOD[k], value=element[k])
            print("element can not locate by this method")
    return None
