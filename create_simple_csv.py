import pandas as pd
import os

def create_simple_database():
    """
    Create an empty DataFrame with only text and image_path columns.
    """
    data = {
        'text': [],        # Text content from .txt files
        'image_path': []   # Path to corresponding image files
    }
    return pd.DataFrame(data)

def process_folder(folder):
    """
    Process a folder containing text files and images.

    Parameters:
    folder: str - Path to the folder to process

    Returns:
    events_df: pd.DataFrame - DataFrame with text and image paths
    """
    data = []

    # Iterate over all .txt files in the folder
    for file in os.listdir(folder):
        if file.endswith('.txt'):
            # Get the base filename without extension
            base_name = os.path.splitext(file)[0]

            # Construct paths for the text file and its matching image
            text_file_path = os.path.join(folder, file)
            image_file_path = os.path.join(folder, f"{base_name}.jpeg")

            # Check if the corresponding image exists
            if os.path.exists(image_file_path):
                with open(text_file_path, 'r', encoding='utf-8') as f:
                    text_content = f.read().strip()

                # Add the text and image path to the data list
                data.append({'text': text_content, 'image_path': image_file_path})
            else:
                print(f"Warning: No matching image found for {text_file_path}")

    # Convert data to a DataFrame
    events_df = pd.DataFrame(data)
    return events_df

def process_all_sources(instagram_folder, email_folder, whatsapp_folder):
    """
    Process all sources and combine into a single DataFrame.

    Parameters:
    instagram_folder: str - Path to Instagram folder
    email_folder: str - Path to Email folder
    whatsapp_folder: str - Path to WhatsApp folder

    Returns:
    events_df: pd.DataFrame - Combined DataFrame with text and image paths
    """
    # Initialize an empty DataFrame
    combined_df = create_simple_database()

    # Process Instagram folder
    # print("Processing Instagram folder...")
    instagram_df = process_folder(instagram_folder)
    combined_df = pd.concat([combined_df, instagram_df], ignore_index=True)

    # Process Email folder
    # print("Processing Email folder...")
    email_df = process_folder(email_folder)
    combined_df = pd.concat([combined_df, email_df], ignore_index=True)

    # Process WhatsApp folder
    # print("Processing WhatsApp folder...")
    whatsapp_df = process_folder(whatsapp_folder)
    combined_df = pd.concat([combined_df, whatsapp_df], ignore_index=True)

    return combined_df

# Main execution
if __name__ == "__main__":
    # Define folder paths
    INSTAGRAM_FOLDER = "/content/data/instagram/"
    EMAIL_FOLDER = "/content/data/email/"
    WHATSAPP_FOLDER = "/content/data/whatsapp/"

    # Process all folders
    events_df = process_all_sources(INSTAGRAM_FOLDER, EMAIL_FOLDER, WHATSAPP_FOLDER)

    # Save the DataFrame to CSV
    output_csv_path = "/content/simple_events_database.csv"
    events_df.to_csv(output_csv_path, index=False)

    print(f"Processed {len(events_df)} events and saved to {output_csv_path}")
    # print("\nFirst few entries:")
    # print(events_df.head())
