from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
import google.generativeai as genai
from PIL import Image
import pdf2image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input , pdf_content , prompt):
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content([input , pdf_content[0] , prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        #Convert Into Bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr , format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/JPEG",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
    
        return pdf_parts
    else:
        raise FileNotFoundError("No File Uploaded")
    

## SETUP Streamlit app

st.set_page_config(page_title = ("ATS Resume Expert"))

st.header("ATS Tracking System")

input_text = st.text_area("Job Description: ",key="input")

uploaded_file = st.file_uploader("Upload Your Resume!(PDF)" , type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully!")

submit1 = st.button("Tell Me About the Resume")

submit2 = st.button("How Can I Improvise My skill")

submit3  = st.button("Get ATS Score")

submit4 = st.button("Percentage Match")

input_prompt1 = """
 You are an experienced Technical Human Resource manager ,your task is to review the provided resume against the job description.
 Please share your professional evaluation on whether the candidate's profile aligns with the role. Highlight the strengths and weaknesses
 of the applicant in the relation to the specified job requirements.
 """

input_prompt2 = """
You are an Technical Human Resource Manager with expertise in the feild of any one job role from data science, Full Stack web development , Big data Engineering , DEVOPS, Data Analytics, your role is to scrutinize the resume in light of the job description provided. Share your insights on the candidate's suitability for the role from an HR perspective. Additionally, offer advice on enhancing the candidate's skills and identify areas that needs to be worked on.
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding in the feild of any one job role from Data Science ,Full Stack web development , Big data Engineering , DEVOPS, Data Analytics and deep ATS Functionality ,your task is to evaluate the resume against the provided job description. give me the percentage match if the resume matches the job description. First the output should come as percentage and then keywords missing.
"""

input_prompt4 = """
You are an expert Applicant Tracking System (ATS) analyst with deep knowledge of how modern ATS software (such as Greenhouse, Lever, Workday, Taleo, iCIMS) parses, ranks, and scores resumes.
You are provided with:
1. Job Description (JD) — detailing required skills, qualifications, experience, and keywords.
2. Candidate Resume — in plain text.

Your task is to:

Evaluate ATS Match Score: Give a score from 0–100 representing how well the resume aligns with the JD.

Keyword Match Analysis: Identify matched keywords/skills, missing keywords, and frequency of important terms from the JD in the resume.

Section-by-Section Relevance: Rate alignment for Skills, Work Experience, Education, and Certifications individually (0–10 scale).

ATS Parsing Friendliness: Assess formatting issues (tables, graphics, headers/footers) that might cause ATS parsing errors and deduct points if present.

Detailed Improvement Suggestions: Provide precise, actionable recommendations to increase the score — e.g., missing skills, more measurable achievements, better keyword usage.

Final Verdict: Summarize the candidate’s overall suitability for the role in 3–4 sentences.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1 , pdf_content , input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the resume!!")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2 , pdf_content , input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the resume!!")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3 , pdf_content , input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the resume!!")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4 , pdf_content , input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please Upload the resume!!")
