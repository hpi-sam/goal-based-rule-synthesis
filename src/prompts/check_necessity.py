CHECK_NECESSITY_PROMPT = '''
You are an expert in causal reasoning for Autonomous Vehicle (AV) systems.

You are given:
1. A main effect.
2. A list of causes.
3. A set of legal laws.
4. A set of safety laws.


effect: {effect}
causes: {causes}
legal_laws: {legal_laws}
safety_laws: {safety_laws}

CRITICAL REASONING RULES:

INDEPENDENT NECESSITY TEST:
- Evaluate EACH cause independently.
- When evaluating one cause, assume ONLY that this cause is FALSE.
- Do NOT assume any other listed causes are present or absent.
- Do NOT assume hidden conditions.
- Only rely on the provided legal and safety laws.

DEFINITION:
- A cause is "necessary" if the effect is logically impossible under the provided laws when this cause is false.
- A cause is "not necessary" if there exists at least one logically possible situation, consistent with the laws, where the effect occurs while this cause is false.

IMPORTANT:
- Do NOT assume substitution by other listed causes.
- Do NOT assume background facts not stated in the laws.
- Do NOT evaluate optimality or quality.
- Safety laws must be fully satisfied.
- Your reasoning must strictly follow the provided laws.

Instructions:
- Evaluate each cause independently.
- Determine whether the effect could legally and safely occur if this cause were false.
- Provide reasoning grounded only in the provided legal and safety laws.


Output JSON format:

{{
  "evaluations": [
    {{
      "cause": "exact cause text",
      "result": "necessary" or "not necessary",
      "reason": "clear explanation, strictly using legal and safety laws why this cause is or is not required for the effect"
    }}
  ]
}}

Example:

effect: Turn left while maintaining low speed.
causes: 
[
    "Safe distance from nearby vehicles",
    "Vehicle speed is low enough to maintain traction",
    "Steering input applied to turn left",
    "No excessive lateral acceleration",
    "Sufficient friction between tires and road",
    "Driver maintains vehicle control",
    "No obstacles blocking the left turn",
    "Vehicle not in violation of legal rules for turning"
]


Output:
{{
  "evaluations": [
    {{
        "cause": "Safe distance from nearby vehicles",
        "result": "not necessary",
        "reason": "Maintaining low-speed left turn is physically possible without considering other vehicles; safe distance affects safety but is not strictly required for the turn to occur according to laws."
    }},
    {{
        "cause": "Vehicle speed is low enough to maintain traction",
        "result": "necessary",
        "reason": "Low speed is required by friction and vehicle control laws; without it, the effect violates safety laws."
    }},
    ...
  ]
}}

IMPORTANT: Output must be strictly valid JSON without markdown or explanations.
'''
