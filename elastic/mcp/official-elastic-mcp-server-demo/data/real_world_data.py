"""
Real-world destination data for the Travel Advisory Application.
This module contains realistic destination information that will be used
to generate correlated data across all indices.
"""

# Real-world destinations with accurate information
REAL_DESTINATIONS = [
    {
        "city": "Paris",
        "country": "France",
        "continent": "Europe",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "description": "Known as the City of Light, Paris is famous for its iconic Eiffel Tower, world-class museums like the Louvre, and charming boulevards. The city offers exceptional cuisine, fashion, and a romantic atmosphere along the Seine River.",
        "best_season": "Spring",
        "climate": "Temperate",
        "language": "French",
        "currency": "EUR",
        "timezone": "Europe/Paris",
        "safety_rating": 8,
        "popularity_score": 95,
        "cost_level": "Luxury",
        "tags": ["Cultural", "Historical", "Romantic", "Urban", "Culinary"]
    },
    {
        "city": "Tokyo",
        "country": "Japan",
        "continent": "Asia",
        "latitude": 35.6762,
        "longitude": 139.6503,
        "description": "Tokyo is a dynamic metropolis that blends ultramodern and traditional elements. From neon-lit skyscrapers and anime culture to historic temples and cherry blossoms, Tokyo offers visitors a unique blend of innovation and tradition.",
        "best_season": "Spring",
        "climate": "Temperate",
        "language": "Japanese",
        "currency": "JPY",
        "timezone": "Asia/Tokyo",
        "safety_rating": 9,
        "popularity_score": 90,
        "cost_level": "Luxury",
        "tags": ["Urban", "Cultural", "Culinary", "Shopping", "Technology"]
    },
    {
        "city": "New York",
        "country": "United States",
        "continent": "North America",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "description": "The Big Apple is a global center for media, culture, art, fashion, and finance. With iconic landmarks like Times Square, Central Park, and the Statue of Liberty, New York City offers endless entertainment options and diverse neighborhoods to explore.",
        "best_season": "Fall",
        "climate": "Continental",
        "language": "English",
        "currency": "USD",
        "timezone": "America/New_York",
        "safety_rating": 7,
        "popularity_score": 92,
        "cost_level": "Luxury",
        "tags": ["Urban", "Cultural", "Shopping", "Nightlife", "Culinary"]
    },
    {
        "city": "Rome",
        "country": "Italy",
        "continent": "Europe",
        "latitude": 41.9028,
        "longitude": 12.4964,
        "description": "The Eternal City is a living museum of ancient ruins, Renaissance art, and vibrant street life. From the Colosseum and Vatican City to charming piazzas and trattorias, Rome offers visitors a journey through history while enjoying la dolce vita.",
        "best_season": "Spring",
        "climate": "Mediterranean",
        "language": "Italian",
        "currency": "EUR",
        "timezone": "Europe/Rome",
        "safety_rating": 7,
        "popularity_score": 88,
        "cost_level": "Moderate",
        "tags": ["Historical", "Cultural", "Culinary", "Religious", "Urban"]
    },
    {
        "city": "Sydney",
        "country": "Australia",
        "continent": "Oceania",
        "latitude": -33.8688,
        "longitude": 151.2093,
        "description": "Sydney is a vibrant harbor city known for its iconic Opera House, Harbour Bridge, and beautiful beaches. With a perfect blend of urban sophistication and natural beauty, Sydney offers visitors world-class dining, cultural experiences, and outdoor adventures.",
        "best_season": "Summer",
        "climate": "Temperate",
        "language": "English",
        "currency": "AUD",
        "timezone": "Australia/Sydney",
        "safety_rating": 9,
        "popularity_score": 85,
        "cost_level": "Luxury",
        "tags": ["Beach", "Urban", "Cultural", "Outdoor", "Relaxation"]
    },
    {
        "city": "Cape Town",
        "country": "South Africa",
        "continent": "Africa",
        "latitude": -33.9249,
        "longitude": 18.4241,
        "description": "Cape Town is a stunning coastal city nestled between mountains and the sea. With attractions like Table Mountain, Cape of Good Hope, and Robben Island, it offers a mix of natural beauty, wildlife, cultural diversity, and historical significance.",
        "best_season": "Summer",
        "climate": "Mediterranean",
        "language": "English",
        "currency": "ZAR",
        "timezone": "Africa/Johannesburg",
        "safety_rating": 6,
        "popularity_score": 80,
        "cost_level": "Moderate",
        "tags": ["Beach", "Mountain", "Cultural", "Outdoor", "Wildlife"]
    },
    {
        "city": "Rio de Janeiro",
        "country": "Brazil",
        "continent": "South America",
        "latitude": -22.9068,
        "longitude": -43.1729,
        "description": "Rio de Janeiro is famous for its stunning landscapes, vibrant culture, and festive atmosphere. From the iconic Christ the Redeemer statue and Copacabana Beach to samba music and Carnival celebrations, Rio offers visitors a lively and unforgettable experience.",
        "best_season": "Summer",
        "climate": "Tropical",
        "language": "Portuguese",
        "currency": "BRL",
        "timezone": "America/Sao_Paulo",
        "safety_rating": 5,
        "popularity_score": 82,
        "cost_level": "Moderate",
        "tags": ["Beach", "Mountain", "Cultural", "Nightlife", "Outdoor"]
    },
    {
        "city": "Bangkok",
        "country": "Thailand",
        "continent": "Asia",
        "latitude": 13.7563,
        "longitude": 100.5018,
        "description": "Bangkok is a vibrant city known for its ornate shrines, bustling street life, and boat-filled canals. The city offers a fascinating mix of traditional Thai culture, modern skyscrapers, exotic food, and vibrant nightlife.",
        "best_season": "Winter",
        "climate": "Tropical",
        "language": "Thai",
        "currency": "THB",
        "timezone": "Asia/Bangkok",
        "safety_rating": 7,
        "popularity_score": 85,
        "cost_level": "Budget",
        "tags": ["Cultural", "Urban", "Culinary", "Shopping", "Nightlife"]
    },
    {
        "city": "Barcelona",
        "country": "Spain",
        "continent": "Europe",
        "latitude": 41.3851,
        "longitude": 2.1734,
        "description": "Barcelona is a vibrant city known for its unique architecture, Mediterranean beaches, and rich cultural heritage. From Gaudí's masterpieces like Sagrada Familia to the Gothic Quarter and lively Las Ramblas, Barcelona offers a perfect blend of history, art, and coastal charm.",
        "best_season": "Spring",
        "climate": "Mediterranean",
        "language": "Spanish",
        "currency": "EUR",
        "timezone": "Europe/Madrid",
        "safety_rating": 7,
        "popularity_score": 87,
        "cost_level": "Moderate",
        "tags": ["Beach", "Cultural", "Historical", "Urban", "Culinary"]
    },
    {
        "city": "Dubai",
        "country": "United Arab Emirates",
        "continent": "Asia",
        "latitude": 25.2048,
        "longitude": 55.2708,
        "description": "Dubai is a city of superlatives, known for its ultramodern architecture, luxury shopping, and vibrant nightlife. From the world's tallest building, Burj Khalifa, to artificial islands and indoor ski slopes, Dubai showcases human innovation in the middle of the desert.",
        "best_season": "Winter",
        "climate": "Dry",
        "language": "Arabic",
        "currency": "AED",
        "timezone": "Asia/Dubai",
        "safety_rating": 9,
        "popularity_score": 86,
        "cost_level": "Luxury",
        "tags": ["Urban", "Shopping", "Luxury", "Desert", "Beach"]
    },
    {
        "city": "Kyoto",
        "country": "Japan",
        "continent": "Asia",
        "latitude": 35.0116,
        "longitude": 135.7681,
        "description": "Kyoto is Japan's cultural heart, famous for its classical Buddhist temples, gardens, imperial palaces, and traditional wooden houses. The city offers visitors a glimpse into Japan's rich history and traditions, from tea ceremonies to geisha culture.",
        "best_season": "Spring",
        "climate": "Temperate",
        "language": "Japanese",
        "currency": "JPY",
        "timezone": "Asia/Tokyo",
        "safety_rating": 9,
        "popularity_score": 84,
        "cost_level": "Moderate",
        "tags": ["Cultural", "Historical", "Religious", "Traditional", "Nature"]
    },
    {
        "city": "Amsterdam",
        "country": "Netherlands",
        "continent": "Europe",
        "latitude": 52.3676,
        "longitude": 4.9041,
        "description": "Amsterdam is known for its artistic heritage, elaborate canal system, and narrow houses with gabled facades. The city offers world-class museums like the Van Gogh Museum, historic sites like Anne Frank House, and a laid-back atmosphere with bicycle-friendly streets.",
        "best_season": "Spring",
        "climate": "Temperate",
        "language": "Dutch",
        "currency": "EUR",
        "timezone": "Europe/Amsterdam",
        "safety_rating": 8,
        "popularity_score": 83,
        "cost_level": "Moderate",
        "tags": ["Cultural", "Historical", "Urban", "Nightlife", "Romantic"]
    },
    {
        "city": "Marrakech",
        "country": "Morocco",
        "continent": "Africa",
        "latitude": 31.6295,
        "longitude": -7.9811,
        "description": "Marrakech is a magical place known for its medina, a medieval walled city with mazelike alleys. The city offers vibrant souks, stunning palaces, beautiful gardens, and a unique blend of Berber, Arab, and French cultural influences.",
        "best_season": "Spring",
        "climate": "Dry",
        "language": "Arabic",
        "currency": "MAD",
        "timezone": "Africa/Casablanca",
        "safety_rating": 7,
        "popularity_score": 79,
        "cost_level": "Budget",
        "tags": ["Cultural", "Historical", "Shopping", "Desert", "Exotic"]
    },
    {
        "city": "Vancouver",
        "country": "Canada",
        "continent": "North America",
        "latitude": 49.2827,
        "longitude": -123.1207,
        "description": "Vancouver is a bustling seaport known for its stunning natural beauty and cultural diversity. Surrounded by mountains and water, the city offers outdoor activities year-round, from skiing to kayaking, along with vibrant neighborhoods, parks, and cultural attractions.",
        "best_season": "Summer",
        "climate": "Temperate",
        "language": "English",
        "currency": "CAD",
        "timezone": "America/Vancouver",
        "safety_rating": 9,
        "popularity_score": 82,
        "cost_level": "Moderate",
        "tags": ["Outdoor", "Mountain", "Urban", "Nature", "Cultural"]
    },
    {
        "city": "Singapore",
        "country": "Singapore",
        "continent": "Asia",
        "latitude": 1.3521,
        "longitude": 103.8198,
        "description": "Singapore is a global financial center with a tropical climate and multicultural population. The city-state offers visitors futuristic architecture, lush gardens, luxury shopping, diverse cuisine, and a perfect blend of Chinese, Malay, Indian, and Western influences.",
        "best_season": "Year-round",
        "climate": "Tropical",
        "language": "English",
        "currency": "SGD",
        "timezone": "Asia/Singapore",
        "safety_rating": 10,
        "popularity_score": 84,
        "cost_level": "Luxury",
        "tags": ["Urban", "Cultural", "Culinary", "Shopping", "Modern"]
    },
    {
        "city": "Prague",
        "country": "Czech Republic",
        "continent": "Europe",
        "latitude": 50.0755,
        "longitude": 14.4378,
        "description": "Prague is a fairytale city known for its well-preserved medieval center. With its stunning castle, Charles Bridge, astronomical clock, and Gothic churches, the city offers visitors a journey through European history while enjoying Czech beer and culture.",
        "best_season": "Spring",
        "climate": "Continental",
        "language": "Czech",
        "currency": "CZK",
        "timezone": "Europe/Prague",
        "safety_rating": 8,
        "popularity_score": 85,
        "cost_level": "Budget",
        "tags": ["Historical", "Cultural", "Urban", "Romantic", "Architectural"]
    },
    {
        "city": "Bali",
        "country": "Indonesia",
        "continent": "Asia",
        "latitude": -8.3405,
        "longitude": 115.0920,
        "description": "Bali is a tropical paradise known for its forested volcanic mountains, iconic rice paddies, beaches, and coral reefs. The island offers visitors spiritual experiences at ancient temples, wellness retreats, surf spots, and a vibrant arts scene.",
        "best_season": "Summer",
        "climate": "Tropical",
        "language": "Indonesian",
        "currency": "IDR",
        "timezone": "Asia/Makassar",
        "safety_rating": 7,
        "popularity_score": 86,
        "cost_level": "Budget",
        "tags": ["Beach", "Cultural", "Spiritual", "Nature", "Relaxation"]
    },
    {
        "city": "Cairo",
        "country": "Egypt",
        "continent": "Africa",
        "latitude": 30.0444,
        "longitude": 31.2357,
        "description": "Cairo is a bustling city on the Nile River, known for its ancient Egyptian treasures. From the pyramids of Giza and the Sphinx to the Egyptian Museum and Islamic architecture, Cairo offers visitors a journey through thousands of years of human history.",
        "best_season": "Winter",
        "climate": "Dry",
        "language": "Arabic",
        "currency": "EGP",
        "timezone": "Africa/Cairo",
        "safety_rating": 6,
        "popularity_score": 78,
        "cost_level": "Budget",
        "tags": ["Historical", "Cultural", "Ancient", "Desert", "Religious"]
    },
    {
        "city": "Buenos Aires",
        "country": "Argentina",
        "continent": "South America",
        "latitude": -34.6037,
        "longitude": -58.3816,
        "description": "Buenos Aires is a sophisticated city known for its European atmosphere, passionate tango dancing, and vibrant cultural scene. With its wide boulevards, distinct neighborhoods, steakhouses, and soccer enthusiasm, the city offers a unique South American experience.",
        "best_season": "Spring",
        "climate": "Temperate",
        "language": "Spanish",
        "currency": "ARS",
        "timezone": "America/Argentina/Buenos_Aires",
        "safety_rating": 6,
        "popularity_score": 79,
        "cost_level": "Budget",
        "tags": ["Cultural", "Urban", "Culinary", "Nightlife", "Historical"]
    },
    {
        "city": "Istanbul",
        "country": "Turkey",
        "continent": "Europe",
        "latitude": 41.0082,
        "longitude": 28.9784,
        "description": "Istanbul is a transcontinental city straddling Europe and Asia across the Bosphorus Strait. With its Byzantine and Ottoman architecture, vibrant bazaars, and rich history as Constantinople, Istanbul offers visitors a unique blend of Eastern and Western influences.",
        "best_season": "Spring",
        "climate": "Mediterranean",
        "language": "Turkish",
        "currency": "TRY",
        "timezone": "Europe/Istanbul",
        "safety_rating": 6,
        "popularity_score": 83,
        "cost_level": "Budget",
        "tags": ["Historical", "Cultural", "Religious", "Shopping", "Culinary"]
    }
]

