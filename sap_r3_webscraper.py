"""
# Developer: Richard Raphael Banak
# Objective: Functions to simplify RPA in SAP R/3
# Creation date: 2020-01-02
"""

# -*- coding: utf-8 -*-

from win32com.client import Dispatch
import win32com.client
import sys
import subprocess
import time
import os

from datetime import datetime, date, timedelta
from win32com.client import DispatchEx

#session = ''
#process = ''
#application = ''

primary_gui_window = "wnd[0]"
secondary_gui_window = "wnd[1]"

sap_gui_path = r'C:\Program Files (x86)\SAP\FrontEnd\SAPgui\saplogon.exe'


def connect_to_environment(enviroment_name):

    global session, process, application

    try:
        # usa current gui
        try:
            SapGuiAuto = win32com.client.GetObject('SAPGUI')
        except:
            process = subprocess.Popen(sap_gui_path)
            time.sleep(5)

            SapGuiAuto = win32com.client.GetObject('SAPGUI')

        if not type(SapGuiAuto) == win32com.client.CDispatch:
            return

        # use current application
        application = SapGuiAuto.GetScriptingEngine
        if not type(application) == win32com.client.CDispatch:
            SapGuiAuto = None
            return

        # use current env / fetch Children
        try:
            connection = application.Children(0)
            session = connection.Children(0)
            close_environment()
        except:
            pass

        connection = application.OpenConnection(enviroment_name, True)

        if not type(connection) == win32com.client.CDispatch:
            application = None
            SapGuiAuto = None
            return

        session = connection.Children(0)
        if not type(session) == win32com.client.CDispatch:
            connection = None
            application = None
            SapGuiAuto = None
            return

#       session.findById("wnd[0]/usr/txtRSYST-BNAME").text = "USERNAME"
#       session.findById("wnd[0]/usr/pwdRSYST-BCODE").text = "PASSWORD"
#       session.findById("wnd[0]").sendVKey(0)

        return  # session, process

    except:
        #dq.log.info(sys.exc_info()[0])
        raise Exception('Conection to SAP Failed')

    #finally:
    #   # bypass warning
    #   time.sleep(2)
    #   try:
    #       brpa.doAction(action='sendVKey', element_path=brpa.primaryGuiWindow, value='3')
    #   except:
    #       pass


def start_transaction(transaction_name):
    session.findById("wnd[0]/tbar[0]/okcd").text = transaction_name
    do_action(action='sendVKey', element_path="wnd[0]", value=0)


def maximize_window(window):
    session.findById(window).maximize()


def do_action(action=None, element_type='id', element_path=None, value=None, wait_before_action=0):

    global session

    time.sleep(wait_before_action)

    if element_type == 'id':
        try:
            element = session.findById(element_path)
        except:
            raise Exception('Element not found: {}'.format(element_path))

    if action == 'sendVKey':
        element.sendVKey(value)

    elif action == 'set_text':
        element.text = value

    elif action == 'press':
        element.press()

    elif action == 'pressToolbarContextButton':
        element.pressToolbarContextButton(value)

    elif action == 'selectContextMenuItem':
        element.selectContextMenuItem(value)

    elif action == 'setListBoxKey':
        element.key = value

    elif action == 'selected':
        element.selected = True

    elif action == 'unselected':
        element.selected = False

    elif action == 'selectRows':
        element.selectedRows = value

    elif action == 'doubleClickCurrentCell':
        element.selectedRows = value
        element.doubleClickCurrentCell()

    elif action == 'select':
        element.select()

    elif action == 'selectionInterval':
        element.selectionInterval = value

    elif action == 'setFocus':
        element.setFocus()

    elif action == 'focusDate':
        element.focusDate = value

    elif action == 'selectNode':
        element.selectNode(value)

    elif action == 'doubleClickNode':
        element.doubleClickNode(value)

    elif action == 'get_text':
        return element.text

    elif action == 'verticalScrollbar.position':
        element.verticalScrollbar.position = value

    elif action == 'caretPosition':
        element.caretPosition = value

    else:
        raise Exception('Action incorret, verify parameters')


def check_element_exists(element_type='id', element_path=None, wait_before_action=0):

    global session

    time.sleep(wait_before_action)

    if element_type == 'id':
        element = session.findById(element_path)

        if element:
            return True
        else:
            return False
    else:
        error = 'Preenchimento do element_type incorreto: {}'.format(
            element_type)
        raise Exception(error)


def close_environment():
    start_transaction("/nex")


def close_sap():
    global process, application
    time.sleep(3)
    try:
        process.terminate()
    except:
        application.quit()


def close_excel(file):
    xl = Dispatch('Excel.Application')
    wb = xl.Workbooks.Open(file)
    wb.Close(True)
