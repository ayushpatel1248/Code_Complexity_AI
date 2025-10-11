import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize model
model = ChatGoogleGenerativeAI(model='gemini-2.5-pro')

# --- Streamlit UI ---
st.set_page_config(page_title="Bhosda AI", layout="centered")

st.markdown("""
    <h1 style='text-align:center; color:#00BFFF;'>🤖 Bhosda AI - Code Complexity Analysis</h1>
    <p style='text-align:center; color:gray;'>Paste your code niche aur dekh kitna optimized likha hai tu...</p>
""", unsafe_allow_html=True)

# Large text area for code input
input_code = st.text_area(" Beta Code Paste Kar Yaha Pe:", height=300, placeholder="Yaha apna code daal...")

# Define prompt template
template = PromptTemplate(
    template="""
    find the time and space complexity of this code:
        {input_code}

    output should be like this and should be in hinglish: 

    example output if code is optimized: 
    Va yr Gandu tu to code krte sikh gaya bohot optmixed likhe he tune to code
    iski, time complexity _ and space complexity _ hai.
    khush reh or jyada mt khush ho peheli bar to tune code krna sikha he.

    example output if code is not optimized: 
    va re gadhe ki gand papa ke paise barbad krne ke liye code likha he tune
    iski time complexity _ and space complexity _ hai.
    thora soch samjh ke code krna shuru kr de warna teri gand me hamesha ke liye dard ho jayega.
    thora optmized code likh ke bhej de fir se.

    example output if code is average: 
    va re gadhe ki gand tune to thora bahut code krna sikha he 
    iski time complexity O(_) and space complexity O(_) hai.
    thora ache se code krna sikh le nhi to suraj lassi gand ki gand chatle.

    example if no code is given instead something else in input then :
    bsdk me kya antaryami hu jo tera code ka analysis kr du bina code ke
    thora code likh ke bhej de fir se
    nhi to gand me bomb fod dunga
    """,
    input_variables=["input_code"]
)

# Create prompt
prompt = template.invoke({"input_code": input_code})

# Submit button
if st.button("Analyze Code"):
    if input_code.strip() == "":
        st.warning("Arre beta! Pehle code to daal 😒")
    else:
        with st.spinner("Rukhja Gandu... Samjhne To De 🤔"):
            response = model.invoke(prompt)

        # --- Output UI ---
        st.markdown("---")
        st.subheader("Model Explanation:")
        st.text_area("Explanation:", value=response.content, height=200)

        # Optional: extract TC & SC roughly if present
        import re
        tc_match = re.search(r"time complexity\s*([O\(].*?[)])", response.content)
        sc_match = re.search(r"space complexity\s*([O\(].*?[)])", response.content)

        tc = tc_match.group(1) if tc_match else "Not clearly mentioned"
        sc = sc_match.group(1) if sc_match else "Not clearly mentioned"

        st.markdown("### Complexity Results:")
        col1, col2 = st.columns(2)
        col1.metric("Time Complexity", tc)
        col2.metric("Space Complexity", sc)