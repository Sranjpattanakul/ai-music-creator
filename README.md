# AI Music Creator Platform

This repository contains the implementation for **Exercise 3** (Domain Layer) and **Exercise 4** (Strategy Pattern), built progressively on top of each other.

---

# Exercise 4 – Strategy Pattern (Mock vs Suno API)

AiSongGenerator is a Django-based AI song generation platform.  
The system supports real song generation via the Suno API and a mock offline strategy for development and testing.

This implementation was developed for **Exercise 4: Apply Strategy Pattern for Song Generation**, building on the domain layer from Exercise 3.

---

## Project Overview

The system supports the following core flow:

1. A **User** registers and logs in via Google OAuth or demo login.
2. The user submits a **Prompt** (title, description, mood, occasion, singer tone, duration).
3. The system generates a **Song** using the selected strategy (Mock or Suno API).
4. Generated songs are stored in the user's **Library** with real-time status tracking.
5. Songs can be favorited, shared via unique token links, and deleted.
6. Saved **Drafts** allow users to resume incomplete prompts later.
7. Completed songs appear on the **Browse** page for all users.

---

## Main Features

- **Strategy Pattern** for song generation (Mock vs Suno API, swappable via env var or UI toggle)
- **Mock strategy** — offline, deterministic, no API calls required
- **Suno API strategy** — real AI generation via SunoApi.org
- Google OAuth 2.0 authentication + demo login fallback
- Full frontend UI (Django Templates, Tailwind CSS, Alpine.js)
- Browse page for public songs
- Library management: favorites, share links, delete, drafts
- Real-time polling with live status counter

---

## Domain Entities

- **User**
- **Library**
- **Song**
- **Prompt**
- **Draft**
- **GenerationJob**
- **ShareLink**
- **PlaybackSession**
- **EqualizerPreset**

---

## Domain Relationships

- One **User** owns one **Library**
- One **Library** contains many **Songs** and **Drafts**
- One **Prompt** is linked to one **GenerationJob**
- One **GenerationJob** tracks one **Song**
- One **Song** can have many **ShareLinks**
- One **User** has one **PlaybackSession**
- One **User** has many **EqualizerPresets**

---

## Project Structure

```text
AiSongGenerator/
├── app/
│   ├── controllers/
│   │   ├── auth_controller.py
│   │   ├── home_controller.py
│   │   ├── pages_controller.py
│   │   ├── generation_controller.py
│   │   ├── song_manager_controller.py
│   │   ├── browse_controller.py
│   │   └── playback_controller.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── library.py
│   │   ├── song.py
│   │   ├── prompt.py
│   │   ├── draft.py
│   │   ├── generation.py
│   │   ├── share.py
│   │   ├── playback.py
│   │   └── equalizer.py
│   │
│   ├── routes/
│   │   ├── auth_urls.py
│   │   ├── generation_urls.py
│   │   ├── manager_urls.py
│   │   ├── browse_urls.py
│   │   └── playback_urls.py
│   │
│   ├── services/
│   │   ├── generation_service.py
│   │   ├── song_manager_service.py
│   │   ├── browse_service.py
│   │   └── playback_service.py
│   │
│   ├── strategies/                   ← Strategy Pattern
│   │   ├── base.py                   ← Abstract interface
│   │   ├── factory.py                ← Centralized strategy selection
│   │   ├── mock_strategy.py          ← Offline mock implementation
│   │   ├── suno_strategy.py          ← Suno API implementation
│   │   └── exceptions.py
│   │
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── home.html
│       ├── library.html
│       └── browse.html
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .env.example
├── manage.py
└── README.md
```

---

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Sranjpattanakul/ai-music-creator.git
cd ai-music-creator
```

### 2. Install dependencies

```bash
pip install django requests python-dotenv
```

### 3. Create a `.env` file

```bash
cp .env.example .env
```

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
GENERATOR_STRATEGY=mock
SUNO_API_KEY=your_api_key_here
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

Never commit `.env` — it contains secrets. Only `.env.example` is committed.

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Run the application

```bash
python manage.py runserver
```

Open `http://localhost:8000` — log in with Google or use the demo login form.

