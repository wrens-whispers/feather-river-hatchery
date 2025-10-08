import os

def get_available_images():
    """Get list of all images in the images folder"""
    image_folder = "images"
    if not os.path.exists(image_folder):
        return []
    
    image_files = [f for f in os.listdir(image_folder) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    return image_files

def find_relevant_image(query):
    """Simple exact keyword matching - one keyword = one image"""
    query_lower = query.lower()
    
    # Direct mapping: if query contains this exact word, show this image
    keyword_to_image = {
        'chinook eggs': 'eggs.jpg',  # More specific first
        'salmon eggs': 'eggs.jpg',
        'fish ladder': 'ladder.jpg',  # More specific first
        'life cycle': 'lifecycle.jpg',  # More specific first
        'chinook': 'chinook.jpg',  # General terms after
        'eggs': 'eggs.jpg',
        'egg': 'eggs.jpg',
        'fishermen': 'fishermen.jpg',
        'fisherman': 'fishermen.jpg',
        'fishing': 'fishing.jpg',
        'habitat': 'habitat.jpg',
        'hatchery': 'hatchery.jpg',
        'ladder': 'ladder.jpg',
        'lifecycle': 'lifecycle.jpg',
        'spawn': 'spawn.jpg',
        'spawning': 'spawning.jpg',
        'steelhead': 'steelhead.jpg',
        'trout': 'trout.jpg',
        'watch': 'underwater.jpg',
        'underwater': 'underwater.jpg',
        'upstream': 'upstream.jpg',
        'window': 'viewing-window.jpg',
        'viewing': 'viewing-window.jpg',
        'wild': 'wild.jpg',
    }
    
    # Check each keyword
    for keyword, image_file in keyword_to_image.items():
        if keyword in query_lower:
            return f"images/{image_file}"
    
    return None

def get_image_description(image_path):
    """Get basic info about the image"""
    if not image_path or not os.path.exists(image_path):
        return None
    
    filename = os.path.basename(image_path)
    description = filename.replace('-', ' ').replace('_', ' ').replace('.jpg', '').replace('.jpeg', '').replace('.png', '')
    return description.title()