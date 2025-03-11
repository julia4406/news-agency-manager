# Setup Guide

Follow these steps to set up and run this project on your local machine.

## Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Virtualenv (optional but recommended)

## 1. Clone the repository

Clone this repository to your local machine using the following command:

```
git clone https://github.com/julia4406/news-agency-manager
cd news-agency-manager
```

## 2. Set up a virtual environment (optional)

It's recommended to use a virtual environment to manage dependencies. To create a virtual environment:

```
python -m venv .venv
```

Activate the virtual environment:

- On Windows:

```.venv\Scripts\activate```

- On macOS/Linux:

```source .venv/bin/activate```

## 3. Install the dependencies

Install the required Python packages from requirements.txt:

```pip install -r requirements.txt```

## 4. Set up environment variables

Make sure to create a `.env` file in the root of the project with the necessary environment variables. You can use the .env.sample file as a reference. For example:

- .env
```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-database-url
```

## 5. Run database migrations

Apply the database migrations to set up your database schema:

```python manage.py migrate```

## 6. Create a superuser (optional)

If you need to create a superuser to access the Django admin panel, run:

```python manage.py createsuperuser```

Follow the prompts to create the superuser account.

## 7. Run the development server

Start the development server:

```python manage.py runserver```

The application will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000)

## 8. Access the admin panel (optional)

You can log into the Django admin panel at:

[http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

Use the superuser credentials you created earlier to log in.

---
That's it! You should now have the project running locally. \
Have fun! Enjoy working on it.