---

## Strategy Pattern: Song Generation

This project implements the **Strategy design pattern** to allow swappable song generation behavior without modifying controllers or services.

### Strategy Interface

Defined in `app/strategies/base.py`:

```python
class SongGeneratorStrategy(ABC):
    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
        ...

    @abstractmethod
    def get_status(self, task_id: str) -> GenerationResult:
        ...
```

Both strategies implement this same interface.

---

### Running in Mock Mode (Offline)

Set in `.env` or select **Mock (Instant)** in the UI:

```env
GENERATOR_STRATEGY=mock
```

Mock mode produces a deterministic song with a fixed placeholder audio URL. No API key or internet connection required.

**Example output:**

```json
{
  "success": true,
  "task_id": "mock-5052fcbc",
  "status": "SUCCESS",
  "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
}
```

---

### Running in Suno Mode (Live API)

Set in `.env` or select **Suno AI (Real)** in the UI:

```env
GENERATOR_STRATEGY=suno
SUNO_API_KEY=your_api_key_here
```

Suno mode calls `POST https://api.sunoapi.org/api/v1/generate`, stores the returned `taskId`, and polls for status every 3 seconds until `SUCCESS` or `FAILED`.

**Example output (initial response):**

```json
{
  "success": true,
  "task_id": "f3ac02ded1b961f27f83acdd9a468c4f",
  "status": "QUEUED",
  "audio_url": null
}
```

Status flow: `QUEUED` → `GENERATING` → `SUCCESS` / `FAILED`

---

### Strategy Selection

Selection is centralized in `app/strategies/factory.py`:

```python
def get_generator(strategy: str = None) -> SongGeneratorStrategy:
    if not strategy:
        strategy = getattr(settings, 'GENERATOR_STRATEGY', 'mock')
    if strategy.lower() == 'suno':
        return SunoSongGeneratorStrategy()
    return MockSongGeneratorStrategy()
```

No `if/else` logic is scattered through controllers or services.

---

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| `POST` | `/api/generation/generate/` | Submit a song generation request |
| `GET` | `/api/generation/status/<task_id>/` | Poll generation status |
| `PATCH` | `/api/library/<user_id>/songs/<song_id>/favorite/` | Toggle favorite |
| `DELETE` | `/api/library/<user_id>/songs/<song_id>/delete/` | Delete song |
| `POST` | `/api/browse/<user_id>/songs/<song_id>/share/` | Create share link |
| `POST` | `/api/library/<user_id>/drafts/save/` | Save draft |
| `DELETE` | `/api/library/<user_id>/drafts/<draft_id>/delete/` | Delete draft |

---

## Notes

- Authentication implemented via Google OAuth 2.0 redirect flow
- Real AI generation implemented via Suno API strategy
- Frontend UI implemented with Django Templates, Tailwind CSS, and Alpine.js
- Strategy selection controlled by `GENERATOR_STRATEGY` env var or per-request UI toggle
- `.env` file must never be committed — it contains secrets

---

## Author

Name: `Sran Jarurangsripattanakul`  
Course: Principle of Software Design  
Exercise: **Exercise 4 – Apply Strategy Pattern for Song Generation**

---

---

# Exercise 3 – Domain Layer Implementation

## Overview
Exercise 3 implements the domain layer for the AI Music Creator Platform using Django ORM.
It translates the domain model from Exercise 2 into a working database schema with full CRUD functionality.

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

---

## Creating a User (Important)

Since this project extends Django's built-in User model with `UserProfile`,
creating a user is a two-step process:

