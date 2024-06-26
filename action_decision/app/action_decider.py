import uuid
import time
import json
from collections import deque

from shared.utils.client_utils.game_state import get_game_state
from shared.utils.client_utils.model_server import generate_text_openrouter
from shared.utils.observe_utils import langfuse_tracking, start_trace
from shared.utils.python_exec_utils import extract_retry

from langfuse import Langfuse
langfuse = Langfuse()

class StrategyNode:
    def __init__(self, action_decider, decision, depth=0):
        self.action_decider = action_decider
        self.decision = decision
        self.children = []
        self.depth = depth
        self.id = str(uuid.uuid4())
    
    def add_child(self, decision):
        new_child = StrategyNode(self.action_decider, decision, self.depth + 1)
        self.children.append(new_child)
        return new_child
    
    def to_dict(self):
        return {
            "id": self.id,
            "decision": self.decision,
            "depth": self.depth,
            "children": [child.to_dict() for child in self.children]
        }
    
    def __repr__(self):
        return f"Decision: {self.decision}, Depth: {self.depth}, Children: {len(self.children)}"

# Utility function for collecting paths
def collect_paths(node, path=None, collected_paths=None):
    if collected_paths is None:
        collected_paths = []
    if path is None:
        path = []
    for child in node.children:
        new_path = path.copy()
        new_path.append(child.decision)  # Add child's decision to path
        if not child.children:
            collected_paths.append(new_path)  # If leaf node, add path to collected_paths
        else:
            collect_paths(child, new_path, collected_paths)  # Recurse into children
    return collected_paths

