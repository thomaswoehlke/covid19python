#!/usr/bin/env bash

JAHRE="2020 2021"
MONATE="01 02 03 04 05 06 07 08 09 10 11 12"


for JAHR in $JAHRE
do
  echo $JAHR
  for MONAT in $MONATE
  do
    echo "$JAHR-$MONAT"
    TAG_DATEI="$JAHR-$MONAT"
    TAG_GREP="$JAHR/$MONAT"
    DATEI="rki/RKI_COVID19__$TAG_DATEI.csv"
    echo $TAG_DATEI
    echo $TAG_GREP
    echo $DATEI
    cat RKI_COVID19.csv | grep $TAG_GREP > $DATEI
  done
done