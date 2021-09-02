"""
# Developer: Richard Raphael Banak
# Objective: Functions to simplify RPA - Webscrapping
# Creation date: 2020-01-02
"""

# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

import os
import time

wait = ''

def start_selenium(chrome_driver_path):

    global driver

    if chrome_driver_path == None:
        path_selenium = r'C:\Users\{}\AppData\Local\SeleniumBasic\chromedriver.exe'.format(os.environ['USERNAME'])
    else:
        path_selenium = chrome_driver_path
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=path_selenium, options=options)
    return driver


def maximize_window():
    driver.maximize_window()


def open_url(url):
    driver.get(url)


def do_action(action='click', element_type='xpath', element_path=None, wait_condition='is_visible', timeout=20, text=None, wait_before_action=0):

    time.sleep(wait_before_action)

    element_type = element_type.replace('_', ' ')

    if wait_condition == 'is_present': # Espera até que o elemento esteja presente no DOM
        element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((element_type, element_path)))

    elif wait_condition == 'is_visible':  # Espera até que o elemento esteja visível 
        element = WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((element_type, element_path)))

    elif wait_condition == 'text_is_present' and text:  # Espera até que o elemento contenha o texto da variavel text
        element = WebDriverWait(driver, timeout).until(EC.text_to_be_present_in_element((element_type, element_path), text))

    elif wait_condition == 'is_clickable': # Espera até que o elemento possa ser clicado
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((element_type, element_path)))

    elif wait_condition == None:
        pass

    else:
        print('Parameter wait_condition incorrect')

    if action == 'click':
        element.click()

    elif action == 'send_keys' and text:
        element.send_keys(text)

    elif action == 'clear':
        element.clear()

    elif action == 'replace_text':
        element.clear()
        element.send_keys(text)
    
    elif action == 'get_text':
        return element.text

    elif action == 'select_by_visible_text':
        Select(element).select_by_visible_text(text)

    elif action == 'show':
        attributes = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
        return attributes
    
    elif action == 'get_attribute':
        return element.get_attribute(text)
        

    elif action == 'wait':
        pass

    else:
        print('Action parameter incorrect: {}'.format(action))

    return True

def wait_element(element_type='xpath', element_path=None, wait_condition='is_visible', timeout=20, text=None, wait_before_action=0):

    time.sleep(wait_before_action)

    if wait_condition == 'is_visible':
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((element_type, element_path)))

    if wait_condition == 'is_invisible':
        WebDriverWait(driver, timeout).until(EC.invisibility_of_element_located((element_type, element_path)))


def element_exists(element_type='xpath', element_path=None, wait_before_action=0):

    time.sleep(wait_before_action)
    try:
        #browser.find_element_by_xpath(xpath).is_displayed()
        EC.presence_of_element_located((element_type, element_path))
    except:
        return False
    return True


def delete_cookies():
    driver.delete_all_cookies()
    

def driver_quit():
    driver.stop_client()
    driver.quit()
