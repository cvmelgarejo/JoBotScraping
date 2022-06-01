# Version sin flask
# Faltaria decidir si poner filtros por fechas

import time
import sqlite3
import os
import platform

#third part libs
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
from webdriver_manager.firefox import GeckoDriverManager


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import pandas as pd


try: # to deploy in heroku, if you want to run locally, just create a file called: local_settings.py
    import local_settings
    DEBUG = True
    print("LOCAL")
except:
    DEBUG = False 
    print("IN HEROKU")



def scrapping(keyword):
    url = "https://www.linkedin.com/jobs/search?keywords=&location=Paraguay&geoId=104065273&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        if DEBUG:
            if "linux" in platform.platform().lower(): 
                wd = webdriver.Firefox(executable_path="./geckodriver")
                #wd = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
            else:
                wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        else: # for heroku
            chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            wd = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        wd.get(url)
        # options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        time.sleep(2)
        wd.maximize_window()
        time.sleep(5)
        search_path = wd.find_element(by=By.XPATH, value="/html/body/div[1]/header/nav/section/section[2]/form/section[1]/input")
        search_keyword = search_path.send_keys(keyword)
        search_path.send_keys(Keys.ENTER)
        time.sleep(3)

        try:
            no_results_message = wd.find_element(by=By.CLASS_NAME, value="core-section-container__main-title").text
        except:
            no_results_message =""
        if  no_results_message != "We couldn’t find a match for":
            no_of_jobs = int(wd.find_element(by=By.CSS_SELECTOR, value="h1>span").text.replace("+", "").replace(",",""))
            job_data = None
            job_id= []
            job_title = []
            company_name = []
            location = []
            date = []
            job_link = []
            seniority = []
            emp_type = []
            job_func = []
            industries = []
            claves = []
            i = 0
            while i <=no_of_jobs/25+1:
                i +=1
                try:
                    wd.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(2)
                except NameError:
                    wd.find_element(by=By.XPATH, value="/html/body/main/div/section/button").click()
                    time.sleep(5)
                except:
                    print("didnt find element to click ")
                    pass
                    time.sleep(5)

            jobs = wd.find_elements(by=By.CSS_SELECTOR, value='[data-row]')

            print("La cantidad de trabajos es "+ str(len(jobs)))
            index = 0
            for job in jobs:
                index +=1
                job_id0 = ""
                job_title0 = ""
                company_name0 = ""
                location0 = ""
                date0 = ""
                job_link0 = ""
                seniority0 = ""
                emp_type0 = ""
                job_func0=[]
                job_func_elements = []
                industries0=[]
                industries_elements=[]
                claves.append(keyword)
                try:
                    job_id0 = job.get_attribute("data-entity-urn").replace("urn:li:jobPosting:","")
                except Exception as e:
                    print('Error: ' + str(e))
                    job_id0 = ("")
                job_id.append(job_id0)
                try:
                        job_title0 = job.find_element(by=By.CSS_SELECTOR, value="h3").get_attribute("innerText")
                except:
                        job_title0 = ''
                job_title.append(job_title0)

                try:
                        company_name0 = job.find_element(by=By.CLASS_NAME, value='base-search-card__subtitle').text
                except:
                        company_name0 = ''
                    
                company_name.append(company_name0)

                try:
                    location0 = job.find_element(by=By.CLASS_NAME, value="job-search-card__location").text
                except:
                    location0 = ""
                location.append(location0)

                try:
                    date0 = job.find_element(by=By.CSS_SELECTOR, value="div>div>time").get_attribute("datetime")
                except:
                    date0 = ""
                date.append(date0)

                try:
                    job_link0 = job.find_element(by=By.CSS_SELECTOR, value="a").get_attribute("href")
                except:
                    job_link0 = ""
                job_link.append(job_link0)
                
                job.click()
                time.sleep(3)

                try:
                    job_criteria =wd.find_element(by=By.CLASS_NAME, value="description__job-criteria-subheader").text.strip()
                    if job_criteria =="Seniority level":
                        seniority0 = wd.find_element(by=By.CLASS_NAME, value=("description__job-criteria-text")).text
                    else:
                        seniority0 =""
                except :
                    seniority0 =""
                seniority.append(seniority0)
                try:
                    emp_type_path = "/html/body/div[1]/div/section/div[2]/div/section/div/ul/li[2]/span"
                    emp_type0 = job.find_element(by=By.XPATH, value=(emp_type_path)).text
                    emp_type.append(emp_type0)
                except:
                    emp_type.append("")

                try:
                    job_func_path = "/html/body/div[1]/div/section/div[2]/div/section/div/ul/li[3]/span"
                    job_func_elements = job.find_element(by=By.XPATH, value=job_func_path).text.split(', ')
                    for element in job_func_elements:
                        element.replace("and ", "")
                        job_func0.append(element)
                    job_func.append(','.join(job_func0))
                except :
                    job_func.append("")
                try:
                    industries_path = "/html/body/div[1]/div/section/div[2]/div/section/div/ul/li[4]/span"
                    industries_elements = job.find_element(by=By.XPATH, value=industries_path).text.split(', ')
                    for element in industries_elements:
                        element.replace("and ", "")
                        industries0.append(element)
                    industries.append(','.join(industries0))
                except :
                    industries.append("")
            data_to_upload = {"keyword":claves, "job_id": job_id, "job_title": job_title,"company_name": company_name,"location": location, "date": date, "job_link": job_link, "seniority": seniority, "job_func": ','.join(job_func),"emp_type": emp_type,  "industries": industries }
            job_data = pd.DataFrame(data_to_upload)
            if SUPABASE_ENABLE:
                data = supabase.table(TABLE_NAME).insert(data_to_upload).execute()
                print("uploaded", data)
            print(job_data)
    except Exception as e:
        print('Error: ' + str(e))
        pass
    wd.close()
    return job_data



#----------------------------------main----------------------------------
SUPABASE_ENABLE = False

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
TABLE_NAME = "jobot"

if SUPABASE_URL != "":
    SUPABASE_ENABLE = True
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else: 
    supabase = None

lista_de_jobs = scrapping("python vue")
#lista_de_jobs.to_csv("data_output.csv")
# try:
#     keywords =request.get("https://test-bot-penguin.herokuapp.com/keywords")
#     unique_list = list(dict.fromkeys(keywords))
#     print(unique_list)
#     for key in unique_list:
#         print(key[1])
#         print(type(key[1]))
#         lista_de_jobs = scrapping(key[1])
#         request.post("https://test-bot-penguin.herokuapp.com/keywords", data=lista_de_jobs)
        
# except Exception as e:
#     print(e)
#     pass

