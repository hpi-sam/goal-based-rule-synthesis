import json
from itertools import combinations
from typing import List, Dict, Any
from llm_adapter import call_llm
from utils.logger import get_logger
from utils.laws import format_physics_laws_for_prompt, format_traffic_laws_for_prompt

from prompts.decompose_effect import DECOMPOSE_EFFECT_PROMPT
from prompts.merge_duplicates import MERGE_DUPLICATES_PROMPT
from prompts.convert_to_symbolic_rule import CONVERT_TO_SYMBOLIC_RULE_PROMPT
from prompts.check_necessity import CHECK_NECESSITY_PROMPT
from prompts.necessity_set import  NECESSITY_SET_PROMPT
from prompts.sufficiency_set import SUFFICIENCY_SET_PROMPT

logger = get_logger()


def decompose_effect(effect: str, legal_laws: List[dict], safety_laws: List[dict]) -> List[str]:
    """
    Uses an LLM to decompose a high-level effect into a list of potential causal conditions.
    
    Args:
        effect: Target outcome to analyze.
        legal_laws: Structured legal constraints to guide decomposition.
        safety_laws: Structured safety/physics constraints to guide decomposition.
    
    Returns:
        List of textual causes contributing to the effect.
    
    Raises:
        ValueError: If LLM response is not valid JSON.
    """
    logger.info("Starting decomposition of effect into causes")
    prompt = DECOMPOSE_EFFECT_PROMPT.format(effect=effect, legal_laws=legal_laws, safety_laws=safety_laws)
    response = call_llm(prompt, max_tokens=512)

    try:
        causes = json.loads(response)
        logger.info("Decomposition of effect completed")
        return causes
    except json.JSONDecodeError:
        raise ValueError("Failed to parse causes JSON from LLM output")

def merge_duplicate_causes(causes: List[dict]) -> List[dict]:
    """
    Uses an LLM to semantically merge duplicate or equivalent causes.
    
    Args:
        causes: List of candidate causes (possibly redundant).
    
    Returns:
        List of unique, merged causes.
    
    Raises:
        ValueError: If LLM response is not valid JSON.
    """
    logger.info("Starting removal of duplicate causes")
    prompt = MERGE_DUPLICATES_PROMPT.format(causes=causes)
    response = call_llm(prompt, max_tokens=512)

    try:
        unique_causes = json.loads(response)
        logger.info("Removal of duplicates completed")
        return unique_causes
    except json.JSONDecodeError:
        raise ValueError("Failed to parse unique causes JSON from LLM output")

def check_necessity(effect: str, causes: List[dict], legal_laws: List[dict], safety_laws: List[dict]) -> List[dict]:
    """
    Uses an LLM to classify each cause as necessary or not for producing the effect.
    
    Args:
        effect: Target outcome.
        causes: unique causes to evaluate.
        legal_laws: Legal constraints.
        safety_laws: Safety/physics constraints.
    
    Returns:
        Structured evaluation results marking individual necessary causes.
    
    Raises:
        ValueError: If LLM response is not valid JSON.
    """
    logger.info("Checking necessary causes")
    prompt = CHECK_NECESSITY_PROMPT.format(effect=effect, causes=causes, legal_laws=legal_laws, safety_laws=safety_laws)
    response = call_llm(prompt, max_tokens=15000)

    try:
        necessary_causes = json.loads(response)
        logger.info("Evaluation of individual necessary causes completed")
        return necessary_causes
    except json.JSONDecodeError:
        raise ValueError("Failed to parse evaluated necessary causes JSON from LLM output")

def necessity_set(effect: str, causes: List[dict], absent_cause: str, legal_laws: List[dict], safety_laws: List[dict]) -> List[dict]:
    """
    Extracts necessity set by testing whether removing specific causes prevents the effect.
    
    Args:
        effect: Target outcome.
        causes: Causes assumed present.
        absent_cause: Cause(s) removed in this counterfactual test.
        legal_laws: Legal constraints.
        safety_laws: Safety/physics constraints.
    
    Returns:
        Result indicating whether the absent cause is truly necessary.
    
    Raises:
        ValueError: If LLM response is not valid JSON.
    """
    logger.info("Validation necessary causes")
    prompt = NECESSITY_SET_PROMPT.format(effect=effect, causes=causes,absent_cause=absent_cause, legal_laws=legal_laws, safety_laws=safety_laws)
    response = call_llm(prompt, max_tokens=15000)

    try:
        validation = json.loads(response)
        logger.info("Validation of necessary causes completed")
        return validation
    except json.JSONDecodeError:
        raise ValueError("Failed to parse validation JSON from LLM output")

