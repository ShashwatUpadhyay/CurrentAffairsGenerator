from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    max_retries=2
)

prompt_template = PromptTemplate(template= """
You are an expert question setter for competitive exams.

TASK:
Based ONLY on the given context, generate {num_questions} multiple-choice questions (MCQs).

CONTEXT:
============================
{context}
============================

RULES:
- Questions must be strictly derived from the context.
- Do NOT use outside knowledge.
- Questions should test factual understanding.
- Avoid trivial or opinion-based questions.
- Each question must have exactly 4 options: A, B, C, D.
- Only ONE option must be correct.
- Options should be plausible and non-overlapping.

OUTPUT FORMAT:
Return the result as a JSON array.
Each element must follow this exact structure:

[
  {{
    "question": "Question text here",
    "A": "Option A text",
    "B": "Option B text",
    "C": "Option C text",
    "D": "Option D text",
    "correct": "A"
  }}
]

IMPORTANT:
- The "correct" field must contain ONLY one of: "A", "B", "C", or "D".
- Do NOT add explanations.
- Do NOT add any text outside the JSON array.
""", input_variables=['context', 'num_questions'])

parser = JsonOutputParser()

chain = prompt_template | llm | parser

def generate_mcqs(context, num_questions=5):
    """
    Generate UPSC & BPSC style Current Affairs MCQs based on the given news article.
    
    Args:
        context (str): The text content of the news article to generate MCQs from.
        num_questions (int): The number of MCQs to generate.
        
    Returns:
        list: A list of dictionaries, where each dictionary represents an MCQ.
    """
    try:
        response = chain.invoke({
            'context': context,
            'num_questions': num_questions
        })
        return response
    except Exception as e:
        print(f"Error generating MCQs: {str(e)}")
        return []

if __name__ == "__main__":
    test_context = """
    The Reserve Bank of India (RBI) has kept the repo rate unchanged at 6.5% for the seventh consecutive time.
    This decision was announced by RBI Governor Shaktikanta Das on February 8, 2024.
    The Monetary Policy Committee (MPC) voted 5-1 in favor of maintaining the status quo.
    The repo rate is the interest rate at which the RBI lends money to commercial banks.
    The central bank also revised its GDP growth forecast for the fiscal year 2024-25 to 7.0% from the earlier 6.5%.
    Inflation projections were revised slightly upwards to 5.4% for the same period.
    """
    
    mcqs = generate_mcqs(test_context, num_questions=5)
    
    if mcqs:
        print("Generated MCQs:")
        for i, mcq in enumerate(mcqs, 1):
            print(f"\n{i}. {mcq['question']}")
            print(f"   A. {mcq['A']}")
            print(f"   B. {mcq['B']}")
            print(f"   C. {mcq['C']}")
            print(f"   D. {mcq['D']}")
            print(f"   Correct: {mcq['correct']}")
    else:
        print("Failed to generate MCQs.")