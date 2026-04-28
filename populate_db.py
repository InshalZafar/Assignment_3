from app import app, db
from models import User, Destination, Review, TravelPlan
from sqlalchemy import func

def populate_db():
    with app.app_context():
        # Create sample users
        users_data = [
            {'username': 'traveler1', 'email': 'traveler1@example.com', 'password': 'password1'},
            {'username': 'explorer2', 'email': 'explorer2@example.com', 'password': 'password2'},
            {'username': 'wanderer3', 'email': 'wanderer3@example.com', 'password': 'password3'},
            {'username': 'globetrotter4', 'email': 'globetrotter4@example.com', 'password': 'password4'}
        ]

        users = []
        for user_data in users_data:
            user = User(username=user_data['username'], email=user_data['email'])
            user.set_password(user_data['password'])
            users.append(user)
            db.session.add(user)

        # Create destinations (keeping the existing code)
        destinations_data = [
            {
                'name': 'New York City',
                'description': 'The city that never sleeps, known for its skyscrapers, Broadway shows, and diverse culture.',
                'location': 'New York, USA',
                'image_url': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'London',
                'description': 'Historic capital of England with iconic landmarks like Big Ben, the Thames River, and world-class museums.',
                'location': 'London, UK',
                'image_url': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Paris',
                'description': 'The City of Light, famous for the Eiffel Tower, Louvre Museum, and romantic atmosphere.',
                'location': 'Paris, France',
                'image_url': 'https://images.unsplash.com/photo-1502602898536-47ad22581b52?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Toronto',
                'description': 'Canada\'s largest city, offering diverse neighborhoods, CN Tower, and multicultural cuisine.',
                'location': 'Toronto, Canada',
                'image_url': 'https://images.unsplash.com/photo-1517935706615-2717063c2225?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Sydney',
                'description': 'Australia\'s vibrant harbor city with the iconic Opera House and Harbour Bridge.',
                'location': 'Sydney, Australia',
                'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Istanbul',
                'description': 'A bridge between Europe and Asia, known for its historic mosques, bazaars, and Bosphorus Strait.',
                'location': 'Istanbul, Turkey',
                'image_url': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Makkah',
                'description': 'The holiest city in Islam, home to the Kaaba and the Grand Mosque.',
                'location': 'Makkah, Saudi Arabia',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Medina',
                'description': 'The second holiest city in Islam, known for the Prophet\'s Mosque and Islamic history.',
                'location': 'Medina, Saudi Arabia',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Kuwait City',
                'description': 'Modern capital with traditional souks, waterfront, and Middle Eastern culture.',
                'location': 'Kuwait City, Kuwait',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Doha',
                'description': 'Qatar\'s capital, featuring modern architecture, museums, and desert landscapes.',
                'location': 'Doha, Qatar',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Los Angeles',
                'description': 'Entertainment capital with Hollywood, beaches, and diverse neighborhoods.',
                'location': 'Los Angeles, USA',
                'image_url': 'https://images.unsplash.com/photo-1534190760961-74e8c1c5c3da?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Manchester',
                'description': 'Northern England\'s cultural hub with music history, canals, and vibrant nightlife.',
                'location': 'Manchester, UK',
                'image_url': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Nice',
                'description': 'French Riviera gem with beautiful beaches, Promenade des Anglais, and Mediterranean charm.',
                'location': 'Nice, France',
                'image_url': 'https://images.unsplash.com/photo-1502602898536-47ad22581b52?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Vancouver',
                'description': 'Canada\'s Pacific gateway with mountains, ocean, and outdoor activities.',
                'location': 'Vancouver, Canada',
                'image_url': 'https://images.unsplash.com/photo-1517935706615-2717063c2225?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Melbourne',
                'description': 'Australia\'s cultural capital with street art, coffee culture, and sporting events.',
                'location': 'Melbourne, Australia',
                'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Ankara',
                'description': 'Turkey\'s capital with ancient history, modern museums, and Anatolian culture.',
                'location': 'Ankara, Turkey',
                'image_url': 'https://images.unsplash.com/photo-1541432901042-2d8bd64b4a9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Jeddah',
                'description': 'Saudi Arabia\'s commercial hub with Red Sea beaches and historic sites.',
                'location': 'Jeddah, Saudi Arabia',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Riyadh',
                'description': 'Saudi Arabia\'s capital with modern development and traditional markets.',
                'location': 'Riyadh, Saudi Arabia',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Hawalli',
                'description': 'Kuwait\'s commercial district with shopping malls and cultural sites.',
                'location': 'Hawalli, Kuwait',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Al Wakrah',
                'description': 'Qatari coastal city with traditional architecture and maritime history.',
                'location': 'Al Wakrah, Qatar',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Chicago',
                'description': 'The Windy City with architecture, deep-dish pizza, and Lake Michigan views.',
                'location': 'Chicago, USA',
                'image_url': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Edinburgh',
                'description': 'Scotland\'s capital with castles, festivals, and literary history.',
                'location': 'Edinburgh, UK',
                'image_url': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Lyon',
                'description': 'France\'s gastronomic capital with Roman history and Renaissance architecture.',
                'location': 'Lyon, France',
                'image_url': 'https://images.unsplash.com/photo-1502602898536-47ad22581b52?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Montreal',
                'description': 'Canada\'s cultural metropolis with European charm and North American energy.',
                'location': 'Montreal, Canada',
                'image_url': 'https://images.unsplash.com/photo-1517935706615-2717063c2225?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            },
            {
                'name': 'Brisbane',
                'description': 'Australia\'s subtropical capital with parks, rivers, and vibrant lifestyle.',
                'location': 'Brisbane, Australia',
                'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80'
            }
        ]

        destinations = []
        for dest_data in destinations_data:
            dest = Destination(**dest_data)
            destinations.append(dest)
            db.session.add(dest)

        db.session.commit()  # Commit to get IDs

        # Create reviews (keeping existing)
        reviews_data = [
            # New York City
            {'content': 'Amazing city! The energy is incredible. Must visit Times Square and Central Park.', 'rating': 5, 'user': users[0], 'dest': destinations[0]},
            {'content': 'Great food scene and museums. A bit crowded but worth it.', 'rating': 4, 'user': users[1], 'dest': destinations[0]},
            {'content': 'Iconic skyline and diverse neighborhoods. Perfect for a weekend getaway.', 'rating': 5, 'user': users[2], 'dest': destinations[0]},

            # London
            {'content': 'Historic and modern blend perfectly. Buckingham Palace and Thames cruise were highlights.', 'rating': 5, 'user': users[1], 'dest': destinations[1]},
            {'content': 'Excellent museums and theater scene. Weather could be better!', 'rating': 4, 'user': users[2], 'dest': destinations[1]},
            {'content': 'Iconic red buses and phone booths. A must-visit for history lovers.', 'rating': 5, 'user': users[3], 'dest': destinations[1]},

            # Paris
            {'content': 'Romantic and beautiful. Eiffel Tower at night is magical.', 'rating': 5, 'user': users[0], 'dest': destinations[2]},
            {'content': 'Amazing art at Louvre and delicious pastries everywhere.', 'rating': 5, 'user': users[1], 'dest': destinations[2]},
            {'content': 'Seine River cruises and charming cafes. Perfect for couples.', 'rating': 4, 'user': users[3], 'dest': destinations[2]},

            # Toronto
            {'content': 'Diverse city with great food. CN Tower views are spectacular.', 'rating': 4, 'user': users[2], 'dest': destinations[3]},
            {'content': 'Friendly people and multicultural neighborhoods. Love the waterfront.', 'rating': 5, 'user': users[3], 'dest': destinations[3]},
            {'content': 'Good mix of urban and nature. Distillery District is fun.', 'rating': 4, 'user': users[0], 'dest': destinations[3]},

            # Sydney
            {'content': 'Stunning harbor and Opera House. Bondi Beach is amazing.', 'rating': 5, 'user': users[1], 'dest': destinations[4]},
            {'content': 'Great weather and outdoor activities. Harbour Bridge climb was thrilling.', 'rating': 5, 'user': users[2], 'dest': destinations[4]},
            {'content': 'Vibrant city with excellent seafood. Royal Botanic Gardens are beautiful.', 'rating': 4, 'user': users[3], 'dest': destinations[4]},

            # Istanbul
            {'content': 'Bridge between continents. Hagia Sophia and Blue Mosque are incredible.', 'rating': 5, 'user': users[0], 'dest': destinations[5]},
            {'content': 'Amazing bazaars and food. Bosphorus cruise was unforgettable.', 'rating': 5, 'user': users[1], 'dest': destinations[5]},
            {'content': 'Rich history and culture. A bit chaotic but authentic.', 'rating': 4, 'user': users[2], 'dest': destinations[5]},

            # Makkah
            {'content': 'Sacred and spiritual. The Kaaba is awe-inspiring.', 'rating': 5, 'user': users[3], 'dest': destinations[6]},
            {'content': 'Powerful religious experience. Very crowded during Hajj.', 'rating': 5, 'user': users[0], 'dest': destinations[6]},
            {'content': 'Holy site with deep significance. Requires proper preparation.', 'rating': 5, 'user': users[1], 'dest': destinations[6]},

            # Medina
            {'content': 'Peaceful and holy. Prophet\'s Mosque is magnificent.', 'rating': 5, 'user': users[2], 'dest': destinations[7]},
            {'content': 'Spiritual journey. Quba Mosque visit was meaningful.', 'rating': 5, 'user': users[3], 'dest': destinations[7]},
            {'content': 'Sacred city with rich Islamic history.', 'rating': 5, 'user': users[0], 'dest': destinations[7]},

            # Kuwait City
            {'content': 'Modern Middle Eastern city with traditional souks.', 'rating': 4, 'user': users[1], 'dest': destinations[8]},
            {'content': 'Good shopping and waterfront. Kuwait Towers are nice.', 'rating': 4, 'user': users[2], 'dest': destinations[8]},
            {'content': 'Clean and organized. Great for business and leisure.', 'rating': 4, 'user': users[3], 'dest': destinations[8]},

            # Doha
            {'content': 'Modern architecture and museums. Katara Cultural Village is great.', 'rating': 4, 'user': users[0], 'dest': destinations[9]},
            {'content': 'Desert and sea combination. Souq Waqif has authentic charm.', 'rating': 5, 'user': users[1], 'dest': destinations[9]},
            {'content': 'Growing city with excellent infrastructure.', 'rating': 4, 'user': users[2], 'dest': destinations[9]},

            # Los Angeles
            {'content': 'Hollywood dreams come true. Beaches and mountains nearby.', 'rating': 4, 'user': users[3], 'dest': destinations[10]},
            {'content': 'Diverse entertainment capital. Walk of Fame is fun.', 'rating': 4, 'user': users[0], 'dest': destinations[10]},
            {'content': 'Great weather and celebrity sightings. Traffic is bad though.', 'rating': 3, 'user': users[1], 'dest': destinations[10]},

            # Manchester
            {'content': 'Music history heaven. John Rylands Library is stunning.', 'rating': 4, 'user': users[2], 'dest': destinations[11]},
            {'content': 'Vibrant nightlife and canals. Football culture is strong.', 'rating': 4, 'user': users[3], 'dest': destinations[11]},
            {'content': 'Northern charm with great food and beer.', 'rating': 4, 'user': users[0], 'dest': destinations[11]},

            # Nice
            {'content': 'Beautiful French Riviera. Promenade and old town are charming.', 'rating': 5, 'user': users[1], 'dest': destinations[12]},
            {'content': 'Perfect for relaxation. Beaches and markets are lovely.', 'rating': 5, 'user': users[2], 'dest': destinations[12]},
            {'content': 'Mediterranean paradise with great food.', 'rating': 4, 'user': users[3], 'dest': destinations[12]},

            # Vancouver
            {'content': 'Stunning nature and city mix. Stanley Park is incredible.', 'rating': 5, 'user': users[0], 'dest': destinations[13]},
            {'content': 'Outdoor activities paradise. Granville Island is fun.', 'rating': 5, 'user': users[1], 'dest': destinations[13]},
            {'content': 'Clean, friendly city with mountains and ocean.', 'rating': 5, 'user': users[2], 'dest': destinations[13]},

            # Melbourne
            {'content': 'Coffee culture and street art. Queen Victoria Market is great.', 'rating': 4, 'user': users[3], 'dest': destinations[14]},
            {'content': 'Cultural hub with festivals and sports.', 'rating': 4, 'user': users[0], 'dest': destinations[14]},
            {'content': 'Vibrant and walkable. Great food scene.', 'rating': 4, 'user': users[1], 'dest': destinations[14]},

            # Ankara
            {'content': 'Capital with museums and history. Ataturk Mausoleum is impressive.', 'rating': 4, 'user': users[2], 'dest': destinations[15]},
            {'content': 'Modern city with ancient roots. Good food and culture.', 'rating': 4, 'user': users[3], 'dest': destinations[15]},
            {'content': 'Political center with interesting sites.', 'rating': 3, 'user': users[0], 'dest': destinations[15]},

            # Jeddah
            {'content': 'Red Sea beauty and modern development.', 'rating': 4, 'user': users[1], 'dest': destinations[16]},
            {'content': 'Historic sites and shopping. Corniche is nice.', 'rating': 4, 'user': users[2], 'dest': destinations[16]},
            {'content': 'Growing city with good infrastructure.', 'rating': 4, 'user': users[3], 'dest': destinations[16]},

            # Riyadh
            {'content': 'Modern capital with traditional markets.', 'rating': 4, 'user': users[0], 'dest': destinations[17]},
            {'content': 'Business hub with good amenities.', 'rating': 4, 'user': users[1], 'dest': destinations[17]},
            {'content': 'Clean and organized. Souks are interesting.', 'rating': 3, 'user': users[2], 'dest': destinations[17]},

            # Hawalli
            {'content': 'Shopping paradise in Kuwait. Avenues Mall is huge.', 'rating': 4, 'user': users[3], 'dest': destinations[18]},
            {'content': 'Commercial district with good food options.', 'rating': 4, 'user': users[0], 'dest': destinations[18]},
            {'content': 'Modern shopping and entertainment area.', 'rating': 4, 'user': users[1], 'dest': destinations[18]},

            # Al Wakrah
            {'content': 'Traditional Qatari architecture and maritime museum.', 'rating': 4, 'user': users[2], 'dest': destinations[19]},
            {'content': 'Historic souk and fishing heritage.', 'rating': 4, 'user': users[3], 'dest': destinations[19]},
            {'content': 'Coastal charm with cultural sites.', 'rating': 4, 'user': users[0], 'dest': destinations[19]},

            # Chicago
            {'content': 'Architecture heaven. Magnificent Mile is amazing.', 'rating': 4, 'user': users[1], 'dest': destinations[20]},
            {'content': 'Deep dish pizza and lakefront views.', 'rating': 4, 'user': users[2], 'dest': destinations[20]},
            {'content': 'Cultural institutions and sports teams.', 'rating': 4, 'user': users[3], 'dest': destinations[20]},

            # Edinburgh
            {'content': 'Castle and festivals make it magical. Scotch whisky tours!', 'rating': 5, 'user': users[0], 'dest': destinations[21]},
            {'content': 'Historic old town and Arthur\'s Seat hike.', 'rating': 5, 'user': users[1], 'dest': destinations[21]},
            {'content': 'Literary history and ghost tours.', 'rating': 4, 'user': users[2], 'dest': destinations[21]},

            # Lyon
            {'content': 'Gastronomic capital. Food halls and bouchons are incredible.', 'rating': 5, 'user': users[3], 'dest': destinations[22]},
            {'content': 'Historic Vieux Lyon and Roman theaters.', 'rating': 4, 'user': users[0], 'dest': destinations[22]},
            {'content': 'Beautiful city with great wine and cuisine.', 'rating': 5, 'user': users[1], 'dest': destinations[22]},

            # Montreal
            {'content': 'European charm in North America. Old Montreal is lovely.', 'rating': 4, 'user': users[2], 'dest': destinations[23]},
            {'content': 'Bilingual culture and poutine. Mount Royal views.', 'rating': 4, 'user': users[3], 'dest': destinations[23]},
            {'content': 'Festivals and underground city.', 'rating': 4, 'user': users[0], 'dest': destinations[23]},

            # Brisbane
            {'content': 'Subtropical paradise with South Bank and Lone Pine.', 'rating': 4, 'user': users[1], 'dest': destinations[24]},
            {'content': 'River city with good food and culture.', 'rating': 4, 'user': users[2], 'dest': destinations[24]},
            {'content': 'Gateway to Queensland. Botanic gardens are beautiful.', 'rating': 4, 'user': users[3], 'dest': destinations[24]},
        ]

        for review_data in reviews_data:
            review = Review(
                content=review_data['content'],
                rating=review_data['rating'],
                user_id=review_data['user'].id,
                destination_id=review_data['dest'].id
            )
            db.session.add(review)

        db.session.commit()

        # Calculate average ratings for destinations
        dest_ratings = {}
        for dest in destinations:
            avg_rating = db.session.query(func.avg(Review.rating)).filter(Review.destination_id == dest.id).scalar()
            dest_ratings[dest.id] = avg_rating or 0

        # Create travel plans with top-rated destinations
        plans_data = [
            {
                'name': 'European Gems',
                'user': users[0],
                'countries': ['France', 'UK']
            },
            {
                'name': 'North American Adventure',
                'user': users[1],
                'countries': ['USA', 'Canada']
            },
            {
                'name': 'Sacred Islamic Journey',
                'user': users[2],
                'countries': ['Saudi Arabia']
            },
            {
                'name': 'Middle Eastern Discovery',
                'user': users[3],
                'countries': ['Turkey', 'Kuwait', 'Qatar']
            },
            {
                'name': 'Aussie Explorer',
                'user': users[0],
                'countries': ['Australia']
            }
        ]

        for plan_data in plans_data:
            plan = TravelPlan(name=plan_data['name'], user_id=plan_data['user'].id)
            db.session.add(plan)
            db.session.commit()  # To get plan.id

            # Get destinations from specified countries, sorted by rating descending
            country_dests = []
            for dest in destinations:
                for country in plan_data['countries']:
                    if country in dest.location:
                        country_dests.append((dest, dest_ratings[dest.id]))
                        break

            # Sort by rating descending and take top 3-4
            country_dests.sort(key=lambda x: x[1], reverse=True)
            top_dests = country_dests[:4]  # Take top 4

            for dest, _ in top_dests:
                plan.destinations.append(dest)

            db.session.commit()

        print("Database populated with sample data including travel plans!")

if __name__ == '__main__':
    populate_db()