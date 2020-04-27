from bs4 import BeautifulSoup
import requests
import json
import time

startTime = time.time()

# final list of courses
finalList = []
url = 'https://www.coursebuffet.com'
response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")
#resultlist-unit-coursetitle
#print(content)
allSubjectLink = url + content.find('a', attrs={"class": "popc-subjectlink"})['href']
responseSubjects = requests.get(allSubjectLink, timeout=5)
contentallSubjects = BeautifulSoup(responseSubjects.content, "html.parser")
subNameTags = contentallSubjects.findAll('li', attrs={"class": "subname"})
print(subNameTags)
exit(0)
subjectUrls = []
courseRatings = []
courseDifficultyLevel = []
finalListSubjects = []
for li in subNameTags:
    finalList.append({"subjectUrl": url + li.a['href'], "subName": li.a.text})
# print(finalList)
# exit(0)

courseTitleTags = {}
courseDescSpans = []
courseInfoUrls =[]
# All the courses and titles.
for subject in finalList:
    subjectUrlResponse = requests.get(subject['subjectUrl'], timeout=10)
    subjectUrlContent = BeautifulSoup(subjectUrlResponse.content, "html.parser")
    courseTitleTags = subjectUrlContent.findAll('span', attrs={"class": "resultlist-unit-coursetitle"})
    courseDescSpans = subjectUrlContent.findAll('span', attrs={"class": "resultlist-unit-coursedesc"})
    subject['courses'] = []
    for course in range(len(courseTitleTags)):
        subject['courses'].append({})
        subjectCourse = subject['courses'][course]
        subjectCourse['courseTitle'] = courseTitleTags[course].a.text
        subjectCourse['courseDesc'] = courseDescSpans[course].span.text
        courseInfoUrl = subjectCourse['courseInfoUrl'] = url + courseTitleTags[course].a['href']
        courseInfoUrlResponse = requests.get(courseInfoUrl, timeout=10)
        courseInfoUrlContent = BeautifulSoup(courseInfoUrlResponse.content, "html.parser")
        courseInfoDetails = courseInfoUrlContent.findAll('ul', attrs={"class": "CourseInfoTab-list1"})
        courseInfoLi = []
        for courseSpan in courseInfoDetails:
            courseInfoLi.extend(courseSpan.findAll('li'))
        subjectCourse['courseInfoDetails'] = {}
        for cis in range(len(courseInfoLi)):
            liTitle = courseInfoLi[cis].find('span').text
            courseInfoLi[cis].find('span').clear()
            subjectCourse['courseInfoDetails'][liTitle] = courseInfoLi[cis].text
        courseRatings = courseInfoUrlContent.find('span', attrs={"class": "ratingblock-underline"})
        courseRating = ""
        if courseRatings is not None:
            courseRating = courseRatings.text
        subjectCourse['courseRating'] = courseRating
        courseTags = courseInfoUrlContent.find('div', attrs={"class": "coursepage-extrainfo-coursetags"})
        subjectCourse['courseTags'] = []
        if courseTags is not None:
            courseMultipleTags = courseTags.findAll('a')
            for t in range(len(courseMultipleTags)):
                subjectCourse['courseTags'].append(courseMultipleTags[t].text)


f = open("c:\\temp\\data1.json", "w")
jsonDump = json.dumps(finalList)
f.write(jsonDump)
f.close()
print(jsonDump)

endTime = time.time()
timeTaken = endTime - startTime
print("Time Taken: ", timeTaken)
exit(0)
