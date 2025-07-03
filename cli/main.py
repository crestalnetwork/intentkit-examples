#!/usr/bin/env python3
"""
Demo script for stream_agent functionality.

This script demonstrates how to:
1. Take keyboard input from the user
2. Convert it to ChatMessageCreate
3. Stream agent execution results
4. Display results using debug_format
5. Loop for continuous interaction

Usage: python main.py
"""

import asyncio
import sys
import logging
from epyxid import XID

from intentkit.core.engine import stream_agent
from intentkit.models.chat import ChatMessageCreate, AuthorType
from intentkit.config.config import config
from intentkit.models.db import init_db, get_session
from intentkit.models.agent import AgentTable
from sqlalchemy import select


async def create_example_agent() -> None:
    """Create an example agent if no agents exist in the database.

    Creates an agent with ID 'example' and basic configuration if the agents table is empty.
    The agent is configured with the 'system' skill with 'read_agent_api_key' state set to 'private'.
    """
    logger = logging.getLogger(__name__)
    try:
        async with get_session() as session:
            # Check if any agents exist - more efficient count query
            result = await session.execute(
                select(select(AgentTable.id).limit(1).exists().label("exists"))
            )
            if result.scalar():
                logger.debug("Example agent not created: agents already exist")
                return  # Agents exist, nothing to do

            # Create example agent
            example_agent = AgentTable(
                id="example",
                name="Example",
                owner="intentkit",
                skills={
                    "system": {
                        "states": {"read_agent_api_key": "private"},
                        "enabled": True,
                    }
                },
            )

            session.add(example_agent)
            await session.commit()
            logger.info("Created example agent with ID 'example'")
    except Exception as e:
        logger.error(f"Failed to create example agent: {str(e)}")
        # Don't re-raise the exception to avoid blocking demo startup


async def main():
    """Main demo function."""
    print("=== IntentKit Stream Agent Demo ===")
    print("This demo shows how to interact with the stream_agent function.")
    print("Type 'quit' or 'exit' to stop.\n")
    
    # Initialize database and create example agent
    print("Initializing database...")
    try:
        # Extract db config parameters explicitly to handle auto_migrate type conversion
        auto_migrate_value = config.db.get("auto_migrate", True)
        if isinstance(auto_migrate_value, str):
            auto_migrate = auto_migrate_value.lower() == "true"
        else:
            auto_migrate = bool(auto_migrate_value) if auto_migrate_value is not None else True
        
        await init_db(
            host=config.db.get("host"),
            username=config.db.get("username"), 
            password=config.db.get("password"),
            dbname=config.db.get("dbname"),
            port=config.db.get("port", "5432"),
            auto_migrate=auto_migrate
        )
        print("Database initialized successfully.")
        
        print("Creating example agent...")
        await create_example_agent()
        print("Example agent setup complete.")
    except Exception as e:
        print(f"Error during initialization: {e}")
        return
    
    # Demo configuration - hardcoded to use "example"
    AGENT_ID = "example"
    CHAT_ID = "example"
    USER_ID = "example"
    
    print(f"Using Agent ID: {AGENT_ID}")
    print(f"Chat ID: {CHAT_ID}")
    print(f"User ID: {USER_ID}\n")
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            # Check for exit conditions
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
                
            if not user_input:
                print("Please enter a message or 'quit' to exit.")
                continue
            
            # Create ChatMessageCreate object
            message = ChatMessageCreate(
                id=str(XID()),
                agent_id=AGENT_ID,
                chat_id=CHAT_ID,
                user_id=USER_ID,
                author_id=USER_ID,
                author_type=AuthorType.WEB,
                model=None,
                thread_type=AuthorType.WEB,
                reply_to=None,
                message=user_input,
                attachments=None,
                skill_calls=None,
                input_tokens=0,
                output_tokens=0,
                time_cost=0.0,
                credit_event_id=None,
                credit_cost=None,
                cold_start_cost=0.0
            )
            
            print("\n" + "="*60)
            print("STREAMING AGENT RESPONSE:")
            print("="*60 + "\n")
            
            # Stream the agent response
            response_count = 0
            async for chat_message in stream_agent(message):
                response_count += 1
                print(f"--- Response {response_count} ---")
                print(chat_message.debug_format())
                print("-" * 40)
            
            if response_count == 0:
                print("No response received from agent.")
            
            print("\n" + "="*60)
            print("END OF RESPONSE")
            print("="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"\nError occurred: {e}")
            print(f"Error type: {type(e).__name__}")
            
            # Ask if user wants to continue
            continue_choice = input("Do you want to continue? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                break


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDemo terminated by user.")
        sys.exit(0)
