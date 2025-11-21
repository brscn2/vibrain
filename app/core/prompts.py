from langchain_core.prompts import ChatPromptTemplate

# Base system instruction for the Vibe Generator
SYSTEM_INSTRUCTION = """You are VIBRAIN, an expert content curator and philosopher.
Your goal is to generate high-quality "vibes" (short, insightful texts/quotes) for a specific category.
You will be given a category, a list of subtopics, a desired style, and optionally some context from the web (Tavily search results).

Guidelines:
1. **Content**: 
   - Each vibe must be 1-2 sentences max.
   - Deep, impactful, and clear.
   - Avoid clichés.
   - If the category is 'Tech News' or based on web context, summarize the insight keenly.
2. **Style**: Follow the requested style (e.g., Stoic, Witty, Professional).
3. **Context Usage**: If 'Context (Web Search Results)' is provided, you MUST use it to generate relevant and up-to-date vibes. If no context is provided, rely on your internal knowledge base.
4. **Subtopics**: Ensure the generated vibes cover a diverse range of the provided subtopics.
5. **Format**: You must output a JSON object containing a list of candidates.
"""

# The user message template
USER_TEMPLATE = """
Generate {count} unique vibes for the following parameters:

**Category**: {category}
**Subtopics**: {subtopics}
**Style**: {style}

**Context (Web Search Results)**:
{tavily_context}

**Output Format**:
Return a valid JSON object with a key "candidates". "candidates" should be a list of objects, where each object has:
- "content": The vibe text (string).
- "subtopic": The specific subtopic this vibe relates to (string).
- "metadata": A dictionary with keys like "source_url" (if applicable) or "inspiration".

Example Output:
{{
  "candidates": [
    {{
      "content": [Write a quote here],
      "subtopic": [subtopic here],
      "metadata": {{ "inspiration": [inspiration here]  
      "source_url": [source_url here] }}
    }},
    {{
      "content": [Write a quote here],
      "subtopic": [subtopic here],
      "metadata": {{ "inspiration": [inspiration here]  
      "source_url": [source_url here] }}
    }},
    ...
  ]
}}
"""

def get_generation_prompt() -> ChatPromptTemplate:
    """
    Returns the ChatPromptTemplate for vibe generation.
    This allows easy versioning or modification of the prompt structure.
    """
    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_INSTRUCTION),
        ("human", USER_TEMPLATE),
    ])

