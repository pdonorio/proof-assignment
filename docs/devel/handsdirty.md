
# Finally start writing some code

Sorry for this long introduction!
We hope now you're all set and ready to write some code.

## add libraries to the backend image

Downloading and parsing and article in Python might require some extra package to be installed. If after some research or from you experience you have one or more then go edit [this `requirements` file](https://github.com/pdonorio/proof-assignment/tree/master/builds/backend/requirements.txt) and add as many as you want. 

After saving your modifications you have to make sure you rebuild the backend container image and restart it. This is possible with the following commands:
```bash
rapydo --services backend build
rapydo --services backend restart
```

Then to quickly check your current list of python packages:
```bash
rapydo shell backend
pip3 freeze | grep -i mypackage

# or try to use it
ipython
[1]: import mypackage
```


## edit the main class code

Currently there is only one custom endpoint in the flask server.
It's `/api/articles` and we configured it to have `GET` and `POST` method enabled in our current [swagger configuration](https://github.com/pdonorio/proof-assignment/tree/master/projects/proof/backend/swagger).

The code for this endpoint is a class `Articles` expected to be located in the file `projects/proof/backend/apis/article.py`.

You'll find an example for `get` and `post` method there, please have a look and read the comments to start some playground.


## call from command line

And finally to test the current code or any code you add there, you start the flask server inside the backend container with:
```bash
restapi launch
```

From another terminal you can then use the `httpie` python library, which was installed together with the controller, so you can do:

```bash
$ http GET localhost:8080/api/articles

HTTP/1.0 200 OK
Content-Length: 186
Content-Type: application/json
Date: Fri, 10 Aug 2018 09:37:51 GMT
Server: Werkzeug/0.14.1 Python/3.6.5

{
    "Meta": {
        "data_type": "<class 'str'>",
        "elements": 1,
        "errors": 0,
        "status": 200
    },
    "Response": {
        "data": "To be implemented",
        "errors": null
    }
}
```

As you can see: 
- the response is wrapped into a standard format
- there is no authentication needed
- it's quite easy to quickly make changes and test

For more informations on what you can do with the `http` binary installed, see the [relative documentation](https://httpie.org/doc#examples).

Have fun!

