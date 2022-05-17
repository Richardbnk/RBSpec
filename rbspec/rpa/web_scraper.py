"""
# Developer: Richard Raphael Banak
# Objective: RPA functions to simplify webscrapping
# Creation date: 2020-01-02
# Updated: 2020-11-16 / 2021-10-01
"""

# -*- coding: utf-8 -*-

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

import os
import time
import platform


def startSelenium(driver_path=None, navigator="chrome", window_size=[1400, 900]):

    global driver

    if driver_path:
        path_selenium = driver_path
    else:
        path_selenium = get_driver_path(navigator=navigator)

    if navigator == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        driver = webdriver.Chrome(executable_path=path_selenium, options=options)
        # https://chromedriver.chromium.org/downloads
    elif navigator == "edge":
        options = Options()
        options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
        driver = Edge(executable_path=path_selenium, capabilities={}, options=options)
        # Resize current window to the set dimension
        # driver.set_window_size(width=1200, height=800)
        # https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

    return driver


def get_driver_path(navigator="chrome"):
    if navigator == "chrome":
        file_name = "chromedriver"
    elif navigator == "edge":
        file_name = "msedgedriver"
    else:
        raise Exception("Wrong navigator (use navigator == ('edge' or 'chrome')")

    if platform.system() == "Windows":
        return os.path.join(
            os.path.expanduser("~"), "Repositories", "files", f"{file_name}.exe"
        )
    else:
        return os.path.join(os.path.expanduser("~"), "Repositories", "files", file_name)


def maximize_window():
    driver.maximize_window()


def open_url(url):
    driver.get(url)


def find_element(
    element_type="xpath", element_path=None, timeout=20, wait_condition="is_visible"
):

    global driver

    if wait_condition == "is_present":
        # Espera até que o elemento esteja presente no DOM
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((element_type, element_path))
        )

    elif wait_condition == "is_visible":
        # Espera até que o elemento esteja visível
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((element_type, element_path))
        )

    elif wait_condition == "text_is_present" and text:
        # Espera até que o elemento contenha o texto da variavel text
        element = WebDriverWait(driver, timeout).until(
            EC.text_to_be_present_in_element((element_type, element_path), text)
        )

    elif wait_condition == "is_clickable":
        # Espera até que o elemento possa ser clicado
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((element_type, element_path))
        )

    elif wait_condition == None:
        pass

    else:
        raise Exception("Parâmetro wait_condition preenchido incorretamente")

    return element


def find_elements(
    element_type="xpath", element_path=None, timeout=20, wait_condition="is_visible"
):

    global driver

    if wait_condition == "is_present":
        # Espera até que o elemento esteja presente no DOM
        elements = WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((element_type, element_path))
        )

    elif wait_condition == "is_visible":
        # Espera até que o elemento esteja visível
        elements = WebDriverWait(driver, timeout).until(
            EC.visibility_of_all_elements_located((element_type, element_path))
        )

    else:
        elements = driver.find_elements(element_type, element_path)
        pass

    return elements


def find_element_at_position(
    element_type="xpath",
    element_path=None,
    element_at_position=0,
    wait_condition="is_visible",
    timeout=20,
    text=None,
    wait_before_action=0,
):
    pass


def do_action(
    action="click",
    element_type="xpath",
    element_path=None,
    element_at_position=0,
    wait_condition="is_visible",
    timeout=20,
    text=None,
    wait_before_action=0,
):

    time.sleep(wait_before_action)

    element_type = element_type.replace("_", " ")

    # find element
    if element_at_position == 0:
        element = find_element(
            element_type=element_type,
            element_path=element_path,
            timeout=timeout,
            wait_condition=wait_condition,
        )
    else:
        element = find_elements(
            element_type=element_type,
            element_path=element_path,
            timeout=timeout,
            wait_condition=wait_condition,
        )[element_at_position]

    # do action
    if action == "click":
        element.click()

    elif action == "send_keys" and text:
        element.send_keys(text)

    elif action == "clear":
        element.clear()

    elif action == "replace_text":
        element.clear()
        element.send_keys(text)

    elif action == "get_text":
        return element.text

    elif action == "select_by_visible_text":
        Select(element).select_by_visible_text(text)

    elif action == "show":
        attributes = driver.execute_script(
            "var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;",
            element,
        )
        return attributes

    elif action == "get_attribute":
        return element.get_attribute(text)

    elif action == "hover":
        ActionChains(driver).move_to_element(element).perform()

    elif action == "wait":
        pass

    else:
        raise Exception(
            "Parâmetro Action está preenchido incorretamente: {}".format(action)
        )

    return True


