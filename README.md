# Best Cars — Full Stack Developer Capstone

An educational car dealership review application based on the IBM Developer Skills Network starter. Prepared by Sabina Zhumagaliyeva with AI coding assistance. Original starter attribution is retained. The provided dealership, review and car records are course demonstration data, not verified business listings.

## Implemented features

- React catalogue with state filter, dealer details, sentiment labels, registration, login/logout, and authenticated review creation.
- Django gateway, CSRF-protected session authentication, validated car models, and Django admin.
- Express/Mongoose API with non-destructive seed data, unique IDs, atomic review numbering, and an optional internal write key.
- Flask/NLTK VADER sentiment service using the bundled lexicon.
- Repeatable container builds and GitHub Actions CI that checks frontend compilation, authentication behavior, and actual MongoDB/sentiment integration.

## Run locally

Use Python 3.12, Node.js 22 and MongoDB. In `server/frontend`, run `npm ci && npm run build`. In `server`, create a Python virtual environment and install `requirements.txt`, then run `python manage.py migrate` and `python manage.py seed_cars`.

Start the services in separate terminals:

```sh
# MongoDB must already be running; choose its URI for your environment.
cd server/database
npm ci
MONGODB_URI=mongodb://127.0.0.1:27017/dealershipsDB node app.js
# From server/:
python djangoapp/microservices/app.py
python manage.py runserver
```

Set `backend_url` (default http://127.0.0.1:3030) and `sentiment_analyzer_url` (default http://127.0.0.1:5050) in the Django environment. Create an admin with `python manage.py createsuperuser`. Test with `python manage.py test djangoapp` and `python scripts/integration_check.py`.

## Deployment configuration

Each service has a Dockerfile. The main Dockerfile is in `server/` and builds React before packaging Django. Configure `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0`, allowed hosts, trusted CSRF origins, service URLs, and `INTERNAL_API_KEY` through private environment/cluster secrets. Do not commit passwords or database files. The demo uses SQLite for accounts and car models; a durable deployment requires persistent storage or an external relational database. MongoDB storage also needs persistence. Sentiment analysis is heuristic and is not guaranteed to reflect a reviewer's intent.

Static contact addresses use reserved `.example` domains and do not receive mail. The About page describes illustrative team roles, not real staff. Cloud availability and CI success should be checked using their actual links; local checks alone do not establish deployment.
