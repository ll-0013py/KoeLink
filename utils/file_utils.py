"""
File utility functions for VoiceTranslateFlow
"""

import os
from datetime import datetime
import pytz


def get_timestamp():
    """Get current timestamp in Tokyo timezone"""
    return datetime.now(pytz.timezone('Asia/Tokyo')).strftime("%Y%m%d_%H%M%S")


def ensure_directory(directory_path):
    """Ensure directory exists, create if it doesn't"""
    os.makedirs(directory_path, exist_ok=True)
    return directory_path


def save_text_file(content, filepath):
    """Save text content to file"""
    directory = os.path.dirname(filepath)
    ensure_directory(directory)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Text file saved: {filepath}")
    return filepath


def save_japanese_script(content, output_dir, timestamp=None):
    """Save Japanese script with timestamp"""
    if timestamp is None:
        timestamp = get_timestamp()
    
    filename = f"jp_script_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    return save_text_file(content, filepath)


def check_file_exists(filepath):
    """Check if file exists and is readable"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    if not os.path.isfile(filepath):
        raise ValueError(f"Path is not a file: {filepath}")
    
    if not os.access(filepath, os.R_OK):
        raise PermissionError(f"File is not readable: {filepath}")
    
    return True


def get_file_info(filepath):
    """Get basic file information"""
    check_file_exists(filepath)
    
    stat = os.stat(filepath)
    return {
        'path': filepath,
        'size': stat.st_size,
        'modified': datetime.fromtimestamp(stat.st_mtime),
        'extension': os.path.splitext(filepath)[1].lower()
    }


def validate_media_file(filepath):
    """Validate media file for processing"""
    info = get_file_info(filepath)
    
    # Common audio/video extensions
    valid_extensions = {'.mp3', '.wav', '.mp4', '.avi', '.mov', '.m4a', '.flac', '.ogg'}
    
    if info['extension'] not in valid_extensions:
        print(f"Warning: File extension '{info['extension']}' may not be supported")
        print(f"Supported extensions: {', '.join(valid_extensions)}")
    
    # Check file size (warn if too large)
    max_size_mb = 500  # 500MB limit
    size_mb = info['size'] / (1024 * 1024)
    
    if size_mb > max_size_mb:
        print(f"Warning: File size ({size_mb:.1f}MB) is quite large. Processing may take time.")
    
    return info


def get_user_input_with_validation(prompt, validator=None):
    """Get user input with optional validation"""
    while True:
        user_input = input(prompt).strip()
        
        if not user_input:
            print("Input cannot be empty. Please try again.")
            continue
        
        if validator:
            try:
                if validator(user_input):
                    return user_input
            except Exception as e:
                print(f"Invalid input: {e}")
                continue
        else:
            return user_input


def confirm_file_path(filepath):
    """Confirm file path with user"""
    print(f"Selected file: {filepath}")
    
    if filepath.startswith('http'):
        print("Remote file detected")
        return filepath
    
    try:
        info = validate_media_file(filepath)
        print(f"File size: {info['size'] / (1024 * 1024):.1f}MB")
        print(f"File type: {info['extension']}")
    except Exception as e:
        print(f"Warning: {e}")
    
    while True:
        confirm = input("Proceed with this file? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            return filepath
        elif confirm in ['n', 'no']:
            return None
        else:
            print("Please enter 'y' or 'n'")


def get_media_file_path():
    """Get and validate media file path from user"""
    while True:
        filepath = get_user_input_with_validation(
            "Please enter the path to your media file (local path or URL): "
        )
        
        confirmed_path = confirm_file_path(filepath)
        if confirmed_path:
            return confirmed_path
        
        print("Please select a different file.")


def list_output_files(output_dir):
    """List all files in output directory"""
    if not os.path.exists(output_dir):
        print(f"Output directory does not exist: {output_dir}")
        return []
    
    files = []
    for filename in os.listdir(output_dir):
        filepath = os.path.join(output_dir, filename)
        if os.path.isfile(filepath):
            files.append(filepath)
    
    return sorted(files)


def print_completion_summary(output_dir):
    """Print summary of generated files"""
    files = list_output_files(output_dir)
    
    if not files:
        print("No output files found.")
        return
    
    print(f"\n=== Processing Complete ===")
    print(f"Output directory: {output_dir}")
    print(f"Generated files ({len(files)}):")
    
    for filepath in files:
        filename = os.path.basename(filepath)
        size = os.path.getsize(filepath)
        print(f"  - {filename} ({size:,} bytes)")
    
    print("===========================\n")