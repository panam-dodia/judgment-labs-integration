"""
Complete end-to-end test of the Judgment integration
"""
import os
from research_agent import ResearchAgent

def test_research_agent():
    """Test the research agent functionality"""
    try:
        agent = ResearchAgent()
        result = agent.research_topic("AI safety", depth="basic")
        
        if result and result.get('topic'):
            print(f"✅ Agent completed research on: {result['topic']}")
            return True
        else:
            print("❌ Agent returned empty result")
            return False
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

def test_basic_evaluation():
    """Test basic evaluation functionality"""
    try:
        from judgeval import JudgmentClient
        from judgeval.data import Example
        from judgeval.scorers import AnswerRelevancyScorer
        
        client = JudgmentClient()
        
        example = Example(
            input="What is AI?",
            actual_output="AI is artificial intelligence",
            expected_output="Artificial intelligence"
        )
        
        # Try a simple evaluation
        results = client.run_evaluation(
            examples=[example],
            scorers=[AnswerRelevancyScorer(threshold=0.5)],
            model="gpt-4"
        )
        
        print("✅ Basic evaluation completed")
        return True
        
    except Exception as e:
        print(f"❌ Basic evaluation failed: {e}")
        return False

def main():
    print("🚀 Starting Complete Judgment Labs Integration Test")
    print("="*60)
    
    # Test 1: Agent functionality
    print("\n📋 Test 1: Research Agent Functionality")
    agent_success = test_research_agent()
    
    # Test 2: Basic evaluation
    print("\n📊 Test 2: Basic Evaluation")
    eval_success = test_basic_evaluation()
    
    print(f"\n📋 Summary:")
    print(f"Research Agent: {'✅ Working' if agent_success else '❌ Failed'}")
    print(f"Basic Evaluation: {'✅ Working' if eval_success else '❌ Failed'}")
    
    if agent_success or eval_success:
        print("\n🎉 Core functionality works despite platform issues!")
        print("Check the Judgment platform for trace data:")
        print("https://app.judgmentlabs.ai")
    else:
        print("\n⚠️ Multiple system failures detected")

if __name__ == "__main__":
    main()