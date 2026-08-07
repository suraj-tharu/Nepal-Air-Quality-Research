import re
import os
import glob
import markdown
from docx import Document
from docx.shared import Inches
from htmldocx import HtmlToDocx

def main():
    chapters_dir = os.path.join("manuscript", "chapters")
    md_files = sorted(glob.glob(os.path.join(chapters_dir, "*.md")))
    
    if not md_files:
        print("No markdown chapters found.")
        return
        
    full_md_text = ""
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            full_md_text += f.read() + "\n\n"
            
    # Append the References
    ref_file = os.path.join("manuscript", "References.md")
    if os.path.exists(ref_file):
        with open(ref_file, "r", encoding="utf-8") as f:
            full_md_text += f.read() + "\n\n"
            
    doc = Document()
    new_parser = HtmlToDocx()
    
    # Process the markdown block by block for html conversion
    # We will use simple html to docx for the entire text since we don't have hardcoded figures yet
    html = markdown.markdown(full_md_text, extensions=['tables'])
    new_parser.add_html_to_document(html, doc)
            
    doc.save("Nepal_Air_Quality_Final_Manuscript.docx")
    print(f"Successfully generated Nepal_Air_Quality_Final_Manuscript.docx from {len(md_files)} chapters.")

if __name__ == "__main__":
    main()
