# app.py
import streamlit as st
import note_generator # Import your refactored script
import io # Need io for BytesIO

# --- Page Configuration (Optional) ---
st.set_page_config(page_title="Handwritten Notes Generator", layout="wide")

st.title("Handwritten Notes PDF Generator")
st.write("Paste your formatted text or upload a .txt file to generate notes.")
st.caption("Use the markup defined in MARKUP_GUIDE.md")

# --- Input Selection ---
input_method = st.radio("Choose input method:", ("Paste Text", "Upload File"), horizontal=True, key="input_method")

markup_text = ""
input_source_name = None

if input_method == "Paste Text":
    markup_text = st.text_area("Paste your formatted markup here:", height=300, key="paste_area")
    if markup_text:
        input_source_name = "Pasted Text"
else:
    uploaded_file = st.file_uploader("Upload your .txt markup file:", type=["txt"], key="uploader")
    if uploaded_file is not None:
        try:
            markup_text = uploaded_file.getvalue().decode("utf-8")
            with st.expander("File Content Preview"):
                 st.text(markup_text)
            input_source_name = uploaded_file.name
        except Exception as e:
            st.error(f"Error reading file: {e}")
            markup_text = ""

# --- Generation Button ---
if st.button("Generate Notes PDF", key="generate_button", disabled=(not markup_text)):
    if markup_text and input_source_name:
        st.write("---")
        with st.spinner("Parsing markup and generating PDF... Please wait."):
            try:
                # 1. Parse the markup
                parsed_elements = note_generator.parse_markup(markup_text)

                if not parsed_elements:
                    st.warning("Parsing resulted in no content elements. Cannot generate PDF.")
                else:
                    # 2. Generate PDF bytes IN MEMORY
                    pdf_bytes = note_generator.generate_pdf_bytes(parsed_elements)

                    if not pdf_bytes:
                         st.error("PDF generation failed or produced empty output.")
                    else:
                        # 3. Provide Download Button using the bytes directly
                        st.success(f"🎉 PDF generated successfully from '{input_source_name}'!")

                        st.download_button(
                            label="Download Generated PDF",
                            data=pdf_bytes, # Use the bytes directly
                            file_name="generated_notes.pdf", # Suggested download name
                            mime="application/pdf",
                            key="download_btn"
                        )

            except Exception as e:
                st.error(f"An error occurred during PDF generation:")
                st.exception(e) # Shows detailed traceback in the app

    else:
        st.warning("Please provide markup text via paste or upload.")

# --- Optional: Link to Markup Guide ---
st.write("---")
# Assuming MARKUP_GUIDE.md is in the same folder and Streamlit can serve it
try:
    with open("MARKUP_GUIDE.md", "r", encoding="utf-8") as guide:
        # Use columns to limit width of displayed guide
        col1, col2 = st.columns([3, 1]) # Make guide column wider
        with col1:
             st.markdown("### Markup Guide Preview")
             st.markdown(guide.read(), unsafe_allow_html=True) # Allows basic HTML/MD rendering
except FileNotFoundError:
    st.markdown("Markup guide file (`MARKUP_GUIDE.md`) not found in script directory.")
except Exception as e:
     st.warning(f"Could not display markup guide: {e}")