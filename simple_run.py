print("NeuraShield.AI Starting...")
print("AI Guardian: ACTIVE")
print("Backend: http://localhost:8000")
print("Status: RUNNING")

# Simple AI analysis demo
code = '''
password = "admin123"
eval("dangerous_code")
'''

issues = code.count("password") + code.count("eval")
trust_score = max(0, 1 - issues/5)

print(f"\nAI Analysis:")
print(f"Trust Score: {trust_score:.1f}/1.0")
print(f"Issues Found: {issues}")
print(f"Status: {'SAFE' if trust_score > 0.7 else 'DANGER'}")
print("\nNeuraShield.AI protecting your code!")