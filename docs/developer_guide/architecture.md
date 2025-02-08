# docs/developer_guide/architecture.md
# System Architecture

## Overview

The Semi-Autonomous Agent system is built with a modular architecture focusing on:
- Separation of concerns
- Event-driven communication
- Extensibility
- Robust error handling

## Key Components

### Core Layer
- AgentCoordinator: Central coordination
- StateManager: State management
- WorkflowManager: Workflow handling

### Service Layer
- FileAnalyzer: Code analysis
- TestManager: Test management
- ValidationManager: Code validation

### Interface Layer
- CLIInterface: Command line interface
- ResponseFormatter: Output formatting
- RequestHandler: Request processing

## Workflow

1. Request Handling
2. State Management
3. Task Execution
4. Result Generation

[See detailed architecture...](./detailed_architecture.md)
