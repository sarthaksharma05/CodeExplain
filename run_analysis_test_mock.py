import json
from core.agent import CodeExplainAgent

# Mock client that returns a valid JSON string but with quiz as an object
class MockClient:
    def __init__(self):
        pass
    def send_prompt(self, system_prompt: str, user_prompt: str) -> str:
        resp = {
            "detected_language": "Python",
            "summary": "Computes factorial of n recursively.",
            "time_complexity": {"value": "O(n)", "explanation": "Recurses n times."},
            "space_complexity": {"value": "O(n)", "explanation": "Call stack."},
            "line_by_line": [
                {"line_number": 1, "code": "def factorial(n):", "explanation": "Defines function."},
                {"line_number": 2, "code": "    if n <= 1:", "explanation": "Base case check."},
            ],
            "improvements": ["Add memoization"],
            # NOTE: quiz is an object here (incorrect per new final contract)
            "quiz": {
                "question": "What is factorial of 0?",
                "options": ["0", "1", "Undefined"],
                "correct_answer": "1",
                "explanation": "By definition, 0! = 1"
            }
        }
        return json.dumps(resp)

agent = CodeExplainAgent(client=MockClient())
code = '''def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
'''
result = agent.analyze_code(code=code, language='English', difficulty='Beginner')
print('Result quiz type:', type(result.get('quiz')))
print('Quiz length:', len(result.get('quiz')))
print('Quiz item keys:', list(result.get('quiz')[0].keys()))
print('\nFull result keys:', list(result.keys()))
