DECOMPOSE_EFFECT_PROMPT = '''
You are an expert in causal reasoning. You task is to decompose an effect into a list of its necessary causes.

You are given 3 things as input.
Input:
{effect}
{legal_laws}
{safety_laws} 

Instructions:
- **Necessary Cause:** A condition that must be present for the effect to occur. If this condition is removed, the effect becomes impossible (The "But-For" Test).
- **Direct Link:** Avoid distal or "butterfly effect" causes. Focus on the immediate safety, and legal requirements.
- Produce only valid logical causes in **strict JSON format**; that ensure that the effect can happen in real world.

The JSON output must follow this exact schema:

{{
  "causes": [
    "cause_1",
    "cause_2",
    ...
  ]
}}


Input:
{effect}

Example:
effect: Turn left while maintaining low speed.
output:
{{
  "causes": [
    "Safe distance from nearby vehicles",
    "Vehicle speed is low enough to maintain traction",
    "Steering input applied to turn left",
    "No excessive lateral acceleration",
    "Sufficient friction between tires and road",
    "Driver maintains vehicle control",
    "No obstacles blocking the left turn",
    "Vehicle not in violation of legal rules for turning"
  ]
}}

IMPORTANT: Output must be strictly JSON, without any markdown, backticks, or explanations.
'''
