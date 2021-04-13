#!/usr/bin/env bash

psql -U covid19data -h localhost covid19data < covid19data.sql
