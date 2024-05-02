
import re

string = """Name: Adriana Flores 
Core Skill: AM Analyst English Level: B2 Technologies: Pascal, Visual Basic, PHP, Assembly language, Microsoft SQL Server, Microsoft SQL Server Express, Ubuntu, Sql Server, SQL, Raspberry, QEMU, Postman, Microsoft Azure Soft Skills: Teamwork, Strong Analytical Skills, Management, Leadership Development, Ethical thinking, Curiosity, Client Oriented, Client Relationship, Adaptability, Analysis, Azure Industry Verticals: Energy, Mobility Certifications: Cloud Computing for beginners -Infrastructure as a Service, Identity and Access Governance (IAM/IAG/IGA), Windows Server 2019 administration, Introduction to Cloud Computing on AWS for beginners 2024, Chat GPT Complete Guide: Learn MidJourney, ChatGPT 4 & More Spoken Languages: Spanish (Native), English (B2)
Matching with company values:
Smart: High Thoughtful: Medium Open: Medium Adaptable: High Trusted: Medium"""
name = ""
if re.search('Name:(.*)\nCore Skill', string):
    name = re.search('Name:(.*)\nCore Skill', string).group(1)

print(name)