# Famous attractions for each destination
DESTINATION_ATTRACTIONS = {
    "Paris": [
        {"name": "Eiffel Tower", "type": "Monument", "description": "Iconic iron lattice tower on the Champ de Mars, named after engineer Gustave Eiffel.", "price_range": "$$", "duration_minutes": 120, "tags": ["Iconic", "Historical", "Romantic"]},
        {"name": "Louvre Museum", "type": "Museum", "description": "World's largest art museum and historic monument housing the Mona Lisa and Venus de Milo.", "price_range": "$$", "duration_minutes": 180, "tags": ["Art", "Historical", "Cultural"]},
        {"name": "Notre-Dame Cathedral", "type": "Religious Site", "description": "Medieval Catholic cathedral on the Île de la Cité known for its French Gothic architecture.", "price_range": "Free", "duration_minutes": 60, "tags": ["Religious", "Historical", "Architectural"]},
        {"name": "Montmartre", "type": "District", "description": "Hilltop district known for its artistic history, the Sacré-Cœur Basilica, and stunning city views.", "price_range": "Free", "duration_minutes": 120, "tags": ["Cultural", "Artistic", "Scenic"]},
        {"name": "Palace of Versailles", "type": "Palace", "description": "Opulent royal château that was the seat of power until the French Revolution.", "price_range": "$$", "duration_minutes": 240, "tags": ["Historical", "Royal", "Gardens"]}
    ],
    "Tokyo": [
        {"name": "Tokyo Skytree", "type": "Tower", "description": "Tallest tower in Japan offering panoramic views of the city.", "price_range": "$$", "duration_minutes": 90, "tags": ["Modern", "Scenic", "Architectural"]},
        {"name": "Senso-ji Temple", "type": "Temple", "description": "Ancient Buddhist temple in Asakusa, Tokyo's oldest temple.", "price_range": "Free", "duration_minutes": 60, "tags": ["Religious", "Historical", "Cultural"]},
        {"name": "Shibuya Crossing", "type": "Landmark", "description": "Famous scramble crossing known as the busiest intersection in the world.", "price_range": "Free", "duration_minutes": 30, "tags": ["Urban", "Iconic", "Photography"]},
        {"name": "Meiji Shrine", "type": "Shrine", "description": "Shinto shrine dedicated to Emperor Meiji and Empress Shoken, set in a forested area.", "price_range": "Free", "duration_minutes": 90, "tags": ["Religious", "Nature", "Peaceful"]},
        {"name": "Tokyo Disneyland", "type": "Theme Park", "description": "Disney theme park featuring attractions, entertainment, and Disney characters.", "price_range": "$$$", "duration_minutes": 480, "tags": ["Family-friendly", "Entertainment", "Fun"]}
    ],
    "New York": [
        {"name": "Statue of Liberty", "type": "Monument", "description": "Iconic neoclassical sculpture on Liberty Island, a symbol of freedom and democracy.", "price_range": "$$", "duration_minutes": 180, "tags": ["Iconic", "Historical", "Patriotic"]},
        {"name": "Central Park", "type": "Park", "description": "Urban park spanning 843 acres in the heart of Manhattan.", "price_range": "Free", "duration_minutes": 120, "tags": ["Nature", "Recreation", "Relaxation"]},
        {"name": "Empire State Building", "type": "Skyscraper", "description": "Iconic 102-story skyscraper offering panoramic views of the city.", "price_range": "$$$", "duration_minutes": 90, "tags": ["Iconic", "Scenic", "Architectural"]},
        {"name": "Metropolitan Museum of Art", "type": "Museum", "description": "One of the world's largest and finest art museums with over 2 million works.", "price_range": "$$", "duration_minutes": 180, "tags": ["Art", "Cultural", "Historical"]},
        {"name": "Broadway", "type": "Theater", "description": "Theater district known for its numerous theaters and world-class performances.", "price_range": "$$", "duration_minutes": 180, "tags": ["Entertainment", "Cultural", "Performing Arts"]}
    ],
    "Rome": [
        {"name": "Colosseum", "type": "Historical Site", "description": "Ancient amphitheater that once hosted gladiatorial contests, the largest ever built.", "price_range": "$", "duration_minutes": 120, "tags": ["Historical", "Iconic", "Ancient"]},
        {"name": "Vatican Museums & Sistine Chapel", "type": "Museum", "description": "Vast museum complex housing Renaissance masterpieces including Michelangelo's Sistine Chapel ceiling.", "price_range": "$", "duration_minutes": 240, "tags": ["Art", "Religious", "Historical"]},
        {"name": "Trevi Fountain", "type": "Monument", "description": "Baroque fountain and one of the most famous fountains in the world.", "price_range": "Free", "duration_minutes": 30, "tags": ["Iconic", "Romantic", "Architectural"]},
        {"name": "Roman Forum", "type": "Historical Site", "description": "Ruins of ancient government buildings at the center of the Roman Empire.", "price_range": "$", "duration_minutes": 120, "tags": ["Historical", "Ancient", "Archaeological"]},
        {"name": "Pantheon", "type": "Monument", "description": "Remarkably preserved ancient Roman temple with the world's largest unreinforced concrete dome.", "price_range": "Free", "duration_minutes": 60, "tags": ["Historical", "Architectural", "Ancient"]}
    ],
    "Sydney": [
        {"name": "Sydney Opera House", "type": "Theater", "description": "Iconic performing arts venue and UNESCO World Heritage Site with distinctive sail-shaped roof.", "price_range": "$", "duration_minutes": 90, "tags": ["Iconic", "Cultural", "Architectural"]},
        {"name": "Sydney Harbour Bridge", "type": "Monument", "description": "Steel arch bridge offering BridgeClimb experiences with panoramic harbour views.", "price_range": "$$", "duration_minutes": 180, "tags": ["Iconic", "Adventure", "Scenic"]},
        {"name": "Bondi Beach", "type": "Beach", "description": "Famous crescent-shaped beach popular for surfing and the coastal walk to Coogee.", "price_range": "Free", "duration_minutes": 180, "tags": ["Beach", "Surfing", "Outdoor"]},
        {"name": "Taronga Zoo", "type": "Zoo", "description": "Harbourside zoo with over 4,000 animals and stunning views of the Sydney skyline.", "price_range": "$", "duration_minutes": 240, "tags": ["Wildlife", "Family-friendly", "Scenic"]},
        {"name": "Royal Botanic Garden", "type": "Park", "description": "30-hectare garden on the harbour foreshore with diverse plant collections.", "price_range": "Free", "duration_minutes": 120, "tags": ["Nature", "Relaxation", "Scenic"]}
    ],
    "Cape Town": [
        {"name": "Table Mountain", "type": "Natural Wonder", "description": "Flat-topped mountain offering cable car rides and hiking trails with panoramic views.", "price_range": "$", "duration_minutes": 240, "tags": ["Nature", "Hiking", "Scenic"]},
        {"name": "Robben Island", "type": "Historical Site", "description": "UNESCO World Heritage Site where Nelson Mandela was imprisoned, now a museum.", "price_range": "$", "duration_minutes": 240, "tags": ["Historical", "Cultural", "Educational"]},
        {"name": "Cape of Good Hope", "type": "Natural Wonder", "description": "Dramatic rocky headland at the southwestern tip of Africa.", "price_range": "$", "duration_minutes": 180, "tags": ["Nature", "Scenic", "Wildlife"]},
        {"name": "V&A Waterfront", "type": "Market", "description": "Vibrant harbour with shops, restaurants, and the Two Oceans Aquarium.", "price_range": "Free", "duration_minutes": 180, "tags": ["Shopping", "Dining", "Entertainment"]},
        {"name": "Kirstenbosch Botanical Garden", "type": "Park", "description": "World-renowned botanical garden on the eastern slopes of Table Mountain.", "price_range": "$", "duration_minutes": 180, "tags": ["Nature", "Gardens", "Scenic"]}
    ],
    "Rio de Janeiro": [
        {"name": "Christ the Redeemer", "type": "Monument", "description": "Iconic Art Deco statue of Jesus Christ atop Corcovado mountain overlooking the city.", "price_range": "$", "duration_minutes": 120, "tags": ["Iconic", "Religious", "Scenic"]},
        {"name": "Sugarloaf Mountain", "type": "Natural Wonder", "description": "Peak reached by cable car offering sweeping views of the harbour and city.", "price_range": "$", "duration_minutes": 180, "tags": ["Scenic", "Nature", "Iconic"]},
        {"name": "Copacabana Beach", "type": "Beach", "description": "World-famous 4km crescent beach known for its lively atmosphere.", "price_range": "Free", "duration_minutes": 180, "tags": ["Beach", "Iconic", "Nightlife"]},
        {"name": "Tijuca National Park", "type": "Park", "description": "World's largest urban forest with hiking trails, waterfalls, and wildlife.", "price_range": "Free", "duration_minutes": 240, "tags": ["Nature", "Hiking", "Wildlife"]},
        {"name": "Escadaria Selarón", "type": "Monument", "description": "Colourful mosaic staircase created by Chilean artist Jorge Selarón.", "price_range": "Free", "duration_minutes": 30, "tags": ["Art", "Cultural", "Photography"]}
    ],
    "Bangkok": [
        {"name": "Grand Palace", "type": "Palace", "description": "Dazzling complex that served as the official residence of the Kings of Siam since 1782.", "price_range": "$", "duration_minutes": 180, "tags": ["Historical", "Royal", "Cultural"]},
        {"name": "Wat Pho", "type": "Temple", "description": "Ancient temple housing a massive 46-metre gold-plated reclining Buddha.", "price_range": "$", "duration_minutes": 90, "tags": ["Religious", "Historical", "Cultural"]},
        {"name": "Chatuchak Weekend Market", "type": "Market", "description": "One of the world's largest outdoor markets with over 15,000 stalls.", "price_range": "Free", "duration_minutes": 240, "tags": ["Shopping", "Cultural", "Food"]},
        {"name": "Wat Arun", "type": "Temple", "description": "Stunning riverside temple with a distinctive spire decorated with colourful porcelain.", "price_range": "$", "duration_minutes": 60, "tags": ["Religious", "Scenic", "Architectural"]},
        {"name": "Khao San Road", "type": "Landmark", "description": "Famous backpacker street known for vibrant nightlife and street food.", "price_range": "Free", "duration_minutes": 120, "tags": ["Nightlife", "Food", "Cultural"]}
    ],
    "Barcelona": [
        {"name": "Sagrada Familia", "type": "Religious Site", "description": "Gaudí's unfinished masterpiece basilica, under construction since 1882.", "price_range": "$", "duration_minutes": 120, "tags": ["Architectural", "Religious", "Iconic"]},
        {"name": "Park Güell", "type": "Park", "description": "Whimsical public park designed by Gaudí with colourful mosaic work and city views.", "price_range": "$", "duration_minutes": 120, "tags": ["Architectural", "Nature", "Artistic"]},
        {"name": "La Rambla", "type": "Landmark", "description": "Tree-lined pedestrian boulevard stretching from Plaça de Catalunya to the waterfront.", "price_range": "Free", "duration_minutes": 90, "tags": ["Urban", "Shopping", "Cultural"]},
        {"name": "Gothic Quarter", "type": "District", "description": "Medieval neighbourhood with narrow streets, historic buildings, and the Barcelona Cathedral.", "price_range": "Free", "duration_minutes": 120, "tags": ["Historical", "Cultural", "Architectural"]},
        {"name": "Casa Batlló", "type": "Monument", "description": "Gaudí-designed building with a skeletal organic facade.", "price_range": "$", "duration_minutes": 90, "tags": ["Architectural", "Artistic", "Iconic"]}
    ],
    "Dubai": [
        {"name": "Burj Khalifa", "type": "Skyscraper", "description": "World's tallest building at 828 metres with observation decks.", "price_range": "$$", "duration_minutes": 120, "tags": ["Iconic", "Modern", "Scenic"]},
        {"name": "Dubai Mall", "type": "Market", "description": "World's largest shopping mall with 1,200+ stores, an aquarium, and ice rink.", "price_range": "Free", "duration_minutes": 300, "tags": ["Shopping", "Entertainment", "Family-friendly"]},
        {"name": "Palm Jumeirah", "type": "Landmark", "description": "Artificial archipelago shaped like a palm tree, home to luxury hotels.", "price_range": "Free", "duration_minutes": 180, "tags": ["Luxury", "Beach", "Modern"]},
        {"name": "Dubai Frame", "type": "Monument", "description": "150-metre tall picture frame-shaped structure offering views of old and new Dubai.", "price_range": "$", "duration_minutes": 60, "tags": ["Modern", "Scenic", "Architectural"]},
        {"name": "Dubai Miracle Garden", "type": "Park", "description": "World's largest natural flower garden with over 150 million flowers.", "price_range": "$", "duration_minutes": 120, "tags": ["Nature", "Photography", "Family-friendly"]}
    ],
    "Kyoto": [
        {"name": "Fushimi Inari Shrine", "type": "Shrine", "description": "Iconic shrine famous for thousands of vermilion torii gates winding up the mountainside.", "price_range": "Free", "duration_minutes": 180, "tags": ["Religious", "Iconic", "Hiking"]},
        {"name": "Kinkaku-ji (Golden Pavilion)", "type": "Temple", "description": "Zen Buddhist temple covered in gold leaf, reflected beautifully in its surrounding pond.", "price_range": "$", "duration_minutes": 60, "tags": ["Religious", "Iconic", "Scenic"]},
        {"name": "Arashiyama Bamboo Grove", "type": "Natural Wonder", "description": "Towering bamboo forest creating an otherworldly atmosphere in western Kyoto.", "price_range": "Free", "duration_minutes": 60, "tags": ["Nature", "Photography", "Peaceful"]},
        {"name": "Nijo Castle", "type": "Castle", "description": "UNESCO World Heritage Site built in 1603 with famous nightingale floors.", "price_range": "$", "duration_minutes": 120, "tags": ["Historical", "Architectural", "Cultural"]},
        {"name": "Gion District", "type": "District", "description": "Kyoto's most famous geisha district with traditional wooden machiya houses.", "price_range": "Free", "duration_minutes": 120, "tags": ["Cultural", "Traditional", "Historical"]}
    ],
    "Amsterdam": [
        {"name": "Rijksmuseum", "type": "Museum", "description": "National museum housing Rembrandt's Night Watch and Vermeer's Milkmaid.", "price_range": "$", "duration_minutes": 180, "tags": ["Art", "Cultural", "Historical"]},
        {"name": "Anne Frank House", "type": "Museum", "description": "Museum in the canal house where Anne Frank and her family hid during WWII.", "price_range": "$", "duration_minutes": 90, "tags": ["Historical", "Cultural", "Educational"]},
        {"name": "Van Gogh Museum", "type": "Museum", "description": "Museum housing the world's largest collection of Van Gogh's paintings and letters.", "price_range": "$", "duration_minutes": 120, "tags": ["Art", "Cultural", "Iconic"]},
        {"name": "Vondelpark", "type": "Park", "description": "Amsterdam's most famous park, popular for picnics, cycling, and open-air theatre.", "price_range": "Free", "duration_minutes": 120, "tags": ["Nature", "Recreation", "Relaxation"]},
        {"name": "Canal Ring", "type": "Landmark", "description": "UNESCO World Heritage canal network best explored by boat tour.", "price_range": "$", "duration_minutes": 90, "tags": ["Scenic", "Historical", "Romantic"]}
    ],
    "Marrakech": [
        {"name": "Jemaa el-Fnaa", "type": "Market", "description": "UNESCO-listed main square and marketplace, the heart of Marrakech's medina.", "price_range": "Free", "duration_minutes": 180, "tags": ["Cultural", "Food", "Entertainment"]},
        {"name": "Bahia Palace", "type": "Palace", "description": "19th-century palace with stunning Islamic architecture and lush gardens.", "price_range": "$", "duration_minutes": 90, "tags": ["Historical", "Architectural", "Cultural"]},
        {"name": "Majorelle Garden", "type": "Park", "description": "Botanical garden created by French painter Jacques Majorelle, later owned by Yves Saint Laurent.", "price_range": "$", "duration_minutes": 90, "tags": ["Nature", "Art", "Peaceful"]},
        {"name": "Koutoubia Mosque", "type": "Religious Site", "description": "Largest mosque in Marrakech with a 77-metre minaret visible across the city.", "price_range": "Free", "duration_minutes": 30, "tags": ["Religious", "Architectural", "Iconic"]},
        {"name": "Saadian Tombs", "type": "Historical Site", "description": "16th-century royal necropolis rediscovered in 1917, featuring intricate tilework.", "price_range": "$", "duration_minutes": 60, "tags": ["Historical", "Architectural", "Cultural"]}
    ],
    "Singapore": [
        {"name": "Gardens by the Bay", "type": "Park", "description": "Futuristic nature park with iconic Supertree Grove and climate-controlled conservatories.", "price_range": "$", "duration_minutes": 180, "tags": ["Nature", "Modern", "Iconic"]},
        {"name": "Marina Bay Sands", "type": "Landmark", "description": "Iconic integrated resort with rooftop infinity pool and SkyPark observation deck.", "price_range": "$", "duration_minutes": 120, "tags": ["Modern", "Luxury", "Scenic"]},
        {"name": "Sentosa Island", "type": "Theme Park", "description": "Resort island with Universal Studios, beaches, and adventure attractions.", "price_range": "$$", "duration_minutes": 480, "tags": ["Entertainment", "Beach", "Family-friendly"]},
        {"name": "Chinatown", "type": "District", "description": "Historic ethnic neighbourhood with temples, street food, and traditional shophouses.", "price_range": "Free", "duration_minutes": 120, "tags": ["Cultural", "Food", "Historical"]},
        {"name": "Singapore Botanic Gardens", "type": "Park", "description": "UNESCO World Heritage Site with the National Orchid Garden.", "price_range": "Free", "duration_minutes": 180, "tags": ["Nature", "Peaceful", "Educational"]}
    ],
    "Prague": [
        {"name": "Prague Castle", "type": "Castle", "description": "Largest ancient castle complex in the world, seat of Czech heads of state.", "price_range": "$", "duration_minutes": 240, "tags": ["Historical", "Architectural", "Iconic"]},
        {"name": "Charles Bridge", "type": "Monument", "description": "14th-century stone bridge lined with 30 baroque statues spanning the Vltava River.", "price_range": "Free", "duration_minutes": 60, "tags": ["Historical", "Scenic", "Iconic"]},
        {"name": "Old Town Square", "type": "Landmark", "description": "Historic square with the Astronomical Clock, Týn Church, and baroque buildings.", "price_range": "Free", "duration_minutes": 90, "tags": ["Historical", "Cultural", "Architectural"]},
        {"name": "St. Vitus Cathedral", "type": "Religious Site", "description": "Gothic cathedral within Prague Castle with stunning stained glass windows.", "price_range": "$", "duration_minutes": 60, "tags": ["Religious", "Architectural", "Historical"]},
        {"name": "Jewish Quarter (Josefov)", "type": "District", "description": "Historic Jewish ghetto with synagogues, the Old Jewish Cemetery, and museums.", "price_range": "$", "duration_minutes": 120, "tags": ["Historical", "Cultural", "Religious"]}
    ],
    "Istanbul": [
        {"name": "Hagia Sophia", "type": "Religious Site", "description": "Former cathedral and mosque, masterpiece of Byzantine architecture.", "price_range": "Free", "duration_minutes": 90, "tags": ["Historical", "Religious", "Architectural"]},
        {"name": "Blue Mosque", "type": "Religious Site", "description": "Iconic mosque known for its blue Iznik tilework and six minarets.", "price_range": "Free", "duration_minutes": 60, "tags": ["Religious", "Architectural", "Iconic"]},
        {"name": "Grand Bazaar", "type": "Market", "description": "One of the world's oldest and largest covered markets with over 4,000 shops.", "price_range": "Free", "duration_minutes": 180, "tags": ["Shopping", "Cultural", "Historical"]},
        {"name": "Topkapi Palace", "type": "Palace", "description": "Ottoman-era palace complex that served as the administrative center of the Ottoman Empire.", "price_range": "$", "duration_minutes": 180, "tags": ["Historical", "Royal", "Cultural"]},
        {"name": "Basilica Cistern", "type": "Historical Site", "description": "Underground cistern built in the 6th century with 336 marble columns.", "price_range": "$", "duration_minutes": 60, "tags": ["Historical", "Architectural", "Mysterious"]}
    ]
}

