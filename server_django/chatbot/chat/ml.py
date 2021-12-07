import os
from re import A
from django.http import response
import nltk
import datetime
from nltk.featstruct import retract_bindings
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
from tensorflow.python.ops.gen_math_ops import rint
import tflearn
import tensorflow as tf
import random
import json
import pickle

import requests
from bs4 import BeautifulSoup

import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

stemmer = LancasterStemmer()
# with open(os.path.join(BASE_DIR,'chat','intents.json')) as file:
# 	data = json.load(file)
with open(os.path.join(BASE_DIR, 'chat', 'data.pickle'), "rb") as f:
    # with open("./data.pickle","rb") as f:
    words, labels, training, output = pickle.load(f)


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

#Loading existing model from disk
model = tflearn.DNN(net)
model.load(os.path.join(BASE_DIR, 'chat', "model.tflearn"))

RESPONSE_PROBABILITY_THRESHOLD = 0.3

stopword = nltk.corpus.stopwords.words('english')


def remove_stopwords(text):
    text = [word for word in text if word not in stopword]
    return text


def getFormLink(message):
    with open(os.path.join(BASE_DIR, 'chat', 'formLinks.json')) as file:
        data = json.load(file)
    s = nltk.word_tokenize(message)
    s = remove_stopwords(s)
    s = [stemmer.stem(word.lower()) for word in s]
    if "form" in s:
        s.remove('form')

    formLinkDict = {}
    for key, value in data.items():
        s_key = nltk.word_tokenize(key)
        s_key = remove_stopwords(s_key)
        s_key = [stemmer.stem(word.lower()) for word in s_key]
        # s_key = ' '.join(s_key)
        for keyword in s:
            if keyword in s_key:
                formLinkDict[key] = value.replace(' ', '%20')

    if len(formLinkDict) > 0:
        return formLinkDict

    return False


def predict(message):
    results = model.predict([bag_of_words(message, words)])[0]
    result_index = np.argmax(results)
    tag = labels[result_index]
    response = {"answered": True, "reply_type": "", "reply": ""}
    if results[result_index] < RESPONSE_PROBABILITY_THRESHOLD:
        response["reply"] = "Ask again"
        response["answered"] = False
        return response
    print(tag)
    return chatBotResponse(message, tag)


