import asyncio
import json
from datetime import datetime
from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# Adjust python path if running as script
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.core.prompts import get_generation_prompt
from app.core.category_informations import CATEGORY_INFOS
from app.schemas.quote import QuoteCategory

class VibeCandidate(BaseModel):
    content: str
    subtopic: str
    metadata: dict = Field(default_factory=dict)

class VibeResponse(BaseModel):
    candidates: List[VibeCandidate]

async def generate_category_vibes(
    category: QuoteCategory, 
    subtopics: List[str], 
    style: str, 
    tavily_query: str,
    count: int = 3,
) -> List[VibeCandidate]:
    print(f"\n=== [{datetime.now().strftime('%H:%M:%S')}] Generating vibes for {category.value.upper()} ===")
    
    # Initialize LLM
    # Using gpt-4o or gpt-3.5-turbo depending on budget/availability
    llm = ChatOpenAI(
        model="gpt-4o", 
        api_key=settings.openai_api_key, 
        temperature=0.7
    )
    
    # Get Prompt
    prompt = get_generation_prompt()
    
    # Output Parser
    parser = JsonOutputParser(pydantic_object=VibeResponse)
    
    # Chain
    chain = prompt | llm | parser
    
    # Context from Tavily (Simulated or Real)
    tavily_context = ""
    if settings.tavily_api_key:
        try:
            # Simple Tavily integration if needed
            from langchain_community.tools.tavily_search import TavilySearchResults
            tool = TavilySearchResults(
                tavily_api_key=settings.tavily_api_key,
                max_results=10,
                exclude_domains=["https://www.youtube.com"]
            )
            print(f"  -> [{datetime.now().strftime('%H:%M:%S')}] Starting Tavily search for query: '{tavily_query}'...")
            results = tool.invoke({"query": tavily_query})
            tavily_context = json.dumps(results, indent=2)
            print(f"  -> [{datetime.now().strftime('%H:%M:%S')}] Fetched {len(results)} context items from Tavily.")
        except Exception as e:
            print(f"  -> [{datetime.now().strftime('%H:%M:%S')}] Tavily search failed: {e}")
            tavily_context = "No external context available (Search Failed)."
    else:
        tavily_context = "No external context available (Missing API Key)."

    try:
        # Invoke Chain
        print(f"  -> [{datetime.now().strftime('%H:%M:%S')}] Invoking LLM chain (generating {count} vibes)...")
        response = await chain.ainvoke({
            "count": count,
            "category": category.value,
            "subtopics": ", ".join(subtopics),
            "style": style,
            "tavily_context": tavily_context
        })
        print(f"  -> [{datetime.now().strftime('%H:%M:%S')}] LLM generation completed.")
        
        # Display Results
        candidates = response.get("candidates", [])
        print(f"  -> Generated {len(candidates)} candidates:\n")
        for i, v in enumerate(candidates, 1):
            print(f"  {i}. [{v.get('subtopic')}]")
            print(f"     \"{v.get('content')}\"")
            print(f"     Metadata: {v.get('metadata')}\n")
        
        return [VibeCandidate(**c) for c in candidates]
            
    except Exception as e:
        print(f"Error generating for {category.value}: {e}")
        return []

async def main():
    all_vibes = {}
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"generated_vibes_{timestamp}.json"

    # Loop through all categories defined in CATEGORY_INFOS
    for category, info in CATEGORY_INFOS.items():
        vibes = await generate_category_vibes(
            category=category,
            subtopics=info["subtopics"],
            style=info["style"],
            count=20,
            tavily_query=info["tavily_query"]
        )
        all_vibes[category.value] = [v.model_dump() for v in vibes]

    # Write to file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_vibes, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ All generated vibes saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())

