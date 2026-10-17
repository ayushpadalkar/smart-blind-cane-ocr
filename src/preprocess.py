import cv2


def load_image(image_path):

    image = cv2.imread(
        str(image_path)
    )

    if image is None:

        raise FileNotFoundError(
            f"Unable to load image: {image_path}"
        )

    return image


def resize_image(
    image,
    width=None,
    height=None
):

    if width is None and height is None:
        return image

    if (
        width is not None
        and height is not None
    ):

        return cv2.resize(
            image,
            (width, height)
        )

    if width is not None:

        ratio = (
            width /
            image.shape[1]
        )

        new_height = int(
            image.shape[0] *
            ratio
        )

        return cv2.resize(
            image,
            (
                width,
                new_height
            )
        )

    ratio = (
        height /
        image.shape[0]
    )

    new_width = int(
        image.shape[1] *
        ratio
    )

    return cv2.resize(
        image,
        (
            new_width,
            height
        )
    )