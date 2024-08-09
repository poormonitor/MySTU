info = {
    "id": "学号",
    "name": "姓名",
    "sex": "性别",
    "cls": "班级",
    "party": "政治面貌",
    "people": "民族",
    "religion": "宗教信仰",
    "identity": "身份证号",
    "bank": "银行卡号",
    "phone": "手机",
    "email": "邮箱",
    "qq": "QQ",
    "domitory": "寝室",
    "bed": "床号",
    "contact": "联系人",
    "domicile": "户籍所在地",
    "fcontact1": "家庭联系人1",
    "fcontact1phone": "家庭联系人1电话",
    "fcontact2": "家庭联系人2",
    "fcontact2phone": "家庭联系人2电话",
    "residence": "居住地",
    "memo": "备注",
}


def datetime_to_str(date_time):
    from pytz import timezone

    tz = timezone("Asia/Shanghai")
    utc = timezone("UTC")

    date_time = date_time.replace(tzinfo=utc)
    date_time = date_time.astimezone(tz)

    return date_time.strftime("%Y-%m-%d %H:%M:%S")
