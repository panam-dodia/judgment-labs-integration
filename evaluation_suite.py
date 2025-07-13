from judgeval import JudgmentClient
from judgeval.data import Example
from judgeval.scorers import (
    AnswerCorrectnessScorer,
    AnswerRelevancyScorer,
    FaithfulnessScorer,
    InstructionAdherenceScorer,
    # Using only confirmed working scorers
)

def test_working_evaluation():
    """Test evaluation with only working scorers"""
    client = JudgmentClient()
    
    example = Example(
        input="What are the benefits of renewable energy?",
        actual_output="Renewable energy reduces greenhouse gas emissions, creates jobs, and provides energy independence.",
        expected_output="Benefits include environmental protection and economic advantages.",
        retrieval_context=["Renewable energy sources produce minimal emissions compared to fossil fuels."]
    )
    
    working_scorers = [
        AnswerCorrectnessScorer(threshold=0.5),
        AnswerRelevancyScorer(threshold=0.5),
        FaithfulnessScorer(threshold=0.5),
        InstructionAdherenceScorer(threshold=0.5),
    ]
    
    try:
        print("🧪 Testing evaluation with working scorers...")
        results = client.run_evaluation(
            examples=[example],
            scorers=working_scorers,
            model="gpt-4"
            # eval_name="working_scorers_test"  # This parameter doesn't exist!
        )
        
        print("✅ Evaluation completed successfully!")
        print("\n📊 Results:")
        for metric, score in results.items():
            print(f"  {metric}: {score}")
        
        return True, results
        
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        return False, None

def test_unit_testing():
    """Test assert_test functionality"""
    client = JudgmentClient()
    
    example = Example(
        input="What is 2+2?",
        actual_output="2+2 equals 4",
        expected_output="4"
    )
    
    try:
        print("\n🧪 Testing unit test functionality...")
        client.assert_test(
            examples=[example],
            scorers=[AnswerCorrectnessScorer(threshold=0.3)],  # Low threshold for simple test
            model="gpt-4"
        )
        print("✅ Unit test passed!")
        return True
    except Exception as e:
        print(f"❌ Unit test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Working Judgment Evaluation Features")
    print("=" * 60)
    
    # Test evaluation
    eval_success, results = test_working_evaluation()
    
    # Test unit testing
    unit_success = test_unit_testing()
    
    print(f"\n📋 Summary:")
    print(f"Evaluation functionality: {'✅ Working' if eval_success else '❌ Broken'}")
    print(f"Unit test functionality: {'✅ Working' if unit_success else '❌ Broken'}")