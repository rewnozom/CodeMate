# docs/api_reference/api_specification.md
# API Reference

## Core API

### AgentCoordinator API
```yaml
name: AgentCoordinator
endpoints:
  process_request:
    method: POST
    path: /api/v1/process
    parameters:
      - name: request
        type: object
        required: true
        schema:
          type: object
          properties:
            type: string
            data: object
    responses:
      200:
        description: Successfully processed request
        schema:
          type: object
          properties:
            success: boolean
            result: object
      400:
        description: Invalid request
      500:
        description: Internal server error
```

### StateManager API
```yaml
name: StateManager
endpoints:
  update_state:
    method: PUT
    path: /api/v1/state
    parameters:
      - name: state
        type: string
        required: true
      - name: metadata
        type: object
    responses:
      200:
        description: State updated successfully
```

[Full API Reference](./api_full.md)
