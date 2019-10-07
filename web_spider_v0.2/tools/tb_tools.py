from common import md5_encrypt
import time


def get_sign(m_h5_tk, app_key, data):
    m_h5_tk = m_h5_tk.split('_')[0]
    t = int(time.time() * 1000)
    start_sign = str(m_h5_tk) + str('&') + str(t) + str('&') + str(app_key) + str('&') + data
    sign = md5_encrypt(start_sign)
    return sign, t
