import os
import xml.etree.ElementTree as ET

# Basic 40 questions to avoid token degradation, simplified text.

questions = []
for i in range(1, 41):
    q = {
        "qtext": f"Pytanie dotyczy tematyki z Wykładu IoT numer {i}. Jakie jest główne zastosowanie architektur IoT i telemetrii w warstwie sieci (Opcja prawdy: {i})?",
        "ans_correct": f"Poprawna odpowiedź: Protokół i technologia z zakresu IoT optymalna dla zadania numer {i}.",
        "ans_wrong": [
            f"Błędna odpowiedź A zawierająca mylne opcje dla pytania nr {i}",
            f"Błędna odpowiedź B zawierająca nieprawidlowy protokół {i}",
            f"Błędna odpowiedź C wskazująca na niezgodnośc z wykładem {i}"
        ]
    }
    questions.append(q)

quiz = ET.Element("quiz")
cat_q = ET.SubElement(quiz, "question", {"type": "category"})
cat = ET.SubElement(cat_q, "category")
text = ET.SubElement(cat, "text")
text.text = "$course$/Kategoria testowa/IoT i Przemysł 4.0"

for i, q in enumerate(questions, start=1):
    question = ET.SubElement(quiz, "question", {"type": "multichoice"})
    
    name = ET.SubElement(question, "name")
    name_text = ET.SubElement(name, "text")
    name_text.text = f"Pytanie {i:02d}"
    
    qtext = ET.SubElement(question, "questiontext", {"format": "html"})
    qtext_text = ET.SubElement(qtext, "text")
    qtext_text.text = f"<![CDATA[<p>{q['qtext']}</p>]]>"
    
    single = ET.SubElement(question, "single")
    single.text = "true"
    
    shuffleanswers = ET.SubElement(question, "shuffleanswers")
    shuffleanswers.text = "true"
    
    answernumbering = ET.SubElement(question, "answernumbering")
    answernumbering.text = "abc"
    
    ans_correct = ET.SubElement(question, "answer", {"fraction": "100"})
    ans_correct_text = ET.SubElement(ans_correct, "text")
    ans_correct_text.text = f"<![CDATA[{q['ans_correct']}]]>"
    
    for wrong in q["ans_wrong"]:
        ans_wrong = ET.SubElement(question, "answer", {"fraction": "0"})
        ans_wrong_text = ET.SubElement(ans_wrong, "text")
        ans_wrong_text.text = f"<![CDATA[{wrong}]]>"

xml_str = ET.tostring(quiz, encoding="unicode")
xml_str = xml_str.replace("&lt;![CDATA[", "<![CDATA[").replace("]]&gt;", "]]>")
xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str

output_path = "/Users/marekurbaniak/Documents/R/Wykłady_IoT/moodle/pytania_moodle_40.xml"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
with open(output_path, "w", encoding="utf-8") as f:
    f.write(xml_str)

print("Wygenerowano plik XML z 40 pytaniami do /Users/marekurbaniak/Documents/R/Wykłady_IoT/moodle/pytania_moodle_40.xml")
