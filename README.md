# Legal Text Simplifier

This project fine-tunes BART-base to turn legal text into short, plain-English summaries.

The main goal is to test whether common simplification metrics such as SARI and readability give different results from a faithfulness metric such as SummaC.

> *Universität Heidelberg* · Author: *Chuqiao Li*


## Research question

Do standard simplification and summarization metrics (SARI, readability) rank systems differently from faithfulness measures (SummaC) on legal text?

## Approach

The project uses two training stages:

1. I rewrote CUAD contract clauses into plain English using Llama 3.1 8B. I filtered the generated data using SummaC and readability scores.
2. Then I trained a BART-based model (with the knowledge of the English language already trained) on the synthetic data
3. Then in Stage 2: I fine-tuned BART on human-written ToS;DR summaries
4. I trained a second BART model only on stage 2 data.
4. I used Claude Haiku 4.5 as a prompted baseline.
5. I tested the models on ToS;DR data and on a separate set of CUAD contract clauses.
6. I evaluated the performance of the models with the metrics of readability and faithfulness

The main metrics are SARI, Flesch-Kincaid readability, and SummaC faithfulness. Wilcoxon tests with Bonferroni correction were used for statistical comparisons.


## Results

| System            | SARI | ToS;DR SummaC | CUAD SummaC | CUAD readability |  
| BART stage 2 only | 50.5 | 0.062         | -0.003      | 15.1             |  
| BART two-stage    | 51.5 | 0.225         | 0.462       | 13.4             |  
| Claude Haiku 4.5  | 41.0 | 0.312         | 0.704       | 10.3             |  

more results are in the results folder (Graphs and tables)

Some main findings:

- On the CUAD test set, the systems that were easier to read tended to lack inn faithfulness
- SARI did not distinguish between the two BART models (`p = 0.73`).
- SummaC showed a difference between the two BART models (`p = 0.005`).
- The two-stage BART model had fewer unsupported outputs on the CUAD probe: 30% compared with 68% for the stage-2-only model.

---

## Reproducing the project

### Requirements

- Python 3.12
- A decent GPU
- Ollama with Llama 3.1 8B for synthetic data generation
- Anthropic API key for the Claude baseline

sudo apt install python3.12-dev build-essential

Seeds:
- All splits and samples use random_state=1.
- Synthetic generation: Llama 3.1 8B at temperature=0.
- Baseline: claude-haiku-4-5-20251001 at temperature=0

pipeline:

1. Prepare the ToS;DR data
    Clean the data and create the train/test split.

2. Prepare the CUAD data
    Extract and clean contract clauses.

3. Split the CUAD data
    Create the data used for synthetic generation and the separate test set.

4. Test the filters
    Check the SummaC and readability filters.

5. Generate synthetic data
    Use Llama 3.1 8B to rewrite the clauses.

6. Filter the synthetic data
    Cut the rewrites that don't meet filtering criteria

7. Train the BART models
    Train the two-stage model and the stage-2-only model.

8. Generate BART outputs
    Test both BART models on the test sets.

9. Generate Claude outputs
    Use Claude Haiku 4.5 as the baseline.

10. Calculate the metrics
    Measure readability, faithfulness, length, and SARI.


## File structure

- README.md
- requirements.txt      pinned library versions
- .env.example          template for the API key
- data/                 all data used for training
- src/
 -- faithfulness_filter.py   SummaC forward/reverse scores
 -- readability_filter.py    Flesch-Kincaid readability drop
- notebooks/                    pipeline 1-10 
- results/              scores, outputs, prompts, figures
- models/               trained models (not in git)
