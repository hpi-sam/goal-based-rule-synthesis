SUFFICIENCY_SET_PROMPT='''
You are an expert in causal verification for an Autonomous Vehicle (AV) system.
You must strictly rely on legal laws and safety laws.

CRITICAL RULE:
You are NOT deciding how to achieve the effect.
You are verifying whether the effect could have already happened under the given conditions.

Instructions:

- Treat the effect as an event whose logical occurrence must be evaluated.
- Treat all present causes as fully true.
- Treat all absent causes as completely false.
- CLOSED-WORLD RULE: Any cause not explicitly listed as present must be treated as false. No additional conditions exist.
- Do NOT reinterpret the effect.
- Do NOT simplify the effect.
- Do NOT assume additional causes.
- Do NOT rely on background knowledge beyond the provided legal and safety laws.
- Determine whether the present causes logically guarantee the effect under the legal and safety laws.
- The effect must occur in all logically possible interpretations consistent with the provided laws and the given causes.
- If there exists any logically possible situation under these constraints where the effect does not occur, then the causes are not sufficient.
- Answer "yes" only if the effect is logically entailed by the present causes.
- Answer "no" if the effect is not logically guaranteed.
- For sufficient causes, indicate:
  - "sufficient" if the present causes logically guarantee the effect,
  - "not sufficient" if they do not logically guarantee the effect.
- Provide a precise explanation grounded strictly in the provided legal and safety laws that determine the sufficiency.

You are given:

Effect:
{effect}

Causes that are absent that are explicitly NOT present (false):
{causes}

Causes that are present:
{present_causes}

Legal laws:
{legal_laws}

Safety laws:
{safety_laws} 


Output strictly in JSON:

{{
  "result": "yes" or "no",
  "reason": <reason>
}}

IMPORTANT: Output must be strictly JSON, without any markdown, backticks, or explanations.
'''
