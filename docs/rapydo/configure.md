
# project configuration

To verify the current configuration project just edit the file:
```
projects/proof/project_configuration.yaml
```

<!--
To override the SMTP variables to add your gmail account so that registration email could be sent you can adjust your `.projectrc`.
-->
You should only override SMTP variables to add a valid gmail account so that registration email could be sent from the Flask server.

Remember to check Flask logs when registering a new profile to see if that works correctly.

NOTE: to avoid commiting that file with sensitive information from that moment on, you may stop tracking it on git with:
```
git update-index --assume-unchanged projects/proof/project_configuration.yaml
```

