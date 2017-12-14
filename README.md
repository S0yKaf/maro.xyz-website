# maro.xyz-website
My blt provides a simple platform for general file upload. It features a public and private mode.

A [cli client](https://github.com/kiniamaro/maro.xyz-website) can be used to upload files or directly via the website.

### Public mode
Everyone can upload and retreive files.

### Private mode
Everyone can see files but only members can upload new files.

## Hacking on maro.xyz

### Requirements
* Python 3
* pip (Python3)
* bower
* nginx
* virtualenv (recommended)
* imagemagick

`git clone git@github.com:maro.xyz/maro.xyz-website.git`

`cd maro.xyz-website`

##### Create a virtualenv

`virtualenv env`

##### Active the virtualenv in the current shell

`. env/bin/activate`

`pip install -r requirements.txt`

`bower install`

`cp deploy/nginx/maro.dev /etc/nginx/sites-enabled/`

##### Change the config file `/etc/nginx/sites-enabled/myb.lt` to your repo's `public/` folder

`sudo systemctl reload nginx`

##### "Temporary"

`sudo sh -c "echo '127.0.0.1 test.maro.xyz api-test.maro.xyz' >> /etc/hosts"`

#### Change the base href in index.html for development
`<base href="http://test.maro.xyz/">`

##### Start the application

`python myblt.py`

##### Profit !

`firefox http://test.maro.xyz`
