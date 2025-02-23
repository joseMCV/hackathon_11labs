import os
import platform
import ctypes.util
#import whisper
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from groq import Groq
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import re

# Windows-specific patch for libc
if platform.system() == "Windows":
    original_find_library = ctypes.util.find_library

    def patched_find_library(name):
        if name == "c":
            return "msvcrt.dll"  # Microsoft C Runtime equivalent
        return original_find_library(name)

    ctypes.util.find_library = patched_find_library

# API Setup
app = FastAPI()

# Ensure temp directories exist
os.makedirs("reports", exist_ok=True)

# Initialize Groq API (Replace with your key)
client = Groq(api_key="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")

# Example output format for extraction
ExampleOutputFormat = """
Important Information Extracted from Transcript:

Patient: Ms. Critchard
Doctor: Dr. Jones

Symptoms and History:
- Duration: Past 3 months
- Rectal bleeding (fresh blood)
- Loose stools (approximately 4 times per day)
- Sour taste in the mouth upon waking
- Epigastric pain and heartburn
- Weight loss
- Crampy pain in the lower left side
- Family history of inflammatory bowel disease (Crohn's/colitis on maternal side)

Examination Findings:
- Mild tenderness in the left lower abdomen (no guarding or rebound tenderness)
- Rigid sigmoidoscopy revealed inflamed and ulcerated mucosa up to about 15 cm with contact bleeding

Preliminary Diagnosis:
- Suspected proctitis, likely related to ulcerative colitis

Planned Next Steps:
- Schedule a flexible sigmoidoscopy for a more detailed examination
- Order blood tests: FBC, U&E, LFT, CRP
- Perform stool tests to rule out infections (e.g., C. difficile)

Treatment Plan:
- Start acycolic mesolazine at 800 mg, three times a day
- Note: Patient is allergic to penicillin (avoid penicillin-based antibiotics)

Follow-Up:
- Schedule a follow-up appointment in approximately two weeks to review test results and treatment response
- Dr. Jones will send a letter to the patient's GP (Dr. O'Reilly) detailing the treatment plan and prescriptions
- Patient advised to contact Dr. Jones or the IBD specialist nurse (Ms. Bryant) if new or worsening symptoms occur
"""

# Helper function: Transcribe audio using Whisper
def transcribe_audio(file_path: str) -> str:
    with open(file_path, "rb") as file:
        translation = client.audio.translations.create(
            file=(file_path, file),  # Pass the file object instead of file.read()
            model="whisper-large-v3",
            response_format="json",
            temperature=0.0
        )
    transcript = translation.text if hasattr(translation, "text") else translation["text"]
    return transcript

# Helper function: Extract important information with Groq
def extract_key_info(transcript: str) -> str:
    system_message = (
    """You are a highly detailed medical consultation letter assistant. Your task is to take a transcribed conversation and extract key information (including patient name, doctor's name, and duration) and provide a detailed summarization covering all of the following headings exactly as specified. The headings are:
    - Patient
    - Doctor
    - Symptoms and History
    - Examination Findings
    - Preliminary Diagnosis
    - Planned Next Steps
    - Treatment Plan
    - Follow-Up

    For each heading, if the transcript does not include the necessary information, you must output 'not specified'. Please output the information in the exact format shown below:
    """
        + ExampleOutputFormat
    )
    
    user_message = (f"Extract key information from the following transcribed conversation in detail, ensuring that every heading is included in the output (with 'not specified' where needed):\n\n{transcript}")

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0.5,
        max_tokens=600
    )
    
    response = completion.choices[0].message.content
    return response