### Step 1: Create the Django User
1. Go to **Authentication and Authorization → Users → Add User**
2. Fill in username and password
3. Click **"Save and continue editing"** ← important, do NOT click "Save" yet
4. On the next page, fill in additional fields (email, first name, last name)
5. Click **Save**

### Step 2: Create the UserProfile
1. Go to **Domain → User profiles → Add User Profile**
2. Select the user you just created
3. Fill in `google_id`
4. Click **Save**

> **Note:** UserProfile extends the built-in Django User to store additional
> domain-specific information. Both records must exist for a complete user entity.

---

## Domain Model Entities

| Entity | Description |
|---|---|
| **User** | Django's built-in User model |
| **UserProfile** | Extends User with `google_id` |
| **Library** | User's personal song collection |
| **Song** | AI-generated music with metadata |
| **Prompt** | Parameters used for song generation |
| **Draft** | Saved prompts not yet submitted for generation |
| **ShareLink** | Shareable links for songs |
| **PlaybackSession** | Tracks the user's current playback state |
| **EqualizerPreset** | Saved audio equalizer settings |

> **Note:** `GenerationJob` was removed from the domain model based on TA feedback
> as it was considered over-modeling for this stage.

---

## Domain Relationships

| Relationship | Type |
|---|---|
| User → UserProfile | One-to-One |
| User → Library | One-to-One |
| Library → Songs | One-to-Many |
| Song → Prompt | One-to-One |
| User → Drafts | One-to-Many |
| User → ShareLinks | One-to-Many |
| Song → ShareLink | One-to-Many |
| User → PlaybackSession | One-to-One |
| User → EqualizerPresets | One-to-Many |

---

## CRUD Operations

All CRUD operations are available through the Django Admin interface at `/admin`.

- **Create** – Click **"Add"** next to any entity in the admin panel
- **Read** – Click on any entity name to view the list of records
- **Update** – Click on any record to open and edit it, then click **Save**
- **Delete** – Open a record and click the **Delete** button at the bottom

---

## Test Data

| Entity | Records |
|---|---|
| User | 1 (john_doe) |
| UserProfile | 1 |
| Library | 1 |
| Prompts | 3 (Birthday Song for Mom, Wedding Anniversary Ballad, Graduation Song) |
| Songs | 3 (Happy Birthday Mom, Forever Together, Summer Vibes) |
| Drafts | 1 (Draft: Graduation Song) |
| ShareLinks | 1 (Share link for Happy Birthday Mom) |
| PlaybackSessions | 1 (john_doe's playback) |
| EqualizerPresets | 1 (Bass Boost) |

---

## Screenshots

### Create
**Creating a new User (Step 1 - Username & Password)**
![Create User Step 1](screenshots/Screenshot_2026-03-24_at_7_46_33_PM.png)

**Creating a new User (Step 2 - Save and continue editing)**
![Create User Step 2](screenshots/Screenshot_2026-03-24_at_7_44_00_PM.png)

### Read
**Prompts list view showing all 3 persisted records**
![Read Prompts](screenshots/Screenshot_2026-03-24_at_7_49_38_PM.png)

### Update
**Editing an existing Prompt (Graduation Song)**
![Update Prompt](screenshots/Screenshot_2026-03-24_at_7_48_10_PM.png)

### Delete
**Selecting a Draft with delete action**
![Delete Draft List](screenshots/Screenshot_2026-03-24_at_7_46_53_PM.png)

**Delete button on Draft detail view**
![Delete Draft Detail](screenshots/Screenshot_2026-03-24_at_7_48_24_PM.png)

---

## Database

SQLite is used as the development database (`db.sqlite3`).
Migration files are committed to the repository to ensure the schema can be reproduced exactly.

---

## Notes (Exercise 3)

- `GenerationJob` was removed from the domain model based on TA feedback (over-modeling)
- All relationships from Exercise 2 domain model are correctly implemented
- Duration validation is applied on Song (valid range: 2:00 – 6:00 minutes)
- This implementation intentionally focuses on the domain layer only
