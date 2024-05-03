<h1> 🧐 HADA Application </h1>

- ## Overview

AI application is designed to meticulously search through Endava profiles, pinpointing the most suitable candidates based on specific job posting requirements. By leveraging advanced algorithms, it meticulously analyses candidate profiles to identify those that align best with the criteria outlined in the job postings

The interviewer's assistant conducts interviews and assesses candidates based on both technical competencies and alignment with company values.

After each interview, the interviewer's assistant provides a comprehensive assessment of each candidate's strengths and weaknesses. Additionally. Finally, users can access a dashboard showcasing insights gathered from each candidate's interview.

- ## How to use HADA
Interacting with HADA follows a straightforward process via its user-friendly interface. Additionally, users can see instructions through the menu located in the left panel of the application.

### Instructions:

#### - File loader
Load the Endava profiles in the HADA repository.

#### - Profile loader
Utilize the profile loader function in HADA to import Endava profiles into its database. This feature offers two options: "Load Profiles" to import PDFs from the repository and process, and "Show Profiles" to view candidates' skills and qualifications.

#### - Search candidates
With the search candidates assistant, you can retrieve the top profiles based on the previously loaded files.

#### - Dashboard candidates
View the statistics of the candidates' qualifications within the candidate dashboard.

#### - HADA Recruiter interview
HADA assists recruiters in conducting interviews with selected candidates.

#### - Dashboard Recruiter
View the final statistics within the Recruiter dashboard.


## 💻 Architecture
![Architecture](images/architecture.png)

## 🛠️ Installation Process

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the next libraries.

```bash
pip install openai
pip install streamlit
pip install python-dotenv
pip install PyPDF2
pip install st-pages
pip install chromadb
pip install pandas
```

Create a .env file in the root folder containing the respective keys

```python
OPENAI_API_KEY=<ADD THE API KEY>   # Ensure you use the correct API key
AZURE_ENDPOINT=<ADD THE ENDPOINT> 
API_VERSION=<ADD THE API VERSION>     # Ensure you use the correct API version
PROFILES_PATH=<ABSOLUTE PROJECT PATH>
```

## 🚀 Usage
The following commands execute the application.


```python

#1. Start the python environment.
    #If you are a windows user use the following
    .\venv\Scripts\activate 
    # If you are linux and Mac OSx user use the following
    source venv/Scripts/activate 

#2. Then start the dependencies
    chroma run
    streamlit run src/main.py
```
## 📘 Additional resources
In the following link you can find the additional resources related to the presentation process


https://drive.google.com/drive/folders/1ICy3z6v8auspf8uQJGvikN1Lk_UNpfVk?usp=sharing


## 🙇 Team members

* Oscar Vivas   
* Hassan Marquez
* Tamara Carrizo Bertuzzi 
* Nicolas Angelini
* Martin Saponara

## 🙏 License

[MIT]
(https://choosealicense.com/licenses/mit/)

*Developed with ❤️ for Endava*
