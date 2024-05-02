import re
import chromadb
from chromadb.config import Settings

def connect_database():
    client_database = chromadb.PersistentClient(path="./database/", settings=Settings(allow_reset=True))
    #client_database = chromadb.HttpClient()
    return client_database


def delete_collection(collection_name):
    client_database = connect_database()
    client_database.reset()

    # delete if exits
    if collection_name in [c.name for c in client_database.list_collections()]:
        client_database.delete_collection(name=collection_name)


def initialize_collection(collection_name):
    client_database = connect_database()

    # delete if exits
    if collection_name in [c.name for c in client_database.list_collections()]:
        client_database.delete_collection(name=collection_name)

    return client_database.get_or_create_collection(name=collection_name)


def load_documents():

    id = 0
    ids = []
    documents = []
    metadatas = []

    list = ["""Name: Adriana Flores Core Skill: AM Analyst English Level: B2 Technologies: Pascal, Visual Basic, PHP, Assembly language, Microsoft SQL Server, Microsoft SQL Server Express, Ubuntu, Sql Server, SQL, Raspberry, QEMU, Postman, Microsoft Azure Soft Skills: Teamwork, Strong Analytical Skills, Management, Leadership Development, Ethical thinking, Curiosity, Client Oriented, Client Relationship, Adaptability, Analysis, Azure Industry Verticals: Energy, Mobility Certifications: Cloud Computing for beginners -Infrastructure as a Service, Identity and Access Governance (IAM/IAG/IGA), Windows Server 2019 administration, Introduction to Cloud Computing on AWS for beginners 2024, Chat GPT Complete Guide: Learn MidJourney, ChatGPT 4 & More Spoken Languages: Spanish (Native), English (B2)
Matching with company values:
Smart: High Thoughtful: Medium Open: Medium Adaptable: High Trusted: Medium""", """Name: Alejandro García Core Skill: Project Management English Level: B2+
Technologies:
Agile
PMI
Jira
Scrum
ITIL v4
AWS services
Confluence
GitHub
Linux
Microsoft Azure
SQL
Soft Skills:

Analysis
Autonomy
Client oriented
Management
Problem Solving
Risk
Strong Analytical Skills
Organization
Match with Company Values:

Smart: Medium
Thoughtful: Medium
Open: High
Adaptable: Medium
Trusted: High"""]
    for response in list:
        documents.append(response)
        name = ""
        if re.search('Name:(.+?)Core Skill', response):
            name = re.search('Name:(.+?)Core Skill', response).group(1)
        source = {}
        source["source"] = name
        metadatas.append(source)

        id += 1
        ids.append("id"+ str(id))

    print(ids)
    print(documents)
    print(metadatas)

    client_database = connect_database()
    client_database.reset()
    collection = client_database.get_or_create_collection(name="embedding_profiles")
    collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
    print("")
    print(collection)
    print(collection.get())
    print(collection.get()["documents"])



if __name__ == "__main__":

    delete_collection("embedding_profiles")
    load_documents()

