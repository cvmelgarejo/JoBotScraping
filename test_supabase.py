# author: Williams Bobadilla
# creted_at: 29 may 2022
# description: supabase test


from curses import keyname
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')


supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

rows= supabase.table("jobs").select("*").execute()
print(rows)

claves ="clave"
job_id =4
job_title ="programdor"
company_name = "name"
location = "location"
job_link ="fsdfohsdfasdfjasdfdsf"
seniority ="senio"
date="20-05-2022"
job_func = ["sdfas","fsdfa"]
emp_type = ""
industries = "Start"

data_to_upload = {"keyword":claves, "job_id": job_id, "job_title": job_title,"company_name": company_name,
                "location": location, "date": date, "job_link": job_link, "seniority": seniority, 
                "job_func": ','.join(job_func),"emp_type": emp_type,  "industries": industries }


#data = supabase.table("jobs").insert(data_to_upload).execute()
#print("uploaded", data)


print("--"*20)
print("querying")
keyword = "clav"
result =supabase.table("jobs").select("*").like("keyword", f"%{keyword}%").execute()
print(result)

