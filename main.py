from fastapi import FastAPI, APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
import math

# Models
class UserProfile(BaseModel):
    user_id: int
    name: str
    interests: List[str]
    location: str
    age: int

class UserMatchResponse(BaseModel):
    user_id: int
    name: str
    interests: List[str]
    location: str
    age: int
    match_score: float
    match_reasons: List[str]

# Mock user data with varied locations and ages
mock_user_profiles = [
    UserProfile(user_id=1, name="Alice", interests=["hiking", "photography", "yoga"], location="London", age=25),
    UserProfile(user_id=2, name="Bob", interests=["hiking", "gaming"], location="Berlin", age=28),
    UserProfile(user_id=3, name="Charlie", interests=["cooking", "yoga"], location="London", age=32),
    UserProfile(user_id=4, name="Diana", interests=["photography", "travel"], location="Paris", age=22),
    UserProfile(user_id=5, name="Eve", interests=["gaming", "cooking"], location="Berlin", age=30),
    UserProfile(user_id=6, name="Frank", interests=["music", "football", "travel"], location="Madrid", age=27),
    UserProfile(user_id=7, name="Grace", interests=["yoga", "reading", "coffee"], location="Rome", age=24),
    UserProfile(user_id=8, name="Hector", interests=["chess", "coding", "gaming"], location="London", age=29),
    UserProfile(user_id=9, name="Ivy", interests=["painting", "travel", "fashion"], location="Paris", age=26),
    UserProfile(user_id=10, name="Jack", interests=["running", "tech", "board games"], location="Berlin", age=31),

    UserProfile(user_id=11, name="Karen", interests=["yoga", "photography", "coffee"], location="London", age=23),
    UserProfile(user_id=12, name="Leo", interests=["basketball", "movies", "gaming"], location="Rome", age=33),
    UserProfile(user_id=13, name="Mona", interests=["cooking", "reading", "travel"], location="Madrid", age=29),
    UserProfile(user_id=14, name="Nathan", interests=["hiking", "cycling", "tech"], location="Paris", age=27),
    UserProfile(user_id=15, name="Olivia", interests=["music", "painting", "fashion"], location="London", age=25),
    UserProfile(user_id=16, name="Paul", interests=["football", "tech", "movies"], location="Berlin", age=30),
    UserProfile(user_id=17, name="Quinn", interests=["coffee", "board games", "travel"], location="Rome", age=28),
    UserProfile(user_id=18, name="Rita", interests=["yoga", "music", "cooking"], location="Madrid", age=22),
    UserProfile(user_id=19, name="Sam", interests=["cycling", "hiking", "photography"], location="London", age=34),
    UserProfile(user_id=20, name="Tina", interests=["chess", "fashion", "travel"], location="Paris", age=26),

    UserProfile(user_id=21, name="Uma", interests=["movies", "coffee", "reading"], location="Berlin", age=27),
    UserProfile(user_id=22, name="Victor", interests=["tech", "coding", "gaming"], location="London", age=29),
    UserProfile(user_id=23, name="Wendy", interests=["photography", "yoga", "painting"], location="Rome", age=24),
    UserProfile(user_id=24, name="Xander", interests=["board games", "football", "travel"], location="Madrid", age=32),
    UserProfile(user_id=25, name="Yara", interests=["fashion", "music", "movies"], location="Paris", age=23),
    UserProfile(user_id=26, name="Zane", interests=["hiking", "cycling", "tech"], location="Berlin", age=35),
    UserProfile(user_id=27, name="Amelia", interests=["coffee", "painting", "photography"], location="London", age=26),
    UserProfile(user_id=28, name="Brian", interests=["gaming", "movies", "football"], location="Rome", age=30),
    UserProfile(user_id=29, name="Clara", interests=["travel", "yoga", "reading"], location="Madrid", age=25),
    UserProfile(user_id=30, name="David", interests=["tech", "cycling", "chess"], location="Paris", age=28),

    UserProfile(user_id=31, name="Ella", interests=["hiking", "coffee", "music"], location="London", age=21),
    UserProfile(user_id=32, name="Felix", interests=["movies", "coding", "gaming"], location="Berlin", age=33),
    UserProfile(user_id=33, name="Gina", interests=["fashion", "yoga", "painting"], location="Rome", age=19),
    UserProfile(user_id=34, name="Hassan", interests=["football", "photography", "tech"], location="Madrid", age=35),
    UserProfile(user_id=35, name="Isabella", interests=["reading", "coffee", "travel"], location="Paris", age=20),
    UserProfile(user_id=36, name="Jonas", interests=["cycling", "gaming", "music"], location="London", age=28),
    UserProfile(user_id=37, name="Kylie", interests=["movies", "board games", "painting"], location="Berlin", age=22),
    UserProfile(user_id=38, name="Liam", interests=["basketball", "tech", "cooking"], location="Rome", age=30),
    UserProfile(user_id=39, name="Maria", interests=["fashion", "coffee", "yoga"], location="Madrid", age=27),
    UserProfile(user_id=40, name="Noah", interests=["hiking", "running", "gaming"], location="Paris", age=23),

    UserProfile(user_id=41, name="Omar", interests=["photography", "coffee", "coding"], location="London", age=35),
    UserProfile(user_id=42, name="Paula", interests=["music", "movies", "travel"], location="Berlin", age=19),
    UserProfile(user_id=43, name="Quincy", interests=["tech", "cycling", "chess"], location="Rome", age=25),
    UserProfile(user_id=44, name="Rosa", interests=["painting", "yoga", "reading"], location="Madrid", age=32),
    UserProfile(user_id=45, name="Sebastian", interests=["gaming", "football", "coffee"], location="Paris", age=26),
    UserProfile(user_id=46, name="Teresa", interests=["travel", "movies", "fashion"], location="London", age=28),
    UserProfile(user_id=47, name="Ulysses", interests=["basketball", "music", "coding"], location="Berlin", age=20),
    UserProfile(user_id=48, name="Valeria", interests=["hiking", "yoga", "coffee"], location="Rome", age=24),
    UserProfile(user_id=49, name="William", interests=["board games", "photography", "gaming"], location="Madrid", age=31),
    UserProfile(user_id=50, name="Xenia", interests=["painting", "reading", "travel"], location="Paris", age=22),

    UserProfile(user_id=51, name="Yusuf", interests=["coding", "chess", "movies"], location="London", age=27),
    UserProfile(user_id=52, name="Zara", interests=["coffee", "music", "fashion"], location="Berlin", age=21),
    UserProfile(user_id=53, name="Aaron", interests=["football", "gaming", "movies"], location="Rome", age=29),
    UserProfile(user_id=54, name="Bella", interests=["yoga", "painting", "reading"], location="Madrid", age=23),
    UserProfile(user_id=55, name="Caleb", interests=["photography", "tech", "cycling"], location="Paris", age=34),
    UserProfile(user_id=56, name="Daisy", interests=["coffee", "fashion", "travel"], location="London", age=20),
    UserProfile(user_id=57, name="Ethan", interests=["basketball", "music", "movies"], location="Berlin", age=32),
    UserProfile(user_id=58, name="Farah", interests=["painting", "reading", "yoga"], location="Rome", age=19),
    UserProfile(user_id=59, name="George", interests=["coding", "board games", "tech"], location="Madrid", age=26),
    UserProfile(user_id=60, name="Hana", interests=["hiking", "coffee", "photography"], location="Paris", age=28),

    UserProfile(user_id=61, name="Ian", interests=["football", "gaming", "music"], location="London", age=24),
    UserProfile(user_id=62, name="Julia", interests=["fashion", "painting", "travel"], location="Berlin", age=35),
    UserProfile(user_id=63, name="Kevin", interests=["movies", "coding", "tech"], location="Rome", age=25),
    UserProfile(user_id=64, name="Lara", interests=["coffee", "reading", "yoga"], location="Madrid", age=27),
    UserProfile(user_id=65, name="Max", interests=["photography", "cycling", "hiking"], location="Paris", age=30),
    UserProfile(user_id=66, name="Nina", interests=["fashion", "music", "movies"], location="London", age=22),
    UserProfile(user_id=67, name="Oscar", interests=["football", "board games", "coding"], location="Berlin", age=29),
    UserProfile(user_id=68, name="Pia", interests=["yoga", "painting", "reading"], location="Rome", age=18),
    UserProfile(user_id=69, name="Quentin", interests=["cycling", "gaming", "tech"], location="Madrid", age=34),
    UserProfile(user_id=70, name="Rania", interests=["travel", "coffee", "photography"], location="Paris", age=23),

    UserProfile(user_id=71, name="Steve", interests=["basketball", "movies", "gaming"], location="London", age=30),
    UserProfile(user_id=72, name="Tara", interests=["yoga", "reading", "coffee"], location="Berlin", age=19),
    UserProfile(user_id=73, name="Umar", interests=["tech", "cycling", "coding"], location="Rome", age=33),
    UserProfile(user_id=74, name="Vera", interests=["painting", "music", "fashion"], location="Madrid", age=20),
    UserProfile(user_id=75, name="Waleed", interests=["football", "hiking", "photography"], location="Paris", age=27),
    UserProfile(user_id=76, name="Ximena", interests=["movies", "coffee", "reading"], location="London", age=21),
    UserProfile(user_id=77, name="Yara", interests=["gaming", "chess", "tech"], location="Berlin", age=28),
    UserProfile(user_id=78, name="Zahid", interests=["yoga", "cooking", "music"], location="Rome", age=24),
    UserProfile(user_id=79, name="Alina", interests=["fashion", "photography", "travel"], location="Madrid", age=26),
    UserProfile(user_id=80, name="Ben", interests=["basketball", "movies", "gaming"], location="Paris", age=35),

    UserProfile(user_id=81, name="Claudia", interests=["coffee", "painting", "yoga"], location="London", age=23),
    UserProfile(user_id=82, name="Daniel", interests=["cycling", "tech", "coding"], location="Berlin", age=31),
    UserProfile(user_id=83, name="Ella", interests=["fashion", "music", "movies"], location="Rome", age=22),
    UserProfile(user_id=84, name="Faisal", interests=["football", "gaming", "board games"], location="Madrid", age=28),
    UserProfile(user_id=85, name="Gloria", interests=["yoga", "photography", "reading"], location="Paris", age=19),
    UserProfile(user_id=86, name="Hamza", interests=["basketball", "movies", "tech"], location="London", age=25),
    UserProfile(user_id=87, name="Irene", interests=["fashion", "travel", "coffee"], location="Berlin", age=20),
    UserProfile(user_id=88, name="James", interests=["cycling", "gaming", "music"], location="Rome", age=29),
    UserProfile(user_id=89, name="Khadija", interests=["painting", "yoga", "photography"], location="Madrid", age=27),
    UserProfile(user_id=90, name="Louis", interests=["hiking", "movies", "football"], location="Paris", age=33),

    UserProfile(user_id=91, name="Marta", interests=["reading", "fashion", "coffee"], location="London", age=24),
    UserProfile(user_id=92, name="Nikolai", interests=["coding", "tech", "board games"], location="Berlin", age=30),
    UserProfile(user_id=93, name="Ola", interests=["yoga", "travel", "music"], location="Rome", age=18),
    UserProfile(user_id=94, name="Pedro", interests=["football", "basketball", "gaming"], location="Madrid", age=26),
    UserProfile(user_id=95, name="Qamar", interests=["coffee", "photography", "movies"], location="Paris", age=28),
    UserProfile(user_id=96, name="Rosa", interests=["painting", "fashion", "yoga"], location="London", age=22),
    UserProfile(user_id=97, name="Salman", interests=["tech", "gaming", "chess"], location="Berlin", age=35),
    UserProfile(user_id=98, name="Tania", interests=["music", "reading", "coffee"], location="Rome", age=20),
    UserProfile(user_id=99, name="Usman", interests=["cycling", "hiking", "football"], location="Madrid", age=34),
    UserProfile(user_id=100, name="Valentina", interests=["photography", "movies", "fashion"], location="Paris", age=25),
]