# Notable events for each destination (dates use month/day for reliable parsing)
DESTINATION_EVENTS = {
    "Paris": [
        {"name": "Bastille Day", "type": "Festival", "description": "French National Day commemorating the Storming of the Bastille with fireworks, military parades on the Champs-Élysées, and public celebrations.", "start_date": "July 14", "end_date": "July 14", "venue": "Champs-Élysées & Eiffel Tower", "local_significance": "High"},
        {"name": "Paris Fashion Week", "type": "Fashion", "description": "One of the Big Four fashion weeks showcasing haute couture and ready-to-wear collections from top designers like Chanel, Dior, and Louis Vuitton.", "start_date": "September 25", "end_date": "October 3", "venue": "Various venues across Paris", "local_significance": "High"},
        {"name": "Roland-Garros French Open", "type": "Sports", "description": "Grand Slam tennis tournament played on clay courts, one of the four major annual tennis events.", "start_date": "May 25", "end_date": "June 8", "venue": "Stade Roland-Garros", "local_significance": "High"},
        {"name": "Nuit Blanche", "type": "Cultural Celebration", "description": "All-night arts festival with free art installations, performances, and exhibitions across the city.", "start_date": "October 4", "end_date": "October 5", "venue": "Various locations across Paris", "local_significance": "Medium"},
        {"name": "Fête de la Musique", "type": "Festival", "description": "Annual music celebration with free concerts and performances on every street corner throughout the city.", "start_date": "June 21", "end_date": "June 21", "venue": "Citywide", "local_significance": "High"}
    ],
    "Tokyo": [
        {"name": "Cherry Blossom Festival (Hanami)", "type": "Festival", "description": "Celebration of cherry blossoms with viewing parties under sakura trees in parks across Tokyo.", "start_date": "March 25", "end_date": "April 10", "venue": "Ueno Park, Shinjuku Gyoen, Chidorigafuchi", "local_significance": "High"},
        {"name": "Tokyo Game Show", "type": "Exhibition", "description": "One of the largest video game expos in the world showcasing upcoming games and gaming technology.", "start_date": "September 18", "end_date": "September 21", "venue": "Makuhari Messe, Chiba", "local_significance": "Medium"},
        {"name": "Sumida River Fireworks Festival", "type": "Festival", "description": "One of Tokyo's oldest and most spectacular fireworks displays with over 20,000 fireworks launched.", "start_date": "July 26", "end_date": "July 26", "venue": "Sumida River, Asakusa", "local_significance": "High"},
        {"name": "Sanja Matsuri", "type": "Festival", "description": "One of Tokyo's largest and liveliest festivals featuring portable shrine processions through Asakusa.", "start_date": "May 16", "end_date": "May 18", "venue": "Senso-ji Temple, Asakusa", "local_significance": "High"},
        {"name": "Tokyo Marathon", "type": "Sports", "description": "One of the six World Marathon Majors attracting over 38,000 runners through iconic Tokyo landmarks.", "start_date": "March 2", "end_date": "March 2", "venue": "Tokyo Metropolitan Government Building to Tokyo Station", "local_significance": "High"}
    ],
    "New York": [
        {"name": "New Year's Eve Ball Drop", "type": "Celebration", "description": "Iconic ball drop celebration in Times Square attracting over a million spectators and broadcast worldwide.", "start_date": "December 31", "end_date": "January 1", "venue": "Times Square", "local_significance": "High"},
        {"name": "Macy's Thanksgiving Day Parade", "type": "Parade", "description": "Annual parade featuring giant character balloons, elaborate floats, marching bands, and celebrity performances.", "start_date": "November 27", "end_date": "November 27", "venue": "Central Park West to Macy's Herald Square", "local_significance": "High"},
        {"name": "US Open Tennis Championships", "type": "Sports", "description": "Grand Slam tennis tournament and the final major of the annual tennis calendar.", "start_date": "August 25", "end_date": "September 7", "venue": "USTA Billie Jean King National Tennis Center, Flushing Meadows", "local_significance": "High"},
        {"name": "New York Fashion Week", "type": "Fashion", "description": "Semi-annual fashion event showcasing collections from top American and international designers.", "start_date": "September 6", "end_date": "September 13", "venue": "Spring Studios & various venues", "local_significance": "High"},
        {"name": "NYC Marathon", "type": "Sports", "description": "World's largest marathon with over 50,000 runners passing through all five boroughs.", "start_date": "November 2", "end_date": "November 2", "venue": "Staten Island to Central Park", "local_significance": "High"}
    ],
    "Rome": [
        {"name": "Easter Mass at St. Peter's", "type": "Religious", "description": "Papal Easter Mass and Urbi et Orbi blessing at St. Peter's Square, attended by tens of thousands.", "start_date": "April 5", "end_date": "April 6", "venue": "St. Peter's Square, Vatican City", "local_significance": "High"},
        {"name": "Rome Film Festival", "type": "Exhibition", "description": "International film festival showcasing premieres and retrospectives at the Auditorium Parco della Musica.", "start_date": "October 15", "end_date": "October 25", "venue": "Auditorium Parco della Musica", "local_significance": "Medium"},
        {"name": "Festa de' Noantri", "type": "Festival", "description": "Traditional Trastevere neighborhood festival with processions, food stalls, and fireworks.", "start_date": "July 16", "end_date": "July 30", "venue": "Trastevere neighborhood", "local_significance": "Medium"}
    ],
    "Sydney": [
        {"name": "Sydney New Year's Eve Fireworks", "type": "Celebration", "description": "World-famous fireworks display over Sydney Harbour Bridge and Opera House, one of the first major NYE celebrations globally.", "start_date": "December 31", "end_date": "January 1", "venue": "Sydney Harbour", "local_significance": "High"},
        {"name": "Vivid Sydney", "type": "Festival", "description": "Annual festival of light, music, and ideas featuring spectacular light installations on the Opera House and Harbour Bridge.", "start_date": "May 23", "end_date": "June 14", "venue": "Sydney Opera House & Circular Quay", "local_significance": "High"},
        {"name": "Sydney Royal Easter Show", "type": "Fair", "description": "Australia's largest annual ticketed event featuring agricultural competitions, carnival rides, and food.", "start_date": "April 10", "end_date": "April 23", "venue": "Sydney Olympic Park", "local_significance": "High"}
    ],
    "Cape Town": [
        {"name": "Cape Town Jazz Festival", "type": "Concert", "description": "Africa's grandest gathering of jazz musicians, dubbed 'Africa's Grandest Gathering'.", "start_date": "March 27", "end_date": "March 28", "venue": "Cape Town International Convention Centre", "local_significance": "High"},
        {"name": "Cape Town Carnival", "type": "Parade", "description": "Vibrant street parade celebrating South African creativity with floats, costumes, and live music.", "start_date": "March 14", "end_date": "March 14", "venue": "Green Point Fan Walk", "local_significance": "Medium"},
        {"name": "Two Oceans Marathon", "type": "Sports", "description": "Ultra-marathon covering 56km around the Cape Peninsula, known as the world's most beautiful marathon.", "start_date": "April 19", "end_date": "April 19", "venue": "Newlands to UCT Campus", "local_significance": "High"}
    ],
    "Rio de Janeiro": [
        {"name": "Rio Carnival", "type": "Festival", "description": "World's largest carnival featuring samba parades, elaborate costumes, and street parties across the city.", "start_date": "February 14", "end_date": "February 18", "venue": "Sambadrome Marquês de Sapucaí", "local_significance": "High"},
        {"name": "Rock in Rio", "type": "Concert", "description": "One of the largest music festivals in the world featuring international rock, pop, and electronic artists.", "start_date": "September 19", "end_date": "September 28", "venue": "Parque Olímpico, Barra da Tijuca", "local_significance": "High"},
        {"name": "New Year's Eve at Copacabana", "type": "Celebration", "description": "Massive beach celebration with fireworks over Copacabana Beach attended by over 2 million people.", "start_date": "December 31", "end_date": "January 1", "venue": "Copacabana Beach", "local_significance": "High"}
    ],
    "Bangkok": [
        {"name": "Songkran Water Festival", "type": "Festival", "description": "Thai New Year celebration famous for massive water fights and traditional ceremonies across the city.", "start_date": "April 13", "end_date": "April 15", "venue": "Khao San Road & Silom Road", "local_significance": "High"},
        {"name": "Loy Krathong", "type": "Cultural Celebration", "description": "Festival of lights where floating lanterns and krathongs are released on waterways to honor the water goddess.", "start_date": "November 5", "end_date": "November 5", "venue": "Chao Phraya River & Lumpini Park", "local_significance": "High"},
        {"name": "Bangkok International Film Festival", "type": "Exhibition", "description": "Annual film festival showcasing Thai and international cinema.", "start_date": "November 20", "end_date": "November 30", "venue": "SF World Cinema, CentralWorld", "local_significance": "Medium"}
    ],
    "Barcelona": [
        {"name": "La Mercè Festival", "type": "Festival", "description": "Barcelona's biggest annual festival honoring the patron saint with human towers, fire runs, and concerts.", "start_date": "September 20", "end_date": "September 24", "venue": "Plaça de Sant Jaume & citywide", "local_significance": "High"},
        {"name": "Primavera Sound", "type": "Concert", "description": "Major international music festival featuring indie, rock, electronic, and pop artists.", "start_date": "June 5", "end_date": "June 7", "venue": "Parc del Fòrum", "local_significance": "High"},
        {"name": "Sant Jordi's Day", "type": "Cultural Celebration", "description": "Catalan celebration of love and literature where couples exchange roses and books.", "start_date": "April 23", "end_date": "April 23", "venue": "Las Ramblas & citywide", "local_significance": "High"}
    ],
    "Dubai": [
        {"name": "Dubai Shopping Festival", "type": "Fair", "description": "Month-long shopping extravaganza with massive discounts, entertainment, and fireworks across the city.", "start_date": "December 15", "end_date": "January 29", "venue": "Dubai Mall & citywide", "local_significance": "High"},
        {"name": "Dubai World Cup", "type": "Sports", "description": "World's richest horse race with a purse of $30.5 million, held at the state-of-the-art Meydan Racecourse.", "start_date": "March 28", "end_date": "March 28", "venue": "Meydan Racecourse", "local_significance": "High"},
        {"name": "Dubai Food Festival", "type": "Food Event", "description": "Citywide culinary celebration featuring restaurant deals, food trucks, and celebrity chef events.", "start_date": "February 21", "end_date": "March 8", "venue": "Various venues across Dubai", "local_significance": "Medium"}
    ],
    "Kyoto": [
        {"name": "Gion Matsuri", "type": "Festival", "description": "One of Japan's most famous festivals spanning the entire month with elaborate float processions.", "start_date": "July 1", "end_date": "July 31", "venue": "Yasaka Shrine & Shijo-dori", "local_significance": "High"},
        {"name": "Jidai Matsuri (Festival of Ages)", "type": "Parade", "description": "Historical parade with participants in costumes from different periods of Kyoto's 1,200-year history.", "start_date": "October 22", "end_date": "October 22", "venue": "Kyoto Imperial Palace to Heian Shrine", "local_significance": "High"},
        {"name": "Hanatoro Illumination", "type": "Cultural Celebration", "description": "Enchanting lantern illumination along the paths of Arashiyama's bamboo grove and Higashiyama district.", "start_date": "December 12", "end_date": "December 21", "venue": "Arashiyama & Higashiyama", "local_significance": "Medium"}
    ],
    "Amsterdam": [
        {"name": "King's Day (Koningsdag)", "type": "Festival", "description": "National holiday celebrating the King's birthday with citywide street parties, orange-themed festivities, and canal boat parades.", "start_date": "April 27", "end_date": "April 27", "venue": "Citywide, especially Vondelpark & canals", "local_significance": "High"},
        {"name": "Amsterdam Light Festival", "type": "Art Show", "description": "Winter light art festival with illuminated installations along Amsterdam's canals and waterways.", "start_date": "November 28", "end_date": "January 19", "venue": "Amsterdam canals", "local_significance": "Medium"},
        {"name": "Amsterdam Dance Event (ADE)", "type": "Concert", "description": "World's largest electronic music conference and festival with over 2,500 artists across 200 venues.", "start_date": "October 15", "end_date": "October 19", "venue": "Various clubs & venues across Amsterdam", "local_significance": "High"}
    ],
    "Marrakech": [
        {"name": "Marrakech International Film Festival", "type": "Exhibition", "description": "Prestigious film festival attracting international stars and filmmakers to the Red City.", "start_date": "November 28", "end_date": "December 6", "venue": "Palais des Congrès", "local_significance": "High"},
        {"name": "Marrakech Popular Arts Festival", "type": "Festival", "description": "Celebration of Moroccan folk arts featuring Berber music, dance, storytelling, and acrobatics.", "start_date": "July 10", "end_date": "July 14", "venue": "El Badi Palace", "local_significance": "Medium"},
        {"name": "Ramadan Nights", "type": "Cultural Celebration", "description": "Special evening celebrations during Ramadan with food markets, music, and community gatherings in Jemaa el-Fnaa.", "start_date": "March 1", "end_date": "March 29", "venue": "Jemaa el-Fnaa Square", "local_significance": "High"}
    ],
    "Vancouver": [
        {"name": "Celebration of Light", "type": "Festival", "description": "International fireworks competition over English Bay, one of the largest offshore fireworks competitions in the world.", "start_date": "July 19", "end_date": "July 26", "venue": "English Bay Beach", "local_significance": "High"},
        {"name": "Vancouver International Film Festival", "type": "Exhibition", "description": "Major film festival screening over 300 films from 80+ countries.", "start_date": "September 25", "end_date": "October 5", "venue": "Vancouver International Film Centre", "local_significance": "Medium"},
        {"name": "Vancouver Folk Music Festival", "type": "Concert", "description": "Annual outdoor music festival at Jericho Beach Park featuring folk, roots, and world music.", "start_date": "July 18", "end_date": "July 20", "venue": "Jericho Beach Park", "local_significance": "Medium"}
    ],
    "Singapore": [
        {"name": "Singapore Grand Prix", "type": "Sports", "description": "Formula 1 night race through the streets of Marina Bay, the first night race in F1 history.", "start_date": "October 3", "end_date": "October 5", "venue": "Marina Bay Street Circuit", "local_significance": "High"},
        {"name": "Chinese New Year Celebrations", "type": "Festival", "description": "Vibrant celebrations in Chinatown with lion dances, street performances, and the Chingay Parade.", "start_date": "January 29", "end_date": "February 12", "venue": "Chinatown & Marina Bay", "local_significance": "High"},
        {"name": "Singapore Food Festival", "type": "Food Event", "description": "Annual celebration of Singapore's diverse culinary heritage with food trails, masterclasses, and tastings.", "start_date": "July 18", "end_date": "August 3", "venue": "Various hawker centres & restaurants", "local_significance": "Medium"}
    ],
    "Prague": [
        {"name": "Prague Spring International Music Festival", "type": "Concert", "description": "Prestigious classical music festival running since 1946, featuring world-renowned orchestras and soloists.", "start_date": "May 12", "end_date": "June 3", "venue": "Rudolfinum & Municipal House", "local_significance": "High"},
        {"name": "Signal Festival", "type": "Art Show", "description": "Light art festival transforming Prague's historic buildings and streets with video mapping and light installations.", "start_date": "October 16", "end_date": "October 19", "venue": "Old Town Square & historic buildings", "local_significance": "Medium"},
        {"name": "Prague Christmas Markets", "type": "Fair", "description": "Enchanting Christmas markets in Old Town Square and Wenceslas Square with traditional crafts, food, and mulled wine.", "start_date": "November 29", "end_date": "January 6", "venue": "Old Town Square & Wenceslas Square", "local_significance": "High"}
    ],
    "Bali": [
        {"name": "Nyepi (Day of Silence)", "type": "Cultural Celebration", "description": "Balinese New Year marked by a day of complete silence, fasting, and meditation across the entire island.", "start_date": "March 29", "end_date": "March 29", "venue": "Island-wide", "local_significance": "High"},
        {"name": "Galungan & Kuningan", "type": "Cultural Celebration", "description": "Important Balinese Hindu festival celebrating the victory of good over evil with decorated temples and offerings.", "start_date": "April 16", "end_date": "April 26", "venue": "Temples island-wide", "local_significance": "High"},
        {"name": "Bali Arts Festival", "type": "Festival", "description": "Month-long celebration of Balinese art, dance, music, and culture with daily performances and exhibitions.", "start_date": "June 14", "end_date": "July 12", "venue": "Taman Werdhi Budaya Art Centre, Denpasar", "local_significance": "High"}
    ],
    "Cairo": [
        {"name": "Cairo International Film Festival", "type": "Exhibition", "description": "One of the oldest film festivals in the Middle East and Africa, showcasing international and Arab cinema.", "start_date": "November 15", "end_date": "November 24", "venue": "Cairo Opera House", "local_significance": "High"},
        {"name": "Sphinx Sound & Light Show", "type": "Cultural Celebration", "description": "Nightly spectacular narrating the history of ancient Egypt with dramatic lighting of the Pyramids and Sphinx.", "start_date": "January 1", "end_date": "December 31", "venue": "Giza Pyramids Complex", "local_significance": "Medium"},
        {"name": "Moulid an-Nabi", "type": "Religious", "description": "Celebration of the Prophet Muhammad's birthday with processions, sweets, and festivities.", "start_date": "September 5", "end_date": "September 5", "venue": "Al-Hussein Mosque & citywide", "local_significance": "High"}
    ],
    "Buenos Aires": [
        {"name": "Buenos Aires Tango Festival", "type": "Festival", "description": "World's largest tango festival and championship with milongas, performances, and classes across the city.", "start_date": "August 1", "end_date": "August 14", "venue": "La Usina del Arte & various milongas", "local_significance": "High"},
        {"name": "Feria de Mataderos", "type": "Fair", "description": "Traditional gaucho fair with folk music, dancing, horseback riding, and Argentine street food.", "start_date": "March 1", "end_date": "December 20", "venue": "Mataderos neighborhood", "local_significance": "Medium"},
        {"name": "Buenos Aires International Book Fair", "type": "Exhibition", "description": "One of the world's largest book fairs attracting over a million visitors with author talks and exhibitions.", "start_date": "April 24", "end_date": "May 12", "venue": "La Rural Exhibition Centre", "local_significance": "High"}
    ],
    "Istanbul": [
        {"name": "Istanbul Music Festival", "type": "Concert", "description": "Prestigious classical music and opera festival held in historic venues across the city.", "start_date": "June 1", "end_date": "June 28", "venue": "Atatürk Cultural Center & historic venues", "local_significance": "High"},
        {"name": "Istanbul Biennial", "type": "Art Show", "description": "Major contemporary art exhibition held biennially, transforming historic spaces into art venues.", "start_date": "September 14", "end_date": "November 10", "venue": "Various historic venues across Istanbul", "local_significance": "High"},
        {"name": "Tulip Festival", "type": "Festival", "description": "Annual spring festival celebrating Istanbul's Ottoman tulip heritage with millions of tulips planted across parks.", "start_date": "April 1", "end_date": "April 30", "venue": "Emirgan Park & Gülhane Park", "local_significance": "Medium"}
    ]
}

