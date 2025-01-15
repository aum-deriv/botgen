from typing import Dict, Any
from mcp.server.fastmcp import Context
import json
import os
import anthropic

class StrategyParser:
    def __init__(self):
        """Initialize Anthropic client"""
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )

    def parse_prompt(self, prompt: str, ctx: Context = None) -> Dict[str, Any]:
        """
        Parse a natural language prompt into strategy parameters using LLM capabilities
        
        Example prompt: "Create a strategy with 5 tick duration, $10 stake, 
        profit target of $100 and stop loss of $50"
        
        Returns a dict of parameters for StrategyGenerator
        """
        # Default parameters
        defaults = {
            "duration": 1,
            "stake": 1,
            "initial_stake": 1,
            "profit_threshold": 1000,
            "loss_threshold": 500,
            "market": "synthetic_index",
            "submarket": "random_index",
            "symbol": "1HZ10V"
        }

        try:
            # Get JSON response from Claude
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"""Extract the trading parameters from this prompt: {prompt}
Please respond with ONLY a JSON object in this format:
{{
    "duration": <number of ticks>,
    "stake": <stake amount in dollars>,
    "initial_stake": <stake amount in dollars>,
    "profit_threshold": <profit target in dollars>,
    "loss_threshold": <stop loss in dollars>
}}"""
                }]
            )
            
            # Parse the JSON response
            extracted = json.loads(response.content)
            # Update defaults with extracted parameters
            params = defaults.copy()
            params.update(extracted)
            return params
            
        except Exception as e:
            print(f"Error extracting parameters: {e}")
            return defaults

    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate the extracted parameters"""
        required = ["duration", "stake", "initial_stake", 
                   "profit_threshold", "loss_threshold"]
                   
        return all(key in params for key in required) and \
               all(isinstance(params[key], (int, float)) for key in required)
