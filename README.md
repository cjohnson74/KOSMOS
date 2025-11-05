# KOSMOS
AI Agents controlling Kerbal Space Program.

## Prerequisites
- **Kerbal Space Program** installed
- **Python 3.8+** installed
- **Poetry** for dependency management
- **OpenAI API key** for the language models

## Installation

### 1. Install Poetry (if not already installed)
```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Or via Homebrew on macOS
brew install poetry
```

### 2. Install KSP Mods
Install the **kRPC mod** for Kerbal Space Program:
- Download and install **CKAN** (KSP mod manager): https://krpc.github.io/krpc/getting-started.html
- Use CKAN to install the **kRPC** mod

### 3. Install Python Dependencies
```bash
# Clone this repository
git clone https://github.com/yourusername/KOSMOS.git
cd KOSMOS

# Install dependencies with Poetry
poetry install
```

## Getting Started

KOSMOS uses OpenAI's GPT-4 as the language model. You need to have an OpenAI API key to use KOSMOS. You can get one from [here](https://platform.openai.com/api-keys).

After the installation process, you can run KOSMOS by:

```python
from kosmos import Kosmos

openai_api_key = "YOUR_API_KEY"

kosmos = Kosmos(
    openai_api_key=openai_api_key,
)

# Start mission execution
kosmos.learn()
```

If you are running KOSMOS for the first time, make sure to:
1. **Launch Kerbal Space Program**
2. **Load a scenario or flight** (make sure you have an active vessel)
3. **Start the kRPC server** in KSP (usually via the kRPC menu)
4. **Run the Python script**

## Usage Examples

### Basic Mission Execution
```python
from kosmos import Kosmos

kosmos = Kosmos(
    openai_api_key="YOUR_API_KEY",
)

# Start lifelong learning and mission execution
kosmos.learn()
```

### Resume from Checkpoint
If you stop the learning process and want to resume from a checkpoint later:

```python
from kosmos import Kosmos

kosmos = Kosmos(
    openai_api_key="YOUR_API_KEY",
    checkpoint_dir="YOUR_CKPT_DIR",
    resume=True,
)

# Resume mission from checkpoint
kosmos.learn()
```

### Execute Specific Task
If you want to run KOSMOS for a specific task:

```python
from kosmos import Kosmos

# First instantiate KOSMOS with maneuver library
kosmos = Kosmos(
    openai_api_key="YOUR_API_KEY",
    maneuver_library_dir="./maneuver_library/trial1",  # Load learned maneuvers
    checkpoint_dir="YOUR_CKPT_DIR",
    resume=False,
)

# Run task decomposition
task = "Launch to orbit"  # e.g. "Launch to orbit", "Land on Mun", "Dock with space station"
sub_goals = kosmos.decompose_task(task=task)

# Execute the sub-goals
kosmos.execute_task(sub_goals=sub_goals)
```

## Quick Start

1. **Set your OpenAI API key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Launch KSP and start kRPC server**

3. **Run KOSMOS:**
   ```bash
   poetry run python main.py
   ```

## Project Structure
- `main.py` - Main entry point
- `kosmos/` - Core KOSMOS package
  - `agents/` - AI agents (Flight, Mission Control, Maneuver, Audit)
  - `env/` - KSP environment interface
  - `utils/` - Utility functions
  - `control_primitives/` - Executable maneuver implementations
  - `control_primitives_context/` - Context examples for AI agents
- `examples/` - Usage examples
- `checkpoint/` - Checkpoint directory (created automatically)

## Available Agents

- **FlightAgent** ✅ - Executes flight maneuvers and controls vessels
- **MissionControlAgent** ⚠️ - Plans and coordinates mission phases
- **ManeuverAgent** ⚠️ - Manages specific maneuver execution
- **AuditAgent** ⚠️ - Monitors and validates mission progress

## Development

To add new dependencies:
```bash
poetry add package-name
```

To run with Poetry:
```bash
poetry run python main.py
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License
See [LICENSE](LICENSE) file for details.