# Famous hotels for each destination
DESTINATION_HOTELS = {
    "Paris": [
        {"name": "The Ritz Paris", "brand": "The Ritz", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Concierge", "Room Service"]},
        {"name": "Four Seasons Hotel George V", "brand": "Four Seasons", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Business Center"]},
        {"name": "Hôtel Plaza Athénée", "brand": "Dorchester Collection", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "Le Meurice", "brand": "Dorchester Collection", "star_rating": 5, "amenities": ["Restaurant", "Bar", "Spa", "Room Service", "Concierge", "Business Center"]},
        {"name": "Hôtel de Crillon", "brand": "Rosewood", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Tokyo": [
        {"name": "Park Hyatt Tokyo", "brand": "Hyatt", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Gym", "Room Service"]},
        {"name": "The Ritz-Carlton Tokyo", "brand": "The Ritz-Carlton", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Business Center"]},
        {"name": "Mandarin Oriental Tokyo", "brand": "Mandarin Oriental", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "Aman Tokyo", "brand": "Aman", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "The Peninsula Tokyo", "brand": "Peninsula", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "New York": [
        {"name": "The Plaza", "brand": "Fairmont", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Business Center"]},
        {"name": "The St. Regis New York", "brand": "St. Regis", "star_rating": 5, "amenities": ["Restaurant", "Bar", "Spa", "Room Service", "Concierge", "Business Center"]},
        {"name": "Four Seasons Hotel New York", "brand": "Four Seasons", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Business Center"]},
        {"name": "The Ritz-Carlton New York, Central Park", "brand": "The Ritz-Carlton", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Business Center"]},
        {"name": "Mandarin Oriental, New York", "brand": "Mandarin Oriental", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Pool", "Room Service", "Concierge"]}
    ],
    "Rome": [
        {"name": "Hotel de Russie", "brand": "Rocco Forte", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "Hotel Hassler Roma", "brand": "Leading Hotels", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "The St. Regis Rome", "brand": "St. Regis", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Business Center"]},
        {"name": "Hotel Eden", "brand": "Dorchester Collection", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "Rome Cavalieri, A Waldorf Astoria Hotel", "brand": "Waldorf Astoria", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Sydney": [
        {"name": "Park Hyatt Sydney", "brand": "Hyatt", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Shangri-La Hotel Sydney", "brand": "Shangri-La", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Four Seasons Hotel Sydney", "brand": "Four Seasons", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "InterContinental Sydney", "brand": "InterContinental", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Business Center"]},
        {"name": "The Langham Sydney", "brand": "Langham", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Cape Town": [
        {"name": "One&Only Cape Town", "brand": "One&Only", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Belmond Mount Nelson Hotel", "brand": "Belmond", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "The Silo Hotel", "brand": "The Royal Portfolio", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Cape Grace Hotel", "brand": "Independent", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Twelve Apostles Hotel and Spa", "brand": "Red Carnation", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Rio de Janeiro": [
        {"name": "Belmond Copacabana Palace", "brand": "Belmond", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Hotel Fasano Rio de Janeiro", "brand": "Fasano", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Fairmont Rio de Janeiro Copacabana", "brand": "Fairmont", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Grand Hyatt Rio de Janeiro", "brand": "Hyatt", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Business Center"]},
        {"name": "Hotel Emiliano Rio", "brand": "Emiliano", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Bangkok": [
        {"name": "Mandarin Oriental Bangkok", "brand": "Mandarin Oriental", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "The Peninsula Bangkok", "brand": "Peninsula", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Shangri-La Hotel Bangkok", "brand": "Shangri-La", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Anantara Siam Bangkok Hotel", "brand": "Anantara", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "The Siam Hotel", "brand": "Independent", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Barcelona": [
        {"name": "Hotel Arts Barcelona", "brand": "The Ritz-Carlton", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "W Barcelona", "brand": "W Hotels", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Mandarin Oriental Barcelona", "brand": "Mandarin Oriental", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Majestic Hotel & Spa Barcelona", "brand": "Leading Hotels", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "El Palace Barcelona", "brand": "Independent", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Dubai": [
        {"name": "Burj Al Arab Jumeirah", "brand": "Jumeirah", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Atlantis The Royal", "brand": "Atlantis", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Armani Hotel Dubai", "brand": "Armani", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "One&Only The Palm", "brand": "One&Only", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Four Seasons Resort Dubai at Jumeirah Beach", "brand": "Four Seasons", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Kyoto": [
        {"name": "The Ritz-Carlton Kyoto", "brand": "The Ritz-Carlton", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "Four Seasons Hotel Kyoto", "brand": "Four Seasons", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Aman Kyoto", "brand": "Aman", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "Park Hyatt Kyoto", "brand": "Hyatt", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "Hotel The Mitsui Kyoto", "brand": "Marriott Luxury", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]}
    ],
    "Amsterdam": [
        {"name": "Waldorf Astoria Amsterdam", "brand": "Waldorf Astoria", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "Hotel De L'Europe Amsterdam", "brand": "Leading Hotels", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Conservatorium Hotel", "brand": "The Set", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Pulitzer Amsterdam", "brand": "Independent", "star_rating": 5, "amenities": ["Restaurant", "Bar", "Room Service", "Concierge", "Business Center", "Gym"]},
        {"name": "InterContinental Amstel Amsterdam", "brand": "InterContinental", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Marrakech": [
        {"name": "Royal Mansour Marrakech", "brand": "Royal Mansour", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "La Mamounia", "brand": "Independent", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Mandarin Oriental Marrakech", "brand": "Mandarin Oriental", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Four Seasons Resort Marrakech", "brand": "Four Seasons", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Amanjena", "brand": "Aman", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Vancouver": [
        {"name": "Fairmont Hotel Vancouver", "brand": "Fairmont", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Rosewood Hotel Georgia", "brand": "Rosewood", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Shangri-La Hotel Vancouver", "brand": "Shangri-La", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Fairmont Pacific Rim", "brand": "Fairmont", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Wedgewood Hotel & Spa", "brand": "Independent", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]}
    ],
    "Singapore": [
        {"name": "Marina Bay Sands", "brand": "Sands", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Raffles Singapore", "brand": "Raffles", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "The Fullerton Hotel Singapore", "brand": "Fullerton", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Capella Singapore", "brand": "Capella", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Mandarin Oriental Singapore", "brand": "Mandarin Oriental", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Prague": [
        {"name": "Four Seasons Hotel Prague", "brand": "Four Seasons", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Business Center"]},
        {"name": "Mandarin Oriental Prague", "brand": "Mandarin Oriental", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "The Augustine", "brand": "Marriott Luxury", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "Aria Hotel Prague", "brand": "Independent", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "Hotel Paris Prague", "brand": "Independent", "star_rating": 5, "amenities": ["Restaurant", "Bar", "Room Service", "Concierge", "Business Center", "Gym"]}
    ],
    "Bali": [
        {"name": "Four Seasons Resort Bali at Sayan", "brand": "Four Seasons", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "The Mulia Bali", "brand": "Mulia", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Ayana Resort Bali", "brand": "Ayana", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Mandapa, A Ritz-Carlton Reserve", "brand": "The Ritz-Carlton", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Bulgari Resort Bali", "brand": "Bulgari", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Cairo": [
        {"name": "Marriott Mena House Cairo", "brand": "Marriott", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Four Seasons Hotel Cairo at Nile Plaza", "brand": "Four Seasons", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "The St. Regis Cairo", "brand": "St. Regis", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Kempinski Nile Hotel Cairo", "brand": "Kempinski", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Sofitel Cairo Nile El Gezirah", "brand": "Sofitel", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Buenos Aires": [
        {"name": "Alvear Palace Hotel", "brand": "Leading Hotels", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Four Seasons Hotel Buenos Aires", "brand": "Four Seasons", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Palacio Duhau - Park Hyatt Buenos Aires", "brand": "Hyatt", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Faena Hotel Buenos Aires", "brand": "Faena", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Hotel Madero Buenos Aires", "brand": "Sofitel", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ],
    "Istanbul": [
        {"name": "Four Seasons Hotel Istanbul at Sultanahmet", "brand": "Four Seasons", "star_rating": 5, "amenities": ["Spa", "Restaurant", "Bar", "Room Service", "Concierge", "Gym"]},
        {"name": "Ciragan Palace Kempinski Istanbul", "brand": "Kempinski", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "The Ritz-Carlton Istanbul", "brand": "The Ritz-Carlton", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Raffles Istanbul", "brand": "Raffles", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]},
        {"name": "Shangri-La Bosphorus Istanbul", "brand": "Shangri-La", "star_rating": 5, "amenities": ["Pool", "Spa", "Restaurant", "Bar", "Room Service", "Concierge"]}
    ]
}

# Travel advisories for each country
COUNTRY_ADVISORIES = {
    "France": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in France. Some areas have increased risk.",
        "health_risks": "No major health risks. Healthcare system is excellent.",
        "safety_risks": "Petty crime in tourist areas. Occasional protests in major cities.",
        "entry_requirements": "Valid passport required. Visa not required for stays under 90 days for most nationalities.",
        "visa_required": False,
        "vaccination_required": ["None"]
    },
    "Japan": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in Japan.",
        "health_risks": "No major health risks. Healthcare system is excellent.",
        "safety_risks": "Low crime rate. Natural disasters such as earthquakes and typhoons may occur.",
        "entry_requirements": "Valid passport required. Visa requirements vary by nationality.",
        "visa_required": True,
        "vaccination_required": ["None"]
    },
    "United States": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in the United States.",
        "health_risks": "No major health risks. Healthcare system is excellent but expensive.",
        "safety_risks": "Crime rates vary by location. Check local advisories for specific cities.",
        "entry_requirements": "Valid passport required. ESTA or visa required depending on nationality.",
        "visa_required": True,
        "vaccination_required": ["None"]
    },
    "Italy": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in Italy.",
        "health_risks": "No major health risks. Healthcare system is good.",
        "safety_risks": "Petty crime in tourist areas. Occasional strikes affecting transportation.",
        "entry_requirements": "Valid passport required. Visa not required for stays under 90 days for most nationalities.",
        "visa_required": False,
        "vaccination_required": ["None"]
    },
    "Australia": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in Australia.",
        "health_risks": "Sun exposure and dehydration in summer months. Healthcare system is excellent.",
        "safety_risks": "Wildlife hazards in certain areas. Strong ocean currents at some beaches.",
        "entry_requirements": "Valid passport and visa or ETA required for all visitors.",
        "visa_required": True,
        "vaccination_required": ["None"]
    },
    "South Africa": {
        "advisory_level": "Medium",
        "description": "Exercise increased caution in South Africa due to crime.",
        "health_risks": "Malaria risk in some northeastern areas. HIV prevalence is high. Good private healthcare available.",
        "safety_risks": "High crime rates in certain areas. Avoid walking alone at night. Carjacking risk.",
        "entry_requirements": "Valid passport with at least two blank pages required. Visa requirements vary.",
        "visa_required": False,
        "vaccination_required": ["Yellow Fever"]
    },
    "Brazil": {
        "advisory_level": "Medium",
        "description": "Exercise increased caution in Brazil due to crime.",
        "health_risks": "Mosquito-borne diseases including dengue and Zika. Yellow fever vaccination recommended for some areas.",
        "safety_risks": "Street crime and muggings in tourist areas. Avoid favelas. Use registered taxis.",
        "entry_requirements": "Valid passport required. Visa requirements vary by nationality.",
        "visa_required": True,
        "vaccination_required": ["Yellow Fever"]
    },
    "Thailand": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in Thailand.",
        "health_risks": "Mosquito-borne diseases in rural areas. Drink bottled water. Good private hospitals in Bangkok.",
        "safety_risks": "Petty crime in tourist areas. Be cautious of scams. Road safety concerns.",
        "entry_requirements": "Valid passport required. Visa exemption for stays under 30 days for many nationalities.",
        "visa_required": False,
        "vaccination_required": ["Hepatitis A"]
    },
    "Spain": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in Spain.",
        "health_risks": "No major health risks. Excellent healthcare system.",
        "safety_risks": "Pickpocketing in tourist areas, especially Barcelona and Madrid. Occasional protests.",
        "entry_requirements": "Valid passport required. Visa not required for stays under 90 days for most nationalities.",
        "visa_required": False,
        "vaccination_required": ["None"]
    },
    "United Arab Emirates": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in the UAE.",
        "health_risks": "Extreme heat in summer months. Excellent modern healthcare facilities.",
        "safety_risks": "Very low crime rate. Strict local laws regarding alcohol, dress code, and public behavior.",
        "entry_requirements": "Valid passport required. Visa on arrival for many nationalities.",
        "visa_required": True,
        "vaccination_required": ["None"]
    },
    "Netherlands": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in the Netherlands.",
        "health_risks": "No major health risks. Excellent healthcare system.",
        "safety_risks": "Bicycle theft and pickpocketing in tourist areas. Watch for cyclists when walking.",
        "entry_requirements": "Valid passport required. Visa not required for stays under 90 days for most nationalities.",
        "visa_required": False,
        "vaccination_required": ["None"]
    },
    "Morocco": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in Morocco. Some areas have increased risk.",
        "health_risks": "Drink bottled water. Stomach illnesses possible. Healthcare varies by region.",
        "safety_risks": "Petty crime and aggressive vendors in tourist areas. Avoid border regions with Algeria.",
        "entry_requirements": "Valid passport required. Visa not required for stays under 90 days for many nationalities.",
        "visa_required": False,
        "vaccination_required": ["Hepatitis A"]
    },
    "Canada": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in Canada.",
        "health_risks": "No major health risks. Excellent healthcare system.",
        "safety_risks": "Low crime rate. Wildlife encounters possible in rural areas. Severe winter weather.",
        "entry_requirements": "Valid passport required. eTA required for visa-exempt nationals flying to Canada.",
        "visa_required": True,
        "vaccination_required": ["None"]
    },
    "Singapore": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in Singapore.",
        "health_risks": "Dengue fever risk. Excellent healthcare system, among the best in Asia.",
        "safety_risks": "Very low crime rate. Strict laws on chewing gum, littering, and drug offenses.",
        "entry_requirements": "Valid passport required. Visa not required for stays under 90 days for most nationalities.",
        "visa_required": False,
        "vaccination_required": ["None"]
    },
    "Czech Republic": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in the Czech Republic.",
        "health_risks": "No major health risks. Good healthcare system.",
        "safety_risks": "Pickpocketing in Prague tourist areas. Taxi scams possible.",
        "entry_requirements": "Valid passport required. Visa not required for stays under 90 days for most nationalities.",
        "visa_required": False,
        "vaccination_required": ["None"]
    },
    "Indonesia": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in Indonesia. Some areas have increased risk.",
        "health_risks": "Mosquito-borne diseases including dengue. Drink bottled water. Healthcare limited outside major cities.",
        "safety_risks": "Petty crime in tourist areas. Volcanic and seismic activity. Strong ocean currents.",
        "entry_requirements": "Valid passport required. Visa on arrival available for many nationalities.",
        "visa_required": True,
        "vaccination_required": ["Hepatitis A"]
    },
    "Egypt": {
        "advisory_level": "Medium",
        "description": "Exercise increased caution in Egypt due to terrorism risk.",
        "health_risks": "Drink bottled water. Stomach illnesses common. Healthcare varies significantly by region.",
        "safety_risks": "Terrorism risk in some areas. Avoid Sinai Peninsula border areas. Tourist police present at major sites.",
        "entry_requirements": "Valid passport required. Visa required, available on arrival for many nationalities.",
        "visa_required": True,
        "vaccination_required": ["Hepatitis A"]
    },
    "Argentina": {
        "advisory_level": "Low",
        "description": "Exercise normal precautions in Argentina.",
        "health_risks": "No major health risks in Buenos Aires. Altitude sickness possible in Andes regions.",
        "safety_risks": "Petty crime in Buenos Aires tourist areas. Express kidnappings rare but reported.",
        "entry_requirements": "Valid passport required. Visa not required for stays under 90 days for most nationalities.",
        "visa_required": False,
        "vaccination_required": ["None"]
    },
    "Turkey": {
        "advisory_level": "Medium",
        "description": "Exercise increased caution in Turkey due to terrorism and arbitrary detentions.",
        "health_risks": "No major health risks. Good private healthcare in Istanbul and Ankara.",
        "safety_risks": "Terrorism risk. Avoid southeastern border areas. Political demonstrations possible.",
        "entry_requirements": "Valid passport required. e-Visa required for many nationalities.",
        "visa_required": True,
        "vaccination_required": ["None"]
    }
}

# Seasonal weather patterns for each destination
DESTINATION_WEATHER = {
    "Paris": {
        "Spring": {"high_celsius": 18, "low_celsius": 8, "precipitation_mm": 25, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 25, "low_celsius": 15, "precipitation_mm": 20, "condition": "Sunny"},
        "Fall": {"high_celsius": 16, "low_celsius": 8, "precipitation_mm": 30, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 8, "low_celsius": 2, "precipitation_mm": 25, "condition": "Cloudy"}
    },
    "Tokyo": {
        "Spring": {"high_celsius": 20, "low_celsius": 10, "precipitation_mm": 120, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 30, "low_celsius": 22, "precipitation_mm": 150, "condition": "Rainy"},
        "Fall": {"high_celsius": 22, "low_celsius": 14, "precipitation_mm": 180, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 12, "low_celsius": 2, "precipitation_mm": 60, "condition": "Sunny"}
    },
    "New York": {
        "Spring": {"high_celsius": 18, "low_celsius": 8, "precipitation_mm": 100, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 29, "low_celsius": 20, "precipitation_mm": 110, "condition": "Sunny"},
        "Fall": {"high_celsius": 18, "low_celsius": 10, "precipitation_mm": 100, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 5, "low_celsius": -3, "precipitation_mm": 90, "condition": "Snowy"}
    },
    "Rome": {
        "Spring": {"high_celsius": 20, "low_celsius": 10, "precipitation_mm": 50, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 31, "low_celsius": 19, "precipitation_mm": 15, "condition": "Sunny"},
        "Fall": {"high_celsius": 22, "low_celsius": 12, "precipitation_mm": 80, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 12, "low_celsius": 4, "precipitation_mm": 70, "condition": "Cloudy"}
    },
    "Sydney": {
        "Spring": {"high_celsius": 22, "low_celsius": 14, "precipitation_mm": 75, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 27, "low_celsius": 20, "precipitation_mm": 100, "condition": "Sunny"},
        "Fall": {"high_celsius": 23, "low_celsius": 15, "precipitation_mm": 120, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 17, "low_celsius": 9, "precipitation_mm": 70, "condition": "Clear"}
    },
    "Cape Town": {
        "Spring": {"high_celsius": 21, "low_celsius": 12, "precipitation_mm": 30, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 27, "low_celsius": 16, "precipitation_mm": 10, "condition": "Sunny"},
        "Fall": {"high_celsius": 23, "low_celsius": 13, "precipitation_mm": 40, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 17, "low_celsius": 8, "precipitation_mm": 80, "condition": "Rainy"}
    },
    "Rio de Janeiro": {
        "Spring": {"high_celsius": 27, "low_celsius": 20, "precipitation_mm": 100, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 32, "low_celsius": 24, "precipitation_mm": 130, "condition": "Thunderstorm"},
        "Fall": {"high_celsius": 28, "low_celsius": 21, "precipitation_mm": 80, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 25, "low_celsius": 18, "precipitation_mm": 40, "condition": "Sunny"}
    },
    "Bangkok": {
        "Spring": {"high_celsius": 35, "low_celsius": 26, "precipitation_mm": 60, "condition": "Sunny"},
        "Summer": {"high_celsius": 33, "low_celsius": 26, "precipitation_mm": 160, "condition": "Rainy"},
        "Fall": {"high_celsius": 32, "low_celsius": 25, "precipitation_mm": 200, "condition": "Rainy"},
        "Winter": {"high_celsius": 32, "low_celsius": 22, "precipitation_mm": 10, "condition": "Sunny"}
    },
    "Barcelona": {
        "Spring": {"high_celsius": 20, "low_celsius": 11, "precipitation_mm": 45, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 29, "low_celsius": 21, "precipitation_mm": 25, "condition": "Sunny"},
        "Fall": {"high_celsius": 21, "low_celsius": 13, "precipitation_mm": 75, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 14, "low_celsius": 6, "precipitation_mm": 40, "condition": "Cloudy"}
    },
    "Dubai": {
        "Spring": {"high_celsius": 35, "low_celsius": 22, "precipitation_mm": 5, "condition": "Sunny"},
        "Summer": {"high_celsius": 42, "low_celsius": 30, "precipitation_mm": 0, "condition": "Sunny"},
        "Fall": {"high_celsius": 36, "low_celsius": 24, "precipitation_mm": 5, "condition": "Sunny"},
        "Winter": {"high_celsius": 25, "low_celsius": 15, "precipitation_mm": 15, "condition": "Clear"}
    },
    "Kyoto": {
        "Spring": {"high_celsius": 20, "low_celsius": 9, "precipitation_mm": 110, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 33, "low_celsius": 24, "precipitation_mm": 180, "condition": "Rainy"},
        "Fall": {"high_celsius": 22, "low_celsius": 12, "precipitation_mm": 120, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 9, "low_celsius": 1, "precipitation_mm": 50, "condition": "Cloudy"}
    },
    "Amsterdam": {
        "Spring": {"high_celsius": 14, "low_celsius": 6, "precipitation_mm": 40, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 22, "low_celsius": 13, "precipitation_mm": 65, "condition": "Partly Cloudy"},
        "Fall": {"high_celsius": 14, "low_celsius": 8, "precipitation_mm": 80, "condition": "Cloudy"},
        "Winter": {"high_celsius": 6, "low_celsius": 1, "precipitation_mm": 70, "condition": "Cloudy"}
    },
    "Marrakech": {
        "Spring": {"high_celsius": 27, "low_celsius": 13, "precipitation_mm": 25, "condition": "Sunny"},
        "Summer": {"high_celsius": 38, "low_celsius": 21, "precipitation_mm": 2, "condition": "Sunny"},
        "Fall": {"high_celsius": 27, "low_celsius": 14, "precipitation_mm": 25, "condition": "Sunny"},
        "Winter": {"high_celsius": 18, "low_celsius": 6, "precipitation_mm": 30, "condition": "Partly Cloudy"}
    },
    "Vancouver": {
        "Spring": {"high_celsius": 14, "low_celsius": 6, "precipitation_mm": 80, "condition": "Rainy"},
        "Summer": {"high_celsius": 22, "low_celsius": 14, "precipitation_mm": 35, "condition": "Sunny"},
        "Fall": {"high_celsius": 13, "low_celsius": 7, "precipitation_mm": 150, "condition": "Rainy"},
        "Winter": {"high_celsius": 7, "low_celsius": 2, "precipitation_mm": 170, "condition": "Rainy"}
    },
    "Singapore": {
        "Spring": {"high_celsius": 32, "low_celsius": 25, "precipitation_mm": 170, "condition": "Thunderstorm"},
        "Summer": {"high_celsius": 31, "low_celsius": 25, "precipitation_mm": 150, "condition": "Partly Cloudy"},
        "Fall": {"high_celsius": 31, "low_celsius": 24, "precipitation_mm": 160, "condition": "Thunderstorm"},
        "Winter": {"high_celsius": 30, "low_celsius": 24, "precipitation_mm": 250, "condition": "Rainy"}
    },
    "Prague": {
        "Spring": {"high_celsius": 15, "low_celsius": 5, "precipitation_mm": 35, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 25, "low_celsius": 14, "precipitation_mm": 65, "condition": "Sunny"},
        "Fall": {"high_celsius": 14, "low_celsius": 6, "precipitation_mm": 35, "condition": "Cloudy"},
        "Winter": {"high_celsius": 3, "low_celsius": -3, "precipitation_mm": 25, "condition": "Snowy"}
    },
    "Bali": {
        "Spring": {"high_celsius": 31, "low_celsius": 24, "precipitation_mm": 90, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 30, "low_celsius": 23, "precipitation_mm": 50, "condition": "Sunny"},
        "Fall": {"high_celsius": 31, "low_celsius": 24, "precipitation_mm": 80, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 30, "low_celsius": 24, "precipitation_mm": 280, "condition": "Rainy"}
    },
    "Cairo": {
        "Spring": {"high_celsius": 30, "low_celsius": 16, "precipitation_mm": 3, "condition": "Sunny"},
        "Summer": {"high_celsius": 36, "low_celsius": 23, "precipitation_mm": 0, "condition": "Sunny"},
        "Fall": {"high_celsius": 30, "low_celsius": 18, "precipitation_mm": 5, "condition": "Sunny"},
        "Winter": {"high_celsius": 20, "low_celsius": 10, "precipitation_mm": 10, "condition": "Clear"}
    },
    "Buenos Aires": {
        "Spring": {"high_celsius": 22, "low_celsius": 12, "precipitation_mm": 90, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 30, "low_celsius": 20, "precipitation_mm": 110, "condition": "Sunny"},
        "Fall": {"high_celsius": 22, "low_celsius": 13, "precipitation_mm": 90, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 14, "low_celsius": 6, "precipitation_mm": 55, "condition": "Cloudy"}
    },
    "Istanbul": {
        "Spring": {"high_celsius": 17, "low_celsius": 9, "precipitation_mm": 45, "condition": "Partly Cloudy"},
        "Summer": {"high_celsius": 28, "low_celsius": 20, "precipitation_mm": 20, "condition": "Sunny"},
        "Fall": {"high_celsius": 19, "low_celsius": 12, "precipitation_mm": 60, "condition": "Partly Cloudy"},
        "Winter": {"high_celsius": 9, "low_celsius": 3, "precipitation_mm": 70, "condition": "Cloudy"}
    }
}
