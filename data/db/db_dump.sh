#!/usr/bin/env bash

pg_dump -U covid19data -h localhost covid19data --clean --if-exists --no-tablespaces  --on-conflict-do-nothing --rows-per-insert=1000 --column-inserts --quote-all-identifiers --no-privileges > covid19data.sql
