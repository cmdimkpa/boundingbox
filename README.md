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

## Front End: BBDisplay.html

The front end is based on a `Slideshow` component from `W3 Schools` and uses some custom `JavaScript` functions for control. `jQuery` is used for making `API calls` to the backend.

### Drawing Bounding Boxes

To draw a bounding box, the system listens for a sequence of `4 clicks`. The locations of the 4 clicks are then transmitted to the `image editing` component of the backend `webservice`. The component then proceeds to draw the bounding box on a copy of the image at the server and returns the view to be displayed by the front end. The edits are `cummulative`, and each respective box is collaged with the previous set. Although automatic regression is not supported, you can manually scroll back to previous states by adjusting the `index` parameter in the browser URL.

