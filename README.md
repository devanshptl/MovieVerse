# MovieVerse API

MovieVerse is an API built using **Django Rest Framework (DRF)**, offering a range of features such as movie and series listings, detailed descriptions, and more. Advanced functionalities like filtering, ordering, pagination, and recommendations enhance the user experience. The API utilizes **token-based authentication** for secure access with automatic token deletion on logout. The API also integrates **scikit-learn** and **pandas** for data processing, analysis, and building machine learning models.

## Features

- **Movie and Series Listings**: View detailed lists of movies and series, categorized by genre and tags.
- **Platform Details**: Shows platform-specific content with availability information.
- **Detailed Movie Descriptions**: Access comprehensive descriptions, including cast, reviews, and more.
- **Category-Based Movie Search**: Filter movies based on genre or other predefined categories.
- **User Reviews**: Write and view multiple reviews on movies and series.
  
## Advanced Features

- **Recommendation System**: 
    - Suggests **5 movies or series** based on the tags from reviews that the user has liked (like=True). 
    - **Ranking**: Recommendations are ranked by the number of matching tags.
    - **Data Science Integration**: Using **scikit-learn** to implement recommendation algorithms like **TF-IDF** and **cosine similarity** for accurate movie suggestions.
    - **Pandas** for handling and analyzing large datasets, providing real-time recommendations based on user behavior.

- **Liked Content**: Users can view a list of content they have liked, with detailed statistics on their interactions.

- **Statistics API**:
    - Provides insights for admins using **pandas** for aggregating and analyzing user-generated content.
    - Generates reports on average ratings, most popular content, and total reviews per movie/show.
    - Leverages **scikit-learn** for predictive analysis of future trends based on historical data.

- **Trending API**: 
    - Allows users to find which shows are currently trending, using **data analysis** techniques to identify popular movies based on user ratings, views, and likes.

- **Follow Platforms**: 
    - Users can follow different platforms and receive notifications when new content is added. 
    - **Data-driven notifications** are sent based on user preferences and the platforms they follow.


## Security and Performance

- **Permissions and Throttling**: Ensures that only authorized users can access certain features, with throttling implemented to control the rate of requests.
- **Filtering, Ordering, and Pagination**: Enhanced usability with support for filtering movies by genre, sorting by rating or release date, and paginating results for large datasets.

## Test Cases

- Basic test cases are included to ensure the API works as expected, and these can be tested using the **Postman** app.


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

## API Setup

- **Find All URLs**: You can find all the available API endpoints in the `urls.py` file.

## Contributing

We welcome any and all contributions! Here are some ways you can get started:

1. **Report bugs**: If you encounter any bugs, please let us know. Open up an issue and let us know the problem.
2. **Contribute code**: If you are a developer and want to contribute, follow the instructions below to get started!
3. **Suggestions**: If you don't want to code but have some awesome ideas, open up an issue explaining some updates or improvements you would like to see!
4. **Documentation**: If you see the need for some additional documentation, feel free to add some!
