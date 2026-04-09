import streamlit as st
import re

# ================= CONFIG =================
st.set_page_config(
    page_title="Text Cleaner PRO",
    layout="centered",
    page_icon="✨"
)

# ================= STYLE =================
st.markdown("""
<style>
button {
    border-radius: 10px !important;
    height: 45px;
    font-size: 16px !important;
}
textarea {
    border-radius: 10px !important;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# ================= TEXT CLEAN =================
def normalize_text(s: str) -> str:
    if not s:
        return ""

    s = s.replace('“', '').replace('”', '').replace('"', '')
    s = s.replace('-', '.').replace('–', '.').replace('—', '.')
    s = s.replace('…', '.')
    s = re.sub(r'\.{2,}', '.', s)
    
    s = re.sub(r'(\d+)\s*%', r'\1 phần trăm', s)
    s = re.sub(r'(\d+)\s*$', r'\1 đô la', s)
    s = re.sub(r"[^0-9A-Za-zÀ-ỹ.,;:?!()$%\s]", " ", s)
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s+([.,;:?!])', r'\1', s)

    def capitalize_sentences(text):
        text = text.strip()
        parts = re.split('([.?!]\s*)', text)
        fixed = []
        for i, seg in enumerate(parts):
            if i % 2 == 0:
                if seg:
                    fixed.append(seg.strip().capitalize())
            else:
                fixed.append(seg)
        return ''.join(fixed).strip()

    return capitalize_sentences(s)

# ================= SESSION =================
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

if "result" not in st.session_state:
    st.session_state.result = ""

# ================= HEADER =================
st.title("✨ Text Cleaner PRO")
st.caption("Chuẩn hóa văn bản nhanh – gọn – đẹp")

# ================= INPUT =================
st.markdown("### 📝 Nhập văn bản")

st.text_area(
    "",
    height=180,
    key="text_input",
    placeholder="Dán nội dung vào đây..."
)

# ================= BUTTONS =================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 Xử lý"):
        st.session_state.result = normalize_text(st.session_state.text_input)

with col2:
    def clear_text():
        st.session_state.text_input = ""
        st.session_state.result = ""

st.button("🗑️ Xóa", on_click=clear_text)

with col3:
    paste = st.text_input("📥 Dán nhanh")
    if paste:
        st.session_state.text_input = paste

# ================= OUTPUT =================
if st.session_state.result:
    st.markdown("### ✅ Kết quả")

    st.text_area(
        "",
        st.session_state.result,
        height=180
    )

    # 🔥 COPY 1 CLICK
    st.code(st.session_state.result, language="text")

    # DOWNLOAD
    st.download_button(
        "📥 Tải file .txt",
        data=st.session_state.result,
        file_name="ket_qua.txt"
    )
