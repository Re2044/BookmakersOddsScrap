import pandas as pd
import numpy as np
import math
from difflib import SequenceMatcher
import smart_match as sm
import time
import json
from selenium.webdriver.firefox.service import Service as FService
from selenium.webdriver.firefox.options import Options as FOptions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
import numpy as np
import time
import pandas as pd
import pickle
import datetime
import re
from webdriver_manager.chrome import ChromeDriverManager
from notifypy import Notify
import asyncio
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
def xbet():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')

    rows = pd.DataFrame(columns=[
        ['Sport','Time','First book', 'Second book', 'Third book', 'Team №1', 'Team №2', 'First to win', 'Draw', 'Second to win',
         'Surplus']])
    sports = ['football','esports']
    for sport in sports:
        web = 'https://1xbet.com/en/line/'+sport

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(web)
        time.sleep(2)
        driver.get(web)
        try:
            try:
                accept = driver.find_element(By.XPATH, '//*[@id="pushfree"]/div/div/div/div/div[2]/div[1]/a')
                accept.click()
            except:
                pass

            tables = driver.find_elements(By.CLASS_NAME, 'dashboard-champ-content')
            #print(len(tables))
            for league in tables:

                # league_name = league.find_element(By.CLASS_NAME,'c-events__liga').text
                dates = league.find_elements(By.CLASS_NAME,"c-events__time-info")
                try:
                    teams = league.find_elements(By.CLASS_NAME, 'c-events__name')
                    odds = league.find_elements(By.CLASS_NAME, 'c-bets')
                    for i in range(0, len(odds) - 1):
                        time_now = dates[i].find_element(By.CLASS_NAME,'c-events__time.min').get_attribute("title")

                        curr_teams = teams[i + 1].find_element(By.CLASS_NAME, 'c-events__teams').get_attribute("title")
                        curr_teams = curr_teams.split(' — ')
                        first_team = curr_teams[0]
                        second_team = curr_teams[1]

                        curr_odds = odds[i + 1].find_elements(By.CLASS_NAME, 'c-bets__inner')

                        res_list = [sport,time_now,"1xbet", "1xbet", "1xbet", first_team, second_team]

                        sure = 1.0
                        sum = 0
                        try:
                            curr = float(curr_odds[0].text)
                            sure = sure - 1.0 / curr
                            res_list.append(curr)
                            sum = sum + curr
                        except:
                            res_list.append(100000000)
                            sum = sum + 100000000
                        try:
                            curr = float(curr_odds[1].text)
                            sure = sure - 1.0 / curr
                            res_list.append(curr)
                            sum = sum + curr
                        except:
                            res_list.append(100000000)
                            sum = sum + 100000000
                        try:
                            curr = float(curr_odds[2].text)
                            sure = sure - 1.0 / curr
                            res_list.append(curr)
                            sum = sum + curr
                        except:
                            res_list.append(100000000)
                            sum = sum + 100000000

                        res_list.append(sure)
                        if sum < 200000000:
                            rows.loc[len(rows)] = res_list
                except:
                    pass
        except:
            pass

            # print([first_odd,second_odd,third_odd,1.0/first_odd+1.0/second_odd+1.0/third_odd]
        driver.close()
    rows.to_csv("C:/Users/Re/Archive/1xbet.csv")

def ggbet():
    options = FOptions()
    options.add_argument('--headless')
    options.add_argument('--start-maximized')
    rows = pd.DataFrame(
        columns=['Sport','Time','First book', 'Second book', 'Third book', 'Team №1', 'Team №2', 'First to win', 'Draw',
                 'Second to win', 'Surplus'])
    sports = ['football','esports']
    for sport in sports:
        web = 'https://gg.bet/en/'+sport
        driver = webdriver.Firefox(service=FService(GeckoDriverManager().install()), options=options)
        try:
            driver.set_window_size(1920, 1080)
            driver.get(web)
            time.sleep(2)
            try:
                accept = driver.find_element(By.CLASS_NAME, 'cookie-agreement__button.cookie-agreement__button--ok')
                accept.click()
            except:
                pass
            in_list = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'app__middle___cwUcf')))
            sec_list = in_list.find_elements(By.CLASS_NAME,
                                             '__app-SmartLink-link.__app-OverviewRow-container.overviewRow__container___2uPYc')
            last_elem = 0
            while len(sec_list) < 50:
                driver.execute_script("arguments[0].scrollIntoView();", sec_list[len(sec_list) - 1])
                time.sleep(2)
                # print(len(sec_list),last_elem)
                sec_list = in_list.find_elements(By.CLASS_NAME,
                                                 '__app-SmartLink-link.__app-OverviewRow-container.overviewRow__container___2uPYc')
                if (len(sec_list) == last_elem):
                    break;
                else:
                    last_elem = len(sec_list)
            # wait for page to load new content

            for row in sec_list:
                try:
                    teams = row.find_elements(By.CLASS_NAME, '__app-LogoTitle-name.logoTitle__name___3_ywM')
                except:
                    teams = row.find_elements(By.CLASS_NAME, '__app-LogoTitle-name.logoTitle__name___3_ywM')
                first_team = teams[0].text
                if len(teams) > 2:
                    second_team = teams[2].text
                else:
                    second_team = teams[1].text
                tr = row.find_element(By.CLASS_NAME, '__app-Market-odds.market__odds___3URGG')
                table = tr.find_elements(By.CLASS_NAME, '__app-OddButton-coef.oddButton__coef___2tokv')

                if len(table) == 3:
                    try:
                        first_odd = float(table[0].text)
                    except:
                        first_odd = 100000000
                    try:
                        second_odd = float(table[1].text)
                    except:
                        second_odd = 100000000
                    try:
                        third_odd  = float(table[2].text)
                    except:
                        third_odd = 100000000
                else:
                    try:
                        first_odd = float(table[0].text)
                    except:
                        first_odd = 100000000
                    second_odd = 100000000
                    try:
                        third_odd = float(table[1].text)
                    except:
                        third_odd = 100000000
                time_now = row.find_element(By.CLASS_NAME,'fixtureData__text___1JMWR').text
                # print(first_odd,second_odd,third_odd)

                surplus = 1.0 - (1.0 / first_odd + 1.0 / second_odd + 1.0 / third_odd)
                if first_odd + second_odd + third_odd < 200000000:
                    rows.loc[len(rows)] = [sport,time_now,"ggbet", "ggbet", "ggbet", first_team, second_team, first_odd, second_odd, third_odd,
                                           surplus]
        except:
            pass
        driver.close()
    rows.to_csv("C:/Users/Re/Archive/ggbet.csv")

