# docs/user_guide/getting_started.md
# Getting Started

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/semi-autonomous-agent.git
cd semi-autonomous-agent
```

2. Set up the environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements/dev.txt
```

3. Configure the agent:
- Copy `.env.example` to `.env`
- Update configuration in `config/default.yaml`

## Basic Usage

### Command Line Interface

Start the agent:
```bash
python src/main.py start
```

Process a request:
```bash
python src/main.py process "analyze the file main.py"
```

[Continue reading...](./usage.md)
