#!/usr/bin/env python3
from flask import Flask, request, jsonify
from strategy_generator import StrategyGenerator
from strategy_parser import StrategyParser

app = Flask(__name__)

# Initialize components
generator = StrategyGenerator()
parser = StrategyParser()

@app.route('/generate_strategy', methods=['POST'])
def generate_strategy():
    """Generate a trading strategy from description"""
    try:
        # Get prompt from request JSON
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt in request body'}), 400
            
        prompt = data['prompt']
        
        # Parse parameters from prompt
        params = parser.parse_prompt(prompt)
        
        if not parser.validate_parameters(params):
            return jsonify({'error': 'Could not extract valid parameters from prompt'}), 400
            
        # Generate strategy XML
        strategy_xml = generator.generate_strategy(
            duration=params["duration"],
            stake=params["stake"],
            initial_stake=params["initial_stake"],
            profit_threshold=params["profit_threshold"],
            loss_threshold=params["loss_threshold"]
        )
        
        return jsonify({'strategy': strategy_xml})
        
    except Exception as e:
        return jsonify({'error': f'Error generating strategy: {str(e)}'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
