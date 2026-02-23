# DrugMesh

> AI-powered drug repurposing knowledge graph linking existing approved compounds to new disease targets using biomedical literature mining, protein interaction networks, and LLM reasoning.

## Vision

Drug development costs $2.6B and takes 12 years per approved drug. **Drug repurposing** — finding new uses for existing approved drugs — can cut that to $300M and 3–5 years. But the biomedical knowledge needed to identify repurposing opportunities is scattered across 35 million PubMed papers, thousands of clinical trials, and dozens of molecular databases.

DrugMesh builds a unified, AI-navigable knowledge graph that connects drugs, targets, diseases, pathways, and clinical evidence — then uses LLM reasoning to surface the most promising repurposing hypotheses.

## Knowledge Graph Coverage

| Data Source | Entities | Relationships |
|-------------|----------|---------------|
| DrugBank | 14,000 drugs | 20,000 drug-target |
| UniProt | 570,000 proteins | 500,000 PPI |
| DisGeNET | 30,000 genes | 1.1M gene-disease |
| PubMed (LLM-mined) | 35M papers | 50M+ extracted |
| ClinicalTrials.gov | 400,000 trials | Indication-drug |
| STRING DB | 67M proteins | 2.6B interactions |
| KEGG Pathways | 500+ pathways | Drug-pathway |

## Core Capabilities

### 1. Drug-Target-Disease Graph
- Multi-hop reasoning: drug → target → pathway → disease
- Graph neural network embeddings for similarity search
- Candidate scoring based on mechanistic plausibility

### 2. Literature Mining
- Real-time PubMed ingestion and relationship extraction
- Claude-powered entity recognition and relation extraction
- Evidence quality scoring (RCT > observational > case report)

### 3. Repurposing Hypothesis Engine
- Ranked list of drug-disease pairs with supporting evidence
- Mechanistic explanation in plain language
- Confidence intervals based on evidence strength
- Side effect / contraindication risk assessment

### 4. Clinical Trial Matching
- Map repurposing candidates to ongoing trials
- Identify gaps: high-plausibility candidates with no active trials
- FDA orphan drug / breakthrough designation eligibility analysis

### 5. Research API
- GraphQL API for custom knowledge graph queries
- Python SDK for computational drug discovery workflows
- Webhook alerts for new evidence matching saved hypotheses

## Example Use Cases

- Find all approved kinase inhibitors that could treat rare metabolic diseases
- Identify drugs that modulate neuroinflammation pathways implicated in ALS
- Surface repurposing candidates for pediatric cancers with no approved therapies
- Analyze why a failed clinical trial drug might work for a different indication

## Roadmap

- [x] Knowledge graph schema + initial drug/target/disease loading
- [x] Claude-powered repurposing reasoning agent
- [ ] Full PubMed literature mining pipeline
- [ ] GNN-based drug-target embedding model
- [ ] ClinicalTrials.gov integration
- [ ] GraphQL API v1
- [ ] Web interface for non-programmers

## Tech Stack

- **Graph DB:** Neo4j, NetworkX
- **ML:** PyTorch, PyG (PyTorch Geometric)
- **AI:** Anthropic Claude for reasoning
- **Backend:** Python, FastAPI
- **NLP:** spaCy, Hugging Face Transformers (BiomedNLP models)
- **Data:** PostgreSQL, Redis

## Getting Started

```bash
git clone https://github.com/raimp001/drugmesh
cd drugmesh
pip install -r requirements.txt
# Load initial knowledge graph
python -m drugmesh.ingest --sources drugbank,uniprot,disgenet
# Start the API server
python -m drugmesh.server
```

## License

MIT License
