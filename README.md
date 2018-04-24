# Quip Application
Application built using [Quip Automation API](https://quip.com/api/).
* [Get a Personal Automatoin API Access Token](https://quip.com/api/personal-token)

## Merger
This application helps user to merge documents present inside a folder.
1. User is provided list of folders, that are accessible to it.
2. Based on user choice of folder all the threads inside the folder are merged.
3. User needs to provide folder (from already provided choice of folders) to keep the Merged file.
4. After providing a title for the merged file application merges all the threads.

### Running

```
python merger.py "<access_token>"
```

You can obtain a personal access token via [quip.com/api/personal-token](https://quip.com/api/personal-token).
