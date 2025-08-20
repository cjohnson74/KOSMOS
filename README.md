# KOSMOS
AI Agents controlling Kerbal Space Program.

## Prerequisites
- **Kerbal Space Program** installed
- **Python 3.8+** installed
- **Poetry** for dependency management

## Setup

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

### 4. Usage

1. **Launch Kerbal Space Program**
2. **Load a scenario or flight** (make sure you have an active vessel)
3. **Start the kRPC server** in KSP (usually via the kRPC menu)
4. **Run the Python script:**
   ```bash
   poetry run python main.py
   ```

## Project Structure
- `main.py` - Basic vessel position streaming example
- `pyproject.toml` - Poetry configuration and dependencies
- `poetry.lock` - Locked dependency versions

## Example Output
The basic script will stream your vessel's position coordinates in real-time:
```
0.5.4
(2688577.068673832, -7.589481473858227, 465412.3802019775)
(2688577.068673832, -7.589481473858227, 465412.3802019775)
...
```

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
