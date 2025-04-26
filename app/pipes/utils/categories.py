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
categories_mapping = {
    "Computers_and_Accessories": ["computers", "laptops", "desktops", "monitors", "printers"],
    "Tools_and_Home_Improvement": ["tools", "home"],
    "Camera_and_Photo": ["cameras", "photography"],
    "Office_Products": ["office", "supplies", "stationery"],
    "Cellphones_and_Accessories": ["cellphone", "mobile", "smartphone"],
    "Luggage_and_Travel_Gear": ["luggage", "travel", "bag"],
    "Video_Games": ["game", "console", "gaming"],
    "Musical_Instruments": ["instrument", "music"],
    "Other_Electronics": ["electronics", "gadgets"],
}