def sufficiency_set(effect: str, causes: List[dict], present_causes:  List[dict], legal_laws: List[dict], safety_laws: List[dict]) -> List[dict]:
    """
    Extracts sufficiency set by testing whether a set of present causes alone guarantees the effect.
    
    Args:
        effect: Target outcome.
        causes: Causes assumed absent.
        present_causes: Causes assumed present.
        legal_laws: Legal constraints.
        safety_laws: Safety/physics constraints.
    
    Returns:
        Result indicating whether present causes are sufficient.
    
    Raises:
        ValueError: If LLM response is not valid JSON.
    """
    logger.info("Validation of sufficient causes")
    prompt = SUFFICIENCY_SET_PROMPT.format(effect=effect, causes=causes,present_causes=present_causes, legal_laws=legal_laws, safety_laws=safety_laws)
    response = call_llm(prompt, max_tokens=15000)

    try:
        validation = json.loads(response)
        logger.info("Validation of sufficient causes completed")
        return validation
    except json.JSONDecodeError:
        raise ValueError("Failed to parse validation JSON from LLM output")

def convert_to_symbolic_rule(condition: str)-> Dict[str,Any]:
    """
    Converts a natural language condition into a structured symbolic rule representation using an LLM.
    
    Args:
        condition: Natural language causal condition.
    
    Returns:
        Cause translated in FOL.
    
    Raises:
        ValueError: If LLM response is not valid JSON.
    """
    logger.info("Starting converting condition to symbolic rule")
    prompt = CONVERT_TO_SYMBOLIC_RULE_PROMPT.format(condition=condition)
    response = call_llm(prompt, max_tokens=15000)

    try:
        rule = json.loads(response)
        logger.info("Converstion completed")
        return rule
    except json.JSONDecodeError:
        raise ValueError("Failed to parse converted rule JSON from LLM output")

def extract_necessary_causes(llm_output):
    # Convert string to dict if needed
    if isinstance(llm_output, str):
        llm_output = json.loads(llm_output)

    evaluations = llm_output["evaluations"]

    return [
        item["cause"]
        for item in evaluations
        if item["result"] == "necessary"
    ]

def extract_sufficient_causes(llm_output):
    # Convert string to dict if needed
    if isinstance(llm_output, str):
        llm_output = json.loads(llm_output)

    evaluations = llm_output["evaluations"]

    return [
        item["cause"]
        for item in evaluations
        if item["result"] == "sufficient"
    ]

def extract_unique_causes(llm_output):
    # Convert string to dict if needed
    if isinstance(llm_output, str):
        llm_output = json.loads(llm_output)

    evaluations = llm_output["unique_causes"]

    return evaluations

def extract_causes(llm_output):
    # Convert string to dict if needed
    if isinstance(llm_output, str):
        llm_output = json.loads(llm_output)

    evaluations = llm_output["causes"]

    return evaluations

def prune_necessary_causes(effect, necessary_causes, traffic_laws, physics_laws):
    """
    Computes minimal necessary cause subsets using combinatorial search with memoized LLM validation.
    
    A subset is minimal necessary if removing it prevents the effect and
    no proper subset has this property.
    
    Args:
        effect: Target outcome.
        necessary_causes: Candidate necessary causes.
        traffic_laws: Legal constraints.
        physics_laws: Safety/physics constraints.
    
    Returns:
        List of minimal necessary cause subsets.
    """
    pruned = necessary_causes.copy()
    found_minimal_subsets = []
    memo = {}

    def is_necessary(test_causes, absent_causes):
        key = (tuple(sorted(test_causes)), tuple(sorted(absent_causes)))
        if key in memo:
            return memo[key]
        result = necessity_set(effect, test_causes, absent_causes, traffic_laws, physics_laws)
        memo[key] = result.get("result") == "no"
        return memo[key]

    n = len(pruned)
    # Start with singletons
    for r in range(1, n + 1):
        for subset in combinations(pruned, r):
            # Skip if any already-found subset is fully contained in this one
            if any(s <= set(subset) for s in found_minimal_subsets):
                continue
            present_causes = [c for c in pruned if c not in subset]
            absent_causes = list(subset)
            logger.info(f"\nPresent Causes:\n{present_causes}")
            logger.info(f"Absent Causes:\n{absent_causes}")
            if is_necessary(present_causes, absent_causes):
                found_minimal_subsets.append(set(subset))

    minimal_subsets = [list(s) for s in found_minimal_subsets]
    return minimal_subsets

