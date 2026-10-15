#!/usr/bin/env bash
set -Eeuo pipefail

# Phantasie III — Linux development environment
PROJECT_DIR="${HOME}/Code/phantasie"
VENV_DIR="${PROJECT_DIR}/.venv"

echo "==> Setting up Phantasie III development environment"

# Check for Debian/Ubuntu package manager.
if ! command -v apt-get >/dev/null 2>&1; then
    echo "ERROR: This script requires Debian/Ubuntu Linux." >&2
    exit 1
fi

# Install system dependencies.
echo "==> Installing system packages"
sudo apt-get update

sudo apt-get install -y \
    python3 \
    python3-dev \
    python3-venv \
    python3-pip \
    build-essential \
    pkg-config \
    git \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev

# Create the project directory.
echo "==> Creating project directory"
mkdir -p "${PROJECT_DIR}"
cd "${PROJECT_DIR}"

# Create or reuse the virtual environment.
if [[ ! -d "${VENV_DIR}" ]]; then
    echo "==> Creating Python virtual environment"
    python3 -m venv "${VENV_DIR}"
fi

# Activate the virtual environment.
# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

# Install Python dependencies.
echo "==> Installing Python packages"
python -m pip install --upgrade pip setuptools wheel
python -m pip install pygame pytest ruff mypy

# Create the project structure.
echo "==> Creating project directories"
mkdir -p \
    src/phantasie \
    tests \
    assets/images \
    assets/audio \
    assets/fonts \
    docs

# Record runtime dependencies.
cat > requirements.txt <<'EOF'
pygame
EOF

# Record development dependencies.
cat > requirements-dev.txt <<'EOF'
-r requirements.txt
pytest
ruff
mypy
EOF

# Create .gitignore if it doesn't exist.
if [[ ! -f .gitignore ]]; then
    cat > .gitignore <<'EOF'
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
.pytest_cache/
.ruff_cache/
.mypy_cache/
.coverage
htmlcov/
.vscode/
.idea/
saves/
*.sav
EOF
fi

# Initialize Git if needed.
if [[ ! -d .git ]]; then
    git init
fi

# Verify the installation.
echo
echo "==> Verifying installation"
python --version
python -c "import pygame; print('Pygame:', pygame.version.ver)"
git --version

echo
echo "==> Development environment ready!"
echo "Project directory: ${PROJECT_DIR}"
echo
echo "Activate the environment with:"
echo "  cd ~/Code/phantasie"
echo "  source .venv/bin/activate"
echo
echo "Install development dependencies later with:"
echo "  python -m pip install -r requirements-dev.txt"

cd ~/Code/phantasie
source .venv/bin/activate
python -c "import pygame; print(pygame.version.ver)"
python -m pytest --version

