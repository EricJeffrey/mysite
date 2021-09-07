
# What this is 

Backend source code of mysite

## Main function:

- pastor
- file-transfer

## Interfaces

- pastor
  - paste,POST,{content:text-to-paste}
  - getall
- file-transfer
  - upload,POST,multipart/form-data
  - listall
  - download?name

Response format: {code: 1/0, content: response-content}

## pip list

- flask
- uwsgi
- werkzeug
- urllib
