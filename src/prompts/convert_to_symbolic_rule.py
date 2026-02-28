CONVERT_TO_SYMBOLIC_RULE_PROMPT=''' 
You are an expert in converting a condition into a symbolic rule.
You are given a single condition in a logical format of if and else) as an input.
Your task is to produce symbolic rule for the condition.
You must follow the grammar provided to you below

Input:
{condition}

Instructions:
- Use the grammar provided below.
- *Do not* make up grammar by yourself.
- Use only the allowed predicates and operators. Map each natural language clause to meaningful predicates rather than inventing new ones
- Before giving the final output break the condition into sub-conditions (intermediate logical steps), then map each step to a symbolic rule
- For each condition, think about what safety outcome or system effect it is describing. Then map it to the symbolic predicates and allowed logical operators.
- Do not create rules that are logically impossible (e.g., a vehicle being both left and right of another at the same time) or that contradict safety logic.
- For conditions involving driver perception, vehicle control, or environment, make sure the symbolic rule reflects the resulting safety outcome (collision avoidance, safe stopping, emergency brake)

Allowed Predicates and their explanations:
- dense(i) - i is closer than rdense(a distance threshold for crowdedness) to Ndense(a number of nearby vehicles that counts as dense) or more agents 
- pred(i,j) - i is the predecessor of j 
- right(i,j) - i is to the right of j 
- left(i,j) - i is to the left of j 
- in-front(i,j) - i is in front of j 
- behind(i,j) - i is behind j 
- merged(i) - i has passed a static merging point, from which on a merge is not possible anymore 
- sd-front(i) - i has a safe distance to the preceding vehicle 
- sd-rear(i) - i has a safe distance to the following vehicle 
- collide(i) - i is colliding with road boundaries or any other agent or obstacle 
- lane-change(i) - i is crossing a lane boundary 
- near(i,j) - i is closer than dnear to j 
- lane-end(i) - i has less than srem remaining to the end of the lane 
- acc(i) - i accelerates with a > alim 
- speed-adv(i,j) - i is faster than j and some threshold vdiff 
- built-up(i) - i is within a built-up area 
- motorway(i) - i is on a road type: motorway 
- div-lane(i) - i is on a lane type: diverging lane 
- acc-lane(i) - i is on a lane type: acceleration lane
- ∆speed(i) - speed of i
- ∆friction(i) - friction of i
- collision(i) - collision of i
- EB(i) - i has applied emergency break

Allowed rule forms ONLY:
1. Universal constraint: ∀x ¬(condition₁ ∧ condition₂)
2. Implication: ∀x(conclusion ← condition)
3. Probabilistic rule: ∀x(ρ(event(x), p%))
4. Conditional probabilistic rule: ∀x, ∃v(ρ(event(x), p%) ← condition involving v)

Allowed comparisons:
1. > greater than
2. < lesser than
3. = equals to
4. >= greater than equals to
5. <= lesser than equals to

Allowed logical operators:
1. ¬ Negation
2. ∧ Conjunction
3. ← Implication

Example:
{{
    "condition": "Stopping distance is within vehicle's braking capability",
    "rule": "∀x(EB(x) ← sd-front(x) ∧ ∆friction(x) > 0)",
    "thinking": "Stopping distance is within vehicle’s braking capability is not only about distance. 
    It is fundamentally about whether the brakes can generate enough deceleration to stop the car before the obstacle. 
    For which there should be enough distance with car in front and friction as non zero"
}}


Output should be in this format (strict JSON only):
{{
    "condition": "logical condition 1",
    "rule": "symbolic rule 1",
    "thinking": "thought process"
}}
IMPORTANT: Output must be strictly JSON, without any markdown, backticks, or explanations.
'''