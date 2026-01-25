from datetime import datetime

class ReportGenerator:
    """
    Generates non-technical, user-friendly reports from validation logs.
    """

    PROVIDER_MAP = {
        "PDFEXPRESS_VALIDATION": "Certification",
        "TITLE_VALIDATOR": "Title Format",
        "ABSTRACT_VALIDATOR": "Abstract",
        "KEYWORDS_VALIDATOR": "Keywords",
        "KEYWORD_VALIDATOR": "Keywords", # Added singular form
        "KEYWORDS CHECKER": "Keywords", # Handle potential inconsistency
        "H1_VALIDATOR": "Section Headings (Level 1)",
        "H2_VALIDATOR": "Sub-section Headings (Level 2)",
        "TABLE_VALIDATOR": "Tables",
        "REF_VALIDATOR": "References",
        "PAGE_VALIDATOR": "Page Count",
        "PDF_EXTRACTOR": "File Processing"
    }

    @staticmethod
    def _clean_error_message(error):
        """
        Simplifies error messages for non-technical users.
        """
        # Add more mappings as needed based on common errors
        if "tuple index out of range" in error:
            return "We encountered an issue reading the structure of your PDF. Please ensure it is a valid text-based PDF."
        return error

    @staticmethod
    def generate_report(paper_name, is_valid, logs):
        """
        Generates a markdown report string.
        """
        status_icon = "✅" if is_valid else "❌"
        status_text = "PASSED" if is_valid else "FAILED"
        
        report = []
        report.append(f"# Validation Report: {paper_name}")
        report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Status:** {status_icon} {status_text}")
        report.append("")
        
        # Extract Author Info
        author_logs = [log for log in logs if log.get('msg_type') == 'REPORT_DATA']
        authors = []
        for log in author_logs:
            data = log.get('data', {})
            if data and data.get('key') == 'author_email':
                authors.append(data.get('value'))
        
        if authors:
            report.append("## Detected Authors")
            for author in authors:
                report.append(f"- {author}")
            report.append("")

        if is_valid:
            report.append("## Summary")
            report.append("Great job! Your paper passed all format checks. It adheres to the required guidelines.")
            return "\n".join(report)

        report.append("## Issues Found")
        report.append("The following areas need attention:")
        report.append("")

        # Group logs by provider
        issues_by_provider = {}
        for log in logs:
            # logs are dicts: {'provider': str, 'error': str, 'span': ...}
            provider = log.get('provider', 'UNKNOWN')
            
            # Skip Author Extractor in issues list since we handled it above
            if provider == 'AUTHOR_EXTRACTOR':
                continue

            error = log.get('error', 'Unknown error')
            
            friendly_provider = ReportGenerator.PROVIDER_MAP.get(provider, provider)
            
            if friendly_provider not in issues_by_provider:
                issues_by_provider[friendly_provider] = []
            
            issues_by_provider[friendly_provider].append(ReportGenerator._clean_error_message(error))

        # Generate sections
        for provider, errors in issues_by_provider.items():
            report.append(f"### {provider}")
            
            # Count occurrences of each error
            error_counts = {}
            for err in errors:
                error_counts[err] = error_counts.get(err, 0) + 1
            
            # Add to report
            for err, count in error_counts.items():
                if count > 1:
                    report.append(f"- {err} ({count} occurrences)")
                else:
                    report.append(f"- {err}")
            report.append("")

        report.append("---")
        report.append("**Next Steps:** Please correct the issues listed above and run the validation again.")
        
        return "\n".join(report)
