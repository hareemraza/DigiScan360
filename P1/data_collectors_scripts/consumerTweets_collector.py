import csv
from faker import Faker
import random
from datetime import datetime

fake = Faker(['es_ES', 'en_US'])

brands = ['JBL', 'Bose', 'Sony', 'Phillips', 'TOZO', 'AKG', 'Logitech', 'Apple', 'Xiaomi', 'oneodio', 'Sennheiser', 'Audio-Technica', 'Beats', 'Skullcandy', 'Marshall', 'Anker']
hashtags = ['#headphones', '#music', '#audio', '#tech', '#soundquality', '#wireless', '#gaming', '#lifestyle', '#gadgets', '#unboxing', '#customerexperience', '#productreview', 
            '#bass', '#noiseCancellation', '#Bluetooth', '#waterproof', '#HiFi', '#Earbuds', '#OverEar', '#OnEar', '#NoiseCancelling', '#TrueWireless','#Audiophile', '#PortableAudio', 
            '#SoundIsolation', '#StudioQuality', '#BassHeads', '#MusicLover', '#PodcastLover', '#WorkoutGear', '#TravelEssentials', '#GadgetLover',
            '#TechInnovations', '#EcoFriendlyTech', '#SmartTech', '#GamingGear', '#VirtualReality', '#HomeTheater', '#MusicProduction', '#DJLife', '#ConcertReady', '#StudyPlaylist',
            '#CodingPlaylist', '#VocalClarity', '#Instrumental', '#SoundtrackLovers', '#RetroVibes', '#FashionTech', '#RandomTweet', '#JustSaying', '#Life', '#FoodForThought']

def misspell(word):
    """Randomly misspells a word with a 5% chance."""
    if random.randint(1, 100) <= 5:
        if len(word) > 3:
            char_to_replace = random.randint(1, len(word) - 2)
            return word[:char_to_replace] + random.choice('aeiou') + word[char_to_replace + 1:]
    return word

def add_noise(tweet):
    if random.randint(0, 10) > 7:
        noise = random.choice([
            " #RandomTweet",
            " #JustSaying",
            " lol",
            " 😂",
            " #Life",
            " #FoodForThought"
        ])
        return tweet + noise
    return tweet
