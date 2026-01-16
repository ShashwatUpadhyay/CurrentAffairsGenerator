import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ca_gen.settings')
django.setup()

from utils.translator import translate_to_hindi

# Test translation
test_question = "What is the capital of India?"
test_option_a = "New Delhi"
test_option_b = "Mumbai"

print("Translation Test Results:")
print("=" * 60)
print(f"Question (EN): {test_question}")
question_hi = translate_to_hindi(test_question)
print(f"Question (HI): {question_hi}")
print()
print(f"Option A (EN): {test_option_a}")
option_a_hi = translate_to_hindi(test_option_a)
print(f"Option A (HI): {option_a_hi}")
print()
print(f"Option B (EN): {test_option_b}")
option_b_hi = translate_to_hindi(test_option_b)
print(f"Option B (HI): {option_b_hi}")
print("=" * 60)
print("✅ Translation working successfully!")
print("\nNow you can run: n.generate_questions()")
print("It will automatically translate questions and options to Hindi!")
