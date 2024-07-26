
# MovieVerse API
MovieVerse is an API built using **Django Rest Framework**. It offers a wide range of features, including movie and series listings, platform details with available movies, detailed movie descriptions, and category-based movie search. Users can write and view multiple reviews for movies and series. The API also incorporates advanced features such as **permissions, throttling, filtering, ordering, searching, and pagination**. For secure access, it uses **token-based authentication** with automatic token deletion upon logout. Basic test cases are available and can be tested using the Postman app.

## Features

- Access a comprehensive list of movies and series.
- View platforms with available movies and series.
- Get detailed descriptions of movies and series.
- Find movies and series based on their category.
- Write and view multiple reviews for movies and series.
- Ensure secure access control for various API endpoints.
- Manage the rate of API requests to prevent abuse.
- Apply filters, order results, and search within the API for more refined data retrieval.
- Efficiently handle large sets of data by paginating results.
- Use token-based authentication to secure API endpoints.
- Automatically delete tokens after logout for enhanced security.
- Basic test cases provided for various API endpoints.
- Testable via the Postman app.




## Installation

1. Clone the repository:

```bash
  https://github.com/devanshptl/MovieVerse---API.git
```


2. Create a virtual environment (optional but recommended):
```bash
 python -m venv venv
```
3. Activate the virtual environment:
  * On Windows:
  ```bash
  venv\Scripts\activate
```
* On macOS and Linux:
```bash
source venv/bin/activate

```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Apply migrations:
```bash
python manage.py migrate
```
6. Run the development server:
```bash
python manage.py runserver
```

    
## API Endpoints

1. Admin Access

```http
  http://127.0.0.1:8000/admin/
```

2. Authentication

- Registration
```http
  POST /accounts/signup/
```
- Login 
```http
  POST /accounts/login/
```
- Logout
```http
  POST /accounts/logout/
```

3. Streaming Platforms
 
 - Create Element & Access List
```http
  GET /watch/platform/
```
- Access, Update & Destroy Individual Element

```http
  GET /watch/platform/<int:streamplatform_id>/
```

4. Watch List
- Create & Access List
```http
  GET /watch/list/
```
- Access, Update & Destroy Individual Element
```http
  GET /watch/list/<int:movie_id>/
```
- Search by Category

```http
  GET /watch/list/<str:category_name>/
```

5. Reviews

- Create Review For Specific Movie 

```http
  POST /watch/<int:watch_id>/createreview/
```

- List Of All Reviews For Specific Movie
```http
  GET /watch/list/<int:watch_id>/review/
```

- Access, Update & Destroy Individual Review

```http
  GET /watch/list/review/<int:watch_id>/
```

6. User Review
```http
  GET /watch/user/<str:username>/
```


## Contributing
We welcome any and all contributions! Here are some ways you can get started:
1. Report bugs: If you encounter any bugs, please let us know. Open up an issue and let us know the problem.
2. Contribute code: If you are a developer and want to contribute, follow the instructions below to get started!
3. Suggestions: If you don't want to code but have some awesome ideas, open up an issue explaining some updates or imporvements you would like to see!
4. Documentation: If you see the need for some additional documentation, feel free to add some!






