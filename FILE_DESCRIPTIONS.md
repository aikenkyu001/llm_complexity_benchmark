# File Descriptions

This document provides a detailed overview of the directory structure and file functions within the LLM Complexity Benchmark project.

## Root Directory

- **README.md**: The main documentation file providing project overview, "Absolute Discipline" methodology, architecture, and key results.
- **requirements.txt**: List of Python dependencies required to run the scripts and training pipeline.
- **FILE_DESCRIPTIONS.md**: This file, providing a map of the project's components.

## 01_TestDefinitions/

This directory contains the core benchmark suite, organized by algorithmic complexity and specific constraints. Each subdirectory typically includes:
- **problem.nl**: Natural language description of the problem.
- **solution.py**: The gold standard (reference) implementation.
- **test_solution.py**: Unit tests used to validate LLM-generated code.

### Categories include:
- **Algorithmic Tasks**: `dijkstra_shortest_path`, `lru_cache`, `sudoku_solver`, `merge_sort_in_place`, etc.
- **Synthetic Complexity**: `synthetic_constraints_n*`, `synthetic_nesting_d*`, `synthetic_context_v*` (used for stress-testing LLMs on specific structural metrics).

## 02_Prompts/

Contains prompt templates used in the multi-stage conversion pipeline.
- **nl_to_lisp.prompt**: Template for converting natural language requirements into an intermediate LISP-like structural representation.
- **lisp_to_code.prompt**: Template for generating finalized Python code from the LISP intermediate representation.

## 03_Scripts/

The engine of the project, containing scripts for data generation, analysis, training, and execution.

### Analysis & Visualization
- **complexity_analyzer.py**: Calculates structural metrics (Cyclomatic complexity, recursion depth, state space size) of problems.
- **aggregate_results.py**: Consolidates raw benchmark data into CSV and JSON summaries.
- **visualizer.py**: Generates charts like the capability radar and complexity-vs-success plots.
- **reanalyze_results.py**: Performs post-hoc analysis on experimental data.

### Data Generation
- **generate_absolute_discipline_data.py**: Creates SFT datasets focused on rigid coding standards and class-based structure.
- **generate_hyper_faithful_data.py / v2**: Generates datasets to enforce strict adherence to logic specifications.
- **generate_synthetic_tasks.py**: Procedurally generates synthetic benchmark cases.
- **generate_targeted_eradication_data.py**: Creates data specifically designed to fix observed model weaknesses.

### Training & Merging
- **qwen_sft_train.py / phi3_sft_train.py**: Training scripts for various model sizes (0.5B to 7B).
- **crystalize_merged_model.py**: Performs the weight crystallization merge (e.g., Discipline vs. Knowledge weights).
- **merge_qwen_adapter.py**: Merges trained LoRA adapters back into the base model.

### Execution
- **run_experiment.py**: Main entry point for running the benchmark on a model.
- **run_local_expert_experiment.py**: Orchestrates benchmarks using local LLM servers (like Ollama).
- **run_*_full_benchmark.sh**: Bash scripts for automated full-suite evaluation of specific model sizes.

## 04_RawData/

Stores the raw JSON/Markdown outputs from various model evaluations.
- **qwen2_5-coder_* / gemma3_12b / llama3_2-vision_11b**: Directories containing timestamped results for each model.
- **qwen_merged_final_model**: Benchmarking results for the crystallized SFT model.

## 05_Reports/

Aggregated findings and analytical artifacts.
- **INTEGRATED_EXPERIMENT_REPORT_JA.md**: Comprehensive Japanese report detailing the performance leap from Base to SFT models.
- **latest_aggregate_results.json**: The authoritative source of truth for the latest benchmark scores.
- **capability_radar.png / complexity_vs_success.png**: Visual representations of model performance across different complexity dimensions.

## 06_References/

Contains research papers, documentation, or reference materials used during the development of the benchmark.

## 07_Finetune/

Contains critical artifacts for the Fine-tuning (SFT) phase.
- **qwen_absolute_discipline_data.jsonl**: The core dataset used to achieve the 58.6% success rate.
- **qwen_merged_final_model/**: The directory containing the finalized, crystallized model weights and configuration.
- **qwen_*_results/**: Training logs, `trainer_state.json`, and checkpoints for reproducibility.
