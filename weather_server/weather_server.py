from mcp.server.fastmcp import FastMCP, Context
from mcp.server.fastmcp.prompts.base import Message, UserMessage, AssistantMessage
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Create MCP server
mcp = FastMCP("Weather")

@mcp.prompt()
def weather_prompt(message: str, ctx: Context) -> list[Message]:
    """Handle weather-related prompts"""
    return [
        UserMessage(message),
        AssistantMessage("Let me check the weather conditions for you.")
    ]

@mcp.tool()
def get_weather(city: str, ctx: Context) -> str:
    """Get current weather for a city"""
    ctx.info(f"Fetching weather data for {city}")
    
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        
        weather_info = f"""
Weather in {data['name']}, {data.get('sys', {}).get('country', '')}:
Temperature: {main['temp']}°C
Feels like: {main['feels_like']}°C
Condition: {weather['description'].capitalize()}
Humidity: {main['humidity']}%
Wind Speed: {wind['speed']} m/s
        """.strip()
        
        ctx.info("Weather data retrieved successfully")
        return weather_info
        
    except requests.exceptions.HTTPError as e:
        error_msg = f"Sorry, I couldn't find weather data for '{city}'. Please check the city name and try again." if e.response.status_code == 404 else f"Error fetching weather data: {str(e)}"
        ctx.error(error_msg)
        return error_msg
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to weather service: {str(e)}"
        ctx.error(error_msg)
        return error_msg
    except KeyError as e:
        error_msg = f"Error parsing weather data: {str(e)}"
        ctx.error(error_msg)
        return error_msg

if __name__ == "__main__":
    mcp.run()
