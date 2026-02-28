# Goal/Rule Synthesis Pipeline for Autonomous Driving

This repository demonstrates a **Goal/Rule Synthesis Pipeline** applied to autonomous driving scenarios. The pipeline decomposes high-level goals into logically consistent causes, consolidates them semantically, translates them into formal symbolic representations, and evaluates necessary and sufficient conditions for achieving the goal.

---

## Pipeline Overview

The pipeline consists of four main stages:

### 1. Decomposition to Causes
- **Objective:** Generate candidate causes that explain how a high-level goal (effect) may occur.  

### 2. Semantic Consolidation
- **Objective:** Merge overlapping causes that refer to the same underlying concept.  
- **Benefit:** Produces a **unique set of causes** for further analysis.  

### 3. Symbolic Translation
- **Objective:** Convert natural language causes into **formal symbolic (FOL) form** for structured reasoning.  
 
### 4. Evaluation of Necessary & Sufficient Causes
- **Objective:** Identify which causes are necessary, sufficient, or both for achieving the effect.  

#### Steps:
1. **Individual Necessity Evaluation**  
   - Assesses each cause independently.  
   - Provides justification referencing **safety or legal constraints**.  

2. **Subset Necessity Evaluation**  
   - Identifies causes that are necessary only in combination. 

3. **Minimal Sufficient Set Evaluation**  
   - Identifies subsets of causes that are sufficient to achieve the effect.  
   - Minimal sufficient sets are combined into a **necessary-and-sufficient set**, capturing all pathways to the effect.  

---

## Quick Start

### Setup

```bash
git clone <repository-url>
# Create a Python virtual environment named "venv"
python3 -m venv venv
# Activate the virtual environment on macOS / Linux
source venv/bin/activate
# Activate the virtual environment on Windows (PowerShell)
.\venv\Scripts\Activate.ps1
# Install required packages
pip install -r requirements.txt
# Create a .env file in the project root and add your OpenApi Key:
OPENAI_API_KEY=your_openai_api_key_here
# Rub the script by running:
python3 src/pipeline.py
```
