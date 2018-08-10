
# backend development

## submissions of web articles/posts

We need to create APIs on a Flask backend to download and parse articles submitted from simple web URLs.

- the APIs download the content of a post/article from there
- the downloaded content is HTML-parsed 
    + you can add your Python library of preference there
    + get authors/date and any interesting metadata, the more the better
        - OPTIONALS (gets you more points):
            * source (facebook, twitter, newyorktimes, e.g.)
            * tags (or topics) may be extracted from most used words if not available
            * location (domain IP provenance)
- the metadata and the text of the article is stored in db
    + mongodb collection
- duplicates are not allowed
    + of course not same URL
    + same title or very close to it
- similar content should be flagged
    + e.g. above 80% of similarity with existing

Also:
- No authentication is required at the moment
    + it would be easily added with minor changes through the framework
- No asynchronous/background task are required in this exercise
    + it's ok if it's slow in checking duplicates
    + for future reference: `RAPyDo` integrates `celery`

