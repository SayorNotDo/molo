import asyncio

import appium.webdriver.webdriver
import yaml
from appium import webdriver
from appium.webdriver.webdriver import AppiumOptions


async def config_provider(f_path: str) -> dict:
    with open(f_path) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
        return conf


async def initialize() -> appium.webdriver.webdriver.WebDriver | None:
    config = await config_provider("../configs/config.yaml")
    print("-> device initialize...")
    desired_caps = dict()
    desired_caps['platformName'] = config['device']['platformName']
    if not desired_caps['platformName']:
        return None
    if desired_caps['platformName'] == 'macOS':
        desired_caps['browserName'] = config['device']['browserName']
        desired_caps['verbose'] = config['device']['verbose']
    if desired_caps['platformName'] == 'Android':
        desired_caps['deviceName'] = config['device']['deviceName']
    if desired_caps['platformName'] == 'iOS':
        pass
    serverInfo = config['device']['server']
    serverUrl = serverInfo['scheme'] + "://" + serverInfo['addr']
    desired_caps['platformVersion'] = config['device']['platformVersion']
    desired_caps['automationName'] = config['device']['automationName']
    options = AppiumOptions()
    options.load_capabilities(desired_caps)
    return webdriver.Remote(serverUrl, options=options)


async def shutdown(driver: appium.webdriver.webdriver.WebDriver) -> None:
    return driver.quit()


if __name__ == '__main__':
    asyncio.run(initialize())
