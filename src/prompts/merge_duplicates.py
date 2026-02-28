MERGE_DUPLICATES_PROMPT='''
You are given a list of causes from a driving situation. 
Some of these causes are repeated or very similar. 

Input:
{causes}

Instructions for deduplication:
- Only merge causes if they truly convey the exact same information.
- Preserve distinct types of reasoning, such as:
   - Legal rules (speed limits, permissions)
   - Safety requirements (reaction time, stopping distance)
   - Physics constraints (friction, braking distance)
- Retain both legal and safety aspects even if they overlap conceptually.
- Each cause must remain logically meaningful and actionable.


The JSON output must follow this exact schema:

{{
  "unique_causes": [
    "unique_cause_1",
    "unique_cause_2",
    ...
  ]
}}


Example:
Input: 
{{
  "causes": [
    "Road must be free of debris, hazards, and obstacles",
    "Road conditions must be dry and clear",
    "Road is not under construction or repair",
    "Speed must be within threshold"
  ]
}}

Output:
{{
  "unique_causes": [
    "Road conditions must be dry and clear, free from debris, hazards, obstacles, or construction/repair activities.",
    "Speed must be within threshold"
  ]
}}

IMPORTANT: Output must be strictly JSON, without any markdown, backticks, or explanations.
'''