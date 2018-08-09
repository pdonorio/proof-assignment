
# Submissions of web articles/posts

The task is to create:

- backend APIs to submit a URL
    + the APIs download the content of a post/article from there
    + the downloaded content is HTML parsed to get authors/dates/tags and any interesting metadata
    + no duplicates is allowed (same URL, same title)
    + the metadata and the text of the article is stored in a mongodb collection
- frontend react UI views
    + to submit URL to the APIs above
    + to list the articles submitted
    + to show one single article content

Also:
- Unittests are required.
- No authentication is required.
- The task can be developed in any language.
- Using at least two containers (frontend and backend) is a plus.
- Instructions to install and run the projects are required.
