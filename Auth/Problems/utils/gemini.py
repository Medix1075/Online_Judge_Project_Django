import google.generativeai as genai
# from django.conf import settings
from decouple import config

# Configure the Gemini API key
import os
print("ENV VAR DEBUG:", os.path.exists('.env'))
print("GEMINI_API_KEY:", config("GEMINI_API_KEY", default="Not Found"))
GEMINI_API_KEY = config("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


def generate_hint(problem):
    prompt = f"""
    You are an expert DSA teacher. Provide a helpful hint for solving the following problem (without revealing the full solution).

    Title: {problem.title}
    Difficulty: {problem.difficulty}
    Description: {problem.description}
    Input: {problem.Input}
    Output: {problem.Output}
    Constraints: {problem.constraints}
    """

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()


def analyze_code(problem, code):
    prompt = f"""
    You are a programming mentor. Analyze the following solution for the coding problem.

    Problem Title: {problem.title}
    Description: {problem.description}

    Code:
    {code}

    Provide feedback on:
    - Logic correctness
    - Time and space complexity
    - Edge case handling
    - Improvements (if any)
    """

    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    return response.text.strip()