# Service functions
async def get_all_users(
    location: Optional[str] = None,
    age_min: Optional[int] = None,
    age_max: Optional[int] = None
) -> List[UserProfile]:
    """Get all users with optional filters for location and age range."""
    users = mock_user_profiles
    if location:
        users = [user for user in users if user.location.lower() == location.lower()]
    if age_min is not None:
        users = [user for user in users if user.age >= age_min]
    if age_max is not None:
        users = [user for user in users if user.age <= age_max]
    return users

async def get_user_by_id(user_id: int) -> Optional[UserProfile]:
    for user in mock_user_profiles:
        if user.user_id == user_id:
            return user
    return None

# Router and matching functions
router = APIRouter()

def calculate_match_score(user: UserProfile, other_user: UserProfile) -> float:
    """Calculate a match score based on interests (40%), location (30%), and age (30%)."""
    # Interest-based score (40%)
    shared_interests = len(set(user.interests) & set(other_user.interests))
    max_interests = max(len(user.interests), len(other_user.interests)) or 1
    interest_score = shared_interests / max_interests if max_interests > 0 else 0

    # Location-based score (30%)
    location_score = 1.0 if user.location.lower() == other_user.location.lower() else 0.5

    # Age-based score (30%)
    age_difference = abs(user.age - other_user.age)
    max_age_diff = 20.0
    age_score = max(0, 1 - (age_difference / max_age_diff))

    # Weighted total: 40% interests, 30% location, 30% age
    total_score = (0.4 * interest_score) + (0.3 * location_score) + (0.3 * age_score)
    return round(total_score, 2)

