import os
import sys
import json
import urllib.request
import urllib.error
from pypdf import PdfReader
import streamlit as st

# =========================================================================
# SECURE BACKEND KEY FALLBACKS & SECRETS MANAGEMENT
# =========================================================================
GEMINI_API_KEY = ""  # Paste your key here or leave empty to use Streamlit Secrets
NVIDIA_NIM_KEY = ""
CUSTOM_API_KEY = ""

if 'streamlit' in sys.modules:
    try:
        if hasattr(st, 'secrets'):
            if 'GEMINI_API_KEY' in st.secrets:
                GEMINI_API_KEY = st.secrets['GEMINI_API_KEY']
    except Exception:
        pass

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", GEMINI_API_KEY)

# =========================================================================
# STREAMLIT PAGE CONFIGURATION
# =========================================================================
st.set_page_config(
    page_title="SAHAY - Government Scheme Finder",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================================
# UI LOCALIZATION DICTIONARY
# =========================================================================
LANG_DICT = {
    "English": {
        "title": "🏛️ SAHAY — Government Scheme Finder",
        "subtitle": "AI-Powered · Native Multi-Language Mapping Ready",
        "filter_title": "🔍 Filter Profile Criteria",
        "cat_label": "Scheme Category",
        "state_label": "Your State / Union Territory",
        "income_label": "Annual Family Income (in Lakhs)",
        "age_label": "Age Group Profile",
        "btn_find": "Find My Schemes",
        "metrics": ["Database Schemes", "Languages Supported", "States Active", "Access Cost", "Free"],
        "tabs": ["💬 AI Chat Assistant & Document Analyzer", "📋 Available Schemes", "📝 How to Apply"],
        "quick_prompts_title": "**Quick Prompts:**",
        "prompts": [
            "Best health schemes in Telangana?",
            "Farmer schemes for low income?",
            "Education scholarships details?",
            "Schemes available for families?"
        ],
        "input_placeholder": "Ask about any scheme or upload a PDF document above to ask questions...",
        "benefit_label": "Benefit",
        "eligibility_label": "Eligibility Criteria",
        "btn_view_steps": "View Application Steps",
        "steps_title": "🛠️ Step-by-Step Instructions:",
        "docs_title": "📂 Required Standard Baseline Documentation Checklist:",
        "doc_items": ["Aadhaar Card Seeding", "Income Certificate", "Domicile Certificate", "Bank Account Passbook"],
        "footer_note": "🔗 Note: Please visit official departmental portals directly. Never pay agent fees."
    },
    "हिंदी": {
        "title": "🏛️ सहायक (SAHAY) — सरकारी योजना खोजक",
        "subtitle": "एआई-संचालित · मूल बहु-भाषा प्रणाली",
        "filter_title": "🔍 अपनी प्रोफ़ाइल फ़िल्टर करें",
        "cat_label": "योजना की श्रेणी",
        "state_label": "आपका राज्य / केंद्र शासित प्रदेश",
        "income_label": "वार्षिक पारिवारिक आय (लाख में)",
        "age_label": "आयु समूह प्रोफ़ाइल",
        "btn_find": "मेरी योजनाएं खोजें",
        "metrics": ["डेटाबेस योजनाएं", "समर्थित भाषाएँ", "सक्रिय राज्य", "प्रवेश शुल्क", "मुफ़्त"],
        "tabs": ["💬 एआई चैट सहायक और दस्तावेज़ विश्लेषक", "📋 उपलब्ध योजनाएं", "📝 आवेदन कैसे करें"],
        "quick_prompts_title": "**त्वरित संकेत (Quick Prompts):**",
        "prompts": [
            "तेलंगाना में सबसे अच्छी स्वास्थ्य योजनाएं कौन सी हैं?",
            "कम आय वाले किसानों के लिए योजनाएं?",
            "शिक्षा छात्रवृत्ति का विवरण?",
            "परिवारों के लिए कौन सी योजनाएं उपलब्ध हैं?"
        ],
        "input_placeholder": "किसी भी योजना या अपने अपलोड किए गए दस्तावेज़ के बारे में पूछें...",
        "benefit_label": "लाभ",
        "eligibility_label": "पात्रता मापदंड",
        "btn_view_steps": "आवेदन के चरण देखें",
        "steps_title": "🛠️ चरण-दर-चरण निर्देश:",
        "docs_title": "📂 आवश्यक मानक दस्तावेज़ चेकलिस्ट:",
        "doc_items": ["आधार कार्ड लिंकिंग", "आय प्रमाण पत्र", "मूल निवास प्रमाण पत्र", "बैंक खाता पासबुक"],
        "footer_note": "🔗 नोट: कृपया सीधे आधिकारिक विभागीय पोर्टल पर जाएं। एजेंट शुल्क कभी न दें।"
    },
    "తెలుగు": {
        "title": "🏛️ సహాయ్ (SAHAY) — ప్రభుత్వ పథకాల గైడ్",
        "subtitle": "AI-ఆధారితం · మల్టీ-లాంగ్వేజ్ సపోర్ట్",
        "filter_title": "🔍 మీ ప్రొఫైల్ ఎంపికలు",
        "cat_label": "పథకం వర్గం (Category)",
        "state_label": "మీ రాష్ట్రం",
        "income_label": "సంవత్సర కుటుంబ ఆదాయం (లక్షలలో)",
        "age_label": "వయస్సు సమూహం",
        "btn_find": "నా పథకాలను కనుగొను",
        "metrics": ["మొత్తం పథకాలు", "అందుబాటులో ఉన్న భాషలు", "కవర్ చేయబడిన రాష్ట్రాలు", "ధర", "ఉచితం"],
        "tabs": ["💬 AI చాట్ అసిస్టెంట్ & డాక్యుమెంట్ ఎనలైజర్", "📋 అందుబాటులో ఉన్న పథకాలు", "📝 ఎలా దరఖాస్తు చేయాలి"],
        "quick_prompts_title": "**త్వరిత ప్రశ్నలు:**",
        "prompts": [
            "తెలంగాణలో ఉత్తమ ఆరోగ్య పథకాలు ఏవి?",
            "తక్కువ ఆదాయం ఉన్న రైతులకు పథకాలు?",
            "విద్యా స్కాలర్‌షిప్‌ల వివరాలు?",
            "కుటుంబాల కోసం అందుబాటులో ఉన్న పథకాలు ఏవి?"
        ],
        "input_placeholder": "పథకాల గురించి లేదా మీరు అప్‌లోడ్ చేసిన డాక్యుమెంట్ గురించి అడగండి...",
        "benefit_label": "లభించే ప్రయోజనం",
        "eligibility_label": "అర్హత ప్రమాణాలు",
        "btn_view_steps": "దరఖాస్తు విధానం చూడండి",
        "steps_title": "🛠️ దశల వారీ సూచనలు:",
        "docs_title": "📂 అవసరమైన డాక్యుమెంట్ల చెక్‌లిస్ట్:",
        "doc_items": ["ఆధార్ కార్డ్ సీడింగ్", "ఆదాయ ధృవీకరణ పత్రం (Income Certificate)", "స్థానికత ధృవీకరణ పత్రం", "బ్యాంక్ ఖాతా పాస్‌బుక్"],
        "footer_note": "🔗 గమనిక: దయచేసి అధికారిక ప్రభుత్వ పోర్టల్‌లను మాత్రమే సందర్శించండి. దళారులను నమ్మి డబ్బులు ఇవ్వకండి."
    }
}

# =========================================================================
# KNOWLEDGE BASE / SCHEMES REPOSITORY (RAG DATA SOURCE)
# =========================================================================
SCHEMES_DB = [
    {
        "id": "pm_ayushman",
        "name": "Ayushman Bharat (PM-JAY)",
        "category": "🏥 Health",
        "ministry": "Ministry of Health and Family Welfare",
        "state": "all",
        "max_income": 5.0,
        "age_group": "any",
        "benefit": "Free Health Cover up to ₹5 Lakhs / year",
        "eligibility": "Families identified in Socio-Economic Caste Census (SECC), low-income households.",
        "tags": ["Cashless", "Hospitalization", "Family"],
        "steps": [
            "Check eligibility on the official PM-JAY portal using your mobile number or Ration Card.",
            "Visit any empaneled government or private hospital.",
            "Contact the 'Ayushman Mitra' at the hospital helpdesk to verify identity.",
            "Produce an Aadhaar card or Ration card to receive a cashless golden health card."
        ]
    },
    {
        "id": "pm_kisan",
        "name": "PM-KISAN Samman Nidhi",
        "category": "🌾 Agriculture",
        "ministry": "Ministry of Agriculture and Farmers Welfare",
        "state": "all",
        "max_income": 3.0,
        "age_group": "any",
        "benefit": "₹6,000 yearly income support in 3 installments",
        "eligibility": "Small and marginal farmer families with cultivable landholding in their name.",
        "tags": ["Direct Benefit Transfer", "Income Support", "Farmers"],
        "steps": [
            "Go to the PM-KISAN online portal and navigate to 'New Farmer Registration'.",
            "Enter your Aadhaar Number and State details.",
            "Fill in land cultivation ownership records and bank account instructions.",
            "Submit the registration for validation by local revenue officials."
        ]
    },
    {
        "id": "rythu_bandhu",
        "name": "Rythu Bharosa / Rythu Bandhu",
        "category": "🌾 Agriculture",
        "ministry": "State Department of Agriculture",
        "state": "telangana",
        "max_income": 10.0,
        "age_group": "any",
        "benefit": "₹10,000 per acre per year for investment support",
        "eligibility": "Farmers owning agricultural land in Telangana status records.",
        "tags": ["State Scheme", "Telangana", "Crop Investment"],
        "steps": [
            "Ensure land details are registered in the Dharani Portal.",
            "Submit bank account seeding request to the local Agriculture Extension Officer (AEO).",
            "Funds are credited before the Kharif and Rabi seasons directly to validated bank links."
        ]
    }
]

# =========================================================================
# HELPER RESPONSIVE TEXT GENERATION WITH ADVANCED PDF INJECTION LOGIC
# =========================================================================
def call_gemini_api(prompt_text, context_data, pdf_text_data, out_lang):
    if not GEMINI_API_KEY:
        return "⚠️ *Please configure your real Gemini API Key inside line 12 or Streamlit Secrets.*"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    system_instruction = (
        f"You are SAHAY, an expert government scheme assistant. Answer the user query using the "
        f"provided matching context schemes data accurately. If custom document raw text content is supplied, "
        f"use it to extract data, cross-reference rules, or analyze user credentials or income guidelines. "
        f"You MUST respond completely in the following language code text script dynamically: {out_lang}. "
        f"Keep details structured and clear."
    )
    
    full_prompt = f"Context Database Schemes:\n{json.dumps(context_data)}\n\n"
    if pdf_text_data:
        full_prompt += f"--- UPLOADED USER DOCUMENT TEXT ---\n{pdf_text_data}\n-----------------------------------\n\n"
    full_prompt += f"User Question: {prompt_text}"
    
    body = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }
    
    try:
        req = urllib.request.Request(url, data=json.dumps(body).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return res_data['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"❌ *Error communicating with Gemini API:* {str(e)}"

# =========================================================================
# INITIALIZING SESSION STATE
# =========================================================================
if "matched_schemes" not in st.session_state:
    st.session_state.matched_schemes = SCHEMES_DB
if "selected_scheme" not in st.session_state:
    st.session_state.selected_scheme = SCHEMES_DB[0]
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================================================================
# FRONTEND INTERFACE - SIDEBAR CONFIGURATION & LANGUAGE SWITCHER
# =========================================================================
st.sidebar.markdown("### 🌐 Choose Language / भाषा चुनें / భాషను ఎంచుకోండి")
selected_lang = st.sidebar.selectbox(
    "Application Language",
    ["English", "हिंदी", "తెలుగు"],
    label_visibility="collapsed"
)

T = LANG_DICT[selected_lang]

st.sidebar.markdown(f"### {T['filter_title']}")
selected_cat = st.sidebar.selectbox(T["cat_label"], ["All Categories", "🏥 Health", "🌾 Agriculture"])
selected_state = st.sidebar.selectbox(T["state_label"], ["All India (Central)", "Telangana"])
annual_income = st.sidebar.slider(T["income_label"], min_value=0.5, max_value=20.0, value=2.5, step=0.5, format="₹%.1f L")
selected_age = st.sidebar.selectbox(T["age_label"], ["Any Age", "Youth (18-35)"])

if st.sidebar.button(T["btn_find"], use_container_width=True):
    filtered = []
    for s in SCHEMES_DB:
        if annual_income > s["max_income"]: continue
        if s["state"] != "all" and selected_state.lower() != s["state"].lower(): continue
        if selected_cat != "All Categories" and s["category"] != selected_cat: continue
        filtered.append(s)
    st.session_state.matched_schemes = filtered

# =========================================================================
# MAIN APP VIEW LAYOUT USING LOCALIZED TOKENS
# =========================================================================
st.title(T["title"])
st.caption(T["subtitle"])

col1, col2, col3, col4 = st.columns(4)
col1.metric(T["metrics"][0], "1,000+", "+12")
col2.metric(T["metrics"][1], "3 Active", f"Using {selected_lang}")
col3.metric(T["metrics"][2], "28+", "Pan-India")
col4.metric(T["metrics"][3], T["metrics"][4], "Public Utility")

st.markdown("---")

tab_chat, tab_schemes, tab_apply = st.tabs(T["tabs"])

# -------------------------------------------------------------------------
# TAB 1: AI CHAT ASSISTANT WITH PDF READER INJECTION
# -------------------------------------------------------------------------
with tab_chat:
    st.markdown(f"#### {T['tabs'][0]}")
    
    # ➕ THE NATIVE PDF ATTACHMENT BOX
    with st.expander("📁 Attach Reference Documents / PDF Rules / Certificates", expanded=True):
        uploaded_pdf = st.file_uploader("Upload an income certificate or scheme guidelines PDF", type=["pdf"])
        
        pdf_extracted_text = ""
        if uploaded_pdf is not None:
            try:
                # Read text using pypdf reader
                pdf_reader = PdfReader(uploaded_pdf)
                pages_text = []
                for page in pdf_reader.pages:
                    text_content = page.extract_text()
                    if text_content:
                        pages_text.append(text_content)
                
                pdf_extracted_text = "\n".join(pages_text)
                st.success(f"📎 Successfully processed '{uploaded_pdf.name}' ({len(pdf_extracted_text)} characters extracted and added to context!)")
            except Exception as e:
                st.error(f"Failed to read PDF file content: {e}")

    st.markdown(T["quick_prompts_title"])
    col_a, col_b, col_c, col_d = st.columns(4)
    p1 = col_a.button(T["prompts"][0], use_container_width=True)
    p2 = col_b.button(T["prompts"][1], use_container_width=True)
    p3 = col_c.button(T["prompts"][2], use_container_width=True)
    p4 = col_d.button(T["prompts"][3], use_container_width=True)
    
    captured_prompt = ""
    if p1: captured_prompt = T["prompts"][0]
    if p2: captured_prompt = T["prompts"][1]
    if p3: captured_prompt = T["prompts"][2]
    if p4: captured_prompt = T["prompts"][3]

    # Render running list of past conversation logs
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    user_input = st.chat_input(T["input_placeholder"])
    final_query = user_input if user_input else captured_prompt

    if final_query:
        st.session_state.messages.append({"role": "user", "content": final_query})
        with st.chat_message("user"):
            st.markdown(final_query)
            
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                # Pass query, schema db, and any parsed text extracted from your PDF
                ai_response = call_gemini_api(
                    final_query, 
                    st.session_state.matched_schemes, 
                    pdf_extracted_text, 
                    selected_lang
                )
                st.markdown(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})

# -------------------------------------------------------------------------
# TAB 2: AVAILABLE SCHEMES VIEW
# -------------------------------------------------------------------------
with tab_schemes:
    st.markdown(f"#### {T['tabs'][1]}")
    for scheme in st.session_state.matched_schemes:
        with st.container():
            st.markdown(f"### {scheme['name']}")
            st.caption(f"🏛️ {scheme['ministry']} | **Category:** {scheme['category']}")
            
            c_a, c_b = st.columns([2, 1])
            with c_a:
                st.markdown(f"💵 **{T['benefit_label']}:** `{scheme['benefit']}`")
                st.markdown(f"📋 **{T['eligibility_label']}:** {scheme['eligibility']}")
            with c_b:
                if st.button(T["btn_view_steps"], key=f"btn_{scheme['id']}", use_container_width=True):
                    st.session_state.selected_scheme = scheme
                    st.success("Selected! Go to How to Apply Tab.")
            st.markdown("---")

# -------------------------------------------------------------------------
# TAB 3: HOW TO APPLY STEPS DETAILED SUBMISSION
# -------------------------------------------------------------------------
with tab_apply:
    target_scheme = st.session_state.selected_scheme
    st.markdown(f"### {target_scheme['name']}")
    
    st.markdown(f"#### {T['steps_title']}")
    for idx, step in enumerate(target_scheme["steps"], start=1):
        st.markdown(f"**{idx}.** {step}")
        
    st.markdown("---")
    st.markdown(f"#### {T['docs_title']}")
    for item in T["doc_items"]:
        st.checkbox(item, value=True, key=f"chk_{item}")
    
    st.markdown("---")
    st.info(T["footer_note"])
