from typing import Dict, Any
import json

class StrategyParser:
    def parse_prompt(self, prompt: str) -> Dict[str, Any]:
        """
        Parse a natural language prompt into strategy parameters
        
        Example prompt: "Create a strategy with 5 tick duration, $10 stake, 
        profit target of $100 and stop loss of $50"
        
        Returns a dict of parameters for StrategyGenerator
        """
        try:
            # Extract numeric values from the prompt
            params = {}
            
            # Set defaults
            params.update({
                "duration": 1,
                "stake": 1,
                "initial_stake": 1,
                "profit_threshold": 1000,
                "loss_threshold": 500,
                "market": "synthetic_index",
                "submarket": "random_index",
                "symbol": "1HZ10V"
            })
            
            # Parse duration
            if "tick" in prompt or "ticks" in prompt:
                words = prompt.split()
                for i, word in enumerate(words):
                    if word in ["tick", "ticks"] and i > 0:
                        try:
                            params["duration"] = int(words[i-1])
                        except ValueError:
                            pass
            
            # Parse stake/initial stake
            if "$" in prompt:
                words = prompt.split()
                for i, word in enumerate(words):
                    if word.startswith("$"):
                        try:
                            amount = float(word.replace("$", ""))
                            if "stake" in prompt[max(0, i-10):i+10]:
                                params["stake"] = amount
                                params["initial_stake"] = amount
                        except ValueError:
                            pass
            
            # Parse profit threshold
            if "profit" in prompt:
                words = prompt.split()
                for i, word in enumerate(words):
                    if word == "profit" and i > 0:
                        try:
                            if words[i-1].startswith("$"):
                                params["profit_threshold"] = float(words[i-1].replace("$", ""))
                        except ValueError:
                            pass
            
            # Parse loss threshold
            if "loss" in prompt:
                words = prompt.split()
                for i, word in enumerate(words):
                    if word == "loss" and i > 0:
                        try:
                            if words[i-1].startswith("$"):
                                params["loss_threshold"] = float(words[i-1].replace("$", ""))
                        except ValueError:
                            pass
            
            return params
            
        except Exception as e:
            print(f"Error parsing prompt: {e}")
            return {}

    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate the extracted parameters"""
        required = ["duration", "stake", "initial_stake", 
                   "profit_threshold", "loss_threshold"]
                   
        return all(key in params for key in required) and \
               all(isinstance(params[key], (int, float)) for key in required)
