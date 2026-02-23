"""drugmesh: AI-powered drug repurposing knowledge graph agent
Uses Claude + PubMed/OpenFDA APIs to discover new uses for existing drugs.
"""
import os
import json
import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import anthropic

app = FastAPI(title="DrugMesh Agent", version="1.0.0")
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
OPENFDA_BASE = "https://api.fda.gov/drug"

class RepurposingQuery(BaseModel):
    drug_name: str
    target_disease: Optional[str] = None
    mechanism_of_interest: Optional[str] = None

class RepurposingResult(BaseModel):
    drug: str
    original_indication: str
    candidate_diseases: list[dict]
    evidence_summary: str
    confidence_score: float
    pubmed_references: list[str]

async def search_pubmed(query: str, max_results: int = 5) -> list[str]:
    """Search PubMed for relevant literature."""
    search_url = f"{PUBMED_BASE}/esearch.fcgi?db=pubmed&term={query}&retmax={max_results}&retmode=json"
    async with httpx.AsyncClient() as http:
        resp = await http.get(search_url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            ids = data.get("esearchresult", {}).get("idlist", [])
            return [f"https://pubmed.ncbi.nlm.nih.gov/{id}/" for id in ids]
    return []

async def get_drug_targets(drug_name: str) -> dict:
    """Get drug mechanism and targets from OpenFDA."""
    url = f"{OPENFDA_BASE}/label.json?search=openfda.generic_name:\"{drug_name}\"&limit=1"
    async with httpx.AsyncClient() as http:
        resp = await http.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            if results:
                label = results[0]
                return {
                    "mechanism": label.get("mechanism_of_action", ["Unknown"])[0] if label.get("mechanism_of_action") else "Unknown",
                    "indications": label.get("indications_and_usage", ["Unknown"])[0] if label.get("indications_and_usage") else "Unknown",
                    "contraindications": label.get("contraindications", [])
                }
    return {"mechanism": "Unknown", "indications": "Unknown", "contraindications": []}

@app.post("/repurpose", response_model=RepurposingResult)
async def find_repurposing_candidates(query: RepurposingQuery):
    """Use Claude to identify drug repurposing candidates with evidence."""
    drug_info = await get_drug_targets(query.drug_name)
    pubmed_refs = await search_pubmed(
        f"{query.drug_name} repurposing {query.target_disease or ''} {query.mechanism_of_interest or ''}"
    )

    prompt = f"""You are a computational pharmacology AI specializing in drug repurposing.

Analyze this drug for repurposing opportunities:
Drug: {query.drug_name}
Known mechanism: {drug_info['mechanism']}
Current indication: {drug_info['indications']}
Target disease of interest: {query.target_disease or 'Any promising target'}

Provide repurposing candidates as JSON:
{{
  "original_indication": "current use",
  "candidate_diseases": [
    {{"disease": "name", "rationale": "mechanistic reason", "evidence_level": "preclinical/clinical/approved"}}
  ],
  "evidence_summary": "2-3 sentence synthesis",
  "confidence_score": 0.0-1.0
}}

Focus on mechanistic plausibility, existing clinical trial data, and safety profile."""

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}]
    )

    text = response.content[0].text
    start = text.find("{")
    end = text.rfind("}") + 1
    try:
        result = json.loads(text[start:end])
    except json.JSONDecodeError:
        result = {"original_indication": drug_info["indications"], "candidate_diseases": [], "evidence_summary": text, "confidence_score": 0.5}

    return RepurposingResult(
        drug=query.drug_name,
        original_indication=result.get("original_indication", drug_info["indications"]),
        candidate_diseases=result.get("candidate_diseases", []),
        evidence_summary=result.get("evidence_summary", ""),
        confidence_score=result.get("confidence_score", 0.5),
        pubmed_references=pubmed_refs
    )

@app.get("/drug/{name}/targets")
async def get_targets(name: str):
    return await get_drug_targets(name)

@app.get("/health")
def health():
    return {"status": "ok", "service": "drugmesh"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
