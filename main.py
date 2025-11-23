from fastmcp import FastMCP
import random
import json

# Create a FastMCP instance 
mcp = FastMCP("Simple Calculator Server")

# Tool: Add two number
@mcp.tool
def add(a:int, b:int) -> int:
    '''Add two numbers together
        Args:
            a: First number
            b: Second number
        Returns:
            Sum of a and b
    
    '''
    return a + b

# tool to generate random number
@mcp.tool
def random_number(min_value: int = 1, max_value: int = 100) -> int:
    '''Generate a random number between min_value and max_value
        Args:
            min_value: Minimum value of the range
            max_value: Maximum value of the range
        Returns:
            Random number between min_value and max_value
    '''
    return random.randint(min_value, max_value) 


# Resources: Server information
@mcp.resource("info://server")
def server_info() -> str:
    '''Get information about this server'''
    info = {
        'name' : 'Simple Calculator Server',
        'version' : '1.0.0',
        'description' : 'A basic MCP server with math tools',
        'tools' : ["add", "random_number"],
        "author" : "Darwin Acharya"
    }
    return json.dumps(info, indent=2)


# Start the server
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)

    