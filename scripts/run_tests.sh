#!/usr/bin/env bash

set -e

#
# Reset test DATABASE
#
function reset_db() {
  echo --------------------
  echo Resetting test DB
  echo --------------------

  docker compose stop owl || true
  RESET_DB_CMD="psql \"postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:/postgres\" <<-'EOF'
  SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'test';
  DROP DATABASE IF EXISTS test;
  CREATE DATABASE test;
  \\connect test
EOF"
echo ${RESET_DB_CMD}
  docker exec -i postgres bash -c "${RESET_DB_CMD}"
  docker compose start owl
}

#
# Run init test procedures
#
function test_init() {
  echo --------------------
  echo Applying migrations
  echo --------------------
  uv run --no-sync alembic upgrade head
}

#
# Init global vars
#
TEST_POSTGRES_DB="test"
POSTGRES_USER="${POSTGRES_USER:-owl}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-hoot}"
POSTGRES_HOST="${POSTGRES_HOST:-db}"
POSTGRES_PORT="${POSTGRES_PORT:-5432}"

RUN_INIT=1
RUN_RESET_DB=1
RUN_TESTS=1
MAX_FAIL="--maxfail=1"
TEST_MODULE="tests"
SHOW_HIDDEN=""

PARAMS=""
while (( "$#" )); do
  case "$1" in
    --help)
      echo Switches:
      echo --no-init : Will not, reset the test DB, superset init and load examples
      echo --no-reset-db: Will not reset the test DB
      echo --no-tests: Will not run any test, by default reset the DB, superset init and load_examples
      echo --reset-db: Just resets the test DB, will not run any test
      echo --module: Run a specific test module: --module tests/charts/api_tests.py for example
      echo --datacraft: Run datacraft tests only
      echo --show-hidden: Show hidden info from pytest: -vv
      echo --no-fail: Continue if some tests fail
      exit 0
      ;;
    --no-init)
      RUN_INIT=0
      RUN_RESET_DB=0
      shift 1
      ;;
    --no-reset-db)
      RUN_RESET_DB=0
      shift 1
      ;;
    --no-tests)
      RUN_TESTS=0
      shift 1
      ;;
    --reset-db)
      RUN_TESTS=0
      RUN_INIT=0
      shift 1
      ;;
    --module)
      TEST_MODULE=$2
      shift 2
      ;;
    --datacraft)
      TEST_MODULE="datacraft_tests"
      shift 1
      ;;
    --show-hidden)
      SHOW_HIDDEN="-vv"
      shift 1
      ;;
    --no-fail)
      MAX_FAIL="NO_MAX_FAIL"
      shift 1
      ;;
    --) # end argument parsing
      shift
      break
      ;;
    --*) # unsupported flags
      echo "Error: Unsupported flag $1" >&2
      exit 1
      ;;
    *) # preserve positional arguments
      PARAMS="$PARAMS $1"
      shift
      ;;
  esac
done

echo ------------------------------------
echo Run init procedures=$RUN_INIT
echo Run reset DB=$RUN_RESET_DB
echo Test to run:"${TEST_MODULE}"
echo ------------------------------------

# Running tests
if [ $RUN_RESET_DB -eq 1 ]
then
  reset_db
fi


if [ $RUN_INIT -eq 1 ]
then
  test_init
fi

pytest
#
#if [ $RUN_TESTS -eq 1 ]
#then
#  if [ "${MAX_FAIL}" != "NO_MAX_FAIL" ]
#  then
#    pytest --durations=0 "${MAX_FAIL}" "${TEST_MODULE}" "${SHOW_HIDDEN}"
#  else
#    pytest --durations=0 "${TEST_MODULE}" "${SHOW_HIDDEN}"
#  fi
#fi