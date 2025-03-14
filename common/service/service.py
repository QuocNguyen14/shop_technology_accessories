import re


def change_to_slug(slug):
    # Đổi ký tự có dấu thành không dấu
    slug = re.sub('[áàảạãăắằẳẵặâấầẩẫậ]', 'a', slug, flags=re.IGNORECASE)
    slug = re.sub('[éèẻẽẹêếềểễệ]', 'e', slug, flags=re.IGNORECASE)
    slug = re.sub('[íìỉĩị]', 'i', slug, flags=re.IGNORECASE)
    slug = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', slug, flags=re.IGNORECASE)
    slug = re.sub('[úùủũụưứừửữự]', 'u', slug, flags=re.IGNORECASE)
    slug = re.sub('[ýỳỷỹỵ]', 'y', slug, flags=re.IGNORECASE)
    slug = re.sub('đ', 'd', slug, flags=re.IGNORECASE)

    slug = slug.lower()

    # Xóa các ký tự đặt biệt
    slug = re.sub(r'[\`|\~|\!|\@|\#|\||\$|\%|\^|\&|\*|\(|\)|\+|\=|\,|\.|\/|\?|\>|\<|\'|\"|\:|\;|_]',
                  '', slug, flags=re.IGNORECASE)

    # Đổi khoảng trắng thành ký tự gạch ngang
    slug = slug.replace(' ', '-')

    # Đổi nhiều ký tự gạch ngang liên tiếp thành 1 ký tự gạch ngang
    # Phòng trường hợp người nhập vào quá nhiều ký tự trắng
    slug = re.sub(r'-{2,}', '-', slug)

    # Xóa các ký tự gạch ngang ở đầu và cuối
    slug = '@' + slug + '@'
    slug = re.sub(r'\@\-|\-\@|\@', '', slug)

    return slug
