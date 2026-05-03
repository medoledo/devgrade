# DevGrade — Complete Project Documentation

> **Last Updated:** May 2026  
> **Maintainer:** DevGrade Team  
> **Status:** Production-Ready

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Full Project Structure](#2-full-project-structure)
3. [Models Documentation](#3-models-documentation)
4. [Templates Documentation](#4-templates-documentation)
5. [Admin Panel Guide](#5-admin-panel-guide)
6. [Business Logic](#6-business-logic)
7. [Deployment Guide](#7-deployment-guide)
8. [How to Add a New Project](#8-how-to-add-a-new-project-step-by-step-for-non-technical-admin)
9. [Future Features](#9-future-features-to-add)

---

## 1. Project Overview

### What is DevGrade?

DevGrade is a **Django-based marketplace website** built for **Egyptian university students** who need ready-made software projects for their final-year graduation requirements. Instead of building projects from scratch or hiring expensive developers, students can browse a catalog of production-ready Django projects, purchase them instantly, or request custom modifications.

### Target Audience

- **Primary:** Egyptian university students (Computer Science, IT, Engineering, MIS)
- **Secondary:** Freelancers and junior developers looking for starter templates
- **Language:** Arabic-first UI with Egyptian dialect (`مصري`) in all user-facing copy
- **Currency:** Egyptian Pounds (EGP) as primary. USD may be shown optionally in the future.

### Two Purchase Types

| Type | Description | Delivery | Price Range |
|------|-------------|----------|-------------|
| **Standard** | Buy the project as-is. Instant download of source code + documentation. | Immediate (Gumroad or direct link) | ~1,500 – 3,000 EGP |
| **Custom** | Request modifications to fit your university's exact requirements. | Delivered via WhatsApp + InstaPay/Vodafone Cash | ~3,000 – 10,000+ EGP |

### Payment Methods (Egyptian Market)

DevGrade is optimized for the Egyptian payment ecosystem:

- **InstaPay** — Primary bank transfer method
- **Vodafone Cash** — Mobile wallet payments
- **WhatsApp-based payment** — Customer sends proof of payment screenshot via WhatsApp, admin confirms manually
- **Gumroad** — Used as a fallback for international customers or those with cards (optional)

> **Note:** The site does NOT require international card processing. All local Egyptian payment methods are supported through manual confirmation workflows.

### Language & Localization

- **UI Direction:** RTL (Right-to-Left) Arabic
- **Font:** Cairo (Google Fonts) — weights 300–800
- **Copy Style:** Egyptian dialect (`اشترى`, `شوف`, `مفيش`, `عايز`)
- **Hardcoded Arabic:** All public-facing templates contain hardcoded Arabic text. Dashboard pages use a mix of Arabic and English.

---

## 2. Full Project Structure

```
devgrade/
├── devgrade/                    # Project configuration package
│   ├── __init__.py
│   ├── asgi.py                  # ASGI application entry point
│   ├── settings.py              # Main Django settings
│   ├── urls.py                  # Root URL configuration + sitemap
│   └── wsgi.py                  # WSGI application entry point
│
├── projects/                    # Main Django app (all business logic)
│   ├── __init__.py
│   ├── admin.py                 # Django Admin model registrations
│   ├── apps.py                  # AppConfig
│   ├── forms.py                 # MessageForm, ProjectForm
│   ├── middleware.py            # NoCacheMiddleware
│   ├── models.py                # All 7 models
│   ├── sitemaps.py              # SEO sitemaps
│   ├── storage.py               # NoCacheStaticFilesStorage
│   ├── tests.py                 # EMPTY — no tests written yet
│   ├── urls.py                  # All app URL routes
│   ├── views.py                 # All view functions
│   ├── management/
│   │   └── commands/
│   │       └── runserver.py     # Custom dev server (no-cache static)
│   └── migrations/
│       └── 0001_initial.py      # Complete initial migration
│
├── static/                      # Static assets
│   ├── css/
│   │   └── main.css             # Custom utilities, animations
│   ├── images/
│   │   └── devlogos.svg         # Site logo & favicon
│   └── js/
│       └── main.js              # HTMX CSRF, alerts, validation
│
├── templates/                   # All HTML templates
│   ├── base.html                # Site-wide RTL layout
│   ├── 403.html, 404.html, 500.html
│   ├── dashboard/               # Admin pages
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── project_form.html
│   │   ├── projects_list.html
│   │   └── categories_list.html
│   ├── pages/                   # Static content
│   │   ├── about.html
│   │   ├── contact.html
│   │   └── faq.html
│   ├── partials/                # HTMX partials
│   │   ├── _alert.html
│   │   ├── _message_form.html
│   │   ├── _message_row.html
│   │   ├── _messages_table.html
│   │   ├── _project_grid.html
│   │   └── _projects_table.html
│   └── projects/                # Public project pages
│       ├── home.html
│       ├── project_detail.html
│       └── project_list.html
│
├── media/                       # User-uploaded files
├── db.sqlite3                   # Development database (SQLite)
├── manage.py
├── requirements.txt
└── README.md
```

### App Breakdown: `projects/`

This is the only Django app. It contains everything:

| File | Responsibility |
|------|---------------|
| `models.py` | All data models (SiteConfig, Category, TechStack, Project, ProjectImage, ProjectFeature, Message) |
| `views.py` | All 20+ view functions (public + dashboard + auth + errors) |
| `forms.py` | `MessageForm` (lead capture) and `ProjectForm` (project CRUD) |
| `urls.py` | All URL routes for the entire site |
| `admin.py` | Admin panel configuration with inlines and custom methods |
| `sitemaps.py` | `ProjectSitemap`, `CategorySitemap`, `StaticViewSitemap` |
| `middleware.py` | `NoCacheMiddleware` — adds `Cache-Control: no-store` to every response |
| `storage.py` | `NoCacheStaticFilesStorage` — appends `?v=<mtime>` for cache busting |

---

## 3. Models Documentation

### `SingletonModel` (Abstract Base)

All models that should only ever have one instance inherit from this.

| Method | Behavior |
|--------|----------|
| `save()` | Forces `pk = 1` before saving |
| `delete()` | No-op — prevents accidental deletion |
| `load()` | Class method: `get_or_create(pk=1)` — always returns the single instance |

---

### `SiteConfig`

**Purpose:** Global site settings. Exactly one row exists. Editable via Django Admin.

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `site_name` | CharField(100) | `"DevGrade"` | Site title across all pages |
| `tagline` | CharField(200) | `"مشاريع Django جاهزة لطلاب الجامعات"` | Homepage H1 subtitle |
| `meta_description` | TextField | Arabic SEO description | Default meta description |
| `meta_keywords` | CharField(300) | `"مشاريع django, مشاريع جامعية..."` | Default meta keywords |
| `contact_email` | EmailField | `"Medoledowork144@gmail.com"` | Displayed on contact page |
| `contact_phone` | CharField(50) | `"01272776895"` | WhatsApp number |
| `footer_text` | TextField(blank) | — | Custom footer paragraph |
| `analytics_code` | TextField(blank) | — | Google Analytics or any tracking script |

**Special Logic:**
- Injected into every template via the `site_config` context processor.
- Admin config disables "Add" if one exists; disables "Delete" entirely.

---

### `Category`

**Purpose:** Project taxonomy / browsing filters.

| Field | Type | Purpose |
|-------|------|---------|
| `name` | CharField(100) | Display name (e.g., "Health & Care") |
| `slug` | SlugField(unique, blank) | URL-friendly identifier. Auto-generated from `name` if blank. |
| `order` | PositiveIntegerField(default=0) | Manual sort order |

**Relationships:**
- Reverse FK: `projects` → `Project` (a category can have many projects)

---

### `TechStack`

**Purpose:** Technology tags displayed as chips on project cards.

| Field | Type | Purpose |
|-------|------|---------|
| `name` | CharField(50) | Display name (e.g., "Django", "Tailwind CSS") |
| `slug` | SlugField(unique, blank) | Auto-generated from `name` |

**Relationships:**
- Reverse M2M: `projects` → `Project` (a tech stack can belong to many projects)

---

### `Project` (Central Entity)

**Purpose:** The main sellable project listing.

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `title` | CharField(200) | — | Project name |
| `slug` | SlugField(unique, blank) | Auto from title | URL identifier |
| `category` | FK → Category | `null=True` | Project type/topic |
| `full_description` | TextField | — | Rich content (supports line breaks) |
| `thumbnail` | ImageField | `upload_to='projects/thumbnails/'` | Card image |
| `demo_url` | URLField(blank) | — | Live preview link |
| `gumroad_standard_url` | URLField(blank) | — | Gumroad checkout link |
| `standard_price` | DecimalField(8,2) | `1500.00` | Standard purchase price (EGP) |
| `custom_price` | DecimalField(8,2) | `null` | Custom build price (EGP). If null, no custom option shown. |
| `tech_stack` | M2M → TechStack | `blank=True` | Technology tags |
| `is_featured` | BooleanField | `False` | Highlighted on homepage |
| `is_published` | BooleanField | `True` | Visible to public |
| `order` | PositiveIntegerField | `0` | Manual display order |
| `created_at` | DateTimeField | `auto_now_add` | — |
| `updated_at` | DateTimeField | `auto_now` | — |

**Reverse Relationships:**
- `images` → `ProjectImage` (gallery screenshots)
- `features` → `ProjectFeature` (bulleted feature list)

**Special Logic:**
- Slug auto-generated from title on save if blank.
- Ordered by `order` ascending, then `created_at` descending.

---

### `ProjectImage`

**Purpose:** Gallery screenshots for a project detail page.

| Field | Type | Purpose |
|-------|------|---------|
| `project` | FK → Project (CASCADE) | Parent project |
| `image` | ImageField | `upload_to='projects/images/'` |

---

### `ProjectFeature`

**Purpose:** Bulleted feature list on project detail page.

| Field | Type | Purpose |
|-------|------|---------|
| `project` | FK → Project (CASCADE) | Parent project |
| `feature` | CharField(200) | Feature text |
| `order` | PositiveIntegerField(default=0) | Display order |

---

### `Message` (Lead / Order System)

**Purpose:** Capture inquiries for custom project orders.

| Field | Type | Purpose |
|-------|------|---------|
| `name` | CharField(200) | Client full name |
| `email` | EmailField | Contact email |
| `phone` | CharField(50, blank) | Phone / WhatsApp number |
| `project_details` | TextField | Requirements description |
| `expected_budget` | CharField(100, blank) | Budget range (free text, e.g., "2000 - 5000") |
| `delivery_date` | DateField(null=True, blank) | Desired deadline |
| `is_aware_min_budget` | BooleanField(default=False) | Client acknowledges minimum budget |
| `status` | CharField(20, choices) | See below |
| `created_at` | DateTimeField | `auto_now_add` |

**STATUS_CHOICES:**

| Value | Label | Meaning |
|-------|-------|---------|
| `unread` | `Unread` | New submission, not seen |
| `opened` | `Opened` | Admin has viewed it |
| `refused` | `Refused` | Declined |
| `accepted` | `Accepted` | Accepted, work started |
| `contacted` | `Contacted` | Reached out to client |

**Methods:**
- `get_summary()` — Returns first 100 characters of `project_details` with `...`

> **Known Inconsistency:** The model's `is_aware_min_budget` label mentions **5000 EGP**, but the contact form template (`_message_form.html`) displays **3000 EGP**. This should be aligned to a single value.

---

## 4. Templates Documentation

### Base Layouts

#### `base.html`
- **Purpose:** Site-wide wrapper for all public pages.
- **Direction:** RTL (`dir="rtl"`)
- **Features:**
  - Tailwind CSS (CDN)
  - HTMX 1.9.12
  - Cairo font family
  - Sticky navbar with mobile hamburger menu
  - Auto-dismissing Django messages container
  - Footer with `site_config` links
  - Open Graph & Twitter Card meta tags
- **Context:** `site_config` (injected by context processor), `page_title`, `meta_description`, `meta_keywords`, `canonical_url`

#### `dashboard/base.html`
- **Purpose:** Admin dashboard wrapper.
- **Features:**
  - Overrides `base.html`'s `navbar` block with empty content (removes public nav)
  - Dark admin top bar: Dashboard | Projects | Categories | View Site | Logout
  - Global kebab menu CSS and JavaScript
  - Inline edit helper functions

---

### Error Pages

| Template | Arabic Text | Purpose |
|----------|-------------|---------|
| `403.html` | `مش مسموحلك تدخل هنا` | Forbidden access |
| `404.html` | `الصفحة دي مش موجودة` | Page not found |
| `500.html` | `حصلت مشكلة في السيرفر` | Server error |

---

### Dashboard Templates

#### `dashboard/dashboard.html`
- **Purpose:** Admin home page.
- **Context:** `stats` (new_messages, total_messages, total_projects), `messages_list`, `status_filter`, `search`, `status_choices`
- **Features:**
  - 3 stats cards
  - Quick action buttons (Manage Projects, Add Project, Manage Categories)
  - HTMX-filtered messages table
  - Status filter dropdown + search input

#### `dashboard/login.html`
- **Purpose:** Custom staff login page.
- **Features:** Centered card, username/password fields, error banner, "Back to website" link.
- **Security:** Only users with `is_staff=True` can authenticate.

#### `dashboard/project_form.html`
- **Purpose:** Add or edit a project.
- **Context:** `form` (ProjectForm), `project` (if editing), `tech_stacks`
- **Features:**
  - **5-step sticky stepper:** Basic Info → Pricing & Links → Tech & Settings → Media → Features
  - Drag-and-drop image upload zones with instant preview
  - Tech stack chip selector (clickable green chips)
  - Interactive feature tags (type + Enter to add, X to remove)
  - Client-side validation with shake animation
  - Character counter for description (0/2000)
  - Arabic labels and placeholders

#### `dashboard/projects_list.html`
- **Purpose:** Project management index.
- **Context:** `projects_list`, `query`, `status_filter`
- **Features:** Search + status filter (HTMX), kebab menu actions.

#### `dashboard/categories_list.html`
- **Purpose:** Category CRUD.
- **Context:** `categories`
- **Features:** Inline add form, table with inline edit (blur/Enter to save), kebab menu with Edit/Delete.

---

### Public Page Templates

#### `projects/home.html`
- **Purpose:** Landing page.
- **Context:** `featured` (top 3), `latest` (top 6), `total_projects`, SEO meta
- **Arabic Copy:** `مشاريع Django جاهزة للتسليم`, `مشاريع احترافية لـ كل مراحل الجامعة`, `شوف المشاريع`, `طلب مخصص`
- **Features:** Hero section with grid background, stats bar, featured projects, latest projects, CTA section

#### `projects/project_list.html`
- **Purpose:** Browse all projects.
- **Context:** `projects`, `categories` (with counts), `active_category`, `query`, SEO meta
- **Features:** Sidebar category filters, search box, active filter pills, includes `_project_grid.html`

#### `projects/project_detail.html`
- **Purpose:** Single project page.
- **Context:** `project`, `related` (3 similar projects), `form` (MessageForm), SEO meta
- **Arabic Copy:** `عن المشروع`, `أهم المميزات`, `التقنيات المستخدمة`, `إيه اللي هتاخده؟`, `اطلب تنفيذ مخصص`
- **Features:**
  - Breadcrumb navigation
  - Main thumbnail + image gallery
  - Full description (`whitespace-pre-line`)
  - Features grid with checkmark icons
  - Tech stack tags
  - Sidebar pricing card (standard + custom)
  - Gumroad / Demo buttons
  - "What's included" checklist
  - **WhatsApp button** with pre-filled message including project title
  - Custom order form section at bottom

#### `pages/about.html`
- **Purpose:** DevGrade story and value proposition.
- **Context:** `total_projects`, SEO meta
- **Arabic Copy:** Full narrative about the founder, the mission, and why students choose DevGrade.

#### `pages/contact.html`
- **Purpose:** General contact page.
- **Context:** `form` (MessageForm), SEO meta
- **Features:**
  - Left column: Email, phone, response time info cards
  - WhatsApp CTA button
  - Right column: `_message_form.html`

#### `pages/faq.html`
- **Purpose:** Frequently asked questions.
- **Features:** 8 accordion items covering purchase, ownership, refunds, custom orders, tech stack, coding knowledge, trial, and delivery time.

---

### Partial Templates (HTMX)

| Template | Purpose | Context |
|----------|---------|---------|
| `_alert.html` | Feedback banner | `message`, `type` |
| `_message_form.html` | Reusable order form | `form`, `project` (optional) |
| `_message_row.html` | Single dashboard row | `msg`, `status_choices` |
| `_messages_table.html` | Full table + pagination | `messages_list`, `status_filter`, `search` |
| `_project_grid.html` | Project cards grid | `projects` |
| `_projects_table.html` | Admin project table | `projects_list`, `query`, `status_filter` |

---

## 5. Admin Panel Guide

### Accessing the Admin Panel

1. Go to `/admin-login/`
2. Enter your staff username and password
3. You will be redirected to `/dashboard/`

> **Note:** The Django Admin at `/admin/` is still accessible but the custom dashboard at `/dashboard/` is the preferred interface for day-to-day management.

### How to Add a New Project (via Dashboard)

1. Navigate to **Dashboard → Add Project** (or `/dashboard/projects/add/`)
2. Follow the 5-step form:
   - **Step 1 — Basic Information:** Enter title, category, and full description.
   - **Step 2 — Pricing & Links:** Set standard price (EGP), custom price (optional), demo URL, and Gumroad link.
   - **Step 3 — Tech Stack & Settings:** Click tech chips to select technologies. Toggle "Featured" and "Published". Set display order.
   - **Step 4 — Media:** Drag and drop the thumbnail and additional screenshots.
   - **Step 5 — Features:** Type each feature and press Enter. They appear as tags.
3. Click **"إنشاء المشروع"** (Create Project).

### How to Manage Custom Orders (Messages)

1. Go to **Dashboard** (`/dashboard/`)
2. Scroll to the **Messages & Orders** table
3. Each row shows:
   - Contact info (name, email, phone)
   - Budget and delivery date
   - **Status dropdown** — change it directly; it saves automatically via HTMX
   - **Kebab menu (⋮)** — View Details or Delete
4. Use the status filter or search box to find specific orders.

### How to Mark a Project as Featured

1. Go to **Dashboard → Projects** (`/dashboard/projects/`)
2. Find the project and click **Edit**
3. In **Step 3 — Tech Stack & Settings**, check the **"مشروع مميز؟"** (Featured?) checkbox
4. Save changes

Featured projects appear in the homepage hero section.

### How to Add Tech Stack, Features, and Screenshots Inline

Tech stack items must be created first:
1. Go to **Django Admin → Tech Stacks → Add**
2. Create entries like "Django", "Tailwind CSS", "PostgreSQL"

Then when adding/editing a project:
- **Tech Stack:** Click chips in Step 3
- **Features:** Type and press Enter in Step 5
- **Screenshots:** Drag images into the dropzone in Step 4

---

## 6. Business Logic

### Standard Purchase Flow

```
Student visits homepage
    ↓
Browses projects → clicks one
    ↓
Project Detail Page
    ↓
Clicks "اشتري النسخة العادية" (Gumroad button)
    ↓
Redirected to Gumroad checkout
    ↓
Student pays → downloads ZIP instantly
```

**Behind the scenes:**
- The `gumroad_standard_url` field on `Project` stores the Gumroad product link.
- If Gumroad is not used, the admin can send the file manually via WhatsApp after receiving InstaPay/Vodafone Cash proof.

### Custom Order Flow

```
Student visits project page (or contact page)
    ↓
Clicks "اطلب تنفيذ مخصص" or fills contact form
    ↓
Fills: name, email, phone, project details, budget, delivery date
    ↓
MUST check "أنا على وعي أن المشروع لن يكلف أقل من ... جنيه"
    ↓
Submits form → message saved as "unread"
    ↓
Admin sees it on Dashboard
    ↓
Admin changes status → contacts student on WhatsApp
    ↓
Student pays via InstaPay / Vodafone Cash
    ↓
Admin delivers customized project files
```

**Behind the scenes:**
- `Message` model stores every inquiry.
- `status` tracks the lifecycle: `unread` → `opened` → `accepted` / `refused` / `contacted`
- The `is_aware_min_budget` checkbox acts as a qualification gate.

### Pricing Structure

| Field | Meaning | Display |
|-------|---------|---------|
| `standard_price` | Price for instant download version | Shown with "EGP" suffix on cards and detail page |
| `custom_price` | Price for bespoke development | Only shown if set; triggers custom order section |

All prices are stored and displayed in **EGP**.

### SEO Keywords

SEO is handled per-page via context variables:
- `page_title` — `<title>` tag and Open Graph title
- `meta_description` — Meta description and OG description
- `meta_keywords` — Meta keywords tag
- `canonical_url` — Canonical link tag

The `site_config` context processor provides default values for all pages. Individual views can override them.

A `sitemap.xml` is auto-generated with:
- All published projects (`ProjectSitemap`)
- All categories (`CategorySitemap`)
- Static views: home, about, faq, contact (`StaticViewSitemap`)

---

## 7. Deployment Guide

### Prerequisites

- VPS with Ubuntu 22.04+
- Python 3.11+
- Nginx
- PostgreSQL (recommended for production)
- Domain or subdomain pointed to your server

### Environment Variables

Before deploying, create a `.env` file or export these variables:

```bash
export DJANGO_SETTINGS_MODULE=devgrade.settings
export SECRET_KEY='your-very-long-random-secret-key-here'
export DEBUG=False
export ALLOWED_HOSTS='devgrade.savekiteg.com,www.devgrade.savekiteg.com'
```

Then modify `settings.py` to read from environment:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-devgrade-change-this-in-production-please')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')
```

### Database Setup (PostgreSQL)

```bash
sudo -u postgres psql
CREATE DATABASE devgrade;
CREATE USER devgrade_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE devgrade TO devgrade_user;
\q
```

Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'devgrade',
        'USER': 'devgrade_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Static & Media Files

```python
# settings.py
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Run:
```bash
python manage.py collectstatic
```

### Gunicorn Setup

Create a systemd service file at `/etc/systemd/system/devgrade.service`:

```ini
[Unit]
Description=DevGrade Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/devgrade
ExecStart=/var/www/devgrade/venv/bin/gunicorn devgrade.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable devgrade
sudo systemctl start devgrade
```

### Nginx Configuration

Create `/etc/nginx/sites-available/devgrade`:

```nginx
server {
    listen 80;
    server_name devgrade.savekiteg.com www.devgrade.savekiteg.com;

    location /static/ {
        alias /var/www/devgrade/staticfiles/;
    }

    location /media/ {
        alias /var/www/devgrade/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/devgrade /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d devgrade.savekiteg.com -d www.devgrade.savekiteg.com
```

### Post-Deployment Checklist

- [ ] Change `SECRET_KEY` to a cryptographically secure random string
- [ ] Set `DEBUG = False`
- [ ] Restrict `ALLOWED_HOSTS` to your domain only
- [ ] Switch from SQLite to PostgreSQL
- [ ] Run `python manage.py migrate`
- [ ] Run `python manage.py collectstatic`
- [ ] Create a superuser: `python manage.py createsuperuser`
- [ ] Configure `SiteConfig` via Django Admin (email, phone, analytics)
- [ ] Set up backups for `media/` and the database

---

## 8. How to Add a New Project (Step by Step for Non-Technical Admin)

### Before You Start

Make sure you have:
- Project thumbnail image (PNG/JPG, ~1200x800px)
- 3–5 screenshot images for the gallery
- Project title in Arabic
- Full description written out
- Price in EGP (standard and custom if applicable)
- Gumroad product URL (if selling via Gumroad)
- Demo URL (optional but recommended)

### Step-by-Step

**Step 1: Log in**
1. Go to `https://devgrade.savekiteg.com/admin-login/`
2. Enter your username and password
3. You will see the Dashboard

**Step 2: Start Adding**
1. Click the green **"Add Project"** button on the dashboard
2. OR go to `/dashboard/projects/add/`

**Step 3: Fill Basic Information**
- **اسم المشروع** — Type the project name (e.g., `نظام إدارة مكتبة جامعية`)
- **الرابط المختصر** — Leave empty. It will be auto-generated.
- **التصنيف** — Select a category from the dropdown (create one first if needed)
- **الوصف الكامل** — Paste the full project description. Include features, tech stack, and who it's for.

**Step 4: Set Pricing & Links**
- **السعر الأساسي** — Enter the standard price (e.g., `1500`)
- **السعر المخصص** — Enter custom build price, or leave empty if not offering custom
- **رابط العرض التجريبي** — Paste demo link
- **رابط Gumroad** — Paste Gumroad checkout link

**Step 5: Choose Tech Stack & Settings**
- Click the green **chips** to select technologies used (Django, Tailwind, etc.)
- Check **"مشروع مميز؟"** if you want it on the homepage
- Check **"منشور؟"** to make it visible to visitors
- **الترتيب** — Leave as `0` unless you want manual ordering

**Step 6: Upload Images**
- Drag your **thumbnail** image into the first dropzone
- Drag your **screenshots** into the second dropzone (multiple allowed)
- You will see previews immediately

**Step 7: Add Features**
- In the features box, type one feature and press **Enter**
- Examples:
  - `تسجيل دخول وخروج للطلاب`
  - `لوحة تحكم للأدمن`
  - `تقرير PDF للكتب المستعارة`
- Keep adding until all features are listed

**Step 8: Save**
1. Click **"إنشاء المشروع"** (the green button at the bottom)
2. You will be redirected back to the projects list
3. Visit the project page on the site to verify it looks correct

### Troubleshooting

- **Images not showing?** Make sure `MEDIA_URL` and `MEDIA_ROOT` are configured, and Nginx serves `/media/`.
- **Project not on homepage?** Check that `is_featured = True` and `is_published = True`.
- **Slug looks weird?** You can edit the slug field manually if the auto-generated one is not ideal.

---

## 9. Future Features to Add

> _This section is reserved for upcoming enhancements. Fill in as the product evolves._

| Feature | Priority | Notes |
|---------|----------|-------|
| | | |
| | | |
| | | |

### Suggested Enhancements

- [ ] **Payment Integration:** Direct InstaPay or Vodafone Cash API integration instead of manual confirmation
- [ ] **Student Reviews:** Allow buyers to leave ratings and testimonials
- [ ] **Project Bundles:** Discounted packages of multiple related projects
- [ ] **Live Chat Widget:** WhatsApp Business API or Tawk.to integration
- [ ] **Email Notifications:** Automated emails when a new custom order is received
- [ ] **Analytics Dashboard:** Charts showing sales, traffic, and conversion rates
- [ ] **Multi-language Support:** English version of the site for international students
- [ ] **Affiliate Program:** Referral links for students to earn commissions
- [ ] **Project Demo Videos:** Embed YouTube walkthroughs on detail pages
- [ ] **Automatic Invoicing:** Generate PDF invoices for each purchase
- [ ] **Dark Mode:** Toggle between light and dark themes
- [ ] **Search Autocomplete:** AJAX-powered search suggestions

---

## Appendix A: Known Issues & Notes

1. **`is_aware_min_budget` inconsistency:** The model label mentions **5000 EGP**, but the contact form template displays **3000 EGP**. Align these to one value.
2. **Empty test suite:** `projects/tests.py` has no tests. Add unit tests for forms, views, and models.
3. **Hardcoded SECRET_KEY:** The development key is prefixed `django-insecure-`. Must be changed in production.
4. **`DEBUG = True` in settings:** Should be `False` in production.
5. **`ALLOWED_HOSTS = ['*']`:** Restrict to actual domain in production.
6. **No database backups configured:** Set up automated PostgreSQL dumps.
7. **Category edit uses POST with inline form:** Consider switching to HTMX for smoother UX.

---

## Appendix B: Quick Reference Commands

```bash
# Development
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
python manage.py shell

# Production (Gunicorn)
gunicorn devgrade.wsgi:application --bind 0.0.0.0:8000 --workers 3

# Database backup (PostgreSQL)
pg_dump -U devgrade_user -d devgrade > backup_$(date +%F).sql

# Restore database
psql -U devgrade_user -d devgrade < backup_2026-05-01.sql
```

---

*End of Documentation*
