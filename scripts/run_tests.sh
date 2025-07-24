#!/usr/bin/env bash

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

set -e

#
# Reset test DATABASE
#
function reset_db() {
  echo --------------------
  echo Resetting test DB
  echo --------------------

  docker compose stop owl || true

  RESET_DB_CMD="psql \"postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/postgres\" <<-SQL
  SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '${TEST_POSTGRES_DB}';
  DROP DATABASE IF EXISTS \"${TEST_POSTGRES_DB}\";
  CREATE DATABASE \"${TEST_POSTGRES_DB}\";
  \\connect \"${TEST_POSTGRES_DB}\"
  SQL"

  echo "$RESET_DB_CMD"
  docker exec -i postgres bash -c "${RESET_DB_CMD}"

  docker compose start owl
}

#
# Run init test procedures (оставлено как в оригинале, при необходимости верните)
#
function test_init() {
  echo --------------------
  echo Applying migrations
  echo --------------------
  uv run --no-sync alembic upgrade head
}

#
# Init global vars (берём из окружения, а если не заданы — используем значения по умолчанию)
#
TEST_POSTGRES_DB=""test
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
echo POSTGRES_DB="${POSTGRES_DB}"
echo POSTGRES_USER="${POSTGRES_USER}"
echo POSTGRES_HOST="${POSTGRES_HOST}"
echo POSTGRES_PORT="${POSTGRES_PORT}"
echo Run init procedures=$RUN_INIT
echo Run reset DB=$RUN_RESET_DB
echo Test to run:"${TEST_MODULE}"
echo ------------------------------------

# Running tests
if [ $RUN_RESET_DB -eq 1 ]
then
  reset_db
fi

pytest

#
#if [ $RUN_INIT -eq 1 ]
#then
#  test_init
#fi
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