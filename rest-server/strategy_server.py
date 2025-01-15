#!/usr/bin/env python3
import os
import anthropic
from mcp.server.fastmcp import FastMCP, Context
from strategy_generator import StrategyGenerator
from strategy_parser import StrategyParser

# Create MCP server
mcp = FastMCP("Strategy")

# Initialize components
generator = StrategyGenerator()
parser = StrategyParser()

# Initialize Anthropic client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

@mcp.prompt()
def strategy_prompt(message: str, ctx: Context) -> str:
    """Handle strategy-related prompts"""
    response = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": message
        }]
    )
    return response.content

@mcp.tool()
def generate_strategy(prompt: str, ctx: Context) -> str:
    """Generate a trading strategy from description"""
    try:
        # Parse parameters from prompt using context
        params = parser.parse_prompt(prompt, ctx)
        
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