def twobet():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('window-size=1920x1080')

    rows = pd.DataFrame(
        columns=['Sport','Time','First book', 'Second book', 'Third book', 'Team №1', 'Team №2', 'First to win', 'Draw',
                 'Second to win', 'Surplus'])
    sports = ['football','esports']
    for sport in sports:
        web = 'https://22bet.com/line/'+sport

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        try:
            driver.get(web)
            time.sleep(2)
            try:
                accept = driver.find_element(By.XPATH, 'f-policy__button.button.button_light.js-cookie-accept')
                accept.click()
            except:
                pass

            tables = driver.find_elements(By.CLASS_NAME, 'dashboard.c-events')
            #print(len(tables))
            for league in tables:
                matches = league.find_elements(By.CLASS_NAME, 'c-events__item')
                #print(len(matches))
                for item in matches:
                    try:
                        curr_teams = item.find_element(By.CLASS_NAME, 'c-events__name').get_attribute('title')
                        #print(len(curr_teams))
                        curr_teams = curr_teams.split(" - ")
                        first_team = curr_teams[0]
                        second_team = curr_teams[1]
                        time_now = item.find_element(By.CLASS_NAME,'c-events__time.min').text
                        curr_odds = item.find_elements(By.CLASS_NAME, 'c-bets__inner')
                        #print(len(curr_odds))
                        res_list = [sport,time_now,"22bet", "22bet", "22bet", first_team, second_team]

                        sure = 1.0
                        sum = 0
                        try:
                            curr = float(curr_odds[0].text)
                            sure = sure - 1.0 / curr
                            res_list.append(curr)
                            sum = sum + curr
                        except:
                            res_list.append(100000000)
                            sum = sum + 100000000
                        try:
                            curr = float(curr_odds[1].text)
                            sure = sure - 1.0 / curr
                            res_list.append(curr)
                            sum = sum + curr
                        except:
                            res_list.append(100000000)
                            sum = sum + 100000000
                        try:
                            curr = float(curr_odds[2].text)
                            sure = sure - 1.0 / curr
                            res_list.append(curr)
                            sum = sum + curr
                        except:
                            res_list.append(100000000)
                            sum = sum + 100000000

                        res_list.append(sure)

                        if sum < 200000000:
                            rows.loc[len(rows)] = res_list
                    except:
                        pass
        except:
            pass
        #print(len(matches))

            # print([first_odd,second_odd,third_odd,1.0/first_odd+1.0/second_odd+1.0/third_odd]
        driver.close()
        rows.drop_duplicates(keep=False)
    rows.to_csv("C:/Users/Re/Archive/22bet.csv")

