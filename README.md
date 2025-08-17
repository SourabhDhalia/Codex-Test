# Codex-Test

This repository contains a simple harness for evaluating [OpenAI Codex](https://openai.com/blog/openai-codex) on small programming tasks.

## Running the harness

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set your OpenAI API key in the environment:

   ```bash
   export OPENAI_API_KEY="your-api-key"
   ```

3. Execute the script:

   ```bash
   python codex_harness.py
   ```

   Use `--dry-run` to skip the API call and simply display the tasks:

   ```bash
   python codex_harness.py --dry-run
   ```

The script will prompt Codex to implement several small functions and verify the generated code against unit tests.
