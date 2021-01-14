#!/usr/bin/env bash

pg_dump -U covid19data -h localhost covid19data --inserts > covid19data.sql