#!/usr/bin/env bash

echo "covid19datapwd"

pg_dump -U covid19data -h localhost covid19data --inserts > covid19data.sql