# Helper function: Generate outpatient letter with Groq
def generate_outpatient_letter(transcript: str) -> str:
    system_message = """
    You are a helpful assistant that transforms transcripts into structured outpatient letters.
    Below is an updated example letter for reference. Notice the headings, structure, style, etc.

    When generating your final letter:
    1. Replicate the same headings, style, and structure as in the example below.
    2. Output only the final letter text (no extra commentary).
    3. The letter must include the following headings exactly (in this order), in bold HTML format:
    - <b>Patient demographics</b>:
    - <b>Attendance details</b>:
    - <b>Diagnosis</b>:
    - <b>History</b>:
    - <b>Family history</b>:
    - <b>Social context</b>:
    - <b>Allergies and adverse reactions</b>:
    - <b>Examination findings</b>:
    - <b>Investigation findings</b>:
    - <b>Procedure</b>:
    - <b>Clinical summary</b>:
    - <b>Actions for healthcare professionals</b>:
    - <b>Changes to medications and medical devices</b>:
    - <b>Medications and medical devices</b>:
    - <b>Signature</b>:
    4. If the transcript does not contain details for any field, fill it out with 'not specified'. 
    If the transcript contains no information for an entire heading, you must still output the heading
    and write 'not specified' under it.
    5. Do not add or remove headings. Use only relevant information from the transcript.
    6. End your response with the final letter text only.

    ==================================
    UPDATED EXAMPLE LETTER FORMAT
    ==================================

    Gastroenterology Department, St Crispin’s Hospital, Donaldstown, DO5 7TP
    Dr. Ruth Jones, Consultant Gastroenterologist
    (01234) 567890
    gj@stcrispins.nhs.uk

    Outpatient letter to General Practitioner

    <b>Patient demographics</b>:
    Patient name: Ms. Agatha Critchard
    Date of birth: 01/02/1964
    Gender: Female
    NHS number: 123456789
    Hospital ID: T189765
    Patient address: 30 Acacia Road, B99 6PL
    Patient email address: frances@delatour.net
    Patient telephone number: not specified

    <b>Attendance details</b>:
    Date of appointment: 01/05/2017
    Contact type: Face to face
    Consultation method: Face to face
    Seen by doctor: Dr. Ruth Jones, Consultant Gastroenterologist
    Care professionals present: Ms. N. Bryant, IBD specialist nurse
    Outcome of patient attendance: Routine appointment

    <b>Diagnosis</b>:
    1. Proctitis
    2. Dyspepsia

    <b>History</b>:
    The patient reports rectal bleeding and weight loss for the past 3 months.

    <b>Family history</b>:
    Several relatives on maternal side had Crohn’s or colitis.

    <b>Social context</b>:
    Patient is a smoker (10 cigarettes/day).

    <b>Allergies and adverse reactions</b>:
    Penicillin (patient experienced a generalized severe rash)

    <b>Examination findings</b>:
    The abdomen was found to be soft but mainly tender in the left iliac fossa.
    No guarding or rebound tenderness.

    <b>Investigation findings</b>:
    Faecal calprotectin levels were 247mcg/l (faeces normal).

    <b>Procedure</b>:
    Rigid sigmoidoscopy performed. Inflamed and ulcerated mucosa with contact bleeding up to 15cm.

    <b>Clinical summary</b>:
    Findings suggest ulcerative colitis (proctitis). 5ASA treatment commenced.

    <b>Actions for healthcare professionals</b>:
    Arrange flexible sigmoidoscopy and blood tests (FBC, U&E, LFT, CRP).

    <b>Changes to medications and medical devices</b>:
    No changes yet. Further review pending test results.

    <b>Medications and medical devices</b>:
    Medication name: Asacol
    Dose: 800 mg
    Form: Oral
    Frequency: 3 x a day
    Comment: 14-day course prescribed in clinic.

    <b>Signature</b>:
    Yours faithfully,
    Person completing record: Dr. Ruth Jones, Consultant Gastroenterologist
    Date: 01/05/17 16:42
    Distribution list: Ms. Agatha Critchard (patient)

    ==================================
    END OF EXAMPLE LETTER FORMAT
    ==================================
    """
    
    human_message = (
        "Here is the transcript from 'important_info.txt':\n\n"
        f"{transcript}\n\n"
        "Please generate the outpatient letter in text form, strictly following the example format. "
        "Use <b>HTML bold</b> for the headings and do not include parentheses after them. "
        "If the transcript has no information for a heading, still output the heading and 'not specified'. "
        "Output only the final letter text with the headings as stated. Then end your response."
    )
    
    client = Groq(api_key="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")

    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": human_message}
        ],
        temperature=0.5,
        max_tokens=2048
    )
    
    response = completion.choices[0].message.content
    return response

# Helper function: Create PDF report
def create_pdf(letter_text: str, output_path: str):
    doc = SimpleDocTemplate(output_path, pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50)
    styles = getSampleStyleSheet()

    heading_style = ParagraphStyle(
        name="HeadingStyle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.black,
        spaceBefore=12,
        spaceAfter=6
    )
    normal_style = styles["Normal"]

    # Define headings
    known_headings = [
        "<b>Patient demographics</b>:",
        "<b>Attendance details</b>:",
        "<b>Diagnosis</b>:",
        "<b>History</b>:",
        "<b>Family history</b>:",
        "<b>Social context</b>:",
        "<b>Allergies and adverse reactions</b>:",
        "<b>Examination findings</b>:",
        "<b>Investigation findings</b>:",
        "<b>Procedure</b>:",
        "<b>Clinical summary</b>:",
        "<b>Actions for healthcare professionals</b>:",
        "<b>Changes to medications and medical devices</b>:",
        "<b>Medications and medical devices</b>:",
        "<b>Signature</b>:"
    ]

    story = []
    lines = letter_text.split("\n")

    for line in lines:
        line_stripped = line.strip()
        if line_stripped in known_headings:
            heading_text = re.sub(r"</?b>", "", line_stripped)
            p = Paragraph(heading_text, heading_style)
        else:
            p = Paragraph(line_stripped, normal_style)

        story.append(p)
        story.append(Spacer(1, 6))

    doc.build(story)

@app.post("/process-audio/")
async def process_audio(file_path: str):
    # If file_path is not absolute, assume it's relative to the current working directory.
    if not os.path.isabs(file_path):
        absolute_file_path = os.path.normpath(os.path.join(os.getcwd(), file_path))
    else:
        absolute_file_path = os.path.normpath(file_path)
    absolute_file_path = "C:\\Users\\josem\\Desktop\\UCL\\hackathon\\app\\uploads\\test_audio.wav"
    print("Looking for audio file at:", absolute_file_path)
    if not os.path.exists(absolute_file_path):
        raise HTTPException(
            status_code=404,
            detail=f"Audio file not found at: {absolute_file_path}"
        )

    try:
        print('transcribing audio')
        transcript = transcribe_audio(absolute_file_path)
        print('extracting key info')
        extracted_info = extract_key_info(transcript)
        print('generating letter')
        final_letter = generate_outpatient_letter(extracted_info)
        directory = os.path.dirname(absolute_file_path)
        pdf_filename = f"{os.path.splitext(os.path.basename(absolute_file_path))[0]}_report.pdf"
        pdf_path = os.path.join(directory, pdf_filename)
        create_pdf(final_letter, pdf_path)
        txt_filename = f"{os.path.splitext(pdf_filename)[0]}.txt"
        txt_path = os.path.join(directory, txt_filename)
        with open(txt_path, "w") as f:
            f.write(final_letter)
        with open(txt_path, "r") as f:
            letter_text = f.read()
        return {"letter_text": letter_text, "pdf_filename": pdf_filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@app.get("/test")
def test_connection():
    return {"message": "API is working!"}