def log_necessary_sets(necessary_sets):
    """
    necessary_sets: List[List[str]]
    """
    if not necessary_sets:
        logger.info("No necessary sets found.")
        return

    for idx, subset in enumerate(necessary_sets, start=1):
        logger.info(f"\nNecessary Set {idx}:")
        for cause in subset:
            logger.info(f"  - {cause}")

def prune_sufficient_causes(effect,causes,traffic_laws,physics_laws):
    """
    Computes minimal sufficient cause subsets using level-wise combinatorial search.
    
    A subset is minimal sufficient if it guarantees the effect and
    no proper subset is already sufficient.
    
    Args:
        effect: Target outcome.
        causes: Candidate causes.
        traffic_laws: Legal constraints.
        physics_laws: Safety/physics constraints.
    
    Returns:
        List of minimal sufficient cause subsets.
    """
    pruned = causes.copy()
    minimal_sufficient_sets = []

    # We grow subset size level by level
    for r in range(1, len(pruned) + 1):
        for combo in combinations(pruned, r):
            present_causes = list(combo)

            # --- PRUNE RULE: skip supersets of already sufficient sets ---
            skip = False
            for s in minimal_sufficient_sets:
                if set(s).issubset(set(present_causes)):
                    skip = True
                    break
            if skip:
                logger.info(f"Skipping (superset of known sufficient set): {present_causes}")
                continue

            absent_causes = [c for c in pruned if c not in present_causes]

            logger.info(f"Present Causes:\n{present_causes}")
            logger.info(f"Absent Causes:\n{absent_causes}")

            response = sufficiency_set(
                effect,
                absent_causes,
                present_causes,
                traffic_laws,
                physics_laws
            )

            if response.get("result") == "yes":
                logger.info(f"Minimal sufficient set found:\n{present_causes}")
                minimal_sufficient_sets.append(present_causes)

    return minimal_sufficient_sets

def log_sufficient_sets(sufficient_sets):
    """
    sufficient_sets: List[List[str]]
    """
    if not sufficient_sets:
        logger.info("No sufficient sets found.")
        return

    for idx, subset in enumerate(sufficient_sets, start=1):
        logger.info(f"\nSufficient Set {idx}:")
        for cause in subset:
            logger.info(f"  - {cause}")

def run_pipeline(effect: str):
    """
    Executes the full causal analysis pipeline:
    
    1. Load predefined legal and safety laws.
    2. Decompose effect into candidate causes.
    3. Merge duplicate causes.
    4. Convert causes to symbolic rules.
    5. Identify necessary causes.
    6. Compute minimal necessary subsets.
    7. Compute minimal sufficient subsets.
    
    Args:
        effect: High-level outcome to analyze.
    """
    logger.info(f"Fetching predefined rules/laws")
    legal_laws = format_traffic_laws_for_prompt()
    safety_laws = format_physics_laws_for_prompt()

    logger.info(f"Starting pipeline for effect:\n{effect}")

    causes = decompose_effect(effect,legal_laws,safety_laws)
    c = extract_causes(causes)
    unique_causes = merge_duplicate_causes(causes)
    uc = extract_unique_causes(unique_causes)

    all_rules = []
    for cond in uc:
        rules = convert_to_symbolic_rule(cond)
        all_rules.append(rules)

    marked_necessary_conditions = check_necessity(effect,uc,legal_laws,safety_laws)

    necessary_causes = extract_necessary_causes(marked_necessary_conditions)

    logger.info(f"Only necessary causes:\n{necessary_causes}")

    logger.info(f"Starting validation for necessary conditions------------------")
    
    log_necessary_sets(prune_necessary_causes(effect,uc,legal_laws,safety_laws))
    
    logger.info(f"Starting validation for sufficient conditions------------------")

    log_sufficient_sets(prune_sufficient_causes(effect,uc,legal_laws,safety_laws))

    logger.info("Pipeline finished successfully.")

if __name__ == "__main__":
    # You can change the top-level effect here to test the pipeline with a different goal
    top_effect_example = "Maintain a constant speed on a highway segment"
    run_pipeline(top_effect_example)

    
    