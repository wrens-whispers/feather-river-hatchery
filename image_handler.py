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
    """Find image based on simple keyword rules"""
    query_lower = query.lower()
    
    # Debug: print what we're searching
    print(f"SEARCHING FOR IMAGE IN: {query_lower[:100]}...")
    
    # Simple keyword to image mapping
    image_map = {
        'chinook': 'chinook.jpg',
        'eggs': 'eggs.jpg',
        'ladder': 'ladder.jpg',
        'spawn': 'spawning.jpg',
        'spawning': 'spawning.jpg',
        'steelhead': 'steelhead.jpg',
        'trout': 'trout.jpg',
        'lifecycle': 'lifecycle.jpg',
        'underwater': 'underwater.jpg',
        'viewing window': 'viewing-window.jpg',
        'window': 'viewing-window.jpg',
        'upstream': 'upstream.jpg',
        'ocean': 'ocean.jpg',
        'wild': 'wild.jpg',
        'habitat': 'habitat.jpg',
        'history': 'history.jpg',
        'fishing': 'fishing.jpg',
        'fishermen': 'fishermen.jpg',
        'raising': 'raising-nurturing.jpg',
        'nurturing': 'raising-nurturing.jpg',
        'waterfall': 'jumping-waterfall.jpg',
        'jumping': 'jumping-waterfall.jpg',
        'springs': 'domingo-springs.jpg',
        'domingo': 'domingo-springs.jpg'
    }
    
    # Check each keyword - simpler matching
    for keyword, image_file in image_map.items():
        if keyword in query_lower:
            print(f"MATCHED KEYWORD: {keyword} -> {image_file}")
            image_path = f"images/{image_file}"
            if os.path.exists(image_path):
                return image_path
    
    print("NO IMAGE MATCH FOUND")
    return None

def get_image_description(image_path):
    """Get basic info about the image"""
    if not image_path or not os.path.exists(image_path):
        return None
    
    filename = os.path.basename(image_path)
    # Convert filename to readable description
    description = filename.replace('-', ' ').replace('_', ' ').replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
    return description.title()