import main
def check(pdf):
    """
    Check the given PDF file for validation.

    Args:
        pdf (str): Path to the PDF file to be checked.

    Returns:
        bool: True if the PDF passes all checks, False otherwise.
    """
    return main.main(pdf, log=True)