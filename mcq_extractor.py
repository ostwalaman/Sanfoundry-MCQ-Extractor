# Importing Modules
import requests
from bs4 import BeautifulSoup
import os
import sys

total_topics_fetched = 0
total_question_fetched = 0

error_question = dict()

print("Default Topic is Computer Networks MCQ\n")

ch = input("Do you want to enter Sanfoundry Site Manually (y/n)?").lower()
fetchall = input("Do you want to fetch all Next Topics to this Topic (y/n)?").lower() #Fetch Specific Page or List of Pages

if(ch == "yes" or ch == "y"):
    next_link = input("Enter Site URL: ").strip()
else:
    next_link = "https://www.sanfoundry.com/computer-networks-mcqs-basics/" #Sample Site / Default Site

filename = input("Enter Filename with .txt extension: ")

try:
    if(filename in os.listdir()):
        print("Filename already Exists! Try Renaming / Deleting the Existing File")
        sys.exit()
    f = open(filename, 'wb')

    while True:
        data = requests.get(next_link)
        soup = BeautifulSoup(data.content, 'html5lib')
        topic = soup.find('h1', attrs = {'class' : 'entry-title'})
        if(topic is None):
            print("Something Went Wrong!!")
            break
        heading = topic.text
        print("Topic:", heading)
        list_of_div = soup.find('div', attrs = {'class' : 'entry-content'})

        # Questions
        questions = list_of_div.findAll('p')[1:-3]

        total_questions = len(questions)
        print("Total Questions: ", total_questions)

        list_of_ans = soup.findAll('span', attrs = {'class' : 'collapseomatic'})

        # Answers
        list_of_ans = soup.findAll('div', attrs = {'class' : 'collapseomatic_content'})[:total_questions]

        f.write("\n\n\t\t".encode() + heading.encode() + '\n\n'.encode())
        print(heading)

        for i in range(total_questions):
            total_question_fetched += 1
            currQuestion = questions[i].text
            currAnswer = list_of_ans[i].text
            f.write(currQuestion.encode() + '\n'.encode() + currAnswer.encode() + '\n\n'.encode())

        # Increment Topic Fetched Counter
        total_topics_fetched += 1
        if(fetchall == 'no' or fetchall == 'n'):
            break
        links = soup.findAll('div', attrs = {'class' : 'sf-nav-bottom'})
        next_link_a = links[1]
        
        link_tag = next_link_a.find('a')

        if(link_tag is None):
            print("End")
            break
        if('Next' in link_tag.text): #Next Link Found
            next_link = link_tag['href']
            print(next_link)
            # break
        else:
            print("End")
            break

    print(f'Total Topics Fetched: {total_topics_fetched} \nTotal Questions {total_question_fetched}')

except requests.exceptions.ConnectionError:
    print("Network Error!!!")