def w(message, tag):

    if tag == "greeting":
        greettingResponses = [
            "Hello!", "Good to see you again!", "Hi there, how can I help?",
            "Hello! I'm Aiyo How may I help you?", "Hey there!"
        ]

        response = {
            "answered": True,
            "reply_type": "text",
            "reply": random.choice(greettingResponses)
        }

        return response

    if tag == "about":
        response = {"answered": True}

        # web scrapping
        url = "https://www.iiitdm.ac.in/Administration/About_IIITDM.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')
        # for elem in soup.find(class_='paragraph'):
        # 	print(elem)
        # for elem in soup.find(class_='paragraph').children:
        # 	print(".......")
        # 	print(elem.text)
        about = soup.find(class_='paragraph').contents
        response["reply_type"]="list"
        response["list"] = [
            about[2].text
        ]

        return response

    if tag == "why_iiitdm":
        response = {"answered": True, "reply_type": "text"}

        # web scrapping
        url = "https://www.iiitdm.ac.in/Admission/Overview.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')
        
        elem = soup.find(class_="paragraph").contents
        response["reply_type"]="text"
        response["reply"] = [elem[0], elem[2].strip()]

        return response
    if tag == "admission_iiitdm":

        response = {"answered": True, "reply_type": "table"}

        # web scrapping
        url = "https://www.iiitdm.ac.in/Admission/Overview.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')
        programs = []
        streams = []
        ancors = []
        table = soup.find('table')
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            ancors.append(row.find('a'))
            cols = [ele.text.strip() for ele in cols]
            programs.append([ele for ele in cols
                             if ele])  # Get rid of empty values
        for row in rows:
            cols = row.find_all('li')
            cols = [ele.text.strip() for ele in cols]
            streams.append([ele for ele in cols
                            if ele])  # Get rid of empty values
        data = {}
        for i, ival in enumerate(programs):
            data[ival[0]] = {
                "link":
                "https://www.iiitdm.ac.in/Admission/" +
                ancors[i].attrs['href'],
                "streams":
                streams[i]
            }
        response["body"] = data

        return response

    if tag == "undergraduate_admission":

        response = {"answered": True, "reply_type": "text"}

        # web scrapping
        url = "https://www.iiitdm.ac.in/Admission/Undergraduate.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(why|about)", message):
            response["reply"] = soup.find('p', class_='paragraph').text
            return response
        if re.search("(apply|get|take)", message.lower()):
            howToApply = soup.find_all('p', class_='paragraph')[1].text
            response["reply"] = howToApply
            return response

        if re.search("(rank)", message.lower()):
            response["reply_type"] = "link"
            response["link"] = url
            response[
                "reply"] = """For delail regarding Opening and Closing Ranks for UG. Admission is based only on All India Ranks (AIR). State Rank is not Considered for admission into IIITs."""
            return response
        response["reply"] = soup.find('p', class_='paragraph').text
        return response

    if tag == "dual_degree_admissions":

        response = {"answered": True, "reply_type": "text"}

        # web scrapping
        url = "https://www.iiitdm.ac.in/Admission/Dual.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(why|about)", message.lower()):
            response["reply"] = soup.find('p', class_='paragraph').text
            return response
        if re.search("(?=(how)).*(?=(apply|get|take))", message.lower()):
            howToApply = soup.find_all('p', class_='paragraph')[1].text
            response["reply"] = howToApply
            return response

        if re.search("(rank)", message.lower()):
            response["reply_type"] = "link"
            response["link"] = url
            response[
                "reply"] = """For delail regarding Opening and Closing Ranks for DD. Admission is based only on All India Ranks (AIR). State Rank is not Considered for admission into IIITs."""
            return response

        response["reply"] = soup.find('p', class_='paragraph').text
        return response

    if tag == "postgraduate_admissions":

        response = {"answered": True, "reply_type": "text"}

        # web scrapping
        url = "https://www.iiitdm.ac.in/Admission/Postgraduate.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(why|about)", message.lower()):
            response["reply"] = soup.find('p', class_='paragraph').text
            return response
        if re.search("(?=(how)).*(?=(apply|get|take))", message.lower()):
            howToApply = soup.find_all('p', class_='paragraph')[1].text
            response["reply"] = howToApply
            return response

        if re.search("(?<=(list))*(?=.*(program))", message.lower()):
            response["reply_type"] = "link"
            response["link"] = url
            r = soup.find_all(id="wrapper")
            listOfProgram = about[0].find_all("li")
            programs = []
            for item in listOfProgram:
                programs.append(item)

            response["reply"] = programs
            return response

        response["reply"] = "Please go to following link."
        return response

    if tag == "curriculum":

        response = {"answered": True, "reply_type": "text"}

        # web scrapping
        url = "https://www.iiitdm.ac.in/Academics/Curriculum.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(why|about)", message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[0].text
            return response
        if re.search("design.*centric ", message.lower()):
            howToApply = soup.find_all('p', class_='paragraph')[1].text
            response["reply"] = howToApply
            return response

        response["reply"] = soup.find_all(
            "p",
            class_='paragraph')[2].text + " Goto below link to get curriculam"
        return response

    if tag == "evaluation":
        response = {"answered": True, "reply_type": "text"}

        # web scrapping
        url = "https://www.iiitdm.ac.in/Academics/Evaluation.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(why|about)", message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[0].text
            return response
        if re.search("(grade|grading|grading.*system)", message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[1].text
            return response

        if re.search("(minimum).*(attendance)", message.lower()):
            para = soup.find_all("p", class_='paragraph')[5].text
            x = re.search('(?<=minimum of )\d\d%', para)
            response["reply"] = x.group()

            return response

        if re.search("(attendance)", message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[5].text
            return response
        if re.search("(grade|letter|associated)", message.lower()):
            response["reply_type"] = "image"
            response[
                "imageLink"] = "https://www.iiitdm.ac.in/img/pics/CGPAPoints.png"
            return response
        if re.search("(formula|calculation|calculated|gpa formula)",
                     message.lower()):
            response["reply_type"] = "image"
            response[
                "imageLink"] = "https://www.iiitdm.ac.in/img/pics/CGPA_Formula.png"
            return response

        response["reply"] = "goto folowing link"
        response["reply_type"] = "link"
        response["answered"] = False
        return response

    if tag == "undergraduate_programs":
        response = {"answered": True, "reply_type": "text"}

        # web scrapping
        url = "https://www.iiitdm.ac.in/Academics/Undergraduate.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(cse|computer|computer science)", message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[0].text
            return response

        if re.search(
                "(ece|electronics|electronics and communication engineering)",
                message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[2].text
            return response

        if re.search("(me|mechanical|mechanical engineering)",
                     message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[4].text
            return response
        if re.search("(sm|smart|smart manufacturing)", message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[6].text
            return response

        response["reply"] = "goto folowing link"
        response["reply_type"] = "link"
        response["answered"] = False
        return response

    if tag == "dual_degree_programs":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Academics/Dual.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')
        para = about = soup.find_all("p", class_='paragraph')

        if re.search("(cse|computer|computer science)", message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[0].text
            return response

        if re.search(
                "(ece|electronics|electronics and communication engineering)",
                message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[2].text
            return response

        if re.search("(me|mechanical|mechanical engineering)",
                     message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[4].text
            return response

        response["reply"] = "goto folowing link"
        response["reply_type"] = "link"
        response["answered"] = False
        return response

    if tag == "postgraduate_programs":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Academics/Postgraduate.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search(
                "(ece|electronics|electronics and communication engineering)",
                message.lower()):
            if re.search("(communication|communication systems)",
                         message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_='paragraph')[0].text
                return response
            if re.search("(microelectronics|vlsi|vlsi systems)",
                         message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_='paragraph')[2].text
                return response
        if re.search("(me|mechanical|mechanical engineering)",
                     message.lower()):
            if re.search("(mechanical|mechanical systems design)",
                         message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_='paragraph')[4].text
                return response
            if re.search("(smart|smart manufacturing)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_='paragraph')[6].text
                return response
        if re.search("(cse|computer|computer science)", message.lower()):
            if re.search(
                    "(data|data science|artificial|artificial intelligence|data science and artificial intelligence)",
                    message.lower()):
                response[
                    "reply"] = "New Course during the year 2021-22. FOr more deail go to link."
                return response
        if re.search("(mdes|integrated|integrated product design)",
                     message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[9].text
            return response

        response["reply"] = "goto folowing link"
        response["reply_type"] = "link"
        response["answered"] = False
        return response

    if tag == "doctoral_programs":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Academics/Doctoral.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(about)", message.lower()):
            response["reply"] = soup.find_all("p", class_='paragraph')[0].text
            return response

        if re.search("(research|research area)", message.lower()):
            response["reply_type"] = "list"
            response["reply"] = soup.find_all("p", class_='paragraph')[1].text
            response["list"] = [
                "Computer Science and Engineering", "Electronics Engineering",
                "Mathematics", "Mechanical Engineering", "Physics"
            ]
            return response

        response["reply"] = "goto folowing link"
        response["reply_type"] = "link"
        response["answered"] = False
        return response

    if tag == "forms":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Academics/forms.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        links = getFormLink(message)

        if links != False:
            response["link"] = url
            response["reply_type"] = "dictionary"
            response["reply"] = "Goto following link to get the form"
            response["dictionary"] = links
            return response

        response[
            "reply"] = "Can't find the desired form. Ask about specific form or vist Institute forms page."
        response["reply_type"] = "link"
        response["answered"] = False
        return response

    if tag == "seating_arrangement":
        response = {"answered": True, "reply_type": "link"}
        response["link"] = "http://iiitdm.ac.in/old/exams/Students_home.php"
        response[
            "reply"] = "Visit the following page to know about the seating arrangement."
        return response

    if tag == "research":
        response = {"answered": True, "reply_type": "link"}

        url = "https://www.iiitdm.ac.in/Research/Overview.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search(
                "(sponsored|research|sponsored research|sponsored research and consultancy|consultancy)",
                message.lower()):
            response["reply_type"] = "text"
            response["reply"] = soup.find_all("p", class_='paragraph')[1].text
            return response

        if re.search("(mou|memorandum|memorandum of understanding)",
                     message.lower()):
            response["reply_type"] = "list"
            response["reply"] = soup.find_all("p", class_='paragraph')[2].text
            response["list"] = [
                "University of Genova, Italy", "University of Catania, Italy",
                "Nagaoka University of Technology, Japan",
                "HITACHI, Japan (Student Exchange Program)"
            ]
            return response

        response["answered"] = False
        response["reply"] = soup.find_all(
            "p", class_='paragraph'
        )[0].text + " For more deail visit following link."
        response["reply_type"] = "link"
        return response

    if tag == "funded_proects":
        response = {"answered": True, "reply_type": "link"}
        response[
            "link"] = "https://www.iiitdm.ac.in/Research/Funded_Project.php"
        response[
            "reply"] = "Visit the following page to know about the funded projects."
        return response

    if tag == "campus":
        response = {"answered": True, "reply_type": "video"}
        response["link"] = "https://www.iiitdm.ac.in/Others/tour.php"
        response[
            "reply"] = "You can get a virual campus tour. Watch campus tour video or expirience 360\N{DEGREE SIGN} view."
        response["videoLink"] = "https://youtu.be/ujtUyW30P60"
        return response

    if tag == "hostel":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Campus/Hostel.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search(
                "(rule.|regulation.|rules and regulations for hostel residents)",
                message.lower()):
            response["reply_type"] = "dictionary"
            response["dictionary"] = {
                "Download Rules and Regulations Booklet for Hostel Residents":
                "https://www.iiitdm.ac.in/img/students/Hostel_Rules_&_Regulations_2018.pdf",
                "Important Circular - I":
                "https://www.iiitdm.ac.in/img/students/1.pdf",
                "Important Circular - II":
                "https://www.iiitdm.ac.in/img/students/2.pdf"
            }
            return response

        response["reply_type"] = "text"
        response["reply"] = soup.find_all("p", class_='paragraph')[0].text
        return response

    if tag == "infrastructure":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Campus/Infrastructure.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')
        if re.search("(map)", message.lower()):
            response["reply_type"] = "image"
            response[
                "imageLink"] = "https://www.iiitdm.ac.in/img/Infrastructure/map.jpg"
            return response

        if re.search("(academic|academic blocks)", message.lower()):
            response["reply_type"] = "text"
            response["reply"] = soup.find_all("p", class_='paragraph')[1].text
            return response

        if re.search("(library|library facility)", message.lower()):
            response["reply_type"] = "text"
            response["reply"] = soup.find_all("p", class_='paragraph')[2].text
            return response

        if re.search("(residence|hall of residence)", message.lower()):
            response["reply_type"] = "text"
            response["reply"] = soup.find_all("p", class_='paragraph')[3].text
            return response

        if re.search("(dining|dining and shopping|shopping)", message.lower()):
            response["reply_type"] = "text"
            response["reply"] = soup.find_all("p", class_='paragraph')[4].text
            return response

        if re.search("(medical|care|doctor|medical aid centre)",
                     message.lower()):
            response["reply_type"] = "text"
            response["reply"] = soup.find_all("p", class_='paragraph')[5].text
            return response

        if re.search("(atm|atm facility)", message.lower()):
            response["reply_type"] = "text"
            response["reply"] = soup.find_all("p", class_='paragraph')[6].text
            return response

        response["reply_type"] = "text"
        response["reply"] = soup.find_all("p", class_='paragraph')[0].text
        return response

    if tag == "about_mess":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Campus/Infrastructure.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(menu|mess menu)", message.lower()):
            response["reply_type"] = "dictionary"
            response["reply"] = "Download mess mene from below link."
            response["dictionary"] = {
                "Download Mess Menu":
                "https://www.iiitdm.ac.in/img/hotels/Final_Menu_2019.pdf"
            }
            return response

        response["reply_type"] = "dictionary"
        response["reply"] = "Get detail of mess menu from below link."
        response["dictionary"] = {
            "Download Mess Menu":
            "https://www.iiitdm.ac.in/img/hotels/Final_Menu_2019.pdf"
        }
        return response

    if tag == "faculty":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/People/faculty.php"
        response["link"] = url
        response["reply_type"] = "link"
        response["reply"] = "Get the list of all faculty."
        return response

    if tag == "Staff":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/People/staff.php"
        response["link"] = url
        response["reply_type"] = "link"
        response["reply"] = "Get the list of all staff."
        return response

    if tag == "sports":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Campus/Sports.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search(
                "(image|facilities|facility|sport. facility|sports facilities)",
                message.lower()):
            response["reply_type"] = "dictionary"
            response["reply"] = soup.find_all(
                "p", class_='subheader')[0].text + "\n" + soup.find_all(
                    "p", class_='paragraph')[0].text

            response["dictionary"] = {
                "Arjuna Sports Complex":
                "https://www.iiitdm.ac.in/img/sports/indoor.jpg",
                "Indoor Badminton Court":
                "https://www.iiitdm.ac.in/img/sports/badminton.JPG",
                "Indoor Basketball Court":
                "https://www.iiitdm.ac.in/img/sports/basketball.jpg",
                "Outdoor Volleyball Court":
                "https://www.iiitdm.ac.in/img/sports/volleyball.JPG",
                "Cricket Ground":
                "https://www.iiitdm.ac.in/img/sports/cricket.jpg",
                "Football Ground":
                "https://www.iiitdm.ac.in/img/sports/football.jpg",
                "Tennis Court":
                "https://www.iiitdm.ac.in/img/sports/tennis.jpg",
                "Table Tennis Room":
                "https://www.iiitdm.ac.in/img/sports/tt.jpg"
            }
            return response
        if re.search("(tournament.)", message.lower()):
            response["reply_type"] = "dictionary"
            response["reply"] = soup.find_all(
                "p", class_='subheader')[0].text + "\n" + soup.find_all(
                    "p", class_='paragraph')[0].text

            response["dictionary"] = {
                "Inter IIIT Sports Meet":
                "https://www.iiitdm.ac.in/img/sports/inter.JPG",
                "Design & Manufacturing Premier League":
                "https://www.iiitdm.ac.in/img/sports/inter.JPG",
                "Freshie Tournament":
                "https://www.iiitdm.ac.in/img/sports/inter.JPG"
            }
            return response
        if re.search("(house.*)", message.lower()):
            houses_d = {}
            houses = soup.find_all("ul")[-7].find_all("li")
            for item in houses:
                key = re.search("([A-Za-z]*)", item.text).group(0)
                val = re.search("(Cap.*[^)])", item.text).group(0)
                houses_d[key] = val

            response["reply_type"] = "dictionary"
            response["dictionary"] = houses_d

            return response

        response["reply_type"] = "text"
        response["reply"] = soup.find_all(
            "p", class_='subheader')[0].text + "\n" + soup.find_all(
                "p", class_='paragraph')[0].text
        return response

    if tag == "cultural_clubs":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Campus/cClubs.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(list|all|are)", message.lower()):
            response["reply_type"] = "list"
            response["list"] = [
                "Cultural Club", "Fun Club", "Art Club", "The Language Club",
                "Dramatics Club", "Literature Club", "Music Club",
                "Dance Club", "Photography Club", "Gaming Club",
                "Adventure Club"
            ]
            return response

        if re.search("(cultural culb|cultural)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[1].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[0].text

            return response

        if re.search("(fan culb|fan)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[3].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[2].text

            return response
        if re.search("(art culb|art)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[5].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[4].text
            return response

        if re.search("(language  culb|language)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[7].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[6].text

            return response
        if re.search("(dramatics culb|dramatics)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[9].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[8].text

            return response
        if re.search("(literature culb|literature)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[11].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[10].text

            return response
        if re.search("(music culb|music)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[13].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[12].text
            return response

        if re.search("(dance culb|dance)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[15].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[14].text
            return response

        if re.search("(photography culb|photography)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[17].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[16].text
            return response

        if re.search("(gaming culb|gaming)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[19].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[18].text
            return response

        if re.search("(adventure culb|adventure)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[21].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[20].text
            return response

        response[
            "reply"] = "Below are the list of clubs. Try asking about individual clubs."
        response["reply_type"] = "list"
        response["list"] = [
            "Cultural Club", "Fun Club", "Art Club", "The Language Club",
            "Dramatics Club", "Literature Club", "Music Club", "Dance Club",
            "Photography Club", "Gaming Club", "Adventure Club"
        ]
        return response

    if tag == "technical_clubs":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Campus/tClubs.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(list|all|are)", message.lower()):
            response["reply_type"] = "list"
            response["list"] = [
                "Robotics", "Electronics Club", "Zerone Club",
                "Entrepreneurship and Investment Club",
                "Industrial Design Corner (IDC)", "Ingenium Club"
            ]
            return response

        if re.search("(designers culb|designers|designer)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[1].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[0].text

            return response

        if re.search("(robotics culb|robotics|robotic)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[3].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[2].text

            return response
        if re.search("(electronics culb|electronics|electronic)",
                     message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[5].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[4].text
            return response

        if re.search("(zerone culb|zerone)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[7].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[6].text

            return response
        if re.search(
                "(entrepreneurship|investment|entrepreneurship and investment club)",
                message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[9].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[8].text

            return response
        if re.search("(industrial design corner|industrial|design)",
                     message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[11].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[10].text

            return response
        if re.search("(ingenium culb|ingenium)", message.lower()):
            response["reply_type"] = "text"
            if re.search("(core|head)", message.lower()):
                response["reply"] = soup.find_all("p",
                                                  class_="paragraph")[13].text
                return response
            response["reply"] = soup.find_all("p", class_="paragraph")[12].text
            return response

        response["reply_type"] = "list"
        response[
            "reply"] = "Below are the list of clubs. Try asking about individual clubs."
        response["list"] = [
            "Robotics", "Electronics Club", "Zerone Club",
            "Entrepreneurship and Investment Club",
            "Industrial Design Corner (IDC)", "Ingenium Club"
        ]
        return response

    if tag == "events":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Campus/events.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(website|url|address)", message.lower()):
            response["reply_type"] = "link"
            response["link"] = "www.samgatha.org"
            return response

        if re.search("(samgatha)", message.lower()):
            response["reply"] = soup.find_all("p", class_="paragraph")[0].text
            return response

        response["reply"] = "Goto the following link."
        response["link"] = url
        return response

    if tag == "ssg":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Campus/events.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        response["reply_type"] = "list"
        response["reply"] = soup.find_all(
            "p",
            class_="paragraph")[0].text + " Get more info from below link."
        response["list"] = [
            "Free Eye Screening Camp",
            "Polio Drops Drive",
            "Computer Classes for Local School Students",
            "Beach Cleaning Activity",
            "Blood Donation",
            "Tree Plantation Activity",
            "Zoo Cleaning Activity",
        ]
        return response

    if tag == "vidhai":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Campus/events.php"
        response["link"] = url
        r = requests.get(url)
        htmlAboutContent = r.content

        soup = BeautifulSoup(htmlAboutContent, 'html.parser')

        if re.search("(vision)", message.lower()):
            response["reply"] = soup.find_all("p", class_="paragraph")[1].text
            response["reply_type"] = "text"
            return response

        if re.search("(mission)", message.lower()):
            mission = soup.find_all("p", class_="paragraph")
            response["reply"] = mission[1] +"\n"+ """‘Teaching’ activity that involves our student-volunteers interested in dispensing knowledge to the students of government schools in a digitalised environment irrespective of the languages the volunteers know. Any volunteer who has a passion for teaching can teach any subject among English, Basic Sciences, Soft-Skills, Mathematics.""" \
                    +"\n"+ """‘Non-Teaching’ activity involves tasks relating to the development of infrastructure of the schools possible with the help of funds raised by the students of the institute"""

            response["reply_type"] = "text"
            return response

        if re.search("(voluntery|voluntery works)", message.lower()):
            vol = soup.find_all("p", class_="paragraph")
            response["reply"] = vol[3].text + vol[4] + "\n" + vol[5] + vol[6]
            response["reply_type"] = "text"
            return response

        response["reply_type"] = "text"
        response["reply"] = soup.find_all("p", class_="paragraph")[0].text
        response["link"] = url
        return response

    if tag == "publications":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Research/Publications.php"
        response["link"] = url
        response["reply_type"] = "link"
        response["reply"] = "Get the detail of publication."
        return response

    if tag == "reach_iiitdm":
        response = {"answered": True, "reply_type": "text"}
        url = "https://www.iiitdm.ac.in/Others/map.php"
        response["link"] = url
        response["reply_type"] = "link"
        response[
            "reply"] = "Get the detail about hoe to reach IIITDM Kancheeppuram."
        return response

    if tag == "academic_calender":
        response = {"answered": True, "reply_type": "text"}
        url = "https://iiitdm.ac.in/Academics/ACADEMIC_CALENDAR.php"
        response["link"] = url
        response["reply_type"] = "link"
        response["reply"] = "Get the detail about academic calender."
        return response

    if tag == "contact":
        response = {"answered": True, "reply_type": "text"}
        url = "https://iiitdm.ac.in/Academics/ACADEMIC_CALENDAR.php"
        response["link"] = url
        response["reply_type"] = "dictionary"
        response["dictionary"] = {
            "Office phone": "+91-44-27476300",
            "Office email": "office@iiitdm.ac.in",
            "Academics phone": "+91-9566715970",
            "Academics email": "academics@iiitdm.ac.in",
            "Hostel email": "hosteloffice@iiitdm.ac.in",
        }
        return response
