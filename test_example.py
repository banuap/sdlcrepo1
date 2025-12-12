"""
Simple test file for test issue
This demonstrates the SDLC workflow is functioning correctly.
"""

def test_basic():
    """A basic test to verify the setup works"""
    assert True, "Basic test should always pass"

def test_addition():
    """Test basic arithmetic"""
    assert 1 + 1 == 2, "Math should work correctly"

if __name__ == "__main__":
    try:
        test_basic()
        test_addition()
        print("All tests passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
        exit(1)
