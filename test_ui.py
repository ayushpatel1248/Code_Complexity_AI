import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
from dotenv import load_dotenv
import re

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-2.5-pro')

class BigO(BaseModel):
    time_complexity: str = Field(description="Time complexity in Big O notation")
    space_complexity: str = Field(description="Time complexity in Big O notation")
    description: str = Field(description="Description of the code complexity in Hinglish")


st.set_page_config(page_title="CodeGuru AI", layout="centered")

st.markdown("""
    <h1 style='text-align:center; color:#00BFFF;'>CodeGuru AI - Code Complexity Analysis</h1>
    <p style='text-align:center; color:gray;'>Paste your code below aur dekho kitna optimized likha hai...</p>
""", unsafe_allow_html=True)

input_code = st.text_area("Code Paste Karo Yahan Pe:", height=300, placeholder="Yahan apna code paste kro...")

parser = PydanticOutputParser(pydantic_object=BigO)


template = PromptTemplate(
    template="""
    Find the time and space complexity of this code:
        {input_code}

    Output should be like this and should be in Hinglish: 

    Example output if code is optimized: 
    Wah yaar! Tumne to kaafi optimized code likha hai 👏
    Iski time complexity _ aur space complexity _ hai.
    Aise hi accha likhte raho!

    Example output if code is not optimized: 
    Arre bhai, code thoda aur sudharo 😅
    Iski time complexity _ aur space complexity _ hai.
    Thoda aur soch samajh ke likho, phir best ban jaayega!

    Example output if code is average: 
    Theek hai bhai, code average hai 🙂
    Iski time complexity O(_) aur space complexity O(_) hai.
    Thoda aur practice karo, aur better likh paoge!

    Example if no code is given instead something else in input:
    Bhai bina code ke main analysis kaise karu 😅
    Pehle thoda code likh ke bhej do phir batata hoon.
    {format_instruction}
    """,
    input_variables=["input_code"],
    partial_variables = {"format_instruction": parser.get_format_instructions()}
)

# prompt = template.invoke({"input_code": input_code})



if st.button("Analyze Code"):
    if input_code.strip() == "":
        st.warning("Arre bhai! Pehle code to daalo 😅")
    else:
        with st.spinner("Thoda ruk jao... Code samajh raha hoon 🤔"):
            chain = template | model | parser
            response = chain.invoke({"input_code": input_code})
            print(response)

        st.markdown("---")
        st.markdown("### Complexity Results:")
        col1, col2 = st.columns(2)
        col1.metric("Time Complexity", response.time_complexity)
        col2.metric("Space Complexity", response.space_complexity)
        st.text_area("Explanation:", value=response.description, height=200)
      
       
