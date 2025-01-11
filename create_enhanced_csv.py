import pandas as pd
import google.generativeai as genai
from PIL import Image
import re
from google.colab import userdata
from datetime import datetime, timedelta

def setup_gemini():
    """Configure Gemini API with the stored key."""
    api_key = userdata.get('GEMINI_API_KEY')
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

def validate_and_fix_date(date_str):
    """
    Validate and fix dates to ensure they're in 2025.
    Returns corrected date string or 'Not specified' if invalid.
    """
    if date_str == 'Not specified':
        return date_str
        
    try:
        # Try to parse the date
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        # If the year is 2024, update it to 2025
        if date_obj.year == 2024:
            date_obj = date_obj.replace(year=2025)
            
        # If the date is before 2025, set it to 2025
        if date_obj.year < 2025:
            date_obj = date_obj.replace(year=2025)
            
        # Return formatted date string
        return date_obj.strftime('%Y-%m-%d')
    except:
        return 'Not specified'

def validate_time(time_str):
    """
    Validate time format and return standardized 24-hour time.
    """
    if time_str == 'Not specified':
        return time_str
        
    try:
        # Try to parse the time in 24-hour format
        datetime.strptime(time_str, '%H:%M')
        return time_str
    except:
        try:
            # Try to convert 12-hour format to 24-hour
            time_obj = datetime.strptime(time_str, '%I:%M %p')
            return time_obj.strftime('%H:%M')
        except:
            return 'Not specified'

def extract_event_info(model, text, image_path):
    """Extract structured event information using Gemini API."""
    source_link = extract_source_from_text(text)
    
    prompt = f"""Analyze the following text and image to extract structured event information for events happening in 2025:
    - Date (YYYY-MM-DD format, MUST be in 2025)
    - Time (24-hour format, e.g., 14:30)
    - Duration (in hours, based on start and end times if mentioned, else default to 1 hour)
    - Type of event (use one of these exact types):
      CLASS, LAB, TUT, DEBSOC, QC, SM, DRAMA, DANCE, HS, MUSIC, LITERARY, DESIGN, PFC, FACC, FEST
    - A short description of the event
    - Source URL (if mentioned in text/image)

    Important: ALL dates should be in 2025. If a date is mentioned without a year, assume 2025.

    Provide output in this format:
    1. Date: <YYYY-MM-DD>
    2. Time: <HH:MM>
    3. Duration: <value>
    4. Type: <value>
    5. Description: <value>
    6. Source: <value>

    Input Text: {text}
    """

    try:
        image = load_image(image_path) if image_path else None
        
        if image:
            response = model.generate_content([prompt, image, text])
        else:
            response = model.generate_content([prompt, text])
            
        response_text = response.text
        
        # Parse response and initialize with defaults
        info = {
            'date': 'Not specified',
            'time': 'Not specified',
            'duration': '1 hour',
            'type': 'Not specified',
            'description': 'Not specified',
            'source': source_link
        }
        
        # Extract information from response
        for line in response_text.strip().split('\n'):
            if line.startswith('1.'):
                info['date'] = validate_and_fix_date(line.split(':', 1)[1].strip())
            elif line.startswith('2.'):
                info['time'] = validate_time(line.split(':', 1)[1].strip())
            elif line.startswith('3.'):
                duration = line.split(':', 1)[1].strip()
                info['duration'] = duration if duration != 'Not specified' else '1 hour'
            elif line.startswith('4.'):
                info['type'] = line.split(':', 1)[1].strip().upper()
            elif line.startswith('5.'):
                info['description'] = line.split(':', 1)[1].strip()
            elif line.startswith('6.'):
                extracted_source = line.split(':', 1)[1].strip()
                info['source'] = extracted_source if extracted_source != 'Not specified' else source_link
        
        return info
        
    except Exception as e:
        print(f"Error processing with Gemini: {e}")
        return {
            'date': 'Not specified',
            'time': 'Not specified',
            'duration': '1 hour',
            'type': 'Not specified',
            'description': 'Not specified',
            'source': source_link
        }

def extract_source_from_text(text):
    """Extract hyperlink from text."""
    link_pattern = r'(https?://[^\s]+)'
    match = re.search(link_pattern, text)
    return match.group(0) if match else 'Not specified'

def process_events_with_gemini(input_csv_path, output_csv_path):
    """Process events database with Gemini and create enhanced CSV."""
    model = setup_gemini()
    df = pd.read_csv(input_csv_path)
    
    # Initialize columns
    df['priority_index'] = 0
    df['date'] = 'Not specified'
    df['time'] = 'Not specified'
    df['type'] = 'Not specified'
    df['duration'] = '1 hour'
    df['description'] = 'Not specified'
    df['source'] = 'Not specified'
    
    total_events = len(df)
    for idx, row in df.iterrows():
        print(f"Processing event {idx + 1}/{total_events}")
        
        info = extract_event_info(model, row['text'], row['image_path'])
        
        # Update DataFrame
        for key in info:
            df.at[idx, key] = info[key]
    
    # Save enhanced database
    df.to_csv(output_csv_path, index=False)
    print(f"Enhanced database saved to {output_csv_path}")
    return df

if __name__ == "__main__":
    input_csv_path = "/content/simple_events_database.csv"
    output_csv_path = "/content/enhanced_events_database.csv"
    
    enhanced_df = process_events_with_gemini(input_csv_path, output_csv_path)
    
    print("\nSample of processed events:")
    print(enhanced_df[['type', 'date', 'time', 'duration', 'description', 'source']].head())
