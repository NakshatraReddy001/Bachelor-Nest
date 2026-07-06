import streamlit as st

def inject_global_css():
    """Injects high-fidelity structural layouts with explicit dark readability contrasts."""
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Root container background override */
        html, body, [data-testid="stAppViewContainer"] { 
            font-family: 'Inter', sans-serif; 
            background-color: #f8fafc !important; 
        }
        
        /* Force clear text visibility globally for standard paragraphs/headers */
        h1, h2, h3, h4, p, label, .stMarkdown p {
            color: #0f172a !important;
        }
        
        /* Premium Custom Nav Layout */
        .custom-navbar { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            background-color: #ffffff !important; 
            padding: 0.75rem 2.5rem; 
            border-bottom: 1px solid #e2e8f0; 
            margin-bottom: 2rem; 
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.05); 
        }
        .nav-logo { 
            font-size: 1.4rem; 
            font-weight: 700; 
            color: #e11d48 !important; 
            display: flex; 
            align-items: center; 
            gap: 0.5rem; 
        }
        .nav-logo span, .nav-logo b {
            color: #475569 !important;
        }
        
        /* Auth Screen Split Columns UI Fixes */
        [data-testid="stColumns"] > div:first-child { 
            background: linear-gradient(135deg, #e11d48 0%, #be123c 100%) !important; 
            padding: 4rem; 
            border-radius: 24px 0 0 24px; 
            display: flex; 
            flex-direction: column; 
            justify-content: center; 
        }
        /* Force white text inside the red hero block side only */
        [data-testid="stColumns"] > div:first-child h1,
        [data-testid="stColumns"] > div:first-child h3,
        [data-testid="stColumns"] > div:first-child p {
            color: #ffffff !important;
        }
        
        [data-testid="stColumns"] > div:last-child { 
            background: #ffffff !important; 
            padding: 4rem; 
            border-radius: 0 24px 24px 0; 
            border: 1px solid #e2e8f0; 
            border-left: none; 
        }
        
        /* Input elements label visibility */
        div[data-baseweb="input"] input {
            color: #0f172a !important;
        }
        
        /* Modular Marketplace Cards */
        .listing-card { 
            background: #ffffff !important; 
            border: 1px solid #e2e8f0; 
            border-radius: 16px; 
            overflow: hidden; 
            transition: transform 0.2s, box-shadow 0.2s; 
            margin-bottom: 1.5rem; 
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05); 
        }
        .listing-card:hover { 
            transform: translateY(-4px); 
            box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1); 
        }
        .card-img-container { 
            height: 200px; 
            width: 100%; 
            overflow: hidden; 
            position: relative; 
            background-color: #e2e8f0; 
        }
        .card-img-container img { 
            width: 100%; 
            height: 100%; 
            object-fit: cover; 
        }
        .badge-type { 
            position: absolute; 
            top: 12px; 
            left: 12px; 
            background: #f97316; 
            color: white !important; 
            padding: 0.25rem 0.75rem; 
            font-size: 0.75rem; 
            font-weight: 600; 
            border-radius: 6px; 
            text-transform: uppercase; 
        }
        .card-content { 
            padding: 1.25rem; 
        }
        .card-price { 
            font-size: 1.35rem; 
            font-weight: 700; 
            color: #0f172a !important; 
            margin-bottom: 0.25rem; 
        }
        .card-title { 
            font-size: 1.1rem; 
            font-weight: 600; 
            color: #1e293b !important; 
            margin-bottom: 0.5rem; 
            white-space: nowrap; 
            overflow: hidden; 
            text-overflow: ellipsis; 
        }
        .card-loc { 
            font-size: 0.875rem; 
            color: #64748b !important; 
            margin-bottom: 0.75rem; 
            display: flex; 
            align-items: center; 
            gap: 0.25rem; 
        }
        .card-specs { 
            display: flex; 
            gap: 1rem; 
            font-size: 0.85rem; 
            color: #475569 !important; 
            border-top: 1px solid #f1f5f9; 
            padding-top: 0.75rem; 
            margin-bottom: 0.75rem; 
        }
        
        .form-section-header { 
            background-color: #f8fafc; 
            border-left: 4px solid #e11d48; 
            padding: 0.5rem 1rem; 
            margin: 1.5rem 0 1rem 0; 
            font-weight: 600; 
            color: #0f172a !important;
        }
        .divider-text { 
            text-align: center; 
            margin: 1.5rem 0; 
            font-size: 0.75rem; 
            color: #94a3b8 !important; 
            letter-spacing: 1px; 
        }
    </style>
    """, unsafe_allow_html=True)