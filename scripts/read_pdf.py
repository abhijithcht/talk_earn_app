import fitz
doc = fitz.open('assets/Talk_and_Earn_Platform_Concept.pdf')
text = ''
for page in doc:
    text += page.get_text()

with open('pdf_content.txt', 'w', encoding='utf-8') as f:
    f.write(text)
print("Extracted PDF to pdf_content.txt")
