categories = [
    "Computers_and_Accessories",
    "Tools_and_Home_Improvement",
    "Camera_and_Photo",
    "Office_Products",
    "Cellphones_and_Accessories",
    "Luggage_and_Travel_Gear",
    "Video_Games",
    "Musical_Instruments",
    "Other_Electronics",
]


# Categories mapping should be carefully picked because if the NER model identifies them as categories, only products containing these in the category field will be returned.
# Some terms intentionally appear in multiple categories to support cross-category search
categories_mapping = {
    "Computers_and_Accessories": [
        "computers", "laptops", "desktops", "monitors", "printers", "keyboard", "mouse", "router", 
        "networking", "storage", "hard drive", "ssd", "ram", "memory", "processor", "cpu", "gpu", 
        "graphics card", "motherboard", "power supply", "pc", "computer accessories", "usb", 
        "cables", "adapters", "webcam", "headset", "speakers", "tablet", "scanner", "server",
        "printer", "bluetooth", "charger", "wireless", "bluetooth speakers", "wireless keyboard",
        "wireless mouse", "office equipment", "computer scanner", "all-in-one printer", "multifunction printer"
    ],
    "Tools_and_Home_Improvement": [
        "tools", "home", "improvement", "drill", "screwdriver", "hammer", "saw", "wrench", 
        "pliers", "sander", "power tools", "hand tools", "measuring", "hardware", "nails", "screws", 
        "plumbing", "electrical", "lighting", "paint", "renovation", "construction", "workshop", 
        "garage", "lawn", "garden", "outdoor", "smart home", "security", "locks", "thermostats",
        "security camera", "doorbell", "smart thermostat", "smart lighting", "smart speaker",
        "home monitoring", "home automation", "smart lock"
    ],
    "Camera_and_Photo": [
        "cameras", "photography", "digital camera", "dslr", "mirrorless", "point and shoot", 
        "lenses", "tripod", "flash", "lighting", "camera bag", "memory card", "sd card", 
        "photo printer", "camera accessories", "filters", "action camera", "gopro", "film", 
        "camcorder", "video camera", "drone", "photography equipment", "studio", "photo editing",
        "smartphone camera", "mobile photography", "camera phone", "smartphone lens",
        "camera storage", "photo scanner", "photo storage"
    ],
    "Office_Products": [
        "office", "supplies", "stationery", "printer paper", "pens", "pencils", "markers", 
        "notebooks", "binders", "folders", "filing", "desk", "chair", "office furniture", 
        "calculator", "shredder", "laminator", "paper clips", "stapler", "tape", "sticky notes", 
        "calendar", "planner", "whiteboard", "bulletin board", "envelopes", "labels", "business cards",
        "scanner", "printer", "multifunction printer", "office electronics", "document scanner",
        "copy machine", "fax machine", "office equipment", "all-in-one printer", "laser printer",
        "inkjet printer", "office chair", "desk accessories", "computer desk", "office storage"
    ],
    "Cellphones_and_Accessories": [
        "cellphone", "mobile", "smartphone", "phone", "iphone", "android", "samsung", "pixel", 
        "phone case", "screen protector", "charger", "power bank", "wireless charger", "phone stand", 
        "phone holder", "headphones", "earbuds", "bluetooth", "phone accessories", "selfie stick", 
        "sim card", "memory card", "phone wallet", "phone grip", "phone mount", "phone repair",
        "mobile audio", "bluetooth headphones", "wireless earbuds", "smartphone photography",
        "mobile gaming", "smartphone gaming", "phone tripod", "smartphone lens", "mobile camera"
    ],
    "Luggage_and_Travel_Gear": [
        "luggage", "travel", "bag", "suitcase", "carry-on", "backpack", "duffel bag", "tote", 
        "travel accessories", "passport holder", "travel pillow", "travel adapter", "packing cubes", 
        "toiletry bag", "luggage tags", "luggage lock", "travel wallet", "money belt", "travel bottles", 
        "travel scale", "travel umbrella", "travel bags", "rolling luggage", "hardside", "softside",
        "laptop bag", "laptop backpack", "camera bag", "electronics travel organizer", 
        "phone travel accessories", "travel charger", "travel power bank", "document holder"
    ],
    "Video_Games": [
        "game", "console", "gaming", "playstation", "xbox", "nintendo", "switch", "pc gaming", 
        "video game", "controller", "gaming headset", "gaming keyboard", "gaming mouse", "gaming chair", 
        "gaming desk", "gaming monitor", "vr", "virtual reality", "game accessories", "game cards", 
        "gaming laptop", "gaming pc", "game software", "digital games", "game downloads", "game streaming",
        "mobile gaming", "smartphone gaming", "tablet gaming", "handheld console", "gaming headphones",
        "gaming earbuds", "gaming smartphone", "game streaming device", "gaming accessories"
    ],
    "Musical_Instruments": [
        "instrument", "music", "guitar", "piano", "keyboard", "drums", "violin", "bass", "saxophone", 
        "trumpet", "flute", "clarinet", "ukulele", "banjo", "amplifier", "microphone", "audio interface", 
        "music stand", "instrument accessories", "music books", "sheet music", "strings", "picks", 
        "pedals", "synthesizer", "recording equipment", "dj equipment", "midi controller",
        "music keyboard", "digital piano", "electronic keyboard", "wireless microphone", "bluetooth speaker",
        "music production", "music software", "digital audio", "headphones", "studio headphones",
        "music headphones", "audio mixer", "recording studio", "music streaming"
    ],
    "Other_Electronics": [
        "electronics", "gadgets", "tv", "television", "smart tv", "home theater", "audio", "speakers", 
        "headphones", "earbuds", "projector", "streaming device", "roku", "amazon fire", "apple tv", 
        "wearables", "smartwatch", "fitness tracker", "smart home", "security camera", "doorbell", 
        "thermostat", "bluetooth speakers", "wireless earbuds", "power strips", "batteries", "chargers",
        "tablet", "e-reader", "kindle", "smart glasses", "virtual assistant", "smart speaker",
        "amazon echo", "google home", "apple homepod", "wireless headphones", "gaming accessories",
        "computer accessories", "camera accessories", "photo accessories", "portable charger", "power bank"
    ],
}
