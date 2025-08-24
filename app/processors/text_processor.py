###
# Text Processor Generated with GPT
###

import json
import re
import pandas as pd
from typing import List, Dict, Any

class PDFTextProcessor:
    """
    A class to process and search formatted text extracted from PDFs.
    Designed for easy use in Jupyter notebooks.
    """

    def __init__(self, formatted_text_data: List[Dict] = None):
        """Initialize with formatted text data."""
        self.processed_data = None
        if formatted_text_data:
            self.load_data(formatted_text_data)

    def load_data(self, formatted_text_data: List[Dict],log=False):
        """Load and process formatted text data."""
        if log:
            print("Processing formatted text data...")
        self.processed_data = self._process_formatted_text(formatted_text_data)
        if log:
            print(f"✓ Processed {len(self.processed_data['text_segments'])} text segments")
            print(f"✓ Indexed {len(self.processed_data['word_index'])} unique words")
        return self

    def load_from_json(self, json_file_path: str):
        """Load data directly from extracted PDF JSON file."""
        with open(json_file_path, 'r', encoding='utf-8') as f:
            pdf_data = json.load(f)

        if 'formatted_text' not in pdf_data:
            raise ValueError("JSON file doesn't contain 'formatted_text' field")

        return self.load_data(pdf_data['formatted_text'])

    def _process_formatted_text(self, formatted_text_data: List[Dict]) -> Dict[str, Any]:
        """Process formatted_text data to create searchable structure."""
        processed_data = {
            'text_segments': [],
            'word_index': {},
            'font_summary': {},
            'size_summary': {}
        }

        segment_id = 0

        for page_data in formatted_text_data:
            page_num = page_data['page']

            for block in page_data.get('blocks', []):
                for line in block.get('lines', []):
                    for span in line.get('spans', []):
                        text = span.get('text', '').strip()

                        if not text:
                            continue

                        font = span.get('font', 'Unknown')
                        size = span.get('size', 0)
                        flags = span.get('flags', 0)
                        color = span.get('color', 0)
                        bbox = span.get('bbox', [0, 0, 0, 0])

                        # Determine text style from flags
                        is_bold = bool(flags & 2**4)
                        is_italic = bool(flags & 2**1)
                        is_superscript = bool(flags & 2**0)
                        is_subscript = bool(flags & 2**2)

                        segment = {
                            'id': segment_id,
                            'text': text,
                            'page': page_num,
                            'font': font,
                            'size': round(size, 2),
                            'color': color,
                            'bbox': bbox,
                            'is_bold': is_bold,
                            'is_italic': is_italic,
                            'is_superscript': is_superscript,
                            'is_subscript': is_subscript,
                            'flags': flags,
                            'x': round(bbox[0], 2) if bbox else 0,
                            'y': round(bbox[1], 2) if bbox else 0,
                            'width': round(bbox[2] - bbox[0], 2) if bbox else 0,
                            'height': round(bbox[3] - bbox[1], 2) if bbox else 0
                        }

                        processed_data['text_segments'].append(segment)

                        # Build word index
                        words = re.findall(r'\b\w+\b', text.lower())
                        for word in words:
                            if word not in processed_data['word_index']:
                                processed_data['word_index'][word] = []
                            processed_data['word_index'][word].append(segment_id)

                        # Update summaries
                        processed_data['font_summary'][font] = processed_data['font_summary'].get(font, 0) + 1
                        size_key = str(round(size, 1))
                        processed_data['size_summary'][size_key] = processed_data['size_summary'].get(size_key, 0) + 1

                        segment_id += 1

        return processed_data

    def search(self, query: str, case_sensitive: bool = False,log = False) -> pd.DataFrame:
        """Search for text and return results as DataFrame."""
        if not self.processed_data:
            raise ValueError("No data loaded. Use load_data() or load_from_json() first.")

        if not case_sensitive:
            query = query.lower()

        results = []

        for segment in self.processed_data['text_segments']:
            text = segment['text'] if case_sensitive else segment['text'].lower()

            if query in text:
                result = segment.copy()
                result['match_text'] = query
                result['match_start'] = text.find(query)
                results.append(result)

        return pd.DataFrame(results)

    def search_word(self, word: str, case_sensitive: bool = False) -> pd.DataFrame:
        """Search for complete words."""
        if not self.processed_data:
            raise ValueError("No data loaded.")

        search_word = word if case_sensitive else word.lower()
        results = []

        if not case_sensitive and search_word in self.processed_data['word_index']:
            segment_ids = self.processed_data['word_index'][search_word]
            results = [self.processed_data['text_segments'][sid] for sid in segment_ids]
        else:
            # Fallback to regex search
            pattern = r'\b' + re.escape(word) + r'\b'
            flags = 0 if case_sensitive else re.IGNORECASE

            for segment in self.processed_data['text_segments']:
                if re.search(pattern, segment['text'], flags):
                    results.append(segment)

        return pd.DataFrame(results)

    def filter_by_properties(self, **filters) -> pd.DataFrame:
        """
        Filter text segments by properties.

        Available filters:
        - font: Font name
        - size, size_min, size_max: Font size filters
        - page: Page number
        - is_bold, is_italic: Style filters
        - color: Color value
        """
        if not self.processed_data:
            raise ValueError("No data loaded.")

        results = []

        for segment in self.processed_data['text_segments']:
            match = True

            if 'font' in filters:
                font_filter = filters['font']
                if isinstance(font_filter, list):
                    if segment['font'] not in font_filter:
                        match = False
                elif segment['font'] != font_filter:
                    match = False

            if 'size' in filters and segment['size'] != filters['size']:
                match = False
            if 'size_min' in filters and segment['size'] < filters['size_min']:
                match = False
            if 'size_max' in filters and segment['size'] > filters['size_max']:
                match = False

            if 'page' in filters:
                page_filter = filters['page']
                if isinstance(page_filter, list):
                    if segment['page'] not in page_filter:
                        match = False
                elif segment['page'] != page_filter:
                    match = False

            if 'is_bold' in filters and segment['is_bold'] != filters['is_bold']:
                match = False
            if 'is_italic' in filters and segment['is_italic'] != filters['is_italic']:
                match = False
            if 'color' in filters and segment['color'] != filters['color']:
                match = False

            if match:
                results.append(segment)

        return pd.DataFrame(results)

    def get_summary(self) -> Dict:
        """Get summary statistics of the document."""
        if not self.processed_data:
            raise ValueError("No data loaded.")

        segments = self.processed_data['text_segments']
        sizes = [s['size'] for s in segments]

        return {
            'total_segments': len(segments),
            'total_pages': max(s['page'] for s in segments) if segments else 0,
            'unique_fonts': len(self.processed_data['font_summary']),
            'unique_sizes': len(self.processed_data['size_summary']),
            'avg_font_size': round(sum(sizes) / len(sizes), 2) if sizes else 0,
            'font_distribution': dict(sorted(self.processed_data['font_summary'].items(),
                                           key=lambda x: x[1], reverse=True)),
            'size_distribution': dict(sorted(self.processed_data['size_summary'].items(),
                                           key=lambda x: float(x[0])))
        }

    def find_headings(self, size_threshold: float = None, include_bold: bool = True) -> pd.DataFrame:
        """Find potential headings based on font size and style."""
        if not self.processed_data:
            raise ValueError("No data loaded.")

        segments = self.processed_data['text_segments']

        if size_threshold is None:
            sizes = [s['size'] for s in segments]
            avg_size = sum(sizes) / len(sizes) if sizes else 12
            size_threshold = avg_size * 1.2

        headings = []
        for segment in segments:
            is_heading = False

            # Large font size
            if segment['size'] > size_threshold:
                is_heading = True

            # Bold text (if enabled)
            if include_bold and segment['is_bold']:
                is_heading = True

            # Short text (might be headings)
            if len(segment['text']) < 100 and segment['size'] >= avg_size:
                is_heading = True

            if is_heading:
                headings.append(segment)

        return pd.DataFrame(headings).sort_values(['page', 'y'], ascending=[True, False]) if headings else pd.DataFrame()

    def export_to_csv(self, filename: str = 'pdf_text_data.csv'):
        """Export all text data to CSV for further analysis."""
        if not self.processed_data:
            raise ValueError("No data loaded.")

        df = pd.DataFrame(self.processed_data['text_segments'])
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"✓ Data exported to {filename}")
        return df

# Quick usage functions for notebook cells
def quick_load(json_file_path: str) -> PDFTextProcessor:
    """Quick function to load PDF data in a notebook cell."""
    processor = PDFTextProcessor()
    return processor.load_from_json(json_file_path)

def display_results(df: pd.DataFrame, max_rows: int = 10):
    """Display search results in a nice format for notebooks."""
    if df.empty:
        print("No results found.")
        return

    print(f"Found {len(df)} results:")
    print("-" * 50)

    for idx, row in df.head(max_rows).iterrows():
        print(f"Page {row['page']} | {row['font']} {row['size']}pt | Bold: {row['is_bold']} | Italic: {row['is_italic']}")
        print(f"Text: {row['text'][:100]}{'...' if len(row['text']) > 100 else ''}")
        print("-" * 50)

    if len(df) > max_rows:
        print(f"... and {len(df) - max_rows} more results")
