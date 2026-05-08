"""Seed Aurelia with a rich, demo-ready catalogue."""
from datetime import date, datetime, timedelta
import random

from app import app
from models import (db, User, Destination, DestinationImage, Review, Reply,
                    TravelPlan, Wishlist)


DESTINATIONS = [
    # Beaches
    ("Santorini", "Oia", "Greece", "Beach", 36.4618, 25.3753,
     "Whitewashed cliff-side villas tumble toward the Aegean. Sunsets in Oia have a way of rearranging your priorities — every traveler should witness one at least once.",
     "https://images.unsplash.com/photo-1570077188670-e3a8d69ac5ff?w=1200",
     ["https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?w=800",
      "https://images.unsplash.com/photo-1601581875309-fafbf2d3ed3a?w=800"]),
    ("Maldives Atolls", "Malé", "Maldives", "Beach", 3.2028, 73.2207,
     "Overwater bungalows above water so clear it borders on illegal. The Maldives is what tropical paradise looks like before marketing departments get involved.",
     "https://images.unsplash.com/photo-1514282401047-d79a71a590e8?w=1200",
     ["https://images.unsplash.com/photo-1505881502353-a1986add3762?w=800"]),
    ("Bora Bora", "Vaitape", "French Polynesia", "Beach", -16.5004, -151.7415,
     "A turquoise lagoon ringed by a volcanic peak. Bora Bora doesn't try to impress you — it simply is impressive.",
     "https://images.unsplash.com/photo-1589197331516-4d84b72ebde3?w=1200",
     []),
    ("Tulum", "Quintana Roo", "Mexico", "Beach", 20.2114, -87.4654,
     "Mayan ruins perched above white sand and bohemian beach clubs that hum to a dawn-to-dusk soundtrack.",
     "https://images.unsplash.com/photo-1512813195386-6cf811ad3542?w=1200",
     []),

    # Mountains
    ("Banff", "Alberta", "Canada", "Mountain", 51.4968, -115.9281,
     "Glacier-blue lakes mirror jagged peaks. In Banff, even the wildlife seems to pose for the camera.",
     "https://images.unsplash.com/photo-1609825488888-3a766db05542?w=1200",
     ["https://images.unsplash.com/photo-1503614472-8c93d56e92ce?w=800"]),
    ("Swiss Alps", "Zermatt", "Switzerland", "Mountain", 45.9763, 7.6586,
     "The Matterhorn cuts the sky like a sculpted shard of ice. Cogwheel trains, cheese fondue, and air so clean it feels imported.",
     "https://images.unsplash.com/photo-1530841344095-0e3a86b3a55e?w=1200",
     []),
    ("Patagonia", "El Chaltén", "Argentina", "Mountain", -49.3315, -72.8868,
     "Wind-scoured glaciers and granite spires. Patagonia rewards the traveler who packs an extra layer and an open calendar.",
     "https://images.unsplash.com/photo-1581019854094-c3c9eb1ecf35?w=1200",
     []),
    ("Mt. Fuji", "Yamanashi", "Japan", "Mountain", 35.3606, 138.7274,
     "A nearly perfect cone reflected in five lakes. Best at dawn, with a thermos of coffee and absolutely no agenda.",
     "https://images.unsplash.com/photo-1490806843957-31f4c9a91c65?w=1200",
     []),

    # Cities
    ("Tokyo", "Tokyo", "Japan", "City", 35.6762, 139.6503,
     "Neon canyons, hidden ramen shops, and 14th-century shrines tucked between skyscrapers. Tokyo runs on contradiction and somehow makes it elegant.",
     "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=1200",
     ["https://images.unsplash.com/photo-1503899036084-c55cdd92da26?w=800"]),
    ("Paris", "Paris", "France", "City", 48.8566, 2.3522,
     "Boulevards, bakeries, the soft golden hour on the Seine. Paris invented the art of taking your time.",
     "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200",
     ["https://images.unsplash.com/photo-1431274172761-fca41d930114?w=800"]),
    ("Marrakech", "Marrakech", "Morocco", "City", 31.6295, -7.9811,
     "Spice-stained souks, palatial riads, and a square that becomes a circus at sunset. Marrakech engages every sense at once.",
     "https://images.unsplash.com/photo-1539020140153-e479b8c22e70?w=1200",
     []),
    ("Lisbon", "Lisbon", "Portugal", "City", 38.7223, -9.1393,
     "Tile-covered hillsides, yellow trams, and fado drifting from open windows. Lisbon's slow charm is intentional.",
     "https://images.unsplash.com/photo-1558370781-d6196949e317?w=1200",
     []),
    ("New York", "New York", "USA", "City", 40.7128, -74.0060,
     "The city that famously doesn't sleep — though it definitely takes naps on the subway. Eight million stories under one skyline.",
     "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=1200",
     []),

    # Adventure
    ("Iceland Highlands", "Landmannalaugar", "Iceland", "Adventure", 63.9869, -19.0608,
     "Rhyolite mountains in chartreuse and rust, hot springs that bubble up through black sand. Iceland is the planet's most generous show-off.",
     "https://images.unsplash.com/photo-1486016006115-74a41448aea2?w=1200",
     []),
    ("Queenstown", "Queenstown", "New Zealand", "Adventure", -45.0312, 168.6626,
     "Skydiving, jet boats, and bungee jumping — the place that invented adrenaline tourism still does it best.",
     "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1200",
     []),
    ("Costa Rica Cloud Forest", "Monteverde", "Costa Rica", "Adventure", 10.3010, -84.8160,
     "Hummingbirds the size of bumblebees and zip-lines through perpetual mist. Pura vida, fully delivered.",
     "https://images.unsplash.com/photo-1518709594023-6eab9bab7b23?w=1200",
     []),
    ("Sahara Dunes", "Merzouga", "Morocco", "Adventure", 31.0989, -4.0114,
     "Camel-trek to a camp under a sky so dense with stars it can ruin city living for you forever.",
     "https://images.unsplash.com/photo-1473496169904-658ba7c44d8a?w=1200",
     []),
    ("Galápagos", "Santa Cruz Island", "Ecuador", "Adventure", -0.7404, -90.3132,
     "The islands that gave Darwin his idea. Sea lions photobomb your snorkel sessions.",
     "https://images.unsplash.com/photo-1515591041745-1f7a7e57c47a?w=1200",
     []),

    # Cultural
    ("Kyoto", "Kyoto", "Japan", "Cultural", 35.0116, 135.7681,
     "Two thousand temples, geisha alleys, and bamboo groves that shoosh with ancient wisdom. Tokyo's elegant elder sister.",
     "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?w=1200",
     ["https://images.unsplash.com/photo-1545569310-c28ddb16e57f?w=800"]),
    ("Petra", "Ma'an", "Jordan", "Cultural", 30.3285, 35.4444,
     "A 2,000-year-old rose-red city carved into sandstone cliffs. The Treasury at first sight is genuinely breathtaking.",
     "https://images.unsplash.com/photo-1552431078-b29b54fe43d4?w=1200",
     []),
    ("Machu Picchu", "Cusco", "Peru", "Cultural", -13.1631, -72.5450,
     "Inca terraces draped over a mountain saddle in the clouds. Get there before the day-trippers do.",
     "https://images.unsplash.com/photo-1526392060635-9d6019884377?w=1200",
     ["https://images.unsplash.com/photo-1587595431973-160d0d94add1?w=800"]),
    ("Angkor Wat", "Siem Reap", "Cambodia", "Cultural", 13.4125, 103.8670,
     "Sandstone temples wrapped by jungle and history. Sunrise here is a candidate for the world's best.",
     "https://images.unsplash.com/photo-1563492065599-3520f775eeed?w=1200",
     []),
    ("Florence", "Tuscany", "Italy", "Cultural", 43.7696, 11.2558,
     "The Renaissance's headquarters. Walk anywhere; you'll hit a Botticelli or a glass of Chianti.",
     "https://images.unsplash.com/photo-1543429776-2782fc8e1acd?w=1200",
     []),
    ("Istanbul", "Istanbul", "Turkey", "Cultural", 41.0082, 28.9784,
     "Where Europe and Asia share a kitchen. Hagia Sophia, the Bosphorus, and possibly the world's best breakfast spread.",
     "https://images.unsplash.com/photo-1524231757912-21f4fe3a7200?w=1200",
     []),
]


