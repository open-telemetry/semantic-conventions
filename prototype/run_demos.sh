#!/bin/bash
# Multi-Backend Demo Runner
# Runs GenAI Security Guardian demos against different trace backends
#
# Usage:
#   ./run_demos.sh all          # Run for all backends
#   ./run_demos.sh appinsights  # Run for App Insights only
#   ./run_demos.sh laminar      # Run for Laminar only
#   ./run_demos.sh langfuse     # Run for Langfuse only
#   ./run_demos.sh traceloop    # Run for Traceloop only

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Load environment variables
if [ -f .env.local ]; then
    set -a
    source .env.local
    set +a
    echo -e "${GREEN}[OK]${NC} Loaded .env.local"
else
    echo -e "${RED}[ERROR]${NC} .env.local not found. Copy .env.example to .env.local and fill in credentials."
    exit 1
fi

print_header() {
    echo ""
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}================================================================${NC}"
}

run_for_backend() {
    local backend=$1
    local venv=$2
    local exporters=$3
    local requirements=$4

    print_header "Running demos for: $backend"

    if [ ! -d "$venv" ]; then
        echo -e "${RED}[ERROR]${NC} Virtual environment $venv not found"
        echo "       Run: python3 -m venv $venv && source $venv/bin/activate && pip install -r $requirements"
        return 1
    fi

    source "$venv/bin/activate"
    python run_all_demos.py --exporters "$exporters" 2>&1
    deactivate 2>/dev/null || true

    echo -e "${GREEN}[OK]${NC} Completed $backend run"
}

# Main logic
case "${1:-all}" in
    appinsights|app-insights|azure)
        run_for_backend "Azure Application Insights" ".venv-appinsights" "appinsights" "requirements-appinsights.txt"
        ;;
    laminar|lmnr)
        run_for_backend "Laminar" ".venv-appinsights" "laminar" "requirements-appinsights.txt"
        ;;
    langfuse)
        run_for_backend "Langfuse" ".venv-appinsights" "langfuse" "requirements-appinsights.txt"
        ;;
    traceloop)
        run_for_backend "Traceloop" ".venv" "traceloop" "requirements-traceloop.txt"
        ;;
    all)
        print_header "Running demos for ALL backends"
        echo ""
        echo "This will run demos 4 times, once per backend."
        echo "Traces will appear in each respective UI."
        echo ""

        # Run App Insights, Laminar, Langfuse with compatible venv
        run_for_backend "Azure Application Insights" ".venv-appinsights" "appinsights" "requirements-appinsights.txt"
        sleep 2

        run_for_backend "Laminar" ".venv-appinsights" "laminar" "requirements-appinsights.txt"
        sleep 2

        run_for_backend "Langfuse" ".venv-appinsights" "langfuse" "requirements-appinsights.txt"
        sleep 2

        # Run Traceloop with its own venv (has SDK that sets up its own provider)
        run_for_backend "Traceloop" ".venv" "traceloop" "requirements-traceloop.txt"

        print_header "All backends completed!"
        echo ""
        echo "Check your trace backends:"
        echo "  - App Insights: https://portal.azure.com/ > Application Insights"
        echo "  - Laminar: https://www.lmnr.ai/"
        echo "  - Langfuse: https://us.cloud.langfuse.com/"
        echo "  - Traceloop: https://app.traceloop.com/"
        ;;
    combined)
        # Run all compatible backends together (not Traceloop due to conflicts)
        run_for_backend "App Insights + Laminar + Langfuse" ".venv-appinsights" "appinsights,laminar,langfuse" "requirements-appinsights.txt"
        ;;
    *)
        echo "Usage: $0 {all|appinsights|laminar|langfuse|traceloop|combined}"
        echo ""
        echo "  all         - Run demos for all backends (4 separate runs)"
        echo "  appinsights - Run demos for Azure Application Insights only"
        echo "  laminar     - Run demos for Laminar only"
        echo "  langfuse    - Run demos for Langfuse only"
        echo "  traceloop   - Run demos for Traceloop only"
        echo "  combined    - Run demos with App Insights + Laminar + Langfuse together"
        exit 1
        ;;
esac
