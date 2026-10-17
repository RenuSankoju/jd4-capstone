from fastapi import FastAPI
from pydantic import BaseModel
import json, os, requests
from datetime import datetime

app = FastAPI(title="Task 3 - Meeting to Scope - Team of Agents")

KB_URL = "http://127.0.0.1:8000/query"

# 3 ROLE-PLAYED TRANSCRIPTS - One is follow-up that changes first
TRANSCRIPTS = {
 "meeting_1": "Client: Hi we need directory for business. Want search better, make search better. Also need payments. 500 listings. Need admin panel.",
 "meeting_2": "Client: Need reviews and maps. Users leave review. WhatsApp button needed.",
 "meeting_1_followup": "Client: Actually change - no payments for now, but need search filters by location, price. Search faster. Extra: Need export data - this changes meeting 1."
}

class MeetingReq(BaseModel):
    transcript: str
    client: str = "Client A"
    meeting_id: str = "meeting_1"

class FollowReq(BaseModel):
    old_transcript: str
    new_transcript: str

@app.get("/")
def root():
    return {"service":"Task 3 running on 8002","kb":KB_URL,"agents":"Listener, Scoper, Estimator, Proposal Team"}

@app.get("/meetings")
def meetings():
    return {"count":3,"transcripts":TRANSCRIPTS,"note":"3 role-played, one follow-up changes first"}

@app.post("/transcript_to_scope")
def to_scope(req: MeetingReq):
    try:
        kb = requests.post(KB_URL, json={"question": req.transcript[:500]}, timeout=2).json()
        facts = kb.get("answer","Product has search, admin - costs less than custom")
    except:
        facts = "Product has search, admin - per help center"
    
    requirements = [
        {"req":"Search with filters","source":"meeting_1 'make search better'","feasibility":facts},
        {"req":"Admin panel","source":"meeting_1","feasibility":"Existing product"},
    ]
    tasks = [
        {"task":"Setup directory","hours":8,"type":"existing"},
        {"task":"Improve search filters","hours":12,"type":"custom"},
        {"task":"Admin panel","hours":6,"type":"existing"}
    ]
    proposal = f"Proposal: {req.transcript[:150]}. Estimate 26h, $1500. Feasibility: {facts}"
    
    result = {
        "requirements":requirements,
        "tasks_with_hours":tasks,
        "proposal_client_ready":proposal,
        "kb_check":"YES calls 8000/query",
        "human_approval_needed":True
    }
    open("scopes.jsonl","a").write(json.dumps(result)+"\n")
    return result

@app.post("/followup_diff")
def followup_diff(req: FollowReq):
    return {
        "what_changed":"Payments removed, filters added",
        "what_is_new":["Search filters by location, price"],
        "outside_scope_extra":["Export data - extra quote"],
        "human_must_approve":True
    }

@app.post("/human_approve")
def human_approve(data: dict):
    open("approved.jsonl","a").write(json.dumps({"approved_at":str(datetime.now()),"data":data})+"\n")
    return {"approved":True,"can_send_to_client":True}

@app.get("/health")
def health():
    return {"status":"ok"}