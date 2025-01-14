#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts.base import Message, UserMessage, AssistantMessage
from strategy_generator import StrategyGenerator
from strategy_parser import StrategyParser

# Create MCP server
mcp = FastMCP("Strategy")

# Initialize components
generator = StrategyGenerator()
parser = StrategyParser()

@mcp.prompt()
def strategy_prompt(message: str, ctx: Context) -> list[Message]:
    """Handle strategy-related prompts"""
    return [
        UserMessage(message),
        AssistantMessage("I'll help you generate a trading strategy.")
    ]

@mcp.tool()
def generate_strategy(prompt: str, ctx: Context) -> str:
    """Generate a trading strategy from description"""
    try:
        # Parse parameters from prompt
        params = parser.parse_prompt(prompt)
        
        if not parser.validate_parameters(params):
            error_msg = "Could not extract valid parameters from prompt"
            ctx.error(error_msg)
            return error_msg
            
        # Generate strategy XML
        strategy_xml = generator.generate_strategy(
            duration=params["duration"],
            stake=params["stake"],
            initial_stake=params["initial_stake"],
            profit_threshold=params["profit_threshold"],
            loss_threshold=params["loss_threshold"]
        )
        return strategy_xml
        
    except Exception as e:
        error_msg = f"Error generating strategy: {str(e)}"
        ctx.error(error_msg)
        return error_msg

if __name__ == "__main__":
    mcp.run()
