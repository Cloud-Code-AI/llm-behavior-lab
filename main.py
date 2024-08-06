from kaizen.llms.provider import LLMProvider
from simple_tasks import *
import json


def run_test(test_func, provider=None, attempts=5):
    results = []
    prompt = ""
    for _ in range(attempts):
        try:
            state, response, usage, prompt = test_func(provider)
            output = {
                "input": test_func.__name__,
                "output": "Test passed",
                "usage": dict(usage),
                "llm_resp": response,
            }
            if state:
                output["status"] = "passed"
            else:
                output["status"] = "failed"
            results.append(output)
        except AssertionError as e:
            results.append(
                {"status": "failed", "input": test_func.__name__, "output": str(e)}
            )
        except Exception as e:
            results.append(
                {"status": "error", "input": test_func.__name__, "output": str(e)}
            )
    return results, prompt


def aggregate_results(results):
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "passed")
    failed = sum(1 for r in results if r["status"] == "failed")
    errors = sum(1 for r in results if r["status"] == "error")
    return {
        "total_attempts": total,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "success_rate": passed / total if total > 0 else 0,
    }


# List of all test functions
test_functions = [
    test_no_letter_e,
    test_haiku_format,
    test_no_names,
    test_grumpy_persona,
    test_alliteration,
    test_increasing_word_length,
    test_palindrome,
    test_acronym,
    test_rhyme_scheme,
    test_word_frequency,
    test_line_count,
    test_word_count_per_line,
    test_alphabetical_words,
    test_alternating_capitalization,
    test_fibonacci_word_lengths,
    test_progressive_letter_exclusion,
]

# Set the llm provider
model = "azure/gpt-4o-mini"
provider = LLMProvider()
# Run all tests and store results
all_results = {}
for test_func in test_functions:
    attempts, prompt = run_test(test_func, provider=provider, attempts=3)
    all_results[test_func.__name__] = {
        "attempts": attempts,
        "aggregate": aggregate_results(attempts),
        "prompt": prompt
    }

# Write results to JSON file
with open(f"{model}/test_results.json", "w") as f:
    json.dump(all_results, f, indent=2)

print("All tests completed. Results stored in 'test_results.json'.")
