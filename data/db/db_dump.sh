#!/usr/bin/env bash

pg_dump -U covid19data -h localhost covid19data --compress=9 --clean --if-exists --no-tablespaces  --on-conflict-do-nothing --rows-per-insert=200 --column-inserts --quote-all-identifiers --no-privileges > covid19data.sql.gz
