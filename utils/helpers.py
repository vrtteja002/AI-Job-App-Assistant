import json
import os
from datetime import datetime, timedelta
import re
from collections import Counter

def validate_json_response(response_text):
    """
    Validates if the text is proper JSON and converts it to a Python dictionary.
    If not, attempts to extract JSON from the text.
    """
    try:
        # Try to parse the entire response as JSON
        return json.loads(response_text)
    except json.JSONDecodeError:
        # If that fails, try to find JSON within the text
        try:
            # Look for text that might be JSON
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start >= 0 and json_end > 0:
                json_text = response_text[json_start:json_end]
                return json.loads(json_text)
            else:
                print("No JSON object found in the response")
                return None
        except Exception as e:
            print(f"Error extracting JSON: {e}")
            return None

def format_date(date_str=None, days_from_now=0, format="%Y-%m-%d"):
    """
    Format date in the specified format.
    If date_str is provided, it parses that date.
    If days_from_now is provided, it calculates a date relative to today.
    """
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, format)
        except ValueError:
            print(f"Invalid date format: {date_str}")
            return None
    else:
        date_obj = datetime.now() + timedelta(days=days_from_now)
    
    return date_obj.strftime(format)

def ensure_directory_exists(directory_path):
    """
    Ensures that the specified directory exists, creating it if necessary.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Created directory: {directory_path}")
    return directory_path

def save_text_to_file(text, file_path, mode='w'):
    """
    Saves text to a file.
    """
    try:
        # Ensure the directory exists
        ensure_directory_exists(os.path.dirname(file_path))
        
        with open(file_path, mode, encoding='utf-8') as file:
            file.write(text)
        print(f"Content saved to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving to file: {e}")
        return False

def read_text_from_file(file_path):
    """
    Reads text from a file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def extract_keywords(text, min_length=4, max_words=10):
    """
    Extract potential keywords from text based on word frequency.
    Simple implementation - for production use consider using NLP libraries.
    """
    # Clean the text
    import re
    from collections import Counter
    
    # Common words to exclude
    stop_words = set([
        'the', 'and', 'a', 'to', 'in', 'of', 'is', 'with', 'for', 'on', 
        'that', 'this', 'at', 'from', 'by', 'an', 'are', 'as', 'be', 'or',
        'you', 'your', 'we', 'our', 'their', 'have', 'has', 'had', 'was',
        'were', 'will', 'would', 'should', 'could', 'can', 'may', 'might',
        'must', 'i', 'they', 'them', 'he', 'she', 'it', 'his', 'her'
    ])
    
    # Clean text and split into words
    words = re.findall(r'\b[a-zA-Z]{' + str(min_length) + r',}\b', text.lower())
    
    # Filter out stop words
    filtered_words = [word for word in words if word not in stop_words]
    
    # Count word frequencies
    word_counts = Counter(filtered_words)
    
    # Return most common words
    return [word for word, count in word_counts.most_common(max_words)]

def similarity_score(text1, text2):
    """
    Calculate a simple similarity score between two texts.
    Uses Jaccard similarity on word sets.
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    
    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    if union == 0:
        return 0
    return intersection / union

def get_file_extension(file_path):
    """
    Extract the file extension from a path.
    """
    return os.path.splitext(file_path)[1].lower()

def sanitize_filename(filename):
    """
    Sanitize a filename by removing invalid characters.
    """
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    return sanitized

def truncate_text(text, max_length=100, ellipsis='...'):
    """
    Truncate text to the specified maximum length.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length-len(ellipsis)] + ellipsis
