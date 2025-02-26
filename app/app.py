from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import requests
from datetime import datetime
from fastapi import FastAPI, HTTPException


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route("/", methods=["GET", "POST"])
def index():
    letter_text = ""
    saved_filename = ""
    if request.method == "POST":
        # Retrieve patient details
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        nhs_number = request.form["nhs_number"]
        dob = request.form["dob"]

        # Retrieve the recorded audio file from the hidden file input
        audio_file = request.files.get("audio_file")
        if audio_file:
            # Save the file using first name, last name, and current date (YYYYMMDD)
            current_date = datetime.now().strftime("%Y%m%d")
            filename = f"{first_name.strip()}_{last_name.strip()}_{current_date}.wav"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            audio_file.save(save_path)
            print("Saved audio file at:", save_path)

            # Build absolute path and call the external API to process the audio
            absolute_path = os.path.abspath(save_path)
            try:
                api_response = requests.post(
                    "http://127.0.0.1:8000/process-audio/",
                    params={"file_path": absolute_path}
                )
                api_response.raise_for_status()
                data = api_response.json()
                letter_text = data.get("letter_text", "No letter text returned.")
                print(letter_text)
                letter_text = "Gastroenterology Department, St Crispin’s Hospital, Donaldstown, DO5 7TP\nDr. Ruth Jones, Consultant Gastroenterologist\n(01234) 567890\ngj@stcrispins.nhs.uk\n\nOutpatient letter to General Practitioner\n\n<b>Patient demographics</b>:\nPatient name: Ms. Critchard\nDate of birth: not specified\nGender: not specified\nNHS number: not specified\nHospital ID: not specified\nPatient address: not specified\nPatient email address: not specified\nPatient telephone number: not specified\n\n<b>Attendance details</b>:\nDate of appointment: not specified\nContact type: not specified\nConsultation method: not specified\nSeen by doctor: Dr. Ruth Jones, Consultant Gastroenterologist\nCare professionals present: not specified\nOutcome of patient attendance: not specified\n\n<b>Diagnosis</b>:\n1. Suspected proctitis, likely related to ulcerative colitis\n\n<b>History</b>:\nThe patient reports rectal bleeding (fresh blood), loose stools (approximately 4 times per day), a sour taste in the mouth upon waking, epigastric pain and heartburn, weight loss, crampy pain in the lower left side, and a family history of inflammatory bowel disease (Crohn's/colitis on maternal side) for the past 3 months.\n\n<b>Family history</b>:\nSeveral relatives on the maternal side had Crohn’s or colitis.\n\n<b>Social context</b>:\nNot specified\n\n<b>Allergies and adverse reactions</b>:\nPenicillin (patient experienced a generalized severe rash)\n\n<b>Examination findings</b>:\nThe abdomen was found to be mildly tender in the left lower abdomen (no guarding or rebound tenderness). Rigid sigmoidoscopy revealed inflamed and ulcerated mucosa up to about 15 cm with contact bleeding.\n\n<b>Investigation findings</b>:\nNot specified\n\n<b>Procedure</b>:\nRigid sigmoidoscopy performed\n\n<b>Clinical summary</b>:\nFindings suggest ulcerative colitis (proctitis).\n\n<b>Actions for healthcare professionals</b>:\nSchedule a flexible sigmoidoscopy for a more detailed examination, order blood tests (FBC, U&E, LFT, CRP), and perform stool tests to rule out infections (e.g., C. difficile).\n\n<b>Changes to medications and medical devices</b>:\nNot specified\n\n<b>Medications and medical devices</b>:\nMedication name: Acycolic mesolazine\nDose: 800 mg\nForm: Oral\nFrequency: 3 x a day\nComment: Patient advised to start this medication and avoid penicillin-based antibiotics due to an allergy.\n\n<b>Signature</b>:\nYours faithfully,\nPerson completing record: Dr. Ruth Jones, Consultant Gastroenterologist\nDate: not specified\nDistribution list: Ms. Critchard (patient), Dr. O'Reilly (GP)"
            except Exception as e:
                letter_text = f"Error calling process-audio API: {str(e)}"

            saved_filename = filename

        # Instead of rendering index.html again, redirect to /edit_report
        return redirect(url_for("edit_report", letter_text=letter_text, filename=saved_filename))
    return render_template("index.html", letter_text=letter_text, saved_filename=saved_filename)

@app.route("/edit_report", methods=["GET", "POST"])
def edit_report():
    if request.method == "POST":
        # Save the edited report.
        edited_text = request.form["edited_text"]
        original_filename = request.form["original_filename"]
        # Remove the extension and append "1.txt" to create a new report file name.
        base, _ = os.path.splitext(original_filename)
        new_report_filename = base + "1.txt"
        report_path = os.path.join(app.config['UPLOAD_FOLDER'], new_report_filename)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(edited_text)
        message = f"Report saved as {new_report_filename}"
        return render_template("edit_report.html", edited_text=edited_text, original_filename=original_filename, message=message)
    else:
        # GET: show the editable report page
        letter_text = request.args.get("letter_text", "")
        original_filename = request.args.get("filename", "")
        return render_template("edit_report.html", edited_text=letter_text, original_filename=original_filename, message="")

@app.route("/final_report")
def final_report():
    # Call the hook URL to get the final report response.
    hook_url = ""
    try:
        # Using GET since clicking the link works.
        response = requests.get(hook_url)
        response.raise_for_status()
        hook_response = response.text
    except Exception as e:
        hook_response = f"Error calling hook: {str(e)}"
    return render_template("final_report.html", hook_response=hook_response)

@app.get("/call-hook")
def call_hook():
    url = ""
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"Error calling hook: {str(e)}"}
    return {"hook_response": response.text}


if __name__ == '__main__':
    app.run(debug=True)
