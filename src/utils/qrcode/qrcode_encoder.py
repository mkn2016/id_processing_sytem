from typing import NoReturn, Union
from qrcode import QRCode, constants


# Transcribes data to QRCode
def encode_data_to_file(data_to_encode: Union[dict, str], file_name: str) -> NoReturn:
    """"
    data_to_encode: mapping or string
    file_name: str or string
    return: None
    """
    qr = QRCode(
        version=1,
        error_correction=constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data_to_encode)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.tobytes()
    img.save(file_name)
