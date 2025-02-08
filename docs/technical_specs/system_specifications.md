# docs/technical_specs/system_specifications.md
# Technical Specifications

## System Requirements

### Hardware Requirements
- CPU: 2+ cores recommended
- RAM: 4GB minimum, 8GB recommended
- Storage: 1GB for base installation

### Software Requirements
- Python 3.9+
- Docker (optional)
- Git

### Network Requirements
- Outbound HTTPS access for LLM API calls
- Local network access for LM Studio

## Performance Specifications

### Response Times
- Analysis requests: < 2 seconds
- Code modifications: < 5 seconds
- Test generation: < 3 seconds

### Concurrency
- Maximum concurrent requests: 10
- Maximum workspace size: 1GB
- Maximum file size: 10MB

[Detailed Specifications](./detailed_specs.md)
