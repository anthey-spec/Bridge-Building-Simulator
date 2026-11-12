from drafter import *
from dataclasses import dataclass
set_website_title("Bridge Building Simulator")
"""
set_site_information(
    author = "Shreya Anthey", 
    description = "You're a civil engineer and your project is to build a bridge in the busy city of Manhattan. Do your best, you're the planner here!",
    sources = "View Final Project 1: Design ; Part 7 LLM Conversation",
    planning = ["Final Project 0 PDF link here", "Final Project 1 PDF link here"]
)
"""

hide_debug_information()
set_website_framed(False)

@dataclass
class Criteria:
    budget: int
    time_duration: float
    construction_workers: int

@dataclass
class Bridge:
    length: int
    width: int
    qualities: list[Criteria]
    stability: bool

@dataclass
class State:
    selected_material: list[str]
    remaining_budget: int
    starting_budget: int
    optional_features: list[str]
    current_bridge: Bridge
    name_of_bridge: str
    list_of_criteria: list[Criteria]
    quantity_of_steel: str
    quantity_of_concrete: str
    quantity_of_stone: str
    quantity_of_asphalt: str
    quantity_of_aluminum: str
    quantity_of_timber: str
    quantity_of_rubber: str
    quantity_of_fiber_reinforced_polymers: str
    previously_failed_bridge: bool
    engineering_explanation: str

quantity = Criteria(budget = 600000, time_duration = 365.0, construction_workers = 100)
starting_bridge = Bridge(length = 1000, width = 110 , qualities = [quantity] , stability = True)
bridging_off = State (
    selected_material = [],
    remaining_budget = 600000,
    starting_budget = 600000,
    optional_features = [],
    current_bridge = starting_bridge,
    name_of_bridge = "",
    list_of_criteria = [quantity],
    previously_failed_bridge = False,
    engineering_explanation = "",
    quantity_of_steel = "0",
    quantity_of_concrete = "0",
    quantity_of_stone = "0",
    quantity_of_asphalt = "0",
    quantity_of_aluminum = "0",
    quantity_of_timber = "0",
    quantity_of_rubber = "0",
    quantity_of_fiber_reinforced_polymers = "0")

@route("/welcome")
def welcome(state: State) -> Page:
    return Page(state, [Button("Next", "/instructions"),
         "Welcome to the Bridge Building Simulator!"
    ])

@route("/instructions")
def instructions(state: State) -> Page:
    return Page(state, [("Project Constraints"), ("Starting budget: $600,000"), ("Time duration: 365.0 days"), ("Construction workers: 100"), Button("Next", "/map_of_city"),
    ])

@route("/map_of_city")
def map_of_city(state: State) -> Page:
    return Page(state, [("Your Construction Site"), ("It's a busy day in Manhattan. A bridge nearby has closed down for repair and has caused a heavier traffic jam come rush hour. Design a bridge over the neighboring river to help solve this problem."), Button("Next", "/bridge_building"),
    ])

@route("/bridge_building")
def bridge_building(state: State) -> Page:
    return Page(state, [("Bridge Design"), ("After viewing your constraints and where the bridge will be built, now it's time to start designing it! Be creative, you're the civil engineer here!"), Button("Next", "/choose_materials"),
    ])

@route("/choose_materials")
def choose_materials(state: State) -> Page:
    return Page(state, [
        "Choose Your Materials" + "\n",
        "Amount of steel needed:",
        TextBox("quantity_of_steel", state.quantity_of_steel), 
        "\n",
        "Amount of concrete needed:",
        TextBox("quantity_of_concrete", state.quantity_of_concrete), 
        "\n",
        "Amount of stone needed:",
        TextBox("quantity_of_stone", state.quantity_of_stone), 
        "\n",
        "Amount of asphalt needed:",
        TextBox("quantity_of_asphalt", state.quantity_of_asphalt), 
        "\n",
        "Amount of aluminum needed:",
        TextBox("quantity_of_aluminum", state.quantity_of_aluminum), 
        "\n",
        CheckBox("uses_timber", False),
        " Include timber in bridge\n",
        CheckBox("uses_rubber", False),
        " Include rubber in bridge\n",
        CheckBox("uses_fiber_reinforced_polymers", True),
        " Include fiber reinforced polymers in bridge\n",
        Button("Continue", "test_bridge"),
        TextArea("engineering_explanation", state.engineering_explanation),
    ])

@route("/test_bridge")
def test_bridge(state: State, quantity_of_steel: str, quantity_of_concrete: str, quantity_of_stone: str, quantity_of_asphalt: str, quantity_of_aluminum: str, engineering_explanation: str, uses_timber: bool, uses_rubber: bool, uses_fiber_reinforced_polymers: bool) -> Page:
    state.quantity_of_steel = quantity_of_steel
    state.quantity_of_concrete = quantity_of_concrete
    state.quantity_of_stone = quantity_of_stone
    state.quantity_of_asphalt = quantity_of_asphalt
    state.quantity_of_aluminum = quantity_of_aluminum
    state.engineering_explanation = engineering_explanation
    state.optional_features = []
    if uses_timber:
        state.optional_features.append("timber")
    if uses_rubber:
        state.optional_features.append("rubber")
    if uses_fiber_reinforced_polymers:
        state.optional_features.append("fiber reinforced polymers")
    total_steel_cost = 2000 * int(state.quantity_of_steel)
    total_concrete_cost = 100000 * int(state.quantity_of_concrete)
    total_stone_cost = 45000 * int(state.quantity_of_stone)
    total_asphalt_cost = 4 * int(state.quantity_of_asphalt)
    total_aluminum_cost = 8500 * int(state.quantity_of_aluminum)
    total_material_cost = total_steel_cost + total_concrete_cost + total_stone_cost + total_asphalt_cost + total_aluminum_cost
    state.remaining_budget = state.starting_budget - total_material_cost
    for criteria in state.current_bridge.qualities:
        required_budget = criteria.budget
    if state.remaining_budget < 0:
        return Page (state, [("You have went over budget. Please go back and find a better solution"), Button("Return to Materials", "choose_materials")])
    if state.current_bridge.stability == False:
        state.previously_failed_bridge = True
        return Page(state, [
            "Your bridge is unstable! You must redesign it.", Button("Restart Bridge", "bridge_building")
            ])
    return Page(state, [
            "Bridge has passed! Click to see results",
            Button("See results", "results")
            ])
        
@route("/results")
def results(state: State) -> Page:
    if state.previously_failed_bridge == True:
        return Page(state, [("Final Results"), ("7/10 job. Bridge did not pass at first but then passed the other time. Good job, civil engineer")
                            ])
    else:
        return Page(state, [("Final Results"), ("10/10 job. Bridge is completely stable and there is no more traffic jams in the city. Great job, civil engineer!")
                            ])

start_server(bridging_off)

