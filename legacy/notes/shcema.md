## normalized schema
# {
#     # identity
#     "task_id": str,
#     "dataset": str,          # "mbpp" | "humaneval" | "apps" | "lcb"
#     "split": str | None,

#     # generation
#     "prompt": str,           # raw problem prompt used to build model prompt
#     "prompt_type": str,      # "function_completion" | "stdin_stdout"
#     "entry_point": str | None,

#     # reference
#     "reference_code": str | None,
#     "reference_solutions": list[str],

#     # evaluation
#     "tests": object,         # dataset-specific test object
#     "test_type": str,        # "assertion" | "stdin_stdout"

#     # optional but useful
#     "difficulty": str | None,
#     "source_url": str | None,
#     "metadata": dict,
# }


## APPS

# [problem_id]

# [question]

# [solutions]

# [input_output]

# [difficulty]

# [url]

# [starter_code]


## mbpp

# [task_id]

# [text]

# [code]

# [test_list]

# [test_setup_code]

# [challenge_test_list]


## Human Eval

# [task_id]

# [prompt]

# [canonical_solution]

# [test]

# [entry_point]



## LCB

# [question_title]

# [question_content]

# [platform]

# [question_id]

# [contest_id]

# [contest_date]

# [starter_code]

# [difficulty]

# [public_test_cases]

# [private_test_cases]

# [metadata]



