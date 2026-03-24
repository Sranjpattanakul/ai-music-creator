# AI Music Creator Platform - Domain Layer Implementation

## Project Overview
This project implements the domain layer for an AI Music Creator Platform using Django ORM. It translates the domain model from Exercise 2 into a working database schema with full CRUD functionality.

## Setup Instructions

### Prerequisites
- Python 3.12+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/Sranjpattanakul/ai-music-creator.git
cd ai-music-creator
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install django
```

4. Run migrations
```bash
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```

6. Start development server
```bash
python manage.py runserver
```

7. Access Django Admin
```
http://127.0.0.1:8000/admin
```

## Domain Model Entities

The following entities are implemented based on Exercise 2 domain model:

- **User** (Django's built-in User model)
- **UserProfile** - Extends User with google_id
- **Library** - User's song collection
- **Song** - Generated music with metadata
- **Prompt** - Song generation parameters
- **Draft** - Saved prompts not yet generated
- **ShareLink** - Shareable song links
- **PlaybackSession** - User's current playback state
- **EqualizerPreset** - Saved audio settings

## CRUD Operations

All CRUD (Create, Read, Update, Delete) operations are available through Django Admin interface at `/admin`.

### Test Data Created:
- 1 User (john_doe)
- 1 UserProfile
- 1 Library
- 3 Prompts (Birthday, Anniversary, Graduation)
- 3 Songs (with different statuses)
- 1 Draft
- 1 ShareLink
- 1 PlaybackSession
- 1 EqualizerPreset

## Screenshots

See `/screenshots` folder for evidence of CRUD functionality.

## Database

SQLite database is used for development (`db.sqlite3`).

## Notes

- GenerationJob entity was removed from the domain model based on TA feedback (over-modeling)
- All relationships from the domain model are correctly implemented
- Validation is applied for duration fields (2:00 - 6:00 minutes)
