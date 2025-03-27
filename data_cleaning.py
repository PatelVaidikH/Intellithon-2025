import html
import re

# Load raw data (Replace this with reading from a file if needed)
raw_data = [
    "&#19996;&#33694;&#24066;, ?? (Guangdong)", "&amp;#19978;&amp;#28023;&amp;#24066;",
    "California", ", Guangdong", ", Ha Noi", "Guangzhou, ?? (Guangdong)",
    "Hefei, ?? (Anhui)", "Texas, Houston", "11, ?? (Guangdong)", 
    "Beijing, 北京 (Beijing)", "99999, New York", "??, ?? (Jiangsu)", 
    "Shanghai, 上海 (Shanghai)", "Mumbai, Maharashtra", "---, Arkansas"
]

def clean_location(location):
    """
    Cleans and standardizes location data.
    """
    # Decode HTML entities (like &#19978; -> 上)
    location = html.unescape(location)

    # Remove leading/trailing commas, dashes, and spaces
    location = re.sub(r'^[,\-.\s]+|[,\-.\s]+$', '', location)

    # Remove numbers and unknown placeholders (??, ???)
    location = re.sub(r'\b\d{1,5}\b', '', location)  # Remove numbers (like 11, 99999)
    location = re.sub(r'\?\?+', '', location)  # Remove "??" or "???"

    # Remove province codes in parentheses (like "Guangdong", "Shandong", etc.)
    location = re.sub(r'\(\w+\)', '', location).strip()

    return location

# Apply cleaning to all locations and remove duplicates
cleaned_locations = sorted(set(clean_location(loc) for loc in raw_data if clean_location(loc)))

# Print the cleaned list
print(cleaned_locations)
