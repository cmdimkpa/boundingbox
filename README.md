# boundingbox
Welcome to the boundingbox project.

To start a new session, visit: http://app.tr1pp.me:3024/boundingbox/api/serve_image?image=bottles&index=0

Then make sure to click the `RESET` button to clear the session. If you want to load the next image, use the `scroll` buttons: `>` and `<` to navigate.

There are only two (2) images available presently: `bottles` & `xmen`.

# Design

The project is powered by `web_service.py` which is the `back end`, with `front end` interaction managed by `bbdisplay.html`.

## Front End: BBDisplay.html

The front end is based on a `Slideshow` component from `W3 Schools` and uses some custom `JavaScript` functions for control. `jQuery` is used for making `API calls` to the backend.

### Drawing Bounding Boxes

To draw a bounding box, the system listens for a sequence of `4 clicks`. The locations of the 4 clicks are then transmitted to the `image editing` component of the backend `webservice`. The component then proceeds to draw the bounding box on a copy of the image at the server and returns the view to be displayed by the front end. The edits are `cummulative`, and each respective box is collaged with the previous set. Although automatic regression is not supported, you can manually scroll back to previous states by adjusting the `index` parameter in the browser URL.

### Reseting your Session and changing the image

Click the `Reset` button at any time to reset your session. This will delete all your edits at the backend from both the server and the database, and start you from scratch.

You can also change the image by scrolling with `>` or `<`.

## Back End: Web_Service.py

The backend is a `Flask` API that is productionized with `Eventlet` via `Flask_SocketIO` extension. 

It is hosted on a private server at `http://app.tr1pp.me:3024`, which is an `AWS EC2 Instance`.

### Data Storage

Two types of data are stored:

1. `edit_counts` of base images. This is stored directly `In memory` and indirectly via the `database`.
2. Current positions of all edits for a particular base image. This is stored in the `localdb`, a serialized `JSON` object.

We also use the array count of current positions of a base image to know the edit count (indirect linkage mentioned above). We have `getter` and `setter` functions for our database which we use as needed.

### Image Editing

We use the `Python Image Library (PIL)` via the `Pillow` project, for editing the images (drawing bounding boxes) via `ImageDraw`.

We have a function `add_bounding_box_to_image` that handles this. The only siginificant data transformation here is the conversion of points from the way they were originally sent via the API to the form usable by this function, and this happens using `make_points(coordset)`.

We also use a `rolling edit` scheme that supports `collaging` while also allowing you to preserve individual states of the image. 

#### Possible Bug
We noticed some `skewing` in the bounding box positions and size relative to what was actually clicked. This will be resolved in future versions of the application.

### Use of Nonces

We use `nonces` in naming images and URLs to force the browser to load from server, because we initially noticed the server was caching images a lot, which would have been disastrous for the application.


### Endpoints: New Box

This endpoint writes a new bounding box to the base image and returns the updated URL, which is then loaded by the browser from the front end.

#### closing the box

The system adds the first position in the position array to the end of the array in order to close the bounding box.

### Endpoints: New Session

This endpoint clears all image edits and resets the image database entry and image edit count.

### Endpoints: Serve Image

The endpoint returns the images requested from the server.
