# IntentKit CLI Examples

This folder contains command-line examples demonstrating IntentKit functionality.

## Stream Agent Demo

The `main.py` script demonstrates how to interact with the IntentKit `stream_agent` function in an interactive way.

### What it does

1. **Takes keyboard input** from the user
2. **Converts it to ChatMessageCreate** with proper configuration
3. **Streams agent execution results** using the `stream_agent` function
4. **Displays results using debug_format** to show detailed execution information
5. **Loops for continuous interaction** until the user types 'quit' or 'exit'

### Usage

This is a **standalone demo** that can be run independently of the main IntentKit project. Here are several ways to run it:

#### Method 1: Using uv run (Recommended)

From the `examples/cli` directory:
```bash
cd examples/cli
uv run python main.py
```

#### Method 2: As a Python module

From the `examples/cli` directory:
```bash
cd examples/cli  
uv run python -m .
```

#### Method 3: Install and use as a script

```bash
cd examples/cli
uv pip install -e .
uv run intentkit-demo
```

#### Method 4: With explicit project specification

From anywhere in the repository:
```bash
uv run --project examples/cli python main.py
```

#### Method 5: Traditional Python (if dependencies are installed)

```bash
cd examples/cli
python main.py
```

### Example Session

```
=== IntentKit Stream Agent Demo ===
This demo shows how to interact with the stream_agent function.
Type 'quit' or 'exit' to stop.

Enter Agent ID (or press Enter for demo agent): my-agent-123
Using Agent ID: my-agent-123
Chat ID: demo-chat-01234567890abcdef
User ID: demo-user-01234567890abcdef

You: Hello, can you help me?

============================================================
STREAMING AGENT RESPONSE:
============================================================

--- Response 1 ---
[ Agent cold start ... ]

------------------- start cost: 2.145 seconds

--- Response 2 ---
[ Agent: ] (2024-01-15 10:30:45 UTC)

 Hello! I'd be happy to help you. What can I assist you with today?

------------------- agent cost: 1.203 seconds

----------------------------------------

============================================================
END OF RESPONSE
============================================================

You: quit
Goodbye!
```

### Features

- **Interactive input loop**: Continuously accepts user input until 'quit' or 'exit'
- **Proper ChatMessageCreate construction**: Shows how to create valid message objects
- **Real-time streaming**: Demonstrates the async streaming nature of the agent
- **Debug formatting**: Uses the built-in `debug_format()` method to show detailed execution info
- **Error handling**: Gracefully handles errors and allows continuation
- **Unique IDs**: Generates proper XID identifiers for messages and chats

### Requirements

- The IntentKit environment must be properly set up
- Database connections must be configured
- The specified agent must exist in the system

### Notes

- The script uses `AuthorType.WEB` to simulate web-based interactions
- Each run creates a new chat session with unique IDs
- The demo shows timing information, token counts, and execution costs
- Cold start costs are displayed when the agent is first initialized

### Dependencies

This example uses the `intentkit` package as defined in the workspace `pyproject.toml`. The dependencies are managed through the workspace configuration.