SAMPLE_REVIEWS = [
    ("Genuinely life-changing. The light, the food, the people — every detail. Already plotting our return.", 5),
    ("Stunning location with a few logistical quirks. Worth the effort, but pack patience.", 4),
    ("A traveler's traveler kind of place. Slow it down, stay longer than you think you should.", 5),
    ("Touristy in spots but the magic is undeniable when you find the quiet corners.", 4),
    ("Honestly cinematic. Felt like walking through a postcard for three days straight.", 5),
    ("Solid trip; not the romantic spectacle Instagram suggested. Still glad we came.", 3),
    ("The off-season visit made this — empty streets, perfect light, no queues.", 5),
]


def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        users = []
        demo_users = [
            ("test", "test@test.com", "1234", "Curator of unusual itineraries.", "#d4af37"),
            ("amelia", "amelia@aurelia.com", "1234", "Architect by trade, photographer by escape.", "#9b59b6"),
            ("jasper", "jasper@aurelia.com", "1234", "Eats his way through every city.", "#e67e22"),
            ("rumi", "rumi@aurelia.com", "1234", "Solo traveler, hiker, occasional poet.", "#27ae60"),
            ("noor", "noor@aurelia.com", "1234", "Diving, ruins, and obscure museums.", "#3498db"),
        ]
        for username, email, pw, bio, color in demo_users:
            u = User(username=username, email=email, bio=bio, avatar_color=color,
                     created_at=datetime.utcnow() - timedelta(days=random.randint(30, 400)))
            u.set_password(pw)
            db.session.add(u)
            users.append(u)
        db.session.commit()

        destinations = []
        for (name, location, country, category, lat, lng, desc, image, gallery) in DESTINATIONS:
            d = Destination(
                name=name, location=location, country=country, category=category,
                latitude=lat, longitude=lng, description=desc, image_url=image,
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 200)),
            )
            db.session.add(d)
            db.session.flush()
            for url in gallery:
                db.session.add(DestinationImage(destination_id=d.id, url=url))
            destinations.append(d)
        db.session.commit()

        for d in destinations:
            n = random.randint(2, 5)
            for _ in range(n):
                u = random.choice(users)
                content, rating = random.choice(SAMPLE_REVIEWS)
                r = Review(content=content, rating=rating,
                           user_id=u.id, destination_id=d.id,
                           created_at=datetime.utcnow() - timedelta(days=random.randint(1, 90)))
                db.session.add(r)
                db.session.flush()
                if random.random() < 0.4:
                    other = random.choice([x for x in users if x.id != u.id])
                    db.session.add(Reply(
                        content=random.choice([
                            "Going next month — any tips?",
                            "Agreed, the off-season is the move.",
                            "Did you stay anywhere you'd recommend?",
                            "This sealed it. Booking tonight.",
                        ]),
                        user_id=other.id, review_id=r.id,
                        created_at=r.created_at + timedelta(days=1),
                    ))
        db.session.commit()

        for u in users[:3]:
            plan = TravelPlan(
                name=random.choice(["A Mediterranean Summer", "Asian Adventure", "Wonders Tour", "Andes & Atacama"]),
                user_id=u.id,
                start_date=date.today() + timedelta(days=random.randint(20, 90)),
                end_date=date.today() + timedelta(days=random.randint(95, 130)),
                budget=random.choice([2500, 4800, 7200, 12000]),
                notes="Notes drafted during a long flight.",
            )
            db.session.add(plan)
            db.session.flush()
            for d in random.sample(destinations, k=random.randint(3, 5)):
                plan.destinations.append(d)
        db.session.commit()

        for u in users:
            for d in random.sample(destinations, k=random.randint(2, 6)):
                if not Wishlist.query.filter_by(user_id=u.id, destination_id=d.id).first():
                    db.session.add(Wishlist(user_id=u.id, destination_id=d.id))
        db.session.commit()

        print(f"Seeded {len(users)} users, {len(destinations)} destinations, "
              f"{Review.query.count()} reviews, {Reply.query.count()} replies, "
              f"{TravelPlan.query.count()} plans, {Wishlist.query.count()} wishlist items.")


if __name__ == '__main__':
    seed()
