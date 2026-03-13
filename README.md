# Smart Academic File Organizer

## Overview
This Python utility scans a folder, cleans inconsistent filenames, and organizes files into categorized directories such as PDFs, Code, Images, Documents, and TextFiles.

## Features
- Cleans inconsistent filenames
- Preserves meaningful numbers in names such as lecture1 -> lecture_1
- Removes redundant suffixes such as final, copy, draft, and duplicate markers like (1)
- Organizes files into folders by type
- Handles duplicate filenames safely
- Prints a summary of renamed, moved, skipped, and duplicate-handled files

## Why I built it
I wanted a project that solved a real problem. Academic folders and downloads get messy quickly, and many files have inconsistent names. This tool automatically cleans and organizes those files while preserving useful information from the original filenames.

## How to run
Use:

python organizer.py

## Example
lecture1.pdf → PDFs/lecture_1.pdf  
lecture-1 final.pdf → PDFs/lecture_1_copy.pdf  
notes_final_final.pdf → PDFs/notes.pdf  
Assignment 2 (1).docx → Documents/assignment_2.docx
