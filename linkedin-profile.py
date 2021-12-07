from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import csv
import parameters
from selenium.webdriver.common.keys import Keys
from time import sleep
from parsel import Selector

data = []

# writer = csv.writer(open('results_file.csv', 'w'))

# writerow() method to the write to the file object
# writer.writerow(['Name', 'Job Title', 'Company', 'College', 'Location', 'URL'])


driver = webdriver.Chrome(parameters.chrome_web_driver)     #chrome_web_driver

driver.get(parameters.linkedin_url)                         #linkedin_url
driver.find_element(By.XPATH, "//*[@id='session_key']")     # username/email

# locate email form by_class_name
username = driver.find_element(By.XPATH, "//*[@id='session_key']")  

# send_keys() to simulate key strokes
username.send_keys(parameters.linkedin_username)            #linkedin_username            

sleep(0.5)

# locate password form by_class_name
password = driver.find_element(By.XPATH, "//*[@id='session_password']")

# send_keys() to simulate key strokes
password.send_keys(parameters.linkedin_password)            #linkedin_password
sleep(0.5)
# locate submit button by_xpath
log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')

# .click() to mimic button click
log_in_button.click()
sleep(0.5)
driver.get(parameters.google_url)                       #google_url  
sleep(3)
# locate search form by_name
search_query = driver.find_element_by_xpath('//*[@name="q"]')

# send_keys() to simulate the search text key strokes
search_query.send_keys(parameters.search_query)   #search_query
sleep(0.5)
# .send_keys() to simulate the return key
search_query.send_keys(Keys.RETURN)
sleep(3)
# locate URL by_class_name
linkedin_urls = driver.find_elements_by_css_selector(".yuRUbf [href]")

linkedin_urls = [url.get_attribute('href') for url in linkedin_urls]

sleep(0.5)
print("links", linkedin_urls)

# driver.page_source

for linkedin_url in linkedin_urls:
    # get the profile URL
    driver.get(linkedin_url)

    # add a 5 second pause loading each URL
    sleep(5)

    # assigning the source code for the webpage to variable sel
    sel = Selector(text=driver.page_source)
    print(sel)

    name = sel.xpath('//*[starts-with(@class, "text-heading-xlarge inline t-24 v-align-middle break-words")]/text()').extract_first()

    if name:
        name = name.strip()


    # xpath to extract the text from the class containing the job title
    job_title = sel.xpath('//*[starts-with(@class, "text-body-medium break-words")]/text()').extract_first()

    if job_title:
        job_title = job_title.strip()


    # xpath to extract the text from the class containing the company
    company = sel.xpath('//*[starts-with(@aria-label, "Current company")]/text()').extract_first()

    if company:
        company = company.strip()


    # xpath to extract the text from the class containing the college
    college = sel.xpath('//*[starts-with(@aria-label, "Education")]/text()').extract_first()

    if college:
        college = college.strip()


    # xpath to extract the text from the class containing the location
    location = sel.xpath('//*[starts-with(@class, "text-body-small inline t-black--light break-words")]/text()').extract_first()

    if location:
        location = location.strip()

    person_data = [name, job_title, company, college, location, linkedin_url]    
    data.append(person_data)
    # print(name,",", job_title,",", company,",", college,",", location)

    linkedin_url = driver.current_url
    name = job_title = company = college = location = 0
# terminates the application
# if data != []:
#     writer.writerows(data)
driver.quit()

header = ['Name', 'Job Title', 'Company', 'College', 'Location', 'URL']

with open(parameters.employee_details, 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write multiple rows
    print(data)
    writer.writerows(data)
