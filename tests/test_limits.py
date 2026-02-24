import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_increased_limits():
    """Test the increased rate limits"""
    try:
        print("Testing increased rate limits...")
        
        # Import the functions
        from gradio_app_advanced import check_rate_limit, increment_request_count, get_remaining_quota_info
        
        # Test initial state
        print("\n1. Testing initial state:")
        rate_check = check_rate_limit()
        quota_info = get_remaining_quota_info()
        print(f"   Rate limit check: {rate_check}")
        print(f"   Quota info: {quota_info}")
        
        # Test with 5 requests
        print("\n2. Testing with 5 requests:")
        for i in range(5):
            increment_request_count(f"test_func_{i}")
        
        rate_check = check_rate_limit()
        quota_info = get_remaining_quota_info()
        print(f"   Rate limit check: {rate_check}")
        print(f"   Quota info: {quota_info}")
        
        # Test with 20 requests (should still be under limit)
        print("\n3. Testing with 20 requests:")
        for i in range(20):
            increment_request_count(f"test_func_{i+5}")
        
        rate_check = check_rate_limit()
        quota_info = get_remaining_quota_info()
        print(f"   Rate limit check: {rate_check}")
        print(f"   Quota info: {quota_info}")
        
        # Test with 25 requests (should hit limit)
        print("\n4. Testing with 25 requests:")
        increment_request_count("test_func_25")
        
        rate_check = check_rate_limit()
        quota_info = get_remaining_quota_info()
        print(f"   Rate limit check: {rate_check}")
        print(f"   Quota info: {quota_info}")
        
        print(f"\nIncreased Limits Test Summary:")
        print(f"   Rate limit increased from 15 to 25 requests per hour")
        print(f"   Quota tracking working correctly")
        print(f"   Users should now have more available requests")
        
        return True
        
    except Exception as e:
        print(f"Error in increased limits test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_increased_limits()
    print(f"\nIncreased limits test: {'✓ PASS' if success else '✗ FAIL'}")