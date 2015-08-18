# myblt-website
My blt provides a simple platform for general file upload. It features a public and private mode.
 
A [cli client](https://github.com/myblt/myblt-client) can be used to upload files or directly via the website.
 
### Public mode
Everyone can upload and retreive files.
 
### Private mode
Everyone can see files but only members can upload new files.

## Hacking on myblt

### Requirements
* Python 3
* pip (Python3)
* bower
* nginx
* virtualenv (recommended)

`git clone git@github.com:myblt/myblt-website.git` 

`cd myblt-website`

##### Create a virtualenv

`virtualenv env`

##### Active the virtualenv in the current shell

`. env/bin/activate`

`pip install -r requirements.txt`

`bower install`

`cp deploy/nginx/myb.lt /etc/nginx/sites-enabled/`

##### Change the config file `/etc/nginx/sites-enabled/myb.lt` to your repo's `public/` folder

`sudo systemctl reload nginx`

##### "Temporary"

`sudo sh -c "echo '127.0.0.1 myb.lt a.myb.lt' >> /etc/hosts"`

##### Start the application

`python myblt.py`

##### Profit !

`firefox http://myb.lt`
