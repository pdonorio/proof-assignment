
# Finally start writing some code

Sorry for this long introduction!
We hope now you're all set and ready to write some code.

## neutrino scaffold

Your work for frontend development basically requires to edit the content 
inside the folder `projects/proof/frontend`.

The code base was created using [neutrino](https://neutrinojs.org/) (from mozilla).

## use containers

After starting up the project with `rapydo start`, you will need to bring up the flask server debug instance:

```bash
rapydo shell backend --command 'restapi launch'
```

Now you can go inside the "react" container, install "node modules" and start the neutrino build:

```bash
rapydo shell react
# NOTE: install will require a few minutes the first time
yarn install && yarn start
```

After this you should be able to see the demo page 
opening with your browser the location [http://localhost:5000](http://localhost:5000).

Now you can start implementing/editing the code, the server will reload automatically and lint your content.


