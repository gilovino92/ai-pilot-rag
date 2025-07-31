from typing import Dict, Type
from abc import ABC, abstractmethod
from app.core.ai_agents.openai_agent import OpenAIAgent


class BaseAIAgent(ABC):
    """Base class for all AI agents."""
    
    @abstractmethod
    def initialize(self):
        """Initialize the AI agent."""
        pass

    @abstractmethod
    def get_client(self):
        """Get the AI client instance."""
        pass


class OpenAIAgentWrapper(BaseAIAgent):
    """Wrapper for OpenAI agent implementation."""
    
    def __init__(self):
        self._agent = OpenAIAgent()
        self._client = None
        self.initialize()

    def initialize(self):
        """Initialize the OpenAI agent."""
        self._client = self._agent.client

    def get_client(self):
        """Get the OpenAI client instance."""
        return self._client


class AIAgentFactory:
    """Factory class for creating AI agents."""
    
    _agents: Dict[str, Type[BaseAIAgent]] = {
        "openai": OpenAIAgentWrapper,
    }

    @classmethod
    def create_agent(cls, agent_type: str) -> BaseAIAgent:
        """
        Create an AI agent instance based on the specified type.
        
        Args:
            agent_type: Type of agent to create ("openai")
            
        Returns:
            An instance of the specified AI agent
            
        Raises:
            ValueError: If the specified agent type is not supported
        """
        if agent_type not in cls._agents:
            raise ValueError(f"Unsupported agent type: {agent_type}")
        
        agent_class = cls._agents[agent_type]
        return agent_class()

    @classmethod
    def register_agent(cls, name: str, agent_class: Type[BaseAIAgent]):
        """
        Register a new AI agent type.
        
        Args:
            name: Name of the agent type
            agent_class: Class implementing the BaseAIAgent interface
        """
        cls._agents[name] = agent_class