def generate_tweet(brand):
    messages = [
                f"Amo mis nuevos auriculares {brand}. ¡La calidad del sonido es increíble! #audio #music {random.choice(hashtags)}",
        f"Just got my {brand} headphones. The noise cancellation is top-notch! #tech #soundquality {random.choice(hashtags)}",
        f"Los auriculares {brand} son incómodos después de unas horas. #audio #review {random.choice(hashtags)}",
        f"Not happy with the battery life of my {brand} headphones. Expected better. #tech {random.choice(hashtags)}",
        f"{brand} headphones are the best investment I’ve made for my daily commute. #wireless #music {random.choice(hashtags)}",
        f"Alguien más tiene problemas con el Bluetooth de los {brand}? #tech #audio {random.choice(hashtags)}",
        f"¡Los auriculares {brand} son una maravilla! Nunca había disfrutado tanto la música. #music #audio {random.choice(hashtags)}",
        f"Loving my new {brand} headphones. It's like I'm discovering my favorite songs all over again. #soundquality #listeningexperience {random.choice(hashtags)}",
        f"No estoy muy convencido con los {brand}, esperaba mejor cancelación de ruido. #tech #review {random.choice(hashtags)}",
        f"Disappointed with the {brand} headset. Battery life is nowhere near what was advertised. #gadgets #tech {random.choice(hashtags)}",
        f"Acabo de comprar auriculares {brand}. Son buenos, pero no me han sorprendido. #audio #headphones {random.choice(hashtags)}",
        f"Got the {brand} headphones as a gift. They're okay, not the best I've had but decent. #listeningexperience {random.choice(hashtags)}",
        f"¿Alguien ha probado los {brand} para gaming? ¿Qué tal la experiencia? #gaming #headphones {random.choice(hashtags)}",
        f"Can anyone recommend a good case for {brand} headphones? Preferably waterproof. #tech #gadgets {random.choice(hashtags)}",
        f"Tip: Para mejorar la vida de la batería en los {brand}, baja un poco el volumen. #audio #tech {random.choice(hashtags)}",
        f"Just found out you can customize the sound profiles on {brand} headphones with their app. Game changer! #tech #soundquality {random.choice(hashtags)}",
        f"Unboxing my new {brand} headphones! Can't wait to test them out. #unboxing #gadgets {random.choice(hashtags)}",
        f"Is it just me, or do {brand} headphones have the best bass out there? #music #bass {random.choice(hashtags)}",
        f"Customer service from {brand} was outstanding! Helped me solve an issue in no time. #customerexperience {random.choice(hashtags)}",
        f"Considering switching to {brand} for their waterproof features. Anyone with experience? #waterproof #tech {random.choice(hashtags)}",
        f"I just compared {brand} headphones with another brand, and the difference is night and day! #productreview #soundquality {random.choice(hashtags)}",
        f"Finally found headphones that don't fall out during my workouts! Thanks, {brand}. #workout #music {random.choice(hashtags)}",
        f"Working from home just got better with my new {brand} noise-cancelling headphones. #workfromhome #tech {random.choice(hashtags)}",
        f"{brand} headphones survived a drop with not a single scratch. Impressed with the build quality! #durability #tech {random.choice(hashtags)}",
        f"Me enamoré de la funcionalidad táctil en los auriculares {brand}. Tan intuitivo! #tecnología #audio {random.choice(hashtags)}",
        f"Anyone else think {brand} has the coolest headphone designs? Standing out in the crowd. #design #style {random.choice(hashtags)}",
        f"Lost my {brand} headphones and found them with the 'Find My Headphones' feature. Lifesaver! #tech #gadgets {random.choice(hashtags)}",
        f"My commute is now my favorite part of the day, thanks to {brand}. Music to my ears, literally. #commute #music {random.choice(hashtags)}",
        f"¿Alguien más ama la app de {brand} para personalizar el sonido? #app #personalización {random.choice(hashtags)}",
        f"Watching movies with {brand} headphones is like being in the theater. #movies #audio {random.choice(hashtags)}",
        f"Could someone help me choose between {brand} and another brand? Looking for the best noise cancellation. #advice #headphones {random.choice(hashtags)}",
        f"Just got a pair of {brand} for my gaming setup. The spatial audio is unreal! #gaming #tech {random.choice(hashtags)}",
        f"The battery life on my {brand} headphones is phenomenal. Days without charging! #battery #gadgets {random.choice(hashtags)}",
        f"Tengo que admitir que los {brand} son los mejores para escuchar podcasts. Claridad increíble. #podcasts #audio {random.choice(hashtags)}",
        f"Did a whole flight with my {brand} headphones. Comfort and sound isolation made it a breeze. #travel #comfort {random.choice(hashtags)}",
        f"The waterproof feature of {brand} headphones is perfect for my sweaty gym sessions. #fitness #waterproof {random.choice(hashtags)}",
        f"Can't believe how quick the charge is on my {brand} headphones. Back to full in no time! #charging #tech {random.choice(hashtags)}",
        f"A la playa con mis auriculares {brand}. ¡La arena y el agua no pueden detener la música! #playa #verano {random.choice(hashtags)}",
        f"Need a durable pair of headphones for my kids, thinking of going with {brand}. Any reviews? #parents #durability {random.choice(hashtags)}",
        f"Setting up my new home office with a pair of {brand} headphones. Productivity, here I come! #homeoffice #productivity {random.choice(hashtags)}",
        f"Can't get over how light and comfortable my new #Earbuds from {brand} are. Perfect for my daily run! #WorkoutGear #MusicLover",
        f"Why did I wait so long to get noise-cancelling headphones? {brand}'s latest model is a game-changer for my productivity. #NoiseCancelling {random.choice(hashtags)}",
        f"The battery life on these {brand} headphones is unbelievable. Over 24 hours of playback on a single charge! #Tech #GadgetLover",
        f"Just treated myself to some high-end {brand} headphones and the sound quality is unmatched. #HiFi #Audiophile",
        f"¿Alguien más piensa que los auriculares {brand} tienen el mejor bajo? Es como estar en un concierto en vivo. #BassHeads #MusicLover",
        f"¡Los {brand} son los mejores para escuchar música clásica! Cada nota suena perfecta. #Audiophile #MusicProduction",
        f"Received my {brand} headphones today, and they're already my favorite tech accessory. Sleek design and amazing sound. #FashionTech #SoundQuality",
        f"Los {brand} no solo tienen un sonido increíble, sino que también son súper cómodos para largas sesiones de estudio. #StudyPlaylist #Comfort",
        f"If you're looking for durable and reliable headphones for your kids, {brand} has some great options. #Parents #Durability",
        f"Exploring the city with my {brand} headphones. The sound isolation makes the bustling streets my personal soundtrack. #TravelEssentials #SoundIsolation",
        f"Just discovered {brand}'s environmental initiative. Love supporting eco-friendly tech! #EcoFriendlyTech #SmartTech",
        f"Ayer probé los {brand} para mi sesión de gaming y ¡vaya diferencia! El audio espacial añade tanto a la experiencia. #GamingGear #TechInnovations",
        f"The customer service from {brand} was top-notch when I had an issue with my headphones. Quick and helpful response. #CustomerExperience #Tech",
        f"¿Alguien más usa sus auriculares {brand} para meditar? La cancelación de ruido es perfecta para concentrarse. #NoiseCancelling #Lifestyle",
        f"After a month with my new {brand} headphones, I can confidently say they're the best I've ever had. #ProductReview #MusicLover",
        f"Los {brand} transformaron mi rutina de ejercicios. La música nunca sonó tan bien en el gimnasio. #WorkoutGear #TrueWireless",
        f"Packing for my next trip and my {brand} headphones are the first thing in my bag. Can't travel without them! #TravelEssentials #Music",
        f"Sorprendido con la calidad de construcción de los {brand}. Se sienten sólidos y premium en la mano. #Tech #GadgetLover",
        f"Just customized the EQ settings on my {brand} app, and now my music sounds even better. Love this feature! #TechInnovations #SoundQuality",
        f"¿Necesitas auriculares que duren todo el día? Los {brand} me duraron un vuelo transatlántico completo. #TravelEssentials #BatteryLife",
        f"Finally got the {brand} headphones I wanted for so long! #excited #newgear",
        f"Does anyone have recommendations for {brand} earbud alternatives? #askingforafriend",
        f"Why are {brand} headphones so pricey? #genuinelycurious",
        f"Just saw someone wearing {brand} on the subway. Instant envy. #want",
        f"My cat chewed through my {brand} headphone cords... #sadface",
        f"Can't decide between {brand} and another brand. #firstworldproblems",
        f"Who else thinks {brand} has the best customer service? #impressed"
    ]
    message = random.choice(messages).format(brand=brand)
    message = ' '.join([misspell(word) if random.randint(1, 20) == 1 else word for word in message.split()])
    message = add_noise(message)
    return message + " " + random.choice(hashtags)

