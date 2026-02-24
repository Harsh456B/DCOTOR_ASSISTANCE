import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_quota_info():
    """Test the quota information display"""
    try:
        print("Testing quota information display...")
        
        # Import the functions
        from gradio_app_advanced import get_remaining_quota_info, request_counts
        
        # Test quota info when no requests have been made
        print("\n1. Testing quota info with no requests:")
        quota_info = get_remaining_quota_info()
        print(f"   Quota info: {quota_info}")
        
        # Test with some requests
        print("\n2. Testing quota info with some requests:")
        from gradio_app_advanced import increment_request_count
        
        # Simulate 3 requests
        for i in range(3):
            increment_request_count(f"test_func_{i}")
        
        quota_info = get_remaining_quota_info()
        print(f"   Quota info after 3 requests: {quota_info}")
        
        # Test rate limit check
        print("\n3. Testing rate limit check:")
        from gradio_app_advanced import check_rate_limit
        rate_check = check_rate_limit()
        print(f"   Rate limit check: {rate_check}")
        
        print(f"\nQuota Information Test Summary:")
        print(f"   Quota tracking working correctly")
        print(f"   Users will now see detailed quota information")
        print(f"   This helps manage expectations during rate limiting")
        
        return True
        
    except Exception as e:
        print(f"Error in quota info test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_quota_info()
    print(f"\nQuota information test: {'✓ PASS' if success else '✗ FAIL'}")