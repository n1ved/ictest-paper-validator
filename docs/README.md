# ICTEST Format Checker Documentation

Welcome to the documentation for the ICTEST Format Checker. This tool automates the process of validating research papers against specific conference guidelines (such as IEEE formatting rules) before they are accepted.

This repository uses a Flask-based backend to extract text, fonts, layout, and metadata from PDF submissions using PyMuPDF. It then runs a suite of formatting checkers to ensure the document conforms to the expected structure and style.

## Documentation Index

1. **[Architecture Overview](architecture.md)**
   Provides a high-level view of how the system works, from the moment a user uploads a PDF to the final report generation.

2. **[Extraction and Processing Component](components/extraction_and_processing.md)**
   Explains how PyMuPDF is used to extract detailed formatting information (text blocks, fonts, sizes, spans) and how this data is structured for the checkers.

3. **[Formatting Checkers](components/checkers.md)**
   Detailed documentation on each individual checker (e.g., Title, Abstract, Headings, Tables, References) and the specific rules they validate.

4. **[Logging and Reporting](components/logging_and_reporting.md)**
   Describes how formatting errors are recorded, how user-friendly markdown reports are generated, and how the system renders a PDF with highlighted errors.
