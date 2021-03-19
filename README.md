# DCSS Confusion Analysis

This repository contains an example websocket service that implements the interactions described in [DCSS Remote AI Service Integration ](https://github.com/mit-teaching-systems-lab/dcss-remote-ai-integration). This demonstration also illustrates the use of the `X-DCSS-MEDIA-REQUEST-TOKEN` header to request media the DCSS server.


## Directory


### `server.js`

The core socket service. This coordinates request, analysis and response. This service will request media from the DCSS server by using the `auth.token` it receives upon client connection to authenticate itself. 

### `confusion.py`

This is a placeholder program that consumes the `token` and `url`, and saves the file locally. 

**ALL FILES SAVED ARE LOST ON EVERY DEPLOYMENT**


## Developer Token

Use `8070cb2467d22a15dabafd5f5128cacc04af86f1` for development. This token will not work on production.


## Creating a Teacher Moments Agent

1. Navigate to [Admin/Agents](https://teachermoments.mit.edu/admin/agents) (assuming your user has sufficient privileges to access this section of the site.).
2. Click **Create a new agent**
3. Enter a name for your new agent
4. Enter a brief description
5. Enter the endpoint: `ws://dcss-caa-production.herokuapp.com`
6. Select one or more Interactions that you want to send to the agent
6. Click "Save"

