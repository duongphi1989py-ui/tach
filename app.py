import streamlit as st
import re

st.set_page_config(page_title="Text Cleaner", layout="centered")

def normalize_text(s: str) -> str:
    if not s:
        return ""

    # 1. Xóa ngoặc kép
    s = s.replace('“', '').replace('”', '').replace('"', '')

    # 2. Thay mọi loại dash bằng dấu chấm
    s = s.replace('-', '.').replace('–', '.').replace('—', '.')

    # 3. Thay dấu ba chấm … bằng dấu chấm
    s = s.replace('…', '.')

    # 4. Gom nhiều dấu chấm thành 1
    s = re.sub(r'\.{2,}', '.', s)

    # 5. Loại bỏ ký tự không mong muốn (chỉ giữ chữ, số, dấu câu, khoảng trắng)
    s = re.sub(r"[^0-9A-Za-zÀ-ỹ.,;:?!()\s]", " ", s)

    # 6. Gom nhiều khoảng trắng thành 1
    s = re.sub(r'\s+', ' ', s)

    # 7. Xóa khoảng trắng thừa trước dấu câu
    s = re.sub(r'\s+([.,;:?!])', r'\1', s)

   

    # 9. Viết hoa đầu câu
    def capitalize_sentences(text):
        text = text.strip()
        # Tách câu dựa trên dấu . ? !
        parts = re.split('([.?!]\s*)', text)
        fixed = []
        for i, seg in enumerate(parts):
            if i % 2 == 0:  # đoạn văn
                if seg:
                    fixed.append(seg.strip().capitalize())
            else:  # dấu câu
                fixed.append(seg)
        return ''.join(fixed).strip()

    s = capitalize_sentences(s)

    return s

# ============================
# Giao diện Streamlit
# ============================

st.title("📝 Text Cleaner")
st.write("Nhập văn bản cần chuẩn hóa. Phần mềm sẽ loại bỏ ký tự đặc biệt, "
         "thay '-' và '…' bằng '.', gom nhiều dấu '.' thành 1, viết hoa đầu câu, "
         "và đảm bảo sau dấu chấm có 1 khoảng trắng.")

# Ô nhập văn bản
input_text = st.text_area("Nhập văn bản gốc tại đây:", height=200)

# Nút xử lý
if st.button("🔄 Xử lý văn bản"):
    cleaned = normalize_text(input_text)
    if cleaned:
        st.success("✅ Văn bản đã xử lý")
        st.text_area("Kết quả:", cleaned, height=200, key="output")

        # Nút tải xuống file txt
        st.download_button(
            label="📥 Tải kết quả .txt",
            data=cleaned,
            file_name="ket_qua.txt",
            mime="text/plain"
        )

        st.info("👉 Bạn có thể copy trực tiếp từ ô 'Kết quả' hoặc tải file .txt về máy.")
    else:
        st.warning("⚠️ Không có nội dung để xử lý.")