def generate_match_reasons(user: UserProfile, other_user: UserProfile) -> List[str]:
    """Generate reasons for why users were matched."""
    reasons = []
    shared_interests = list(set(user.interests) & set(other_user.interests))
    if shared_interests:
        reasons.append(f"Matching Hobbies: {', '.join(shared_interests)}")
    if user.location.lower() == other_user.location.lower():
        reasons.append(f"Same location: {user.location}")
    else:
        reasons.append(f"Nearby location: {other_user.location}")
    age_difference = abs(user.age - other_user.age)
    if age_difference <= 5:
        reasons.append(f"Similar age range: {other_user.age} years old")
    return reasons

@router.get("/api/v1/match/users/v2/{user_id}", response_model=List[UserMatchResponse])
async def get_user_matches_v2(
    user_id: int,
    location: Optional[str] = Query(None, description="Filter by location (e.g., London)"),
    age_min: Optional[int] = Query(None, description="Minimum age filter", ge=18),
    age_max: Optional[int] = Query(None, description="Maximum age filter", le=100)
):
    """Get matched users with optional filters for location and age range."""
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get all users with filters applied
    all_users = await get_all_users(location=location, age_min=age_min, age_max=age_max)
    
    matches = []
    for other_user in all_users:
        if other_user.user_id != user_id:  # Don't match user with themselves
            score = calculate_match_score(user, other_user)
            if score >= 0.3:  # Threshold to filter weak matches
                reasons = generate_match_reasons(user, other_user)
                matches.append(
                    UserMatchResponse(
                        user_id=other_user.user_id,
                        name=other_user.name,
                        interests=other_user.interests,
                        location=other_user.location,
                        age=other_user.age,
                        match_score=score,
                        match_reasons=reasons
                    )
                )

    # Sort matches by score in descending order
    matches.sort(key=lambda x: x.match_score, reverse=True)
    return matches[:5]  # Return top 5 matches

# FastAPI app
app = FastAPI(title="Smart Matching API")

# Include the matching API router
app.include_router(router)

# Optional: Add a root endpoint for basic health check
@app.get("/")
async def root():
    return {"message": "Smart Matching API is running"}

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)