# Handwritten Notes PDF Generator

A Python application using Streamlit and ReportLab to convert specially formatted text markup into aesthetically pleasing, two-column, handwritten-style PDF notes.

*(This project was developed using Python, with AI assistance utilized during coding and brainstorming phases, akin to consulting documentation or search engines.)*
This project is available on huggingface as a web app:
<a>https://huggingface.co/spaces/CursiveCurse/Markup-To-Handwritten-PDF</a>
## Motivation

Taking detailed notes by hand on a physical notebook can be very time-consuming, although the results are often visually engaging and easy to read. On the other hand, using AI language models (like ChatGPT) to summarize concepts or generate explanations often produces plain, unformatted text that lacks visual appeal and can be hard to scan quickly.

This project bridges that gap. It provides a way to take text output (potentially from an AI, or manually written) formatted with simple tags, and automatically generates PDF notes that mimic a clean, handwritten aesthetic, similar to well-organized notebook pages. The choice of PDF ensures perfect clarity and scalability when zooming, overcoming the pixelation issues inherent in image-based notes.

## Features

*   **Markup Parsing:** Parses plain text input formatted with custom tags (`[MAIN_TITLE]`, `[SUB_TITLE]`, `[POINT:symbol]`, `[BOX]`, etc.).
*   **PDF Generation:** Creates multi-page PDF documents using the ReportLab library.
*   **Handwritten Styling:** Uses custom TrueType/OpenType fonts (`main.ttf`, `sub.ttf`) for titles and body text.
*   **Two-Column Layout:** Automatically arranges content into two columns per page.
*   **Automatic Flow Control:** Handles column and page breaks automatically based on content height. Manual breaks (`[COLUMN_BREAK]`, `[PAGE_BREAK]`) are also supported.
*   **Styling:**
    *   Distinct fonts and sizes for main titles, subtitles, and body text.
    *   Transparent background highlighting for subtitles.
    *   Bordered boxes for highlighted notes.
    *   Inline text coloring using `<font>` tags.
*   **Web GUI:** A simple web interface built with Streamlit allows:
    *   Pasting markup text directly.
    *   Uploading a `.txt` file containing markup.
    *   Generating the PDF with a button click.
    *   Downloading the generated PDF.
    *   Previewing the Markup Guide.

## Screenshot / Example Output (Placeholder)

*(Consider adding a screenshot of the generated PDF style here)*
<!-- ![Example PDF Output](path/to/example_output.png) -->

*(Consider adding a screenshot of the Streamlit GUI here)*
<!-- ![Streamlit GUI](path/to/gui_screenshot.png) -->

## Setup

1.  **Prerequisites:**
    *   Python 3.8 or later installed.
    *   `pip` (Python package installer).

2.  **Clone Repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

3.  **Create Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # Activate (Windows)
    .\venv\Scripts\activate
    # Activate (macOS/Linux)
    source venv/bin/activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Add Fonts:**
    *   Place your chosen TrueType (`.ttf`) or OpenType (`.otf`) font files in the main project directory.
    *   Rename them to `main.ttf` (for the main title font) and `sub.ttf` (for subtitles and body text). *You can change these filenames in `note_generator.py` if needed.*

## Running the Application

1.  Make sure your virtual environment is activated.
2.  Navigate to the project directory in your terminal.
3.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
4.  Streamlit will provide a local URL (usually `http://localhost:8501`) - open this in your web browser.

## Usage

1.  **Prepare Markup:** Create your notes content in a plain text editor, using the tags defined in `MARKUP_GUIDE.txt` (or `MARKUP_GUIDE.md`). You can use inline `<font color='...'>...</font>` tags for specific word coloring.
2.  **Input via GUI:**
    *   **Paste Text:** Select the "Paste Text" option and paste your markup into the text area.
    *   **Upload File:** Select the "Upload File" option and browse to select your `.txt` file containing the markup.
3.  **Generate:** Click the "Generate Notes PDF" button.
4.  **Download:** Once generation is complete, a "Download Generated PDF" button will appear. Click it to save the PDF file to your computer.

## Development Journey & Challenges

The development involved several iterations:

*   **Initial Concept:** Generate PDF with basic text and layout.
*   **Styling:** Integrating custom fonts and defining specific styles (highlights, colors, sizes) using ReportLab.
*   **Layout Engine:** Implementing the two-column structure and, critically, the automatic overflow detection (`check_and_handle_overflow`) to manage column and page breaks dynamically based on estimated element height. This ensures the user doesn't need to predict breaks.
*   **Markup Parser:** Creating the `parse_markup` function to translate the user-friendly tags into a structured format the generation engine understands.
*   **Highlighting Issues:** Iteratively refining the highlight placement for main titles (initially margin-based, then text-relative) and subtitles (ensuring highlight width matched text width using `stringWidth` instead of relying solely on `Paragraph.wrapOn`).
*   **File Handling:** Encountering `PermissionError` on Windows when using `tempfile` with ReportLab's file saving. The workaround was to switch to generating the PDF into an in-memory `io.BytesIO` buffer and passing the bytes directly to Streamlit for download, avoiding intermediate disk writes during the request.
*   **Simplification:** Features like embedded images and reliable cross-font emoji support were initially considered but later removed to focus on the core text-to-PDF functionality, as they added significant complexity (requiring Pillow, font checks, potentially SVG handling).
*   **GUI:** Adding a Streamlit interface (`app.py`) to provide a user-friendly way to input markup and receive the PDF, separating the UI from the core generation logic (`note_generator.py`).

## Future Ideas

*   More robust height estimation for `check_and_handle_overflow`.
*   Support for basic image embedding (`[IMAGE:path]`).
*   Support for simple tables.
*   More advanced list formatting (nested lists, different bullet styles via markup).
*   User-selectable color themes or fonts via the GUI.
*   Improved error handling in the parser for invalid markup.
*   Direct PDF preview within the Streamlit app (technically challenging).
## License

MIT License

Copyright (c) 2025 Mayank Saini

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
