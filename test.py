import requests
import json

def test_tts_api():
    """Test the Google AI Studio TTS API"""
    url = "http://localhost:8000/tts"
    
    # Test 1: Basic request
    print("Test 1: Basic TTS request")
    data = {
        "text": "Hello this is a test",
        "voice_name": "Kore"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Test 1 PASSED: Basic TTS request successful")
        else:
            print(f"❌ Test 1 FAILED: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test 1 ERROR: {str(e)}")
    
    print("\n" + "="*50)
    
    # Test 2: Request with different voice
    print("Test 2: TTS request with different voice")
    data = {
        "text": "Testing with different voice",
        "voice_name": "Puck"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Test 2 PASSED: Different voice request successful")
        else:
            print(f"❌ Test 2 FAILED: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test 2 ERROR: {str(e)}")
    
    print("\n" + "="*50)
    
    # Test 3: Request without voice name (should use default)
    print("Test 3: TTS request without voice name")
    data = {
        "text": "Testing default voice"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Test 3 PASSED: Default voice request successful")
        else:
            print(f"❌ Test 3 FAILED: Status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Test 3 ERROR: {str(e)}")
    
    print("\n" + "="*50)
    
    # Test 4: Empty text (should fail)
    print("Test 4: Empty text request")
    data = {
        "text": ""
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("⚠️ Test 4 UNEXPECTED: Empty text should not succeed")
        else:
            print("✅ Test 4 PASSED: Empty text correctly failed")
            
    except Exception as e:
        print(f"❌ Test 4 ERROR: {str(e)}")
    
    print("\n" + "="*50)
    print("Testing completed!")

if __name__ == "__main__":
    test_tts_api()
