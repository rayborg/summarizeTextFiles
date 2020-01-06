#!/bin/bash
#First install pdfminer with: pip install pdfminer

#Create a directory called text then run this script in same folder as your PDFs
for f in *.pdf; do
  pdf2txt.py "$f" >> ./text/"${f%}.txt"
done
