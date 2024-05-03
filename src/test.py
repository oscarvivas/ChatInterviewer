
import re

text = """Smart: high
Thoughtful: medium
Open: medium
Adaptable: medium
Trusted: low"""

lines = text.split('\n')
values = []
qualifications = []

for line in lines:
    try:
        value, qualification = line.split(': ')
        value = re.sub(r'[^A-Z:a-z0-9]+', '', value.strip())
        qualification = qualification.strip() 
        if value in ['Smart', 'Thoughtful', 'Open', 'Adaptable', 'Trusted', 'smart', 'thoughtful', 'open', 'adaptable', 'trusted']:
            values.append(value)
            qualifications.append(qualification)
    except Exception as e:
        print("Error method extract_qualifications " + str(e))
        


string = """Name: Adriana Flores 
Core Skill: AM Analyst English Level: B2 Technologies: Pascal, Visual Basic, PHP, Assembly language, Microsoft SQL Server, Microsoft SQL Server Express, Ubuntu, Sql Server, SQL, Raspberry, QEMU, Postman, Microsoft Azure Soft Skills: Teamwork, Strong Analytical Skills, Management, Leadership Development, Ethical thinking, Curiosity, Client Oriented, Client Relationship, Adaptability, Analysis, Azure Industry Verticals: Energy, Mobility Certifications: Cloud Computing for beginners -Infrastructure as a Service, Identity and Access Governance (IAM/IAG/IGA), Windows Server 2019 administration, Introduction to Cloud Computing on AWS for beginners 2024, Chat GPT Complete Guide: Learn MidJourney, ChatGPT 4 & More Spoken Languages: Spanish (Native), English (B2)
Matching with company values:
Smart: High Thoughtful: Medium Open: Medium Adaptable: High Trusted: Medium"""
name = ""
if re.search('Name:(.*)\nCore Skill', string):
    name = re.search('Name:(.*)\nCore Skill', string).group(1)

print(name)


string = """Yes, I understand the task. Here's how I'll proceed:

Count the skills mentioned in the job description.
Count how many of those skills are also listed in the candidate's resume.
Divide the number of matching skills by the total number of skills mentioned in the job description to calculate the match percentage.
Let's start by listing the skills mentioned in the job description and the candidate's resume:

Skills mentioned in the job description:

C#
Visual Studio
SQL Server
React
Node.js
Angular
HTML
CSS
JavaScript
RESTful APIs
Git
Skills mentioned in the candidate's resume:

Java
Python
SQL
Microsoft SQL Server
HTML
CSS
PostgreSQL
Oracle
MongoDB
Selenium
Git
GitHub
Now, let's count the matching skills:

Count of skills mentioned in the job description: 11
Count of matching skills between the job description and the resume: 3 (HTML, CSS, Git)
Now, let's calculate the match percentage:

Match percentage: (3 / 11) * 100 = 27.27%
Here's the result presented as a bullet point:

Match percentage: 27.27%
"""

last_line = string.splitlines()[-1]
print(last_line)



