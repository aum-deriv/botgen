class StrategyGenerator:
    def __init__(self):
        self.variables = {}
        
    def add_variable(self, var_id, var_name, var_type="", is_local=False, is_cloud=False):
        """Add a variable definition to the strategy"""
        self.variables[var_id] = {
            "type": var_type,
            "id": var_id,
            "name": var_name,
            "islocal": str(is_local).lower(),
            "iscloud": str(is_cloud).lower()
        }

    def generate_variables_section(self):
        """Generate the variables section of the XML"""
        xml = '  <variables>\n'
        for var in self.variables.values():
            xml += f'    <variable type="{var["type"]}" id="{var["id"]}" '
            xml += f'islocal="{var["islocal"]}" iscloud="{var["iscloud"]}">{var["name"]}</variable>\n'
        xml += '  </variables>\n'
        return xml

    def generate_trade_definition(self, market="synthetic_index", submarket="random_index", symbol="1HZ10V", duration=1, stake=1):
        """Generate the trade definition section with required hierarchy and trade options"""
        return f'''
  <block type="trade_definition" id="trade_def_main" deletable="false" x="0" y="0">
    <statement name="TRADE_OPTIONS">
      <block type="trade_definition_market" id="market_def" deletable="false" movable="false">
        <field name="MARKET_LIST">{market}</field>
        <field name="SUBMARKET_LIST">{submarket}</field>
        <field name="SYMBOL_LIST">{symbol}</field>
        <next>
          <block type="trade_definition_tradetype" id="tradetype_def" deletable="false" movable="false">
            <field name="TRADETYPECAT_LIST">callput</field>
            <field name="TRADETYPE_LIST">callput</field>
            <next>
              <block type="trade_definition_contracttype" id="contracttype_def" deletable="false" movable="false">
                <field name="TYPE_LIST">both</field>
                <next>
                  <block type="trade_definition_candleinterval" id="candleinterval_def" deletable="false" movable="false">
                    <field name="CANDLEINTERVAL_LIST">60</field>
                    <next>
                      <block type="trade_definition_restartbuysell" id="restart_def" deletable="false" movable="false">
                        <field name="TIME_MACHINE_ENABLED">FALSE</field>
                        <next>
                          <block type="trade_definition_restartonerror" id="error_def" deletable="false" movable="false">
                            <field name="RESTARTONERROR">TRUE</field>
                            <next>
                              <block type="trade_definition_tradeoptions" id="tradeoptions_def">
                                <mutation has_first_barrier="false" has_second_barrier="false" has_prediction="false"></mutation>
                                <field name="DURATIONTYPE_LIST">t</field>
                                <value name="DURATION">
                                  <shadow type="math_number">
                                    <field name="NUM">{duration}</field>
                                  </shadow>
                                </value>
                                <value name="AMOUNT">
                                  <shadow type="math_number">
                                    <field name="NUM">{stake}</field>
                                  </shadow>
                                </value>
                              </block>
                            </next>
                          </block>
                        </next>
                      </block>
                    </next>
                  </block>
                </next>
              </block>
            </next>
          </block>
        </next>
      </block>
    </statement>
'''

    def generate_initialization(self, initial_stake=1, profit_threshold=1000, loss_threshold=500):
        """Generate initialization block with standard variables"""
        return f'''
    <statement name="INITIALIZATION">
      <block type="variables_set" id="initial_stake_set">
        <field name="VAR" id="initial_stake_var">Initial Stake</field>
        <value name="VALUE">
          <shadow type="math_number">
            <field name="NUM">{initial_stake}</field>
          </shadow>
        </value>
        <next>
          <block type="variables_set" id="profit_threshold_set">
            <field name="VAR" id="profit_threshold_var">Profit Threshold</field>
            <value name="VALUE">
              <shadow type="math_number">
                <field name="NUM">{profit_threshold}</field>
              </shadow>
            </value>
            <next>
              <block type="variables_set" id="loss_threshold_set">
                <field name="VAR" id="loss_threshold_var">Loss Threshold</field>
                <value name="VALUE">
                  <shadow type="math_number">
                    <field name="NUM">{loss_threshold}</field>
                  </shadow>
                </value>
              </block>
            </next>
          </block>
        </next>
      </block>
    </statement>
  </block>
'''

    def generate_before_purchase(self, contract_type="CALL"):
        """Generate the before purchase block with standard structure"""
        return f'''
  <block type="before_purchase" id="before_purchase" deletable="false">
    <statement name="BEFOREPURCHASE_STACK">
      <block type="purchase" id="purchase">
        <field name="PURCHASE_LIST">{contract_type}</field>
      </block>
    </statement>
  </block>
'''

    def generate_after_purchase(self, conditions=None):
        """Generate the after purchase block with trade again logic"""
        conditions_xml = ""
        if conditions:
            conditions_xml = conditions
        
        return f'''
  <block type="after_purchase" id="after_purchase">
    <statement name="AFTERPURCHASE_STACK">
      <block type="controls_if" id="trade_again_condition">
        <value name="IF0">
          {conditions_xml if conditions_xml else '''
          <block type="logic_compare">
            <field name="OP">LT</field>
            <value name="A">
              <block type="read_details">
                <field name="DETAIL_INDEX">4</field>
              </block>
            </value>
            <value name="B">
              <block type="variables_get">
                <field name="VAR" id="profit_threshold_var">Profit Threshold</field>
              </block>
            </value>
          </block>
          '''}
        </value>
        <statement name="DO0">
          <block type="trade_again" id="trade_again"></block>
        </statement>
      </block>
    </statement>
  </block>
'''

    def create_contract_check(self, result_type="win"):
        """Create a contract check result block"""
        return f'''
          <block type="contract_check_result">
            <field name="CHECK_RESULT">{result_type}</field>
          </block>
'''

    def create_read_details(self, detail_index):
        """Create a read details block"""
        return f'''
          <block type="read_details">
            <field name="DETAIL_INDEX">{detail_index}</field>
          </block>
'''

    def create_purchase(self, contract_type="CALL"):
        """Create a purchase block"""
        return f'''
          <block type="purchase">
            <field name="PURCHASE_LIST">{contract_type}</field>
          </block>
'''

    def create_trade_again(self):
        """Create a trade again block"""
        return '''
          <block type="trade_again"></block>
'''

    def generate_strategy(self, duration=1, stake=1, initial_stake=1, profit_threshold=1000, loss_threshold=500):
        """Generate complete strategy XML with proper structure"""
        # Add standard variables
        self.add_variable("initial_stake_var", "Initial Stake")
        self.add_variable("current_stake_var", "Current Stake")
        self.add_variable("profit_threshold_var", "Profit Threshold")
        self.add_variable("loss_threshold_var", "Loss Threshold")
        self.add_variable("total_profit_var", "Total Profit")
        
        # Start XML
        xml = '''<?xml version="1.0" encoding="UTF-8"?>
<xml xmlns="http://www.w3.org/1999/xhtml" is_dbot="true" collection="false">
'''
        
        # Add variables section
        xml += self.generate_variables_section()
        
        # Add trade definition with parameters
        xml += self.generate_trade_definition(duration=duration, stake=stake)
        
        # Add initialization with parameters
        xml += self.generate_initialization(
            initial_stake=initial_stake,
            profit_threshold=profit_threshold,
            loss_threshold=loss_threshold
        )
        
        # Add before and after purchase blocks
        xml += self.generate_before_purchase()
        xml += self.generate_after_purchase()
        
        # Close XML
        xml += "</xml>"
        
        return xml

def example_usage():
    """Example of how to use the StrategyGenerator"""
    generator = StrategyGenerator()
    
    # Generate a basic strategy with custom parameters
    strategy_xml = generator.generate_strategy(
        duration=5,          # 5 tick duration
        stake=10,           # Initial stake amount
        initial_stake=10,   # Starting stake
        profit_threshold=100,  # Stop at 100 profit
        loss_threshold=50    # Stop at 50 loss
    )
    
    # Save to file
    with open("generated_strategy.xml", "w") as f:
        f.write(strategy_xml)

if __name__ == "__main__":
    example_usage()
