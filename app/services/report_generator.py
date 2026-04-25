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

    @staticmethod
    def generate_html_report(paper_name, is_valid, logs):
        """
        Generates an HTML report string.
        """
        status_color = "#28a745" if is_valid else "#dc3545"
        status_text = "PASSED" if is_valid else "FAILED"
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            f"<title>Validation Report: {paper_name}</title>",
            "<style>",
            "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }",
            "h1 { border-bottom: 2px solid #eee; padding-bottom: 10px; }",
            "h2 { color: #444; margin-top: 30px; }",
            "h3 { color: #666; }",
            f".status-box {{ display: inline-block; padding: 10px 20px; border-radius: 5px; color: white; background-color: {status_color}; font-weight: bold; margin: 20px 0; }}",
            ".meta { color: #666; font-size: 0.9em; }",
            ".error-list { background-color: #f8f9fa; padding: 15px 30px; border-radius: 5px; border-left: 4px solid #dc3545; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>Validation Report: {paper_name}</h1>",
            f"<div class='meta'><strong>Date:</strong> {date_str}</div>",
            f"<div class='status-box'>Status: {status_text}</div>"
        ]
        
        # Extract Author Info
        author_logs = [log for log in logs if log.get('msg_type') == 'REPORT_DATA']
        authors = []
        for log in author_logs:
            data = log.get('data', {})
            if data and data.get('key') == 'author_email':
                authors.append(data.get('value'))
        
        if authors:
            html.append("<h2>Detected Authors</h2>")
            html.append("<ul>")
            for author in authors:
                html.append(f"<li>{author}</li>")
            html.append("</ul>")

        if is_valid:
            html.append("<h2>Summary</h2>")
            html.append("<p>Great job! Your paper passed all format checks. It adheres to the required guidelines.</p>")
            html.append("</body></html>")
            return "\n".join(html)

        html.append("<h2>Issues Found</h2>")
        html.append("<p>The following areas need attention:</p>")

        # Group logs by provider
        issues_by_provider = {}
        for log in logs:
            provider = log.get('provider', 'UNKNOWN')
            if provider == 'AUTHOR_EXTRACTOR':
                continue

            error = log.get('error', 'Unknown error')
            friendly_provider = ReportGenerator.PROVIDER_MAP.get(provider, provider)
            
            if friendly_provider not in issues_by_provider:
                issues_by_provider[friendly_provider] = []
            
            issues_by_provider[friendly_provider].append(ReportGenerator._clean_error_message(error))

        # Generate sections
        for provider, errors in issues_by_provider.items():
            html.append(f"<h3>{provider}</h3>")
            html.append("<ul class='error-list'>")
            
            error_counts = {}
            for err in errors:
                error_counts[err] = error_counts.get(err, 0) + 1
            
            for err, count in error_counts.items():
                if count > 1:
                    html.append(f"<li>{err} <strong>({count} occurrences)</strong></li>")
                else:
                    html.append(f"<li>{err}</li>")
            html.append("</ul>")

        html.append("<hr style='margin-top: 40px; border: 0; border-top: 1px solid #eee;'>")
        html.append("<p><strong>Next Steps:</strong> Please correct the issues listed above and run the validation again.</p>")
        html.append("</body></html>")
        
        return "\n".join(html)

