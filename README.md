# urlsToSwagger-007
Converts a List Of URLS to Swagger 2.0 Format.

## Usage
> urlsToSwagger-007 -i urls.txt -t "myProject" -u "8.8.8.8" -p "https" -o swagger.json

## Flags
```
-i --input INPUTFILE     --> File containing the list of URLs along with its HttpMethod
-t --title TITLE         --> Title of the swagger
-u --host                --> HostName Without http/https
-p --protocol PROTOCOL   --> Protocol/Scheme [http or https]
-o --output FILENAME     --> Output Filename
-v, --verbose            --> Disable Vervose mode (Don't Print on Terminal)
```

## Examples of different Formats
```
1)Basic --> GET:/api/v2/test
> urlsToSwagger-007 -i urls.txt -t "myProject" -u "8.8.8.8" -p "https" -o swagger.json

2)Urls With Protocol --> GET:https://test.com/api/v2/test
> urlsToSwagger-007 -i urls.txt -t "myProject" -u "8.8.8.8" -p "https" -o swagger.json -f

3)With Different Delimiter --> GET https://test.com/api/v2/test
> urlsToSwagger-007 -i urls.txt -t "myProject" -u "8.8.8.8" -p "https" -d " " -o swagger.json

4)For any other format modify the getAPIList() method accordingly.
```
