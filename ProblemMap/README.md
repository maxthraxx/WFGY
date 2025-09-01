# WFGY Problem Map 1.0 — bookmark it. you’ll need it
## 🛡️ reproducible AI bugs, permanently fixed at the reasoning layer

**WFGY Problem Map = a reasoning layer for your AI.**  
load [**TXT OS**](https://github.com/onestardao/WFGY/blob/main/OS/README.md) or [**WFGY Core**](https://github.com/onestardao/WFGY/tree/main/core), then ask: *“which problem map number am i hitting?”*  
you’ll get a diagnosis and exact fix steps — no infra changes required.

**16 reproducible failure modes, each with a clear fix (MIT).** *(e.g. rag drift, broken indexes)*  
**A semantic firewall you install once, and every failure stays fixed.**  

> most readers found this map useful and left a ⭐ — if it helps you too, please star it so others can discover.

<details>
<summary><strong>⏱️ 30 seconds: Why WFGY Works as a Semantic Firewall</strong></summary>

<br>

> Most fixes today happen **after generation**:  
> - The model outputs something wrong, then we patch it with retrieval, chains, or tools.  
> - This means the same failures reappear again and again.  
>
> WFGY inverts the sequence.  
> - **Before generation**, it inspects the semantic field (tension, residue, drift signals).  
> - If the state is unstable, it loops, resets, or redirects the path.  
> - Only a stable semantic state is allowed to generate output.  

This is why every failure mode, once mapped, stays fixed.  
You’re not firefighting after the fact—you’re installing a reasoning firewall at the entry point.

---

</details>


<details>
<summary>💥 WFGY Global Fix Map — full index (new, click to open)</summary>

### 🧭 Providers & Agents

| Family | Coverage (all links) |
|--------|-----------------------|
| [LLM Providers](./GlobalFixMap/LLM_Providers/README.md) | [OpenAI](./GlobalFixMap/LLM_Providers/openai.md) · [Azure OpenAI](./GlobalFixMap/LLM_Providers/azure_openai.md) · [Anthropic](./GlobalFixMap/LLM_Providers/anthropic.md) · [Claude (Anthropic)](./GlobalFixMap/LLM_Providers/anthropic_claude.md) · [Google Gemini](./GlobalFixMap/LLM_Providers/gemini.md) <br> [Google Vertex AI](./GlobalFixMap/LLM_Providers/google_vertex_ai.md) · [Mistral](./GlobalFixMap/LLM_Providers/mistral.md) · [Meta LLaMA](./GlobalFixMap/LLM_Providers/meta_llama.md) · [Cohere](./GlobalFixMap/LLM_Providers/cohere.md) · [DeepSeek](./GlobalFixMap/LLM_Providers/deepseek.md) <br> [Kimi (Moonshot)](./GlobalFixMap/LLM_Providers/kimi.md) · [Groq](./GlobalFixMap/LLM_Providers/groq.md) · [xAI Grok](./GlobalFixMap/LLM_Providers/grok_xai.md) · [AWS Bedrock](./GlobalFixMap/LLM_Providers/aws_bedrock.md) · [OpenRouter](./GlobalFixMap/LLM_Providers/openrouter.md) <br> [Together AI](./GlobalFixMap/LLM_Providers/together.md) |
| [Agents & Orchestration](./GlobalFixMap/Agents_Orchestration/README.md) | [Autogen](./GlobalFixMap/Agents_Orchestration/autogen.md) · [CrewAI](./GlobalFixMap/Agents_Orchestration/crewAI.md) · [Haystack Agents](./GlobalFixMap/Agents_Orchestration/haystack_agents.md) · [LangChain](./GlobalFixMap/Agents_Orchestration/langchain.md) <br> [LangGraph](./GlobalFixMap/Agents_Orchestration/langgraph.md) · [LlamaIndex](./GlobalFixMap/Agents_Orchestration/llamaindex.md) · [OpenAI Assistants v2](./GlobalFixMap/Agents_Orchestration/openai_assistants_v2.md) · [Rewind Agents](./GlobalFixMap/Agents_Orchestration/rewind_agents.md) <br> [Semantic Kernel](./GlobalFixMap/Agents_Orchestration/semantic_kernel.md) · [Smolagents](./GlobalFixMap/Agents_Orchestration/smolagents.md) |
| [Chatbots & CX](./GlobalFixMap/Chatbots_CX/README.md) | [Amazon Lex](./GlobalFixMap/Chatbots_CX/amazon_lex.md) · [Azure Bot Service](./GlobalFixMap/Chatbots_CX/azure_bot_service.md) · [Dialogflow CX](./GlobalFixMap/Chatbots_CX/dialogflow_cx.md) · [Freshchat](./GlobalFixMap/Chatbots_CX/freshchat.md) <br> [Freshdesk](./GlobalFixMap/Chatbots_CX/freshdesk.md) · [Intercom](./GlobalFixMap/Chatbots_CX/intercom.md) · [Microsoft Copilot Studio](./GlobalFixMap/Chatbots_CX/microsoft_copilot_studio.md) · [Rasa](./GlobalFixMap/Chatbots_CX/rasa.md) <br> [Salesforce Einstein Bots](./GlobalFixMap/Chatbots_CX/salesforce_einstein_bots.md) · [Twilio Studio](./GlobalFixMap/Chatbots_CX/twilio_studio.md) · [Watson Assistant](./GlobalFixMap/Chatbots_CX/watsonx_assistant.md) · [Zendesk](./GlobalFixMap/Chatbots_CX/zendesk.md) |
| [Cloud Serverless](./GlobalFixMap/Cloud_Serverless/README.md) | [Cold Start Concurrency](./GlobalFixMap/Cloud_Serverless/cold_start_concurrency.md) · [Timeouts & Streaming Limits](./GlobalFixMap/Cloud_Serverless/timeouts_streaming_body_limits.md) · [Stateless Grain Patterns](./GlobalFixMap/Cloud_Serverless/stateless_grain_patterns.md) · [EPC Cache Invalidations](./GlobalFixMap/Cloud_Serverless/epc_cache_invalidations.md) <br> [Egress Rules & Webhooks](./GlobalFixMap/Cloud_Serverless/egress_rules_and_webhooks.md) · [Serverless CI/CD](./GlobalFixMap/Cloud_Serverless/serverless_ci_cd.md) · [Bootstrapping & Migrations](./GlobalFixMap/Cloud_Serverless/svc_bootstrapping_migrations.md) · [Secrets Rotation](./GlobalFixMap/Cloud_Serverless/secrets_rotation.md) <br> [Multi-Region Routing](./GlobalFixMap/Cloud_Serverless/multi_region_routing.md) · [Failover Drills](./GlobalFixMap/Cloud_Serverless/region_failover_drills.md) · [Observability & SLOs](./GlobalFixMap/Cloud_Serverless/observability_slos.md) · [Canary Releases](./GlobalFixMap/Cloud_Serverless/canary_releases.md) <br> [Blue-Green Switchovers](./GlobalFixMap/Cloud_Serverless/blue_green_switchovers.md) · [Disaster Recovery](./GlobalFixMap/Cloud_Serverless/disaster_recovery_tabletop.md) · [Data Retention & Backups](./GlobalFixMap/Cloud_Serverless/data_retention_and_backups.md) · [Privacy & PII Edges](./GlobalFixMap/Cloud_Serverless/privacy_and_pii_edges.md) |


#### 🧭 Data & Retrieval
| Family | Coverage (all links) | Notes |
|---|---|---|
| [Vector DBs & Stores](./GlobalFixMap/VectorDBs_and_Stores/README.md) | [FAISS](./GlobalFixMap/VectorDBs_and_Stores/faiss.md) · [Chroma](./GlobalFixMap/VectorDBs_and_Stores/chroma.md) · [Qdrant](./GlobalFixMap/VectorDBs_and_Stores/qdrant.md) · [Weaviate](./GlobalFixMap/VectorDBs_and_Stores/weaviate.md) · [Milvus](./GlobalFixMap/VectorDBs_and_Stores/milvus.md) <br> [pgvector](./GlobalFixMap/VectorDBs_and_Stores/pgvector.md) · [Redis](./GlobalFixMap/VectorDBs_and_Stores/redis.md) · [Elasticsearch](./GlobalFixMap/VectorDBs_and_Stores/elasticsearch.md) · [Pinecone](./GlobalFixMap/VectorDBs_and_Stores/pinecone.md) · [Typesense](./GlobalFixMap/VectorDBs_and_Stores/typesense.md) <br> [Vespa](./GlobalFixMap/VectorDBs_and_Stores/vespa.md) | metric, analyzer, index hygiene |
| [RAG + VectorDB](./GlobalFixMap/RAG_VectorDB/README.md) | [Metric Mismatch](./GlobalFixMap/RAG_VectorDB/metric_mismatch.md) · [Normalization & Scaling](./GlobalFixMap/RAG_VectorDB/normalization_and_scaling.md) · [Tokenization & Casing](./GlobalFixMap/RAG_VectorDB/tokenization_and_casing.md) · [Chunking → Embedding Contract](./GlobalFixMap/RAG_VectorDB/chunking_to_embedding_contract.md) <br> [Vectorstore Fragmentation](./GlobalFixMap/RAG_VectorDB/vectorstore_fragmentation.md) · [Dimension Mismatch & Projection](./GlobalFixMap/RAG_VectorDB/dimension_mismatch_and_projection.md) · [Update & Index Skew](./GlobalFixMap/RAG_VectorDB/update_and_index_skew.md) <br> [Hybrid Retriever Weights](./GlobalFixMap/RAG_VectorDB/hybrid_retriever_weights.md) · [Duplication & Collapse](./GlobalFixMap/RAG_VectorDB/duplication_and_near_duplicate_collapse.md) · [Poisoning & Contamination](./GlobalFixMap/RAG_VectorDB/poisoning_and_contamination.md) | store-agnostic knobs |
| [Retrieval](./GlobalFixMap/Retrieval/README.md) | [Retrieval Playbook](./GlobalFixMap/Retrieval/retrieval_playbook.md) · [Traceability](./GlobalFixMap/Retrieval/retrieval_traceability.md) · [Rerankers](./GlobalFixMap/Retrieval/rerankers.md) · [Query Parsing Split](./GlobalFixMap/Retrieval/query_parsing_split.md) <br> [Chunk Alignment](./GlobalFixMap/Retrieval/chunk_alignment.md) · [ΔS Probes](./GlobalFixMap/Retrieval/ds_probes.md) · [Eval Recipes](./GlobalFixMap/Retrieval/retrieval_eval_recipes.md) · [Store-Agnostic Guardrails](./GlobalFixMap/Retrieval/store_agnostic_guardrails.md) | end-to-end routing & contracts |
| [Embeddings](./GlobalFixMap/Embeddings/README.md) | [Metric Mismatch](./GlobalFixMap/Embeddings/metric_mismatch.md) · [Normalization & Scaling](./GlobalFixMap/Embeddings/normalization_and_scaling.md) · [Tokenization & Casing](./GlobalFixMap/Embeddings/tokenization_and_casing.md) · [Chunking → Embedding Contract](./GlobalFixMap/Embeddings/chunking_to_embedding_contract.md) <br> [Vectorstore Fragmentation](./GlobalFixMap/Embeddings/vectorstore_fragmentation.md) · [Dimension Mismatch & Projection](./GlobalFixMap/Embeddings/dimension_mismatch_and_projection.md) · [Update & Index Skew](./GlobalFixMap/Embeddings/update_and_index_skew.md) <br> [Hybrid Retriever Weights](./GlobalFixMap/Embeddings/hybrid_retriever_weights.md) · [Duplication & Collapse](./GlobalFixMap/Embeddings/duplication_and_near_duplicate_collapse.md) · [Poisoning & Contamination](./GlobalFixMap/Embeddings/poisoning_and_contamination.md) | embedding≠semantic checks |
| [Chunking](./GlobalFixMap/Chunking/README.md) | [Chunk ID Schema](./GlobalFixMap/Chunking/chunk_id_schema.md) · [Checklist](./GlobalFixMap/Chunking/chunking_checklist.md) · [Code / Tables / Blocks](./GlobalFixMap/Chunking/code_tables_blocks.md) · [Section Detection](./GlobalFixMap/Chunking/section_detection.md) <br> [Title Hierarchy](./GlobalFixMap/Chunking/title_hierarchy.md) · [PDF Layouts & OCR](./GlobalFixMap/Chunking/pdf_layouts_ocr.md) · [Reindex & Migration](./GlobalFixMap/Chunking/reindex_migration.md) <br> [Eval Precision & Recall](./GlobalFixMap/Chunking/eval_rag_precision_recall.md) · [Live Monitoring](./GlobalFixMap/Chunking/live_monitoring_rag.md) | chunk/section discipline |
| [RAG](./GlobalFixMap/RAG/README.md) | [Retrieval Drift](./GlobalFixMap/RAG/retrieval_drift.md) · [Hallucination RAG](./GlobalFixMap/RAG/hallucination_rag.md) · [Citation Break](./GlobalFixMap/RAG/citation_break.md) · [Hybrid Failure](./GlobalFixMap/RAG/hybrid_failure.md) <br> [Index Skew](./GlobalFixMap/RAG/index_skew.md) · [Context Drift](./GlobalFixMap/RAG/context_drift.md) · [Entropy Collapse](./GlobalFixMap/RAG/entropy_collapse.md) · [Eval Drift](./GlobalFixMap/RAG/eval_drift.md) | visual routes, acceptance targets |


#### 🧭 Input & Parsing
| Family (link) | Coverage examples | Notes |
|---|---|---|
| [**DocumentAI_OCR**](./GlobalFixMap/DocumentAI_OCR/README.md) | scanned PDFs, tables, math, anchors | pre-embedding text integrity |
| [**OCR_Parsing**](./GlobalFixMap/OCR_Parsing/README.md) | hyphen splits, headers, code/math collapse | parser rails & checks |
| [**Language**](./GlobalFixMap/Language/README.md) | multilingual mixes, CJK/RTL/Indic | cross-script retrieval stability |
| [**LanguageLocale**](./GlobalFixMap/LanguageLocale/README.md) | locale drift, full/halfwidth, diacritics | analyzer/normalization profiles |

#### 🧭 Reasoning & Memory
| Family (link) | Coverage examples | Notes |
|---|---|---|
| [**Reasoning**](./GlobalFixMap/Reasoning/README.md) | entropy overload, loops, symbolic collapse, bridge proofs | BBMC/BBPF/BBCR/BBAM rails |
| [**MemoryLongContext**](./GlobalFixMap/MemoryLongContext/README.md) | desync, echo loops, boundary fade, signal drop | long-window guardrails |
| [**Multimodal_LongContext**](./GlobalFixMap/Multimodal_LongContext/README.md) | image+text spans, stitching | multimodal joins & anchors |

#### 🧭 Automation & Ops
| Family (link) | Coverage examples | Notes |
|---|---|---|
| [**Automation**](./GlobalFixMap/Automation/README.md) | Zapier, n8n, Make, GitHub Actions, GHL, Airtable… | idempotency, warmups, fences |
| [**OpsDeploy**](./GlobalFixMap/OpsDeploy/README.md) | rollback, retries, traffic mirroring, read-only mode, migrations | prod safety rails |
| [**Safety_PromptIntegrity**](./GlobalFixMap/Safety_PromptIntegrity/README.md) | prompt injection, jailbreaks, role order, citations-first, tool timeouts | schema locks |
| [**PromptAssembly**](./GlobalFixMap/PromptAssembly/README.md) | JSON/tool calls, templates, eval prompts | contract & eval kits |
| [**LocalDeploy_Inference**](./GlobalFixMap/LocalDeploy_Inference/README.md) | ollama, vLLM, llama.cpp, loaders/quant, kv-cache | local stack guardrails |
| [**DevTools_CodeAI**](./GlobalFixMap/DevTools_CodeAI/README.md) | Copilot, Cursor, Cody, Codeium, Tabnine, JetBrains AA | IDE/assist rails |

#### 🧭 Eval & Governance
| Family (link) | Coverage examples | Notes |
|---|---|---|
| [**Eval**](./GlobalFixMap/Eval/README.md) | ship gates, precision/recall, ΔS/λ probes | SDK-free evals |
| [**Eval_Observability**](./GlobalFixMap/Eval_Observability/README.md) | live probes, regression boards | drift alarms |
| [**Governance**](./GlobalFixMap/Governance/README.md) | policies, approvals, audit trails | program-level rails |
| [**Enterprise_Knowledge_Gov**](./GlobalFixMap/Enterprise_Knowledge_Gov/README.md) | residency, sensitivity, expiry, compliance | knowledge governance |

</details>


<div align="center">
  <img src="https://github.com/onestardao/WFGY/raw/main/OS/images/tree-semantic-memory.gif"
       alt="semantic memory & reasoning fix in action"
       width="100%" style="max-width:900px" loading="lazy">
</div>

---

> **❓ BigBig Question — If AI bugs are not random but mathematically inevitable, can we finally define and prevent them?**  
> *(this repo is one experiment toward that direction)*

---


## quick access

> don’t worry if this looks long. with TXT OS loaded, simply ask your LLM:  
> *“which Problem Map number fits my issue?”* it will point you to the right page.

- **Semantic Clinic (triage when unsure):** [Fix symptoms fast →](./SemanticClinicIndex.md)
- **Getting Started (practical):** [Guard a RAG pipeline with WFGY →](./getting-started.md)
- **Beginner Guide:** [Find and fix your first failure →](./BeginnerGuide.md)
- **Diagnose by symptom:** [`Diagnose.md` table →](./Diagnose.md)
- **Visual RAG Guide:** [`RAG Architecture & Recovery`](./rag-architecture-and-recovery.md)  
  high-altitude map linking symptom × stage × failure class with exact recovery paths.
- **Multi-Agent chaos:** [Role drift & memory overwrite →](./Multi-Agent_Problems.md)
- **Field reports:** [Real bugs and fixes from users →](https://github.com/onestardao/WFGY/discussions/10)
- **TXT OS directory:** [browse the OS repo →](../OS/README.md)
- **MVP demos:** [Minimal WFGY examples →](./mvp_demo/README.md)

> tip: if you’re new, skip scrolling — use the **minimal quick-start** below.

---

## quick-start downloads (60 sec)

> new here? skip the map. grab TXT OS or the WFGY PDF, boot, then ask your model:  
> *“answer using WFGY: <your question>”* or *“which Problem Map number am i hitting?”*

| tool | link | 3-step setup |
|------|------|--------------|
| **WFGY 1.0 PDF** | [engine paper](https://github.com/onestardao/WFGY/blob/main/I_am_not_lizardman/WFGY_All_Principles_Return_to_One_v1.0_PSBigBig_Public.pdf) | 1) download  2) upload to your LLM  3) ask: “answer using WFGY + <your question>” |
| **TXT OS** | [TXTOS.txt](https://github.com/onestardao/WFGY/blob/main/OS/TXTOS.txt) | 1) download  2) paste into any LLM chat  3) type “hello world” to boot |

---

## why this matters long-term

these 16 errors are not random. they are structural weak points every ai pipeline hits eventually.  
with WFGY as a **semantic firewall** you don’t just fix today’s issue — you shield tomorrow’s.

> this isn’t just a bug list. it’s an **x-ray** for your pipeline, so you stop guessing and start repairing.

see the end-to-end view: [`RAG Architecture & Recovery`](./rag-architecture-and-recovery.md)

---

## 🧪 one-click sandboxes — run WFGY instantly
run lightweight diagnostics with zero install and zero api key. powered by colab.

> these tools map directly to the problem classes. others are handled inside WFGY and will surface in later CLIs.

<details>
<summary><strong>ΔS diagnostic (mvp)</strong> — measure semantic drift</summary>

[open in colab](https://colab.research.google.com/github/onestardao/WFGY/blob/main/tools/wfgy_diagnose_colab.ipynb)

detects: No.2 — [Interpretation Collapse](./retrieval-collapse.md)  
steps: run all, paste prompt+answer, read ΔS and fix tip
</details>

<details>
<summary><strong>λ_observe checkpoint</strong> — mid-step re-grounding</summary>

[open in colab](https://colab.research.google.com/github/onestardao/WFGY/blob/main/tools/wfgy_lambda_observe_colab.ipynb)

fixes: No.6 — [Logic Collapse & Recovery](./logic-collapse.md)  
steps: run all, compare ΔS before/after, fallback to BBCR if needed
</details>

<details>
<summary><strong>ε_resonance</strong> — domain-level harmony</summary>

[open in colab](https://colab.research.google.com/github/onestardao/WFGY/blob/main/tools/wfgy_e_resonance_colab.ipynb)

explains: No.12 — [Philosophical Recursion](./philosophical-recursion.md)  
steps: run, tune anchors, read ε
</details>

<details>
<summary><strong>λ_diverse</strong> — answer-set diversity</summary>

[open in colab](https://colab.research.google.com/github/onestardao/WFGY/blob/main/tools/wfgy_lambda_diverse_colab.ipynb)

detects: No.3 — [Long Reasoning Chains](./context-drift.md)  
steps: run, supply ≥3 answers, read score
</details>

---

## failure catalog (with fixes)

> if you are unsure which one applies, ask your LLM with TXT OS loaded:  
> *“which Problem Map number matches my trace?”* it will route you.

### legend
`[IN]` Input & Retrieval   `[RE]` Reasoning & Planning  
`[ST]` State & Context     `[OP]` Infra & Deployment  
`{OBS}` Observability/Eval `{SEC}` Security `{LOC}` Language/OCR

| #  | problem domain (with layer/tags)           | what breaks                                   | doc |
|----|--------------------------------------------|-----------------------------------------------|-----|
| 1  | **[IN]** hallucination & chunk drift {OBS} | retrieval returns wrong/irrelevant content    | [hallucination.md](./hallucination.md) |
| 2  | **[RE]** interpretation collapse           | chunk is right, logic is wrong                | [retrieval-collapse.md](./retrieval-collapse.md) |
| 3  | **[RE]** long reasoning chains {OBS}       | drifts across multi-step tasks                | [context-drift.md](./context-drift.md) |
| 4  | **[RE]** bluffing / overconfidence         | confident but unfounded answers               | [bluffing.md](./bluffing.md) |
| 5  | **[IN]** semantic ≠ embedding {OBS}        | cosine match ≠ true meaning                   | [embedding-vs-semantic.md](./embedding-vs-semantic.md) |
| 6  | **[RE]** logic collapse & recovery {OBS}   | dead-ends, needs controlled reset             | [logic-collapse.md](./logic-collapse.md) |
| 7  | **[ST]** memory breaks across sessions     | lost threads, no continuity                   | [memory-coherence.md](./memory-coherence.md) |
| 8  | **[IN]** debugging is a black box {OBS}    | no visibility into failure path               | [retrieval-traceability.md](./retrieval-traceability.md) |
| 9  | **[ST]** entropy collapse                  | attention melts, incoherent output            | [entropy-collapse.md](./entropy-collapse.md) |
| 10 | **[RE]** creative freeze                   | flat, literal outputs                         | [creative-freeze.md](./creative-freeze.md) |
| 11 | **[RE]** symbolic collapse                 | abstract/logical prompts break                | [symbolic-collapse.md](./symbolic-collapse.md) |
| 12 | **[RE]** philosophical recursion           | self-reference loops, paradox traps           | [philosophical-recursion.md](./philosophical-recursion.md) |
| 13 | **[ST]** multi-agent chaos {OBS}           | agents overwrite or misalign logic            | [Multi-Agent_Problems.md](./Multi-Agent_Problems.md) |
| 14 | **[OP]** bootstrap ordering                | services fire before deps ready               | [bootstrap-ordering.md](./bootstrap-ordering.md) |
| 15 | **[OP]** deployment deadlock               | circular waits in infra                       | [deployment-deadlock.md](./deployment-deadlock.md) |
| 16 | **[OP]** pre-deploy collapse {OBS}         | version skew / missing secret on first call   | [predeploy-collapse.md](./predeploy-collapse.md) |

for No.13 deep dives:  
• role drift → [`multi-agent-chaos/role-drift.md`](./multi-agent-chaos/role-drift.md)  
• cross-agent memory overwrite → [`multi-agent-chaos/memory-overwrite.md`](./multi-agent-chaos/memory-overwrite.md)

---

## minimal quick-start

1) open **Beginner Guide** and follow the symptom checklist.  
2) use the **Visual RAG Guide** to locate the failing stage.  
3) open the matching page and apply the patch.

ask any LLM to apply WFGY (TXT OS makes it smoother):

```

i’ve uploaded TXT OS / WFGY notes.
my issue: \[e.g., OCR tables look fine but answers point to wrong sections]
which WFGY modules should i apply and in what order?

```

<details>
<summary><strong>status & difficulty</strong></summary>

| #  | problem (with layer/tags)                  | difficulty* | implementation |
|----|--------------------------------------------|-------------|----------------|
| 1  | **[IN]** hallucination & chunk drift {OBS} | medium      | ✅ stable |
| 2  | **[RE]** interpretation collapse           | high        | ✅ stable |
| 3  | **[RE]** long reasoning chains {OBS}       | high        | ✅ stable |
| 4  | **[RE]** bluffing / overconfidence         | high        | ✅ stable |
| 5  | **[IN]** semantic ≠ embedding {OBS}        | medium      | ✅ stable |
| 6  | **[RE]** logic collapse & recovery {OBS}   | very high   | ✅ stable |
| 7  | **[ST]** memory breaks across sessions     | high        | ✅ stable |
| 8  | **[IN]** debugging black box {OBS}         | medium      | ✅ stable |
| 9  | **[ST]** entropy collapse                  | high        | ✅ stable |
| 10 | **[RE]** creative freeze                   | medium      | ✅ stable |
| 11 | **[RE]** symbolic collapse                 | very high   | ✅ stable |
| 12 | **[RE]** philosophical recursion           | very high   | ✅ stable |
| 13 | **[ST]** multi-agent chaos {OBS}           | very high   | ✅ stable |
| 14 | **[OP]** bootstrap ordering                | medium      | ✅ stable |
| 15 | **[OP]** deployment deadlock               | high        | ⚠️ beta |
| 16 | **[OP]** pre-deploy collapse {OBS}         | medium-high | ✅ stable |

\*distance from default LLM behavior to a production-ready fix.
</details>

---

### 🔬 Behind the Map
The Problem Map is practical and ready to use.  
But if you wonder *why* these fixes work, and how we’re defining physics inside embedding space:  
→ [The Hidden Value Engine (WFGY Physics)](https://github.com/onestardao/WFGY/tree/main/value_manifest/README.md)

---


## 🔮 coming soon: global fix map

a universal layer above providers, agents, and infra.  
Problem Map is step one. **Global Fix Map** expands the same reasoning-first firewall to RAG, infra boot, agents, evals, and more. same zero-install experience. launching around **Sep**.

---

## contributing / support

- open an issue with a minimal repro (inputs → calls → wrong output).  
- PRs for clearer docs, repros, or patches are welcome.  
- project home: [github.com/onestardao/WFGY](https://github.com/onestardao/WFGY)  
- TXT OS: [browse the OS](https://github.com/onestardao/WFGY/tree/main/OS)  
- if this map helped you, a ⭐ helps more devs find it.


---


### 🧭 Explore More

| Module                | Description                                              | Link     |
|-----------------------|----------------------------------------------------------|----------|
| WFGY Core             | WFGY 2.0 engine is live: full symbolic reasoning architecture and math stack | [View →](https://github.com/onestardao/WFGY/tree/main/core/README.md) |
| Problem Map 1.0       | Initial 16-mode diagnostic and symbolic fix framework    | [View →](https://github.com/onestardao/WFGY/tree/main/ProblemMap/README.md) |
| Problem Map 2.0       | RAG-focused failure tree, modular fixes, and pipelines   | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/rag-architecture-and-recovery.md) |
| Semantic Clinic Index | Expanded failure catalog: prompt injection, memory bugs, logic drift | [View →](https://github.com/onestardao/WFGY/blob/main/ProblemMap/SemanticClinicIndex.md) |
| Semantic Blueprint    | Layer-based symbolic reasoning & semantic modulations   | [View →](https://github.com/onestardao/WFGY/tree/main/SemanticBlueprint/README.md) |
| Benchmark vs GPT-5    | Stress test GPT-5 with full WFGY reasoning suite         | [View →](https://github.com/onestardao/WFGY/tree/main/benchmarks/benchmark-vs-gpt5/README.md) |

---

> 👑 **Early Stargazers: [See the Hall of Fame](https://github.com/onestardao/WFGY/tree/main/stargazers)** —  
> Engineers, hackers, and open source builders who supported WFGY from day one.

> <img src="https://img.shields.io/github/stars/onestardao/WFGY?style=social" alt="GitHub stars"> ⭐ [WFGY Engine 2.0](https://github.com/onestardao/WFGY/blob/main/core/README.md) is already unlocked. ⭐ Star the repo to help others discover it and unlock more on the [Unlock Board](https://github.com/onestardao/WFGY/blob/main/STAR_UNLOCKS.md).

<div align="center">

[![WFGY Main](https://img.shields.io/badge/WFGY-Main-red?style=flat-square)](https://github.com/onestardao/WFGY)
&nbsp;
[![TXT OS](https://img.shields.io/badge/TXT%20OS-Reasoning%20OS-orange?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS)
&nbsp;
[![Blah](https://img.shields.io/badge/Blah-Semantic%20Embed-yellow?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlahBlahBlah)
&nbsp;
[![Blot](https://img.shields.io/badge/Blot-Persona%20Core-green?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlotBlotBlot)
&nbsp;
[![Bloc](https://img.shields.io/badge/Bloc-Reasoning%20Compiler-blue?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlocBlocBloc)
&nbsp;
[![Blur](https://img.shields.io/badge/Blur-Text2Image%20Engine-navy?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlurBlurBlur)
&nbsp;
[![Blow](https://img.shields.io/badge/Blow-Game%20Logic-purple?style=flat-square)](https://github.com/onestardao/WFGY/tree/main/OS/BlowBlowBlow)
&nbsp;
</div>
