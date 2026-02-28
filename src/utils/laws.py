# laws.py

"""
Traffic and Physics laws for traffic scene reasoning.

- TRAFFIC_LAWS: human/motor vehicle traffic regulations
- PHYSICS_LAWS: vehicle dynamics and physical constraints
- Utility functions to fetch lists and prompt-ready formats
"""

# ----------------------------------------------------------------------
# Traffic laws
# ----------------------------------------------------------------------
TRAFFIC_LAWS = {
    "keep_control": "A person operating a vehicle may only travel at a speed that allows them to be in constant control of their vehicle",
    "above_minimum_speed": "No motor vehicle must, without good reason, travel so slowly as to impede the flow of traffic",
    "below_speed_limit": "Adhere to the maximum permissible speed",
    "no_stopping": "On motorways and motor roads, stopping is prohibited, including on verges",
    "keep_right": "Keep as far to the right as possible except when dense traffic with multiple lanes, built-up area, outside built-up area with three or more lanes",
    "speed_adv_overtaking": "Only overtake if the ego vehicle travels at a speed substantially higher than that of the vehicle to be overtaken",
    "overtaking_maneuver": "Make sure that traffic approaching from behind is not endangered. Keep a sufficient lateral distance from other road users",
    "no_right_overtaking": "Only overtake on the left",
    "safe_distance": "A person operating a vehicle moving behind another vehicle must, as a rule, keep a sufficient distance from that other vehicle",
    "being_overtaken": "A vehicle being overtaken must not increase the vehicle's speed",
    "emergency_stopping": "Apply emergency break incase of sudden obstacle",
    "traffic_light": "Follow Traffic light signals"
}

# ----------------------------------------------------------------------
# Physics laws
# ----------------------------------------------------------------------
PHYSICS_LAWS = {
    "stationary_no_friction_decrease": "A stationary vehicle cannot experience decreasing friction",
    "max_acceleration_limited_by_friction": "A vehicle cannot accelerate faster than the friction between tires and road allows",
    "max_deceleration_limited_by_friction": "A vehicle cannot decelerate faster than the friction between tires and road allows",
    "slip_if_force_exceeds_friction": "A vehicle will skid or slip if the longitudinal or lateral force exceeds available friction",
    "collision_without_emergency_brake": "A vehicle will collide if it does not apply the emergency brake",
    "collision_if_moving": "A vehicle may collide if it is moving",
    
    # ---- Speeding and speed-related behavior ----
    "too_fast_for_conditions": "A vehicle traveling faster than safe for current road and weather conditions may lose control",
    "braking_distance_increases_with_speed": "The distance required to stop a vehicle increases with speed",
    "turning_radius_increases_with_speed": "A vehicle must reduce speed before a turn to maintain traction",
    "speeding_reduces_reaction_time": "At higher speeds, the time to react to obstacles or traffic decreases",
    "overtake_speed_requirement": "A vehicle must have a sufficient speed advantage to safely overtake another vehicle",
    "overspeed_on_curve_risk": "Exceeding safe speed limits on a curve may result in skidding or leaving the lane",
    "speed_limited_by_friction": "Maximum safe speed is limited by the friction between tires and road surface",
    "hydroplaning_risk": "At high speed on wet roads, a vehicle may hydroplane and lose contact with the road",
}

# ----------------------------------------------------------------------
# Internal helper to merge both
# ----------------------------------------------------------------------
def _merge_laws():
    merged = {}
    merged.update(TRAFFIC_LAWS)
    merged.update(PHYSICS_LAWS)
    return merged

# ----------------------------------------------------------------------
# Traffic law getters
# ----------------------------------------------------------------------
def get_traffic_laws():
    """Return dictionary of traffic laws"""
    return TRAFFIC_LAWS

def get_traffic_laws_list():
    """Return list of traffic law names"""
    return list(TRAFFIC_LAWS.keys())

def format_traffic_laws_for_prompt():
    """Return prompt-ready text for traffic laws"""
    return "\n".join([f"{k} : {v}" for k, v in TRAFFIC_LAWS.items()])

# ----------------------------------------------------------------------
# Physics law getters
# ----------------------------------------------------------------------
def get_physics_laws():
    """Return dictionary of physics laws"""
    return PHYSICS_LAWS

def get_physics_laws_list():
    """Return list of physics law names"""
    return list(PHYSICS_LAWS.keys())

def format_physics_laws_for_prompt():
    """Return prompt-ready text for physics laws"""
    return "\n".join([f"{k} : {v}" for k, v in PHYSICS_LAWS.items()])

# ----------------------------------------------------------------------
# Merged laws getters
# ----------------------------------------------------------------------
def get_all_laws():
    """Return dictionary of traffic + physics laws"""
    return _merge_laws()

def get_all_laws_list():
    """Return list of all law names"""
    return list(_merge_laws().keys())

def format_all_laws_for_prompt():
    """Return prompt-ready text of all laws"""
    return "\n".join([f"{k} : {v}" for k, v in _merge_laws().items()])
