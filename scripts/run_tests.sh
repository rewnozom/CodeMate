# scripts/run_tests.sh
#!/bin/bash

# Run all tests
echo "Running tests..."
pytest tests/ -v --cov=src --cov-report=term-missing