def betwinner():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--start-maximized')

    rows = pd.DataFrame(
        columns=['Sport','Time','First book', 'Second book', 'Third book', 'Team №1', 'Team №2', 'First to win', 'Draw',
                 'Second to win', 'Surplus'])
    sports = ['football','esports']
    for sport in sports:
        web = 'https://betwinner.com/en/line/'+sport
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        try:
            driver.get(web)
            driver.set_window_size(1920, 1080)

            time.sleep(2)

            try:
                accept = driver.find_element(By.XPATH, '//*[@id="pushfree"]/div/div/div/div/div[2]/div[1]/a')
                accept.click()
            except:
                pass

            list = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'ui-dashboard.dashboard')))
            table = list.find_elements(By.CLASS_NAME, 'ui-dashboard-champ.dashboard-champ.dashboard__champ')
            for league in table:

                games = league.find_elements(By.CLASS_NAME, 'ui-dashboard-game.dashboard-game')
                # print(len(games))
                for game in games:

                    teams = game.find_elements(By.CLASS_NAME, 'caption__label')
                    curr_odds = game.find_elements(By.CLASS_NAME, 'market__value')

                    first_team = teams[0].text
                    second_team = teams[1].text
                    time_now = game.find_element(By.CLASS_NAME,'dashboard-game-info__item.dashboard-game-info__date').text+" "+game.find_element(By.CLASS_NAME,'dashboard-game-info__item.dashboard-game-info__time').text
                    res_list = [sport,time_now,"betwinner", "betwinner", "betwinner", first_team, second_team]

                    sure = 1.0
                    sum = 0
                    try:
                        curr = float(curr_odds[0].text)
                        sure = sure - 1.0 / curr
                        res_list.append(curr)
                        sum = sum + curr
                    except:
                        res_list.append(100000000)
                        sum = sum + 100000000
                    try:
                        curr = float(curr_odds[1].text)
                        sure = sure - 1.0 / curr
                        res_list.append(curr)
                        sum = sum + curr
                    except:
                        res_list.append(100000000)
                        sum = sum + 100000000
                    try:
                        curr = float(curr_odds[2].text)
                        sure = sure - 1.0 / curr
                        res_list.append(curr)
                        sum = sum + curr
                    except:
                        res_list.append(100000000)
                        sum = sum + 100000000

                    res_list.append(sure)
                    if sum < 200000000:
                        rows.loc[len(rows)] = res_list
                    # print([first_odd,second_odd,third_odd,1.0/first_odd+1.0/second_odd+1.0/third_odd])
        except:
            pass
        driver.close()
    rows.to_csv("C:/Users/Re/Archive/betwinner.csv")
def main():
    while True:
        xbet()
        ggbet()
        twobet()
        betwinner()
        first_data = pd.read_csv("C:/Users/Re/Archive/1xbet.csv")

        second_data = pd.read_csv("C:/Users/Re/Archive/ggbet.csv")

        third_data = pd.read_csv("C:/Users/Re/Archive/22bet.csv")

        fourth_data = pd.read_csv("C:/Users/Re/Archive/betwinner.csv")

        result_data = pd.DataFrame(columns=['Sport','Time','First book','Second book','Third book','Team №1','Team №2','First to win','Draw','Second to win','Surplus'])

        res_dict = []
        all_dict = []
        first_dict = first_data.to_dict('records')
        second_dict = second_data.to_dict('records')
        third_dict = third_data.to_dict('records')
        fourth_dict = fourth_data.to_dict('records')
        for item in first_dict:
            all_dict.append(item)
        for item in second_dict:
            all_dict.append(item)
        for item in third_dict:
            all_dict.append(item)
        for item in fourth_dict:
            all_dict.append(item)


        for item in all_dict:
            s = item['Team №1'].find("The")
            if s !=-1 :
                item['Team №1'].replace("The","")
            s = item['Team №2'].find("The")
            if s != -1:
                item['Team №2'].replace("The","")
        #print(all_dict)
        for item in all_dict:
            val = item['Team №1']
            for it in all_dict:
                if it['Sport'] == item['Sport'] and it != item and similar(it['Team №1'],val)-0.85>=0.0000000001 and similar(it['Team №2'],item['Team №2'])-0.85>=0.0000000001:
                    first_odd = float(item['First to win'])
                    draw_odd = float(item['Draw'])
                    sec_odd = float(item['Second to win'])
                    firsts_odd = float(it['First to win'])
                    draws_odd = float(it['Draw'])
                    secs_odd = float(it['Second to win'])
                    sure = 1.0
                    if firsts_odd > first_odd and firsts_odd != 100000000:
                        item['First to win'] = firsts_odd
                        sure = sure - 1.0 / firsts_odd
                        item['First book'] = it['First book']
                    else:
                        sure = sure - 1.0 / first_odd
                    if draws_odd > draw_odd and draws_odd != 100000000:
                        item['Draw'] = draws_odd
                        sure = sure - 1.0 / draws_odd
                        item['Second book'] = it['Second book']
                    else:
                        sure = sure - 1.0 / draw_odd
                    if secs_odd > sec_odd and secs_odd != 100000000:
                        item['Second to win'] = secs_odd
                        sure = sure - 1.0 / secs_odd
                        item['Third book'] = it['Third book']
                    else:
                        sure = sure - 1.0 / sec_odd
                    item['Surplus'] = sure
                    #print(item)
                    all_dict.remove(it)

        for item in all_dict:
            if item['Surplus'] - 0.0 <= 0.000000000000001:
                all_dict.remove(item)
            print(item)
        res_dict = []
        for item in all_dict:
            if item['Surplus'] - 0.0 >= 0.00000000001:
                res_dict.append(item)
                notification = Notify()
                notification.title="found odd"
                notification.message = item['Sport']+ " "+item['Time']+ " " + item['Team №1'] + " "+item['Team №2'] + " "+ item['First book'] + " "+ item['Second book'] + " "+ item['Third book']
                notification.send()


        df = pd.DataFrame.from_records(res_dict)

        df.to_csv("C:/Users/Re/Archive/result.csv")
        time.sleep(300)

main()