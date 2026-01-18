# AI-Powered Current Affairs Platform for UPSC & BPSC

A bilingual (English/Hindi) web application that automatically fetches current affairs news, generates MCQ quizzes using AI, and provides an interactive learning platform for UPSC and BPSC exam preparation.

## 🚀 Features

- **Automated News Scraping**: Fetches latest current affairs from reliable sources
- **AI-Generated MCQs**: Automatically creates UPSC/BPSC style multiple-choice questions from news articles using Google's Gemini API
- **Bilingual Support**: Complete English and Hindi translation for UI and content
- **Interactive Quiz Interface**: Practice MCQs with instant feedback (correct/incorrect highlighting)
- **Modern UI**: Clean, professional design with green/black/gray/white theme
- **Pagination**: Efficient loading with "Load More" functionality
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Admin Dashboard**: Manage news articles, questions, and track quiz performance

## 📋 Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment support (virtualenv)

## 🛠️ Installation & Setup

### Windows Setup

1. **Clone the repository**

   ```powershell
   git clone https://github.com/ShashwatUpadhyay/CurrentAffairsGenerator.git
   cd CurrentAffairsGenerator
   ```

2. **Create and activate virtual environment**

   ```powershell
   python -m venv env
   .\env\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:

   ```
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

   Get your API key from: https://ai.google.dev/

5. **Run migrations**

   ```powershell
   python manage.py migrate
   python manage.py compilemessages
   ```

6. **Create superuser (admin)**

   ```powershell
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```powershell
   python manage.py runserver
   ```

8. **Access the application**
   - Homepage: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/
   - Rosetta (Translation): http://localhost:8000/rosetta/

### Linux / macOS Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/ShashwatUpadhyay/CurrentAffairsGenerator.git
   cd CurrentAffairsGenerator
   ```

2. **Create and activate virtual environment**

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the project root:

   ```
   GEMINI_API_KEY=your_google_gemini_api_key_here
   ```

5. **Run migrations**

   ```bash
   python manage.py migrate
   python manage.py compilemessages
   ```

6. **Create superuser (admin)**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**

   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Homepage: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/
   - Rosetta (Translation): http://localhost:8000/rosetta/

## 📖 Usage

### Fetching News and Generating MCQs

1. **Automatic Method**: Run the master script to fetch news and generate MCQs

   ```bash
   python utils/master.py
   ```

2. **Django Shell Method**:

   ```bash
   python manage.py shell
   ```

   ```python
   from base.models import News

   # Fetch a news article
   news = News.objects.first()

   # Generate MCQs for it
   news.generate_questions()
   ```

3. **Admin Panel**: Add news manually via Django admin at `/admin/`

### Translating Content

- Static UI strings: Visit http://localhost:8000/rosetta/
- News content: Automatically translated when MCQs are generated
- Manual translation: Edit `.po` files in `locale/hi/LC_MESSAGES/`

## 🏗️ Project Structure

```
CurrentAffairsGenerator/
├── base/                      # Main Django app
│   ├── models.py             # News, Question, Option models
│   ├── views.py              # API endpoints and page views
│   ├── serializers.py        # DRF serializers
│   ├── admin.py              # Admin interface customization
│   └── translation.py        # Model translation configuration
├── ca_gen/                    # Django project settings
│   ├── settings.py           # Project configuration
│   └── urls.py               # URL routing
├── utils/                     # Utility scripts
│   ├── scraper.py            # News scraping functionality
│   ├── mcq_generator.py      # AI-powered MCQ generation
│   ├── translator.py         # Translation utilities
│   └── master.py             # Master script for automation
├── static/                    # Static files (CSS, JS, images)
│   ├── css/
│   │   ├── style.css         # Homepage styles
│   │   └── quiz.css          # Quiz page styles
│   ├── js/
│   │   ├── main.js           # Homepage functionality
│   │   └── quiz.js           # Quiz functionality
│   └── images/
├── templates/                 # HTML templates
│   ├── home.html             # Homepage
│   └── mcq.html              # Quiz page
├── locale/                    # Translation files
│   └── hi/                   # Hindi translations
├── media/                     # User-uploaded files
├── db.sqlite3                # SQLite database
├── manage.py                 # Django management script
└── requirements.txt          # Python dependencies
```

## 🔑 Key Technologies

- **Backend**: Django 6.0, Django REST Framework
- **AI**: Google Gemini API (gemini-2.5-flash)
- **Translation**: django-modeltranslation, deep-translator
- **Frontend**: Vanilla JavaScript, CSS
- **Database**: SQLite (development), PostgreSQL (recommended for production)
- **Web Scraping**: BeautifulSoup4, Requests

## 📝 API Endpoints

- `GET /news_api/` - Paginated list of news articles
- `GET /news_api/?page=2` - Get specific page
- `GET /questions/<news_uid>/` - Get MCQs for a specific news article
- `GET /mcq/<news_uid>/` - Quiz page for a news article

## 🌐 Translation Workflow

1. Add translatable strings in code:

   ```python
   from django.utils.translation import gettext as _
   message = _("Your text here")
   ```

2. Extract messages:

   ```bash
   python manage.py makemessages -l hi --ignore=env
   ```

3. Translate in `.po` files or use Rosetta

4. Compile messages:

   ```bash
   python manage.py compilemessages
   ```

5. Restart server

## 🎨 Customization

### Change Page Size (Pagination)

Edit `ca_gen/settings.py`:

```python
REST_FRAMEWORK = {
    'PAGE_SIZE': 12,  # Change this value
}
```

### Update Color Theme

Edit `static/css/style.css` and `static/css/quiz.css`:

```css
:root {
  --primary-green: #10b981;
  --dark-green: #059669;
  --black: #000000;
  /* ... modify colors ... */
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Shashwat Upadhyay**

- GitHub: [@ShashwatUpadhyay](https://github.com/ShashwatUpadhyay)

## 🙏 Acknowledgments

- Google Gemini API for AI-powered MCQ generation
- Django community for excellent documentation
- All contributors and users of this platform

## 📞 Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Contact via email (if provided in GitHub profile)

---

**Note**: This is a development setup. For production deployment, configure:

- PostgreSQL database
- Proper static file serving (whitenoise or CDN)
- Environment variable management
- Security settings (DEBUG=False, ALLOWED_HOSTS, etc.)
- HTTPS/SSL certificates
- Caching (Redis/Memcached)
