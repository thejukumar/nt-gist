#!/usr/bin/env bash
# ===========================================================================
# Support Context Budget Lab — one-command local setup + run.
#
#   ./run.sh            install deps (if needed) and start backend + frontend
#   ./run.sh --install  install/refresh dependencies only, then exit
#   ./run.sh --check     verify prerequisites + env, then exit
#
# No Docker. Everything runs on your local machine.
# Prerequisites (the script checks these for you): uv, node, npm.
# ===========================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

# --- pretty logging -------------------------------------------------------
c_reset="\033[0m"; c_blue="\033[34m"; c_green="\033[32m"; c_yellow="\033[33m"; c_red="\033[31m"
info()  { echo -e "${c_blue}➜${c_reset} $*"; }
ok()    { echo -e "${c_green}✓${c_reset} $*"; }
warn()  { echo -e "${c_yellow}!${c_reset} $*"; }
die()   { echo -e "${c_red}✗ $*${c_reset}" >&2; exit 1; }

# --- prerequisite checks --------------------------------------------------
check_prereqs() {
  info "Checking prerequisites..."
  command -v uv   >/dev/null 2>&1 || die "uv not found. Install: curl -LsSf https://astral.sh/uv/install.sh | sh"
  command -v node >/dev/null 2>&1 || die "node not found. Install Node.js 18+ from https://nodejs.org"
  command -v npm  >/dev/null 2>&1 || die "npm not found. It ships with Node.js."
  ok "uv $(uv --version | awk '{print $2}'), node $(node --version), npm $(npm --version)"
}

# --- .env handling --------------------------------------------------------
check_env() {
  if [ ! -f "$ROOT_DIR/.env" ]; then
    warn ".env not found — creating one from .env.example"
    cp "$ROOT_DIR/.env.example" "$ROOT_DIR/.env"
    warn "Edit .env and add TAVILY_API_KEY and NEBIUS_API_KEY, then re-run ./run.sh"
    exit 1
  fi
  # shellcheck disable=SC1090
  set -a; source "$ROOT_DIR/.env"; set +a
  local missing=()
  [ -z "${TAVILY_API_KEY:-}" ] || [[ "${TAVILY_API_KEY}" == tvly-... ]] && missing+=("TAVILY_API_KEY")
  [ -z "${NEBIUS_API_KEY:-}" ] && missing+=("NEBIUS_API_KEY")
  if [ "${#missing[@]}" -gt 0 ]; then
    die "Missing required env vars in .env: ${missing[*]}"
  fi
  ok ".env present with required keys"
}

# --- dependency installation ----------------------------------------------
install_deps() {
  info "Installing backend dependencies (uv sync)..."
  (cd "$BACKEND_DIR" && uv sync)
  ok "Backend deps ready"

  info "Installing frontend dependencies (npm install)..."
  (cd "$FRONTEND_DIR" && npm install --silent)
  ok "Frontend deps ready"
}

# --- run both servers -----------------------------------------------------
run_all() {
  local host="${BACKEND_HOST:-127.0.0.1}" port="${BACKEND_PORT:-8000}"
  info "Starting backend  → http://${host}:${port}"
  (cd "$BACKEND_DIR" && uv run uvicorn main:app --host "$host" --port "$port" --reload) &
  BACKEND_PID=$!

  info "Starting frontend → http://localhost:3000"
  (cd "$FRONTEND_DIR" && npm run dev) &
  FRONTEND_PID=$!

  trap 'echo; info "Shutting down..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true' INT TERM EXIT
  ok "Both servers running. Press Ctrl+C to stop."
  wait
}

# --- entrypoint -----------------------------------------------------------
main() {
  case "${1:-}" in
    --check)   check_prereqs; check_env; ok "All checks passed." ;;
    --install) check_prereqs; check_env; install_deps; ok "Install complete." ;;
    "")        check_prereqs; check_env; install_deps; run_all ;;
    *)         die "Unknown option: $1 (use --check, --install, or no args)" ;;
  esac
}

main "$@"