class ActionDecider:
    def __init__(self):
        self.llm = generate_text_openrouter
        self.llm_name = "gemini-7b-it"
        self.last_game_state = None
        self.trace = None
        self.session_id = None
        self.active_span = None
        self.root = None
        self.current_step = None
        self.current_node = None
        self.start_time = None
        self.end_time = None
    
    async def get_game_state(self):
        game_state = await get_game_state()
        self.last_game_state = game_state['state']
        return self.last_game_state
        
    async def ask_llm_for_initial_decision(self):
        prompt = "Given the following summary, what is the highest level decision you need to make in the game?"
        prompt += f"\n{self.last_game_state['summary']}"
        return await self.get_initial_decision(prompt=prompt, session_id=self.session_id)
    
    @langfuse_tracking(name="get-initial-decision", trace_id_attr="trace.id", model_attr="llm_name")
    async def get_initial_decision(self, prompt, session_id):
        response = await self.llm(prompt, session_id=session_id) 
        if not response["success"]:
            return None
        return response["text"]
        
    async def get_llm_response_to_explore_options(self, node):
        prompt = f"Given the following decision: {node.decision}, what are the possible options?"
        prompt += f"\n Format the response as an array of options."
        response = await self.generate_options(prompt=prompt, session_id=self.session_id)
        if response is None:
            return None
        
        prompt = "Convert the list of options to a python list called `options`:"
        prompt += f"\n{response}"
        parent_span = self.active_span
        span = langfuse.span(
            trace_id=self.trace.id,
            parent_observation_id=self.active_span.id,
            name="convert-to-list",
            input=response
        )
        self.active_span = span
        converted_list = await self.convert_to_list_and_extract_options(prompt=prompt)
        span.end(output=converted_list)
        self.active_span = parent_span
        return converted_list

    
    @langfuse_tracking(name="generate-options", trace_id_attr="trace.id", parent_observation_id_attr="active_span.id", model_attr="llm_name")
    async def generate_options(self, prompt, session_id):
        response = await self.llm(prompt, session_id=session_id)
        return response["text"]
    
    @extract_retry(var_name="options")
    async def convert_to_list_and_extract_options(self, prompt):
        return await self.convert_to_list(prompt=prompt)

    @langfuse_tracking(name="convert-to-list", trace_id_attr="trace.id", parent_observation_id_attr="active_span.id", model_attr="llm_name")
    async def convert_to_list(self, prompt):
        response = await self.llm(prompt)
        if not response["success"]:
            return None
        return response["text"]
    
    async def is_option_feasible(self, node):
        global_span = self.active_span
        span = langfuse.span(
            trace_id=self.trace.id,
            parent_observation_id=self.active_span.id,
            name="query-feasibility",
            input=node.decision
        )
        self.active_span = span
        # Placeholder for your implementation to query the LLM
        prompt = f"This is the summary of a game state:"
        prompt += f"\n{self.last_game_state['summary']}"
        prompt += f"\nGiven a decision scenario where the action is to '{node.decision}', evaluate if this option is feasible."
        prompt += f"\nGenerate a Python code response that assigns a boolean value to a variable named feasible, explaining the logic behind the feasibility assessment in a comment directly above the assignment."
        prompt += f"\nThe explanation should be general, avoiding any assumptions about the current state or context that aren't explicitly given in the prompt."
        feasibility = await self.query_feasibility(prompt=prompt)
        if feasibility is None:
            return False
        
        prompt = "Extract the value of the variable `feasible` from the response and in python code, assign it to a variable named `feasible`."
        prompt += f"\n{feasibility}"

        parent_span = self.active_span
        span = langfuse.span(
            trace_id=self.trace.id,
            parent_observation_id=self.active_span.id,
            name="extract-feasibility",
            input=feasibility
        )
        self.active_span = span
        feasibility_bool = await self.convert_to_boolean_and_extract_feasibility(prompt=prompt)
        span.end(output=feasibility_bool)
        self.active_span = parent_span
        parent_span.end(output=feasibility_bool)
        self.active_span = global_span
        return feasibility_bool
    
    @extract_retry(var_name="feasible")
    async def convert_to_boolean_and_extract_feasibility(self, prompt):
        return await self.convert_to_bool(prompt=prompt)

    @langfuse_tracking(name="convert-to-boolean", trace_id_attr="trace.id", parent_observation_id_attr="active_span.id", model_attr="llm_name")
    async def convert_to_bool(self, prompt):
        response = await self.llm(prompt)
        if not response["success"]:
            return None
        return response["text"]

    @langfuse_tracking(name="query-feasibility", trace_id_attr="trace.id", parent_observation_id_attr="active_span.id", model_attr="llm_name")
    async def query_feasibility(self, prompt):
        response = await self.llm(prompt)
        if not response["success"]:
            return None
        return response["text"]

    async def decide(self, depth_limit=2):
        await self.get_game_state()
        
        self.session_id = str(uuid.uuid4())
        self.current_node = StrategyNode(self, "Getting initial decision...")
        self.current_step = "Getting initial decision..."
        self.end_time = None
        self.start_time = time.time()
        self.trace = start_trace("action-decision", user_id="ashis", session_id=self.session_id, input=self.last_game_state, metadata=None, tags=None)
        initial_decision = await self.ask_llm_for_initial_decision()
        self.current_step = None

        span = self.trace.span(
            name="build-decision-tree",
            input=initial_decision
            )
        self.active_span = span

        self.root = StrategyNode(self, initial_decision)

        queue = deque([self.root])
        while queue:
            self.current_node = queue.popleft()
            if self.current_node.depth >= depth_limit:
                continue

            tree_span = langfuse.span(
                trace_id=self.trace.id,
                parent_observation_id=span.id,
                name="explore-decision-tree",
                input=self.current_node.decision
            )
            self.active_span = tree_span
            self.current_step = f"Generating options for {self.current_node.id} : {self.current_node.decision[:100]}..."
            options = await self.get_llm_response_to_explore_options(self.current_node)
            self.current_step = None
            parent_node = self.current_node
            if options is not None:
                for option in options:
                    child_node = self.current_node.add_child(option)
                    self.current_node = child_node
                    self.current_step = f"Checking feasibility of {child_node.id} : {str(child_node.decision)[:100]}..."
                    if await self.is_option_feasible(child_node):
                        queue.append(child_node)
                    else:
                        print(f"Option {option} is not feasible")
                    self.current_node = parent_node
                    self.current_step = None

            tree_span.end(output="done")
            self.active_span = span

            self.current_node = None
        
        self.current_step = "Done. Ranking strategies..."
        
        self.end_time = time.time()
        
        span.end(output="done")

        feasible_strategies = []
        for child in self.root.children:
            feasible_strategies.extend(collect_paths(child))
        ranked_strategies = await self.rank_strategies(feasible_strategies)
        # result = ranked_strategies[0] if ranked_strategies else None
        # self.trace.update(
        #     output=result
        # )
        self.current_step = ranked_strategies
        return ranked_strategies

    async def rank_strategies(self, strategies):
        # Constructing the prompt for ranking strategies
        prompt = "Please rank the following strategies based on their effectiveness:\n"
        for i, strategy in enumerate(strategies, 1):
            prompt += f"{i}: {' > '.join(strategy)}\n"
        prompt += "\nProvide your ranking."

        # Assuming self.generator is a function that interacts with the LLM
        response = await self.llm(prompt)
        # Here, you would parse the LLM's response to extract the ranking
        # This example assumes the response is directly usable as a ranking
        if not response["success"]:
            return None
        return response["text"]
    
    def get_decision_tree(self):
        if self.root:
            result = {
                "success": True,
                "data": {
                    "tree": self.root.to_dict(),
                    "current_node_id": self.current_node.id if self.current_node else None,
                    "current_node_desc": repr(self.current_node) if self.current_node else None,
                    "current_step": self.current_step if self.current_step else None,
                    "start_time": self.start_time if self.start_time else None,
                    "end_time": self.end_time if self.end_time else None,
                }
            }
            return result
        return {"success": False, "error": "No decision tree available."}
    
    def stream_decision_tree(self):
        while True:
            data = json.dumps(self.get_decision_tree())  # Ensures JSON format
            yield f"data: {data}\n\n"
            time.sleep(0.2)