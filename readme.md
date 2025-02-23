# Steven: The Doctor’s Co-Pilot – Less Admin, More Patient Care

Steven is a medical co-pilot designed to streamline the administrative tasks of healthcare professionals by leveraging advanced natural language processing and conversational AI. The project automates tasks such as note-taking, report drafting, and referral letter composition, allowing doctors to devote more time to patient care and clinical decision-making.

---
## Table of Contents

- [Problem Statement]
- [Our Solution]
- [Team]
- [Technical Details]
  - [Tech Stack]
  - [Orchestration via Make]
  - [Front-End]
- [How We Built It]
- [Development Experience]
  - [Encountered Challenges]
  - [Our Accomplishments]
  - [What We Learned]
- [What's Next]
- [Compliance]
- [Useful Links]


---
## Problem Statement

Doctors today spend a significant amount of time on administrative tasks—such as note-taking, drafting reports, and composing follow-up referral letters—detracting from the critical time needed for patient care and clinical decision making. 

 - **Administrative Overload:** Doctors are burdened with paperwork and administrative duties during and after consultations.
- **Time Management:** The extensive time spent on non-clinical tasks reduces the availability for patient care and thoughtful clinical decision-making.
- **Workflow Efficiency:** Current systems lack a seamless, automated way to handle routine documentation and support decision-making.

---
## Our Solution

Steven is a medical co-pilot that listens to the doctor-patient conversation in real time, and then, post-consultation, automates the administrative process and acts as a co-pilot for medical decision-making. It generates detailed reports—saving up to 50% of the time normally spent on these tasks—and improves the differential diagnosis. By leveraging a natural, conversational interface designed for busy, on-the-move healthcare professionals, Steven ultimately frees up more time for doctors to focus on what they are good at.

---
## Team

- **Alexander Stern** – Member of Technical Staff  
  *Email:* alexander.stern.20@ucl.ac.uk
- **Amit John** – Member of Technical Staff  
  *Email:* amit.john.24@ucl.ac.uk
- **José Cáceres** – Member of Technical Staff  
  *Email:* [jose.valenzuela.24@ucl.ac.uk](mailto:jose.valenzuela.24@ucl.ac.uk)
- **Niklas Falk** – Member of Technical Staff  
  *Email:* niklas.falk.24@ucl.ac.uk

---
## Technical Details

### Tech Stack

- Interactive multi-agent system to transcribe audio file into draft report using a summarization and writing agent connected via CrewAI.
- Conversational agent using Elevenlabs and connecting it via Make and Google Drive to the draft report.
- Orchestration via Make:
	- Front-end built with Flask, we used Lovable for our mock-up

Public repository link:
- Conversational agent: [https://elevenlabs.io/app/talk-to?agent_id=h0Z4SUEsg1CRFgHzW7HG](https://elevenlabs.io/app/talk-to?agent_id=h0Z4SUEsg1CRFgHzW7HG)
- GitHub repository:

### How we built it

- Interactive multi-agent system to transcribe audio file into draft report using a summarization and writing agent connected via CrewAI
- Conversational agent using Elevenlabs and connecting it via Make and Google Drive to the draft report
- Front-end built with Flask, we used Lovable for our mock-up

---
## The Development Experience
### Encountered Challenges

- Getting the multi-agent architecture to summarize long audio transcriptions
- Not knowing the exact tools that Doctors currently use in the NHS healthcare, hence having to make some assumptions with work-flows.

### Our Accomplishments

- Showing our product to medical students and them getting excited. They told us that a doctor supervisor of theirs has specifically said that they wish they had "a robot" doing all these boring administrative tasks.
- Creating multi agent LLM ecosystem -Using [make.com](http://make.com/) to save lot's time building the backend, and integrating it with Eleven Labs conversational agent.

### What We Learned

- **Conversational Agent Development:** 
  - Gained practical experience building and integrating Elevenlabs conversational agents.
- **Identifying Industry Pain Points:** 
  - Recognized and addressed a critical inefficiency in the medical administrative workflow.
- **Agile Development:** 
  - Demonstrated that even complex, multi-component systems can be built rapidly with the right tools and collaborative effort.

---
## What's next for Steven: Doctor’s Co-Pilot – Less Admin, More Patient Care

Steven enables a future where healthcare is patient focused as doctors can spend more time doing what they are good at, allowing for improved differential diagnosis and increased patient throughput. The industry is crying out for these cost and time saving AI tools. We want to iterate on the MVP that we made in 24 hours, and make it production-grade, with a better backend infrastructure.

---
## Compliance

We confirm our adherence to the hackathon’s rules and deadlines. All project guidelines have been followed to ensure a compliant and innovative submission.

---

## Useful Links

- **Conversational Agent Demo:**  
  [Talk to Steven](https://elevenlabs.io/app/talk-to?agent_id=h0Z4SUEsg1CRFgHzW7HG)
- **GitHub Repository:**  
  *(Link to be provided in the repository)*

---

*Steven: The Doctor’s Co-Pilot – enabling a future where healthcare is truly patient-focused by reducing administrative overhead and empowering medical professionals to focus on what matters most.*
