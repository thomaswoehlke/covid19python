#!/usr/bin/env bash

gunzip covid19data.sql.gz

psql -U covid19data -h localhost covid19data < covid19data.sql

gzip covid19data.sql