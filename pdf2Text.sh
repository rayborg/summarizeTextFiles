#!/bin/bash
for f in *.pdf; do
  pdf2txt.py "$f" >> ./text/"${f%}.txt"
done
