import re

class TextProcessor:
    def __init__(self):
        # Common abbreviations mapping
        self.abbreviations = {
            'Mr.': 'Mister',
            'Mrs.': 'Missus', 
            'Ms.': 'Miss',
            'Dr.': 'Doctor',
            'Prof.': 'Professor',
            'Sr.': 'Senior',
            'Jr.': 'Junior',
            'Ltd.': 'Limited',
            'Inc.': 'Incorporated',
            'Corp.': 'Corporation',
            'Co.': 'Company',
            'etc.': 'etcetera',
            'vs.': 'versus',
            'e.g.': 'for example',
            'i.e.': 'that is',
            'Ave.': 'Avenue',
            'St.': 'Street',
            'Rd.': 'Road',
            'Blvd.': 'Boulevard'
        }
    
    def clean_text(self, text):
        """Basic text cleaning"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s.,!?;:\'"()-]', '', text)
        
        return text
    
    def expand_abbreviations(self, text):
        """Expand common abbreviations"""
        for abbrev, expansion in self.abbreviations.items():
            text = text.replace(abbrev, expansion)
        return text
    
    def process_punctuation(self, text):
        """Handle punctuation for better speech"""
        # Add pauses for better speech rhythm
        text = text.replace(',', ', ')  # Ensure space after comma
        text = text.replace('.', '. ')  # Ensure space after period
        text = text.replace('!', '! ')  # Ensure space after exclamation
        text = text.replace('?', '? ')  # Ensure space after question
        text = text.replace(';', '; ')  # Ensure space after semicolon
        text = text.replace(':', ': ')  # Ensure space after colon
        
        # Clean up multiple spaces
        text = ' '.join(text.split())
        
        return text
    
    def handle_special_cases(self, text):
        """Handle special text cases"""
        # Handle common contractions
        contractions = {
            "won't": "will not",
            "can't": "cannot",
            "n't": " not",
            "'re": " are",
            "'ve": " have",
            "'ll": " will",
            "'d": " would",
            "'m": " am"
        }
        
        for contraction, expansion in contractions.items():
            text = text.replace(contraction, expansion)
        
        return text
    
    def process_text(self, text):
        """Main text processing pipeline"""
        if not text or not isinstance(text, str):
            return ""
        
        # Apply all processing steps
        text = self.clean_text(text)
        text = self.expand_abbreviations(text)
        text = self.handle_special_cases(text)
        text = self.process_punctuation(text)
        
        return text.strip()

# Test the processor
if __name__ == "__main__":
    processor = TextProcessor()
    test_text = "Dr. Smith won't be available today, etc. Please contact Mr. Johnson at the Corp. office."
    result = processor.process_text(test_text)
    print("Original:", test_text)
    print("Processed:", result)