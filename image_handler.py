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
        # More specific multi-word phrases first (English and Spanish)
        'chinook eggs': 'eggs.jpg',
        'huevos de chinook': 'eggs.jpg',
        'salmon eggs': 'eggs.jpg',
        'huevos de salmón': 'eggs.jpg',
        'fish ladder': 'ladder.jpg',
        'escalera de peces': 'ladder.jpg',
        'life cycle': 'lifecycle.jpg',
        'ciclo de vida': 'lifecycle.jpg',
        'bajo el agua': 'underwater.jpg',
        'río arriba': 'upstream.jpg',

        # General single words (English and Spanish with conjugations)
        'chinook': 'chinook.jpg',
        'ciclo': 'lifecycle.jpg',
        'criadero': 'hatchery.jpg',
        'desova': 'spawn.jpg',  # he/she/it spawns
        'desovan': 'spawn.jpg',  # they spawn
        'desovar': 'spawn.jpg',  # to spawn (infinitive)
        'desove': 'spawning.jpg',  # spawning (noun)
        'egg': 'eggs.jpg',
        'eggs': 'eggs.jpg',
        'escalera': 'ladder.jpg',
        'fish': 'fish.jpg',
        'fisherman': 'fishermen.jpg',
        'fishermen': 'fishermen.jpg',
        'fishing': 'fishing.jpg',
        'habitat': 'habitat.jpg',
        'hábitat': 'habitat.jpg',
        'hatchery': 'hatchery.jpg',
        'historia': 'history.jpg',
        'history': 'history.jpg',
        'huevo': 'eggs.jpg',
        'huevos': 'eggs.jpg',
        'ladder': 'ladder.jpg',
        'lifecycle': 'lifecycle.jpg',
        'look': 'underwater.jpg',
        'mira': 'underwater.jpg',  # look! (command) / he/she looks
        'miran': 'underwater.jpg',  # they look
        'mirar': 'underwater.jpg',  # to look (infinitive)
        'miro': 'underwater.jpg',  # I look
        'observa': 'viewing-window.jpg',  # observe! / he/she observes
        'observación': 'viewing-window.jpg',
        'observan': 'viewing-window.jpg',  # they observe
        'observo': 'viewing-window.jpg',  # I observe
        'ocean': 'ocean.jpg',
        'océano': 'ocean.jpg',
        'pesca': 'fishing.jpg',  # fishing (noun) / he/she fishes
        'pescan': 'fishing.jpg',  # they fish
        'pescador': 'fishermen.jpg',
        'pescadores': 'fishermen.jpg',
        'pez': 'fish.jpg',
        'salvaje': 'wild.jpg',
        'see': 'underwater.jpg',
        'spawn': 'spawn.jpg',
        'spawning': 'spawning.jpg',
        'steelhead': 'steelhead.jpg',
        'trout': 'trout.jpg',
        'trucha': 'trout.jpg',
        'underwater': 'underwater.jpg',
        'upstream': 'upstream.jpg',
        've': 'underwater.jpg',  # see! (command) / he/she sees
        'ven': 'underwater.jpg',  # they see / come here
        'ventana': 'viewing-window.jpg',
        'veo': 'underwater.jpg',  # I see
        'ver': 'underwater.jpg',  # to see (infinitive)
        'viewing': 'viewing-window.jpg',
        'watch': 'underwater.jpg',
        'wild': 'wild.jpg',
        'window': 'viewing-window.jpg',
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