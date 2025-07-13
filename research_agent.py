import os
from typing import List, Dict
from openai import OpenAI
from judgeval.tracer import Tracer, wrap
from judgeval.scorers import (
    AnswerRelevancyScorer, 
    FaithfulnessScorer, 
)
from judgeval.data import Example
from judgeval import JudgmentClient
from dotenv import load_dotenv

load_dotenv()

# Initialize wrapped OpenAI client for automatic LLM tracing
client = wrap(OpenAI())

# Initialize Judgment tracer
judgment = Tracer(project_name="research_assistant_agent")

class ResearchAgent:
    def __init__(self):
        self.tools = {
            "web_search": self.web_search_simulation,
            "summarize": self.summarize_content,
            "fact_check": self.fact_check
        }
    
    @judgment.observe(span_type="tool")
    def web_search_simulation(self, query: str) -> Dict:
        """Simulated web search tool"""
        # In a real implementation, this would call an actual search API
        mock_results = {
            "query": query,
            "results": [
                {
                    "title": f"Research on {query}",
                    "snippet": f"Comprehensive information about {query} including key findings and methodologies.",
                    "url": f"https://example.com/research/{query.replace(' ', '-')}"
                }
            ]
        }
        return mock_results
    
    @judgment.observe(span_type="tool")
    def summarize_content(self, content: str) -> str:
        """Summarize provided content"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a precise summarization assistant. Provide concise, accurate summaries."},
                {"role": "user", "content": f"Summarize the following content:\n\n{content}"}
            ]
        )
        return response.choices[0].message.content
    
    @judgment.observe(span_type="tool")
    def fact_check(self, claim: str, context: str) -> Dict:
        """Fact-check a claim against provided context"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a fact-checking assistant. Verify claims against context and respond with 'VERIFIED', 'UNVERIFIED', or 'CONTRADICTED' plus explanation."},
                {"role": "user", "content": f"Claim: {claim}\nContext: {context}\nVerification:"}
            ]
        )
        return {
            "claim": claim,
            "verification": response.choices[0].message.content,
            "context_used": context
        }
    
    @judgment.observe(span_type="function")
    def research_topic(self, topic: str, depth: str = "basic") -> Dict:
        """Main research function"""
        # Step 1: Search for information
        search_results = self.web_search_simulation(topic)
        
        # Step 2: Summarize findings
        content_to_summarize = f"Topic: {topic}\nResults: {search_results['results']}"
        summary = self.summarize_content(content_to_summarize)
        
        # Step 3: Generate comprehensive response
        research_prompt = f"""
        Research Topic: {topic}
        Search Results: {search_results}
        Summary: {summary}
        Depth: {depth}
        
        Provide a comprehensive research report including:
        1. Key findings
        2. Important insights
        3. Potential implications
        4. Areas for further research
        """
        
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert research assistant. Provide thorough, well-structured research reports."},
                {"role": "user", "content": research_prompt}
            ]
        )
        
        result = {
            "topic": topic,
            "search_results": search_results,
            "summary": summary,
            "research_report": final_response.choices[0].message.content,
            "depth": depth
        }
        
        # Online evaluation
        example = Example(
            input=topic,
            actual_output=result["research_report"],
            retrieval_context=[str(search_results), summary]
        )
        
        judgment.async_evaluate(
            scorers=[
                AnswerRelevancyScorer(threshold=0.7),
                FaithfulnessScorer(threshold=0.8)
            ],
            example=example,
            model="gpt-4"
        )
        
        return result

def main():
    agent = ResearchAgent()
    
    # Example research queries
    topics = [
        "artificial intelligence ethics",
        "climate change mitigation strategies",
        "quantum computing applications"
    ]
    
    for topic in topics:
        print(f"\n{'='*50}")
        print(f"Researching: {topic}")
        print('='*50)
        
        result = agent.research_topic(topic, depth="comprehensive")
        print(f"Research Report:\n{result['research_report'][:500]}...")

if __name__ == "__main__":
    main()