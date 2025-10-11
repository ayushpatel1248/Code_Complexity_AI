import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Initialize model
model = ChatGoogleGenerativeAI(model='gemini-2.5-pro')

# --- Streamlit UI ---
st.set_page_config(page_title="CodeGuru AI", layout="centered")

st.markdown("""
    <h1 style='text-align:center; color:#00BFFF;'>CodeGuru AI - Code Complexity Analysis</h1>
    <p style='text-align:center; color:gray;'>Paste your code below aur dekho kitna optimized likha hai...</p>
""", unsafe_allow_html=True)

# Large text area for code input
input_code = st.text_area("Code Paste Karo Yahan Pe:", height=300, placeholder="Yahan apna code paste kro...")

# Define prompt template
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
    """,
    input_variables=["input_code"]
)

# Create prompt
prompt = template.invoke({"input_code": input_code})

# Submit button
if st.button("Analyze Code"):
    if input_code.strip() == "":
        st.warning("Arre bhai! Pehle code to daalo 😅")
    else:
        with st.spinner("Thoda ruk jao... Code samajh raha hoon 🤔"):
            response = model.invoke(prompt)

        # --- Output UI ---
        st.markdown("---")
        st.text_area("Explanation:", value=response.content, height=200)

        # Optional: extract TC & SC roughly if present
        tc_match = re.search(
            r"(?:time\s*complexity\s*[:=]?\s*|TC\s*[:=]?\s*)(O\s*\(.*?\))",
            response.content,
            flags=re.IGNORECASE
        )
        sc_match = re.search(
            r"(?:space\s*complexity\s*[:=]?\s*|SC\s*[:=]?\s*)(O\s*\(.*?\))",
            response.content,
            flags=re.IGNORECASE
        )

        tc = tc_match.group(1) if tc_match else "Not clearly mentioned"
        sc = sc_match.group(1) if sc_match else "Not clearly mentioned"

        st.markdown("### Complexity Results:")
        col1, col2 = st.columns(2)
        col1.metric("Time Complexity", tc)
        col2.metric("Space Complexity", sc)