def wait_element(
    element_type="xpath",
    element_path=None,
    wait_condition="is_visible",
    timeout=20,
    wait_before_action=0,
):

    time.sleep(wait_before_action)

    if wait_condition == "is_visible":
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((element_type, element_path))
        )

    if wait_condition == "is_invisible":
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((element_type, element_path))
        )


def element_exists(element_type="xpath", element_path=None, wait_before_action=0):

    time.sleep(wait_before_action)
    try:
        EC.presence_of_element_located((element_type, element_path))
    except:
        return False
    return True


def delete_cookies():
    driver.delete_all_cookies()


def driver_quit():
    driver.stop_client()
    driver.quit()


def close_last_openned_window(main_window_index=0, window_to_be_closed_index=1):
    try:
        driver.switch_to.window(driver.window_handles[window_to_be_closed_index])
        driver.close()
        driver.switch_to.window(driver.window_handles[main_window_index])
    except:
        # print('Nenhuma janela foi fechada')
        pass


def click(
    element_type="xpath",
    element_path=None,
    element_at_position=0,
    wait_condition="is_visible",
    timeout=20,
    text=None,
    wait_before_action=0,
):
    return do_action(
        action="click",
        element_type=element_type,
        element_path=element_path,
        element_at_position=element_at_position,
        wait_condition=wait_condition,
        timeout=timeout,
        text=text,
        wait_before_action=wait_before_action,
    )


def send_keys(
    element_type="xpath",
    element_path=None,
    element_at_position=0,
    wait_condition="is_visible",
    timeout=20,
    text=None,
    wait_before_action=0,
):
    return do_action(
        action="send_keys",
        element_type=element_type,
        element_path=element_path,
        element_at_position=element_at_position,
        wait_condition=wait_condition,
        timeout=timeout,
        text=text,
        wait_before_action=wait_before_action,
    )


def clear(
    element_type="xpath",
    element_path=None,
    element_at_position=0,
    wait_condition="is_visible",
    timeout=20,
    text=None,
    wait_before_action=0,
):
    return do_action(
        action="clear",
        element_type=element_type,
        element_path=element_path,
        element_at_position=element_at_position,
        wait_condition=wait_condition,
        timeout=timeout,
        text=text,
        wait_before_action=wait_before_action,
    )


def replace_text(
    element_type="xpath",
    element_path=None,
    element_at_position=0,
    wait_condition="is_visible",
    timeout=20,
    text=None,
    wait_before_action=0,
):
    return do_action(
        action="replace_text",
        element_type=element_type,
        element_path=element_path,
        element_at_position=element_at_position,
        wait_condition=wait_condition,
        timeout=timeout,
        text=text,
        wait_before_action=wait_before_action,
    )


def get_text(
    element_type="xpath",
    element_path=None,
    element_at_position=0,
    wait_condition="is_visible",
    timeout=20,
    text=None,
    wait_before_action=0,
):
    return do_action(
        action="get_text",
        element_type=element_type,
        element_path=element_path,
        element_at_position=element_at_position,
        wait_condition=wait_condition,
        timeout=timeout,
        text=text,
        wait_before_action=wait_before_action,
    )


def select_by_visible_text(
    element_type="xpath",
    element_path=None,
    element_at_position=0,
    wait_condition="is_visible",
    timeout=20,
    text=None,
    wait_before_action=0,
):
    return do_action(
        action="select_by_visible_text",
        element_type=element_type,
        element_path=element_path,
        element_at_position=element_at_position,
        wait_condition=wait_condition,
        timeout=timeout,
        text=text,
        wait_before_action=wait_before_action,
    )


def show(
    element_type="xpath",
    element_path=None,
    element_at_position=0,
    wait_condition="is_visible",
    timeout=20,
    text=None,
    wait_before_action=0,
):
    return do_action(
        action="show",
        element_type=element_type,
        element_path=element_path,
        element_at_position=element_at_position,
        wait_condition=wait_condition,
        timeout=timeout,
        text=text,
        wait_before_action=wait_before_action,
    )


def get_attribute(
    element_type="xpath",
    element_path=None,
    element_at_position=0,
    wait_condition="is_visible",
    timeout=20,
    text=None,
    wait_before_action=0,
):
    return do_action(
        action="get_attribute",
        element_type=element_type,
        element_path=element_path,
        element_at_position=element_at_position,
        wait_condition=wait_condition,
        timeout=timeout,
        text=text,
        wait_before_action=wait_before_action,
    )


def hover(
    element_type="xpath",
    element_path=None,
    element_at_position=0,
    wait_condition="is_visible",
    timeout=20,
    text=None,
    wait_before_action=0,
):
    return do_action(
        action="hover",
        element_type=element_type,
        element_path=element_path,
        element_at_position=element_at_position,
        wait_condition=wait_condition,
        timeout=timeout,
        text=text,
        wait_before_action=wait_before_action,
    )
