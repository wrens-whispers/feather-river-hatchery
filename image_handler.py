import os
from PIL import Image

def get_available_images():
    """Get list of all images in the images folder"""
    image_folder = "images"
    if not os.path.exists(image_folder):
        return []
    
    image_files = [f for f in os.listdir(image_folder) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return image_files

def find_relevant_image(query):
    """Find exact or partial keyword match in image filenames"""
    images = get_available_images()
    query_lower = query.lower()
    
    # First try: exact word match
    query_words = query_lower.split()
    for image in images:
        image_name = image.lower().replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
        if image_name in query_words:
            return f"images/{image}"
    
    # Second try: partial match (keyword appears anywhere in query)
    for image in images:
        image_name = image.lower().replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
        if image_name in query_lower:
            return f"images/{image}"
    
    return None

def get_image_description(image_path):
    """Get basic info about the image"""
    if not image_path or not os.path.exists(image_path):
        return None
    
    filename = os.path.basename(image_path)
    # Convert filename to readable description
    description = filename.replace('-', ' ').replace('_', ' ').replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
    return description.title()