def random_null_chance(value, chance=10):
    """Randomly returns an empty string instead of the value based on the specified chance."""
    return value if random.randint(1, 100) > chance else ''

author_ids = []
data = []
for _ in range(10000):  
    brand = random.choice(brands)
    tweet_text = generate_tweet(brand) 
    language = 'es' if tweet_text.startswith(('Los', 'Amo')) else 'en'
    author_id = fake.numerify(text="##########")
    author_ids.append(author_id)
    in_reply_to_user_id = random.choice(author_ids) if random.randint(1, 100) <= 40 and author_ids else None
    data.append({
        "tweet_id": fake.unique.uuid4(),
        "author_id": author_id,
        "screen_name": fake.unique.user_name(),
        "timestamp": fake.date_time_between(start_date="-2y", end_date="now").strftime('%Y-%m-%dT%H:%M:%SZ'),
        "text": tweet_text,
        "in_reply_to_user_id": in_reply_to_user_id,
        "lang": language,
        "impression_count": random.randint(100, 10000),
        "like_count": random.randint(0, 500),
        "reply_count": random.randint(0, 100),
        "repost_count": random.randint(0, 100),
        "quote_count": random.randint(0, 50),
        "hashtags": [tag for tag in tweet_text.split() if tag.startswith("#")],
        "user_followers_count": random.randint(2000, 10000) if random.random() < 0.1 else random.randint(10, 1200),
        "user_following_count": random.randint(10, 100) if random.random() < 0.1 else random.randint(50, 1000),
        "verified": True if random.random() < 0.1 else False
    })

csv_file = "consumer_tweets.csv"
try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        for tweet in data:
            writer.writerow(tweet)
    print(f"Data successfully saved to {csv_file}")
except IOError:
    print("I/O error")
