from typing import Dict, Any
import json
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

class StrategyParser:
    def __init__(self):
        """Initialize Anthropic client"""
        self.client = anthropic.Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )

    def parse_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Parse a natural language prompt into strategy parameters using LLM capabilities
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
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{
                    "role": "user",
                    "content": f"""What are the trading parameters in this sentence? '{prompt}'
                    Give the output in json format (exclude those keys which are not found):
                        {{
                            "duration": 1,
                            "initial_stake": 1,
                            "profit_threshold": 1000,
                            "loss_threshold": 500,
                            "market": "synthetic_index",
                            "submarket": "random_index",
                            "symbol": "1HZ10V"
                        }}
                    Do not reply anything other than json. """
                }]
            )
            
            # Parse the JSON response
            print(response.content[0].text)
            extracted = json.loads(response.content[0].text)
            # Update defaults with extracted parameters
            params = defaults.copy()
            params.update(extracted)
            # print("extracted", extracted)
            # print("params   ", params)
            return params
            
        except Exception as e:
            print(f"Error extracting parameters: {e}")
            return defaults

    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate the extracted parameters"""
        required = ["duration", "stake", "profit_threshold", "loss_threshold"]
                   
        return all(key in params for key in required) and \
               all(isinstance(params[key], (int, float)) for key in required)
