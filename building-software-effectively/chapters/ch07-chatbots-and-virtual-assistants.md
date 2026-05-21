# Chatbots and Virtual Assistants

## Core concepts

- Three implementation tiers: **no-code** (Chatbase — upload data, deploy in 2 minutes), **drag-and-drop** (Botpress — visual workflow builder, more powerful but 30-40 min setup), **code-based** (LangChain — full control, SDK/API, requires dev skills).
- Chatbot output is highly dependent on the underlying LLM. All three tools produced similar answers to the same questions because they used similar GPT models.
- Chatbase is the easiest way to deploy a production chatbot with custom training data (9/10). LangChain is the most powerful for complex agentic workflows (10/10).

## Frameworks introduced

**Chatbot implementation spectrum** — No-code (upload data → deploy) → Drag-and-drop (build visual flows) → Code-based SDKs (full control, agentic workflows, multi-agent systems via LangGraph). Higher tiers offer more control but require more technical skill.

**Shift from list-search-detail to chatbot UI** — Traditional app UIs follow a structured navigation pattern. LLM-based chatbots replace this with unstructured "talk with the data" interactions. This creates room for hallucinations but offers a more natural user experience.

## Key techniques

**RAG chatbot setup:** Upload training data (CSV, documents) as the knowledge base. The AI retrieves relevant context from this data to ground its answers, reducing hallucination compared to relying on the model's training alone.

**Agentic workflow composition (Botpress/LangChain):** Combine multiple agents (retrieval, reasoning, action) into a pipeline. LangChain's LangGraph enables multi-agent systems for complex decision-making.

## Connection to other chapters

Synthesizes patterns from earlier chapters: code generation (Chapter 1) for building chatbots, data analysis (Chapter 5) for training data, documentation (Chapter 6) for chatbot knowledge bases. LangChain is the most developer-friendly framework for building AI-powered applications.
