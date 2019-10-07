import re
import hashlib

def get_regex(regex, text, num):  # 获取对应的正则
    """
    @函数名：正则表达式匹配(匹配一个)
    @功能: 正则匹配，输出指定组的匹配结果
    """

    try:
        result = re.search(regex, text).group(num).strip()
    except:
        result = ''

    return result


def field_mapping(mapping_dict, src, dst):
    """
    @函数名：field_mapping
    @功能: 对源和目的字典进行字段对应，映射关系在mapping_dict中
    """

    for key in mapping_dict:
        if mapping_dict[key] in src.keys():
            dst[key] = src[mapping_dict[key]]

    return


def md5_encrypt(start_sign):
    hl = hashlib.md5()
    hl.update(start_sign.encode(encoding='utf-8'))
    return hl.hexdigest()


