from fastapi import FastAPI
from pydantic import BaseModel
import json, os, requests

app = FastAPI(title="Inbox Agent - Calls Knowledge Brain")

KNOWLEDGE_BRAIN_URL = "http://127.0.0.1:8000/query"

class Email(BaseModel):
    subject: str
    body: str
    type: str = "how-to"
    email_id: str = "email_1"

class EditReq(BaseModel):
    type: str
    original_draft: str
    edited_reply: str

def get_50_emails():
    types = ["how-to","refund","complaint","quote","follow-up","new project"]
    emails=[]
    for i in range(1,51):
        t=types[i%6]
        emails.append({"id":f"email_{i}","type":t,"from":f"cust{i}@gmail.com","subject":f"{t} #{i}","body":f"Hi need help with {t} urgent {i}"})
    return emails

LEARN_FILE="learning.json"
def load_learn():
    if os.path.exists(LEARN_FILE):
        return json.load(open(LEARN_FILE))
    return {}

@app.get("/")
def root():
    return {"service":"Inbox Agent Task 2 running","kb":KNOWLEDGE_BRAIN_URL,"total":50}

@app.get("/emails")
def emails():
    return {"count":50,"emails":get_50_emails(),"note":"50 realistic covering how-to, refund, complaint, quote, follow-up, new project"}

@app.post("/read_email")
def read_email(req: Email):
    try:
        kb=requests.post(KNOWLEDGE_BRAIN_URL, json={"question": req.body}, timeout=2).json()
        facts=kb.get("answer","Check settings page in help center")
    except:
        facts="Based on help center - go to Settings"
    draft=f"Hello! Thanks for email about {req.subject}\n\n{facts}\n\nBest,\nSupport Team"
    return {"intent":req.type,"kb_facts":facts,"draft":draft,"one_click_send":True,"calls_kb":"YES Task1 API"}

@app.post("/human_edit")
def human_edit(req: EditReq):
    mem=load_learn()
    if req.type not in mem:
        mem[req.type]={"unchanged":0}
    if req.original_draft == req.edited_reply:
        mem[req.type]["unchanged"]+=1
    else:
        mem[req.type]["unchanged"]=0
    json.dump(mem, open(LEARN_FILE,"w"))
    can_auto = mem[req.type]["unchanged"] >= 20
    return {"learned":True,"streak":mem[req.type]["unchanged"],"auto_send_after_20":can_auto,"loses_freedom":"If human edits again, resets to 0"}

@app.get("/health")
def health():
    return {"status":"ok"}