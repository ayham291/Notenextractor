#! /usr/bin/python3

import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException as NoEle
from bs4 import BeautifulSoup
from time import sleep
from secrets import pw, username
import os
import re
from sys import platform


class QIS_BOT:
    def __init__(self, username, pw):
        chorme_opt = Options()
        chorme_opt.add_argument('--headless')
        global path1
        import sys
        if platform == 'linux' or platform == 'linux2':
            path1 = os.path.join(sys.path[0], 'chromedriver')
        elif platform == 'win32':
            path1 = os.path.join(sys.path[0], 'chromedriver.exe')
        self.driver = webdriver.Chrome(options=chorme_opt)
        self.driver.get("https://qis.othr.de/")
        sleep(2)
        self.driver.find_element_by_xpath("//*[@id='asdf']").send_keys(username)
        self.driver.find_element_by_xpath("//*[@id='fdsa']").send_keys(pw)
        self.driver.find_element_by_xpath("//*[@id='loginForm:login']").click()
        try:
            self.driver.find_element_by_xpath("//*[@id='makronavigation']/ul/li[3]/a").click()
        except NoEle:
            self.driver.close()
            sleep(5)
            QIS_BOT(username, pw)
        pass
        self.driver.find_element_by_xpath("//*[@id='wrapper']/div[5]/div[2]/div/form/div/ul/li[2]/a").click()
        self.driver.find_element_by_xpath("//*[@id='wrapper']/div[5]/div[2]/form/ul/li/a[1]").click()
        self.driver.find_element_by_xpath("//*[@id='wrapper']/div[5]/div[2]/form/ul/li/ul/li/a[1]/img").click()
    def Find(self):
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        match = soup.findAll("tr", {})
        f = open("Noten.csv", "a")
        tday = datetime.datetime.now()
        f.write('\n' + 'Version: %s' % tday + '\n')
        for tr in match:
            trs = tr.text.replace(',', '.')
            pattern = re.compile(r'\d{7}')
            pattern_v1 = re.compile(r'\d{5}')
            pattern_v2 = re.compile(r'(Winter.*)|(Sommer.*)')
            x1 = re.sub(pattern, '', trs)
            x2 = re.sub(pattern_v1, '', x1)
            x3 = re.sub(pattern_v2, '', x2)
            string = x3
            Durchschnitt = re.search(r'\t\n\n\n\t\t\s\d\.\d\s\n\t\n\n\n', string)
            p1 = re.search(r'\t\n\n\s{25}\t.*\n', string)
            bestanden = re.search(r'\t\t\t\s{25}\t.*\n\s{12}\t\t\n', string)
            credit = re.search(r'\t\t\n\n\t\t\t\d\.\d+\n\t\t\n\n\t\t\t', string)
            Note = re.search(r'\t\t\t\t\t\t\d.\d\n\t\n\t', string)
            # print(repr(string))
            for fach in range(1):
                if p1:
                    fach = ' '.join(p1.group().split())
                    be = ' '.join(bestanden.group().split())
                    f.write(fach + ',' + be)
                    print(fach)
                    print('Status: ' + be)
                else:
                    pass
                if Note:
                    no = ''.join(Note.group().split())
                    f.write(',' + no)
                    print('Note: ' + no)
                else:
                    pass
                if credit:
                    cre = ' '.join(credit.group().split())
                    f.write(',,' + cre + '\n')
                    print('Credits: ' + cre + '\n')
                else:
                    pass
            if Durchschnitt:
                DS = ''.join(Durchschnitt.group().split())
                f.write('Durchschnitt: ' + DS + '\n')
                print('Durchschnitt: ' + DS + '\n')
            else:
                pass
        f.close()
        self.driver.close()


QIS = QIS_BOT(username, pw)
QIS.Find()
