"""
Test various integration patterns and identify gaps
"""
import asyncio
from judgeval.tracer import Tracer

# Test async tracing
async def test_async_tracing():
    judgment = Tracer(project_name="async_test")
    
    @judgment.observe(span_type="async_tool")
    async def async_operation():
        await asyncio.sleep(0.1)
        return "async result"
    
    try:
        result = await async_operation()
        print("✅ Async tracing works")
        return result
    except Exception as e:
        print(f"❌ Async tracing failed: {e}")
        return None

# Test custom scorer integration with correct import path
def test_custom_scorer():
    """Test if custom scorers work as expected"""
    try:
        # Try the documented import path first
        from judgeval.scorers.base import BaseScorer
        print("✅ judgeval.scorers.base import works")
    except ImportError:
        try:
            # Try alternative import paths
            from judgeval.scorers import BaseScorer
            print("✅ judgeval.scorers.BaseScorer import works")
        except ImportError:
            try:
                # Try finding BaseScorer in the main scorers module
                import judgeval.scorers as scorers
                BaseScorer = getattr(scorers, 'BaseScorer', None)
                if BaseScorer:
                    print("✅ Found BaseScorer in main scorers module")
                else:
                    print("❌ BaseScorer not found anywhere")
                    return False
            except Exception as e:
                print(f"❌ Custom scorer import issue: {e}")
                return False
    
    # Try to create a custom scorer
    try:
        class CustomQualityScorer(BaseScorer):
            def __init__(self, threshold: float = 0.5):
                super().__init__(threshold=threshold)
            
            def score(self, input_text: str, output_text: str, **kwargs) -> float:
                # Custom scoring logic
                return 0.8
        
        # Try to instantiate it
        scorer = CustomQualityScorer(threshold=0.7)
        print("✅ Custom scorer creation and instantiation works")
        return True
        
    except Exception as e:
        print(f"❌ Custom scorer creation failed: {e}")
        return False

# Test error handling
def test_error_scenarios():
    """Test how the system handles various error scenarios"""
    judgment = Tracer(project_name="error_test")
    
    @judgment.observe(span_type="error_prone")
    def failing_function():
        raise ValueError("Intentional test error")
    
    try:
        failing_function()
        print("❌ Error should have been raised")
        return False
    except ValueError:
        print("✅ Error handling in tracing works - error was properly raised")
        return True
    except Exception as e:
        print(f"❌ Unexpected error handling behavior: {e}")
        return False

def test_available_imports():
    """Test what's actually available for import"""
    print("\n🔍 Testing Available Imports:")
    print("-" * 40)
    
    # Test tracer imports
    try:
        from judgeval.tracer import Tracer, wrap
        print("✅ Tracer and wrap")
    except ImportError as e:
        print(f"❌ Tracer imports: {e}")
    
    # Test client imports
    try:
        from judgeval import JudgmentClient
        print("✅ JudgmentClient")
    except ImportError as e:
        print(f"❌ JudgmentClient: {e}")
    
    # Test data imports
    try:
        from judgeval.data import Example
        print("✅ Example")
    except ImportError as e:
        print(f"❌ Example: {e}")
    
    # Test scorer base class locations
    base_locations = [
        "judgeval.scorers.base.BaseScorer",
        "judgeval.scorers.BaseScorer", 
        "judgeval.BaseScorer"
    ]
    
    print("\n📍 Looking for BaseScorer:")
    for location in base_locations:
        try:
            module_path, class_name = location.rsplit('.', 1)
            exec(f"from {module_path} import {class_name}")
            print(f"✅ Found at: {location}")
            break
        except ImportError:
            print(f"❌ Not at: {location}")

async def main():
    print("🧪 Testing Judgment Integration Patterns")
    print("="*50)
    
    # Test 1: Async tracing
    print("\n1️⃣ Testing Async Tracing:")
    await test_async_tracing()
    
    # Test 2: Available imports
    print("\n2️⃣ Testing Available Imports:")
    test_available_imports()
    
    # Test 3: Custom scorer creation
    print("\n3️⃣ Testing Custom Scorer Creation:")
    custom_success = test_custom_scorer()
    
    # Test 4: Error handling
    print("\n4️⃣ Testing Error Handling:")
    error_success = test_error_scenarios()
    
    print(f"\n📊 Results Summary:")
    print(f"Custom Scorers: {'✅ Working' if custom_success else '❌ Broken'}")
    print(f"Error Handling: {'✅ Working' if error_success else '❌ Broken'}")

if __name__ == "__main__":
    asyncio.run(main())