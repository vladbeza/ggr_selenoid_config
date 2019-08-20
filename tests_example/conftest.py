import pytest
from appium import webdriver as appium_driver
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", dest="browser")
    parser.addoption("--remote_driver_host", action="store",
                     default="http://test:test@localhost:4444/wd/hub",
                     dest="remote_host")
    parser.addoption('--enable_vnc',
                     action="store_true",
                     dest="enable_vnc")


@pytest.fixture
def browser(request):
    browser_name = request.config.option.browser
    host = request.config.option.remote_host
    is_vnc_used = request.config.option.enable_vnc

    if browser_name.lower() == "chrome":
        capabilities = DesiredCapabilities.CHROME
        capabilities["enableVNC"] = is_vnc_used

    elif browser_name.lower() == "firefox":
        capabilities = DesiredCapabilities.FIREFOX
        capabilities["enableVNC"] = is_vnc_used

    elif browser_name.lower() in ("ie", "internetexplorer"):
        capabilities = DesiredCapabilities.INTERNETEXPLORER
        capabilities["ie.usePerProcessProxy"] = True
        capabilities["ie.browserCommandLineSwitches"] = "-private"
        capabilities["ie.ensureCleanSession"] = True
        capabilities["requireWindowFocus "] = False
        capabilities["enableVNC"] = is_vnc_used

    elif browser_name.lower() == "opera":
        capabilities = DesiredCapabilities.OPERA
        capabilities["enableVNC"] = is_vnc_used

    elif browser_name.lower() == "chrome-mobile":
        capabilities = {'browserName': 'chrome',
                        'version': 'mobile-75.0',
                        'enableVNC': is_vnc_used
                        }
    elif browser_name.lower() == "android":
        capabilities = {'deviceName': 'Nexus 5',
                        'browserName': 'chrome',
                        'platformVersion': '7.1.1',
                        'version': 'mobile-76.0',
                        'platformName': "Android"
                        # 'enableVNC': is_vnc_used,
                        # "appPackage": "",
                        # "appActivity": "",
                        # "env": ["SKIN-WXGA808"],
                        # "enableVideo": True,
                        # "videoName": ""
                        }
    else:
        raise ValueError("Incorrect browser name")

    if browser_name.lower() in ("chrome", "firefox", "ie",
                                "internetexplorer", "opera"):
        driver = webdriver.Remote(command_executor=host,
                                  desired_capabilities=capabilities)
        driver.set_window_rect(0, 0, 1920, 1080)
    else:
        driver = appium_driver.Remote(command_executor=host,
                                      desired_capabilities=capabilities)
    driver.implicitly_wait(5)
    yield driver

    driver.quit()

