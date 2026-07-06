"""
parsikit.validators
~~~~~~~~~~~~~~~~~~~
Identity, banking, and telephone format validations for Iranian standards.
"""

from __future__ import annotations
from typing import TypedDict, Literal
import re

_TO_ENGLISH = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


class BankDetails(TypedDict):
    name: str
    code: str


class BillDetails(TypedDict):
    is_valid: bool
    amount_rial: int
    amount_toman: int
    type: str
    type_code: str


class PlateDetails(TypedDict):
    part1: str
    letter: str
    part2: str
    province_code: str
    province: str
    category: str


_CARD_BIN_TO_BANK: dict[str, BankDetails] = {
    "603799": {"name": "بانک ملی ایران", "code": "melli"},
    "589210": {"name": "بانک سپه", "code": "sepah"},
    "627648": {"name": "بانک توسعه صادرات ایران", "code": "tose-saderat"},
    "627961": {"name": "بانک صنعت و معدن", "code": "sanat-o-madan"},
    "603770": {"name": "بانک کشاورزی", "code": "keshavarzi"},
    "628023": {"name": "بانک مسکن", "code": "maskan"},
    "627760": {"name": "پست بانک ایران", "code": "post-bank"},
    "502908": {"name": "بانک توسعه تعاون", "code": "tose-taavon"},
    "627412": {"name": "بانک اقتصاد نوین", "code": "eghtesad-novin"},
    "622106": {"name": "بانک پارسیان", "code": "parsian"},
    "627884": {"name": "بانک پارسیان", "code": "parsian"},
    "639194": {"name": "بانک پارسیان", "code": "parsian"},
    "639346": {"name": "بانک پاسارگاد", "code": "pasargad"},
    "502229": {"name": "بانک پاسارگاد", "code": "pasargad"},
    "627488": {"name": "بانک کارآفرین", "code": "karafarin"},
    "621986": {"name": "بانک سامان", "code": "saman"},
    "639347": {"name": "بانک سینا", "code": "sina"},
    "502806": {"name": "بانک شهر", "code": "shahr"},
    "504706": {"name": "بانک شهر", "code": "shahr"},
    "502938": {"name": "بانک دی", "code": "dey"},
    "603769": {"name": "بانک صادرات ایران", "code": "saderat"},
    "610433": {"name": "بانک ملت", "code": "mellat"},
    "991975": {"name": "بانک ملت", "code": "mellat"},
    "627353": {"name": "بانک تجارت", "code": "tejarat"},
    "585983": {"name": "بانک تجارت", "code": "tejarat"},
    "589463": {"name": "بانک رفاه کارگران", "code": "refah"},
    "636214": {"name": "بانک آینده", "code": "ayandeh"},
    "628157": {"name": "مؤسسه اعتباری توسعه", "code": "tosee"},
    "505416": {"name": "بانک گردشگری", "code": "gardeshgari"},
    "639607": {"name": "بانک سرمایه", "code": "sarmayeh"},
    "504172": {"name": "بانک قرض‌الحسنه رسالت", "code": "resalat"},
    "606373": {"name": "بانک قرض‌الحسنه مهر ایران", "code": "mehr-iran"},
    "606256": {"name": "مؤسسه اعتباری ملل", "code": "melal"},
}

_SHEBA_CODE_TO_BANK: dict[str, BankDetails] = {
    "010": {"name": "بانک مرکزی جمهوری اسلامی ایران", "code": "central-bank"},
    "011": {"name": "بانک صنعت و معدن", "code": "sanat-o-madan"},
    "012": {"name": "بانک ملت", "code": "mellat"},
    "013": {"name": "بانک رفاه کارگران", "code": "refah"},
    "014": {"name": "بانک مسکن", "code": "maskan"},
    "015": {"name": "بانک سپه", "code": "sepah"},
    "016": {"name": "بانک کشاورزی", "code": "keshavarzi"},
    "017": {"name": "بانک ملی ایران", "code": "melli"},
    "018": {"name": "بانک تجارت", "code": "tejarat"},
    "019": {"name": "بانک صادرات ایران", "code": "saderat"},
    "020": {"name": "بانک توسعه صادرات ایران", "code": "tose-saderat"},
    "021": {"name": "پست بانک ایران", "code": "post-bank"},
    "022": {"name": "بانک توسعه تعاون", "code": "tose-taavon"},
    "051": {"name": "مؤسسه اعتباری توسعه", "code": "tosee"},
    "052": {"name": "بانک سپه (قوامین سابق)", "code": "sepah"},
    "053": {"name": "بانک کارآفرین", "code": "karafarin"},
    "054": {"name": "بانک پارسیان", "code": "parsian"},
    "055": {"name": "بانک سامان", "code": "saman"},
    "056": {"name": "بانک پاسارگاد", "code": "pasargad"},
    "057": {"name": "بانک گردشگری", "code": "gardeshgari"},
    "058": {"name": "بانک سرمایه", "code": "sarmayeh"},
    "059": {"name": "بانک سینا", "code": "sina"},
    "060": {"name": "بانک قرض‌الحسنه مهر ایران", "code": "mehr-iran"},
    "061": {"name": "بانک شهر", "code": "shahr"},
    "062": {"name": "بانک آینده", "code": "ayandeh"},
    "063": {"name": "بانک دی", "code": "dey"},
    "064": {"name": "بانک سپه (حکمت سابق)", "code": "sepah"},
    "065": {"name": "مؤسسه اعتباری توسعه صنعت و تجارت", "code": "tosee-sanat-o-tejarat"},
    "066": {"name": "بانک سپه (انصار سابق)", "code": "sepah"},
    "069": {"name": "بانک ایران زمین", "code": "iran-zamin"},
    "070": {"name": "بانک سپه (مهر اقتصاد سابق)", "code": "sepah"},
    "073": {"name": "بانک سپه (کوثر سابق)", "code": "sepah"},
    "075": {"name": "مؤسسه اعتباری ملل", "code": "melal"},
    "078": {"name": "بانک خاورمیانه", "code": "khavarmiyaneh"},
    "079": {"name": "بانک مشترک ایران و ونزوئلا", "code": "iran-venezuela"},
    "080": {"name": "بانک قرض‌الحسنه رسالت", "code": "resalat"},
}

_BILL_TYPES = {
    "1": "آب", "2": "برق", "3": "گاز", "4": "تلفن ثابت",
    "5": "تلفن همراه", "6": "عوارض شهرداری", "7": "سازمان مالیاتی", "8": "جرایم راهنمایی و رانندگی"
}

_PROVINCE_CODES = {
    "11": "تهران", "22": "تهران", "33": "تهران", "44": "تهران", "55": "تهران",
    "66": "تهران", "77": "تهران", "88": "تهران", "99": "تهران", "10": "تهران",
    "20": "تهران", "30": "تهران", "40": "تهران", "50": "تهران", "60": "تهران",
    "90": "تهران",
    "12": "خراسان رضوی", "32": "خراسان رضوی", "42": "خراسان رضوی", "36": "خراسان رضوی", "74": "خراسان رضوی",
    "13": "اصفهان", "23": "اصفهان", "43": "اصفهان", "53": "اصفهان", "67": "اصفهان",
    "14": "خوزستان", "24": "خوزستان", "34": "خوزستان",
    "15": "آذربایجان شرقی", "25": "آذربایجان شرقی", "35": "آذربایجان شرقی",
    "16": "قم",
    "17": "آذربایجان غربی", "27": "آذربایجان غربی", "37": "آذربایجان غربی",
    "18": "همدان", "28": "همدان",
    "19": "کرمانشاه", "29": "کرمانشاه", "39": "کرمانشاه",
    "21": "البرز", "38": "البرز", "68": "البرز", "78": "البرز",
    "26": "خراسان شمالی",
    "31": "لرستان", "41": "لرستان",
    "45": "کرمان", "65": "کرمان", "75": "کرمان",
    "46": "گیلان", "56": "گیلان", "76": "گیلان",
    "47": "مرکزی", "57": "مرکزی",
    "48": "بوشهر", "58": "بوشهر",
    "49": "کهگیلویه و بویراحمد",
    "51": "کردستان", "61": "کردستان",
    "52": "خراسان جنوبی",
    "54": "یزد", "64": "یزد",
    "59": "گلستان", "69": "گلستان",
    "62": "مازندران", "72": "مازندران", "82": "مازندران", "92": "مازندران",
    "71": "چهارمحال و بختیاری", "81": "چهارمحال و بختیاری",
    "79": "قزوین", "89": "قزوین",
    "84": "هرمزگان", "94": "هرمزگان",
    "85": "سیستان و بلوچستان", "95": "سیستان و بلوچستان",
    "86": "سمنان", "96": "سمنان",
    "87": "زنجان", "97": "زنجان",
    "91": "اردبیل",
    "98": "ایلام",
}

_PLATE_CATEGORIES = {
    "ت": "تاکسی",
    "ع": "عمومی",
    "الف": "دولتی",
    "پ": "پلیس",
    "ث": "سپاه پاسداران",
    "ش": "ارتش جمهوری اسلامی ایران",
    "ز": "وزارت دفاع",
    "ف": "ستاد کل نیروهای مسلح",
    "ک": "ادوات کشاورزی",
    "گ": "گذر موقت",
    "ژ": "جانبازان و معلولین",
    "D": "سیاسی",
    "S": "سرویس سفارتخانه",
}

_NATIONAL_CODE_PREFIXES = {
    "001": ("تهران", "تهران مرکزی"), "002": ("تهران", "تهران مرکزی"), "003": ("تهران", "تهران مرکزی"), "004": ("تهران", "تهران مرکزی"), "005": ("تهران", "تهران مرکزی"), "006": ("تهران", "تهران مرکزی"), "007": ("تهران", "تهران مرکزی"), "008": ("تهران", "تهران مرکزی"), "011": ("تهران", "تهران"), "015": ("تهران", "تهران"), "020": ("تهران", "تهران"), "025": ("تهران", "تهران"), "044": ("تهران", "تهران"), "045": ("تهران", "تهران"), "160": ("تهران", "تهران"), "161": ("تهران", "اسلامشهر"), "162": ("تهران", "پاكدشت"), "163": ("تهران", "دماوند"), "164": ("تهران", "رباط كريم"), "165": ("تهران", "ری"), "166": ("تهران", "شهریار"), "167": ("تهران", "شمیرانات"), "168": ("تهران", "فیروزکوه"), "169": ("تهران", "ورامین"),
    "031": ("البرز", "کرج"), "032": ("البرز", "کرج"), "400": ("البرز", "کرج"), "401": ("البرز", "کرج"), "402": ("البرز", "فردیس"), "403": ("البرز", "هشتگرد"), "405": ("البرز", "نظرآباد"), "407": ("البرز", "اشتهارد"),
    "113": ("اصفهان", "اردستان"), "114": ("اصفهان", "آران و بیدگل"), "115": ("اصفهان", "نایین"), "116": ("اصفهان", "نطنز"), "117": ("اصفهان", "خمینی شهر"), "118": ("اصفهان", "خوانسار"), "119": ("اصفهان", "دهاقان"), "120": ("اصفهان", "سمیرم"), "121": ("اصفهان", "شاهین شهر"), "122": ("اصفهان", "شهرضا"), "123": ("اصفهان", "فریدن"), "124": ("اصفهان", "فریدونشهر"), "125": ("اصفهان", "فلاورجان"), "126": ("اصفهان", "گلپایگان"), "127": ("اصفهان", "اصفهان"), "128": ("اصفهان", "اصفهان"), "129": ("اصفهان", "اصفهان"), "130": ("اصفهان", "کاشان"), "131": ("اصفهان", "خوانسار"), "132": ("اصفهان", "مبارکه"), "133": ("اصفهان", "نجف آباد"), "134": ("اصفهان", "لنجان"), "135": ("اصفهان", "شاهین شهر"),
    "136": ("آذربایجان شرقی", "تبریز"), "137": ("آذربایجان شرقی", "تبریز"), "138": ("آذربایجان شرقی", "تبریز"), "139": ("آذربایجان شرقی", "آذرشهر"), "140": ("آذربایجان شرقی", "اسکو"), "141": ("آذربایجان شرقی", "اهر"), "142": ("آذربایجان شرقی", "بستان آباد"), "143": ("آذربایجان شرقی", "بناب"), "144": ("آذربایجان شرقی", "جلفا"), "149": ("آذربایجان شرقی", "سراب"), "150": ("آذربایجان شرقی", "شبستر"), "152": ("آذربایجان شرقی", "عجب شیر"), "153": ("آذربایجان شرقی", "مراغه"), "154": ("آذربایجان شرقی", "مرند"), "155": ("آذربایجان شرقی", "میانه"), "505": ("آذربایجان شرقی", "ملکان"), "506": ("آذربایجان شرقی", "هریس"), "507": ("آذربایجان شرقی", "هشترود"),
    "274": ("آذربایجان غربی", "ارومیه"), "275": ("آذربایجان غربی", "ارومیه"), "280": ("آذربایجان غربی", "خوی"), "281": ("آذربایجان غربی", "سلماس"), "282": ("آذربایجان غربی", "ماکو"), "283": ("آذربایجان غربی", "نقده"), "284": ("آذربایجان غربی", "پیرانشهر"), "285": ("آذربایجان غربی", "مهاباد"), "286": ("آذربایجان غربی", "بوکان"), "287": ("آذربایجان غربی", "میاندوآب"), "288": ("آذربایجان غربی", "تکاب"), "289": ("آذربایجان غربی", "شاهین دژ"), "290": ("آذربایجان غربی", "سردشت"), "291": ("آذربایجان غربی", "پلدشت"), "292": ("آذربایجان غربی", "چایپاره"), "293": ("آذربایجان غربی", "شوط"),
    "443": ("یزد", "یزد"), "444": ("یزد", "یزد"), "445": ("یزد", "ابرکوه"), "446": ("یزد", "اردکان"), "447": ("یزد", "بافق"), "448": ("یزد", "تفت"), "551": ("یزد", "مهریز"), "552": ("یزد", "میبد"), "553": ("یزد", "صدوق"),
    "228": ("فارس", "شیراز"), "229": ("فارس", "شیراز"), "230": ("فارس", "شیراز"), "236": ("فارس", "آباده"), "237": ("فارس", "مرودشت"), "238": ("فارس", "لارستان"), "239": ("فارس", "جهرم"), "240": ("فارس", "فساء"), "241": ("فارس", "کازرون"), "242": ("فارس", "فیروزآباد"), "243": ("فارس", "داراب"), "244": ("فارس", "نی ریز"), "245": ("فارس", "بوانات"), "246": ("فارس", "خرامه"), "247": ("فارس", "اقلید"), "248": ("فارس", "ممسنی"), "249": ("فارس", "سپیدان"), "250": ("فارس", "لامرد"), "251": ("فارس", "استهبان"), "252": ("فارس", "قیر و کارزین"), "253": ("فارس", "زرین دشت"), "254": ("فارس", "مهر"), "255": ("فارس", "پاسارگاد"), "256": ("فارس", "ارسنجان"),
    "092": ("خراسان رضوی", "مشهد"), "093": ("خراسان رضوی", "مشهد"), "094": ("خراسان رضوی", "مشهد"), "095": ("خراسان رضوی", "تربت حیدریه"), "096": ("خراسان رضوی", "سبزوار"), "097": ("خراسان رضوی", "نیشابور"), "098": ("خراسان رضوی", "قوچان"), "105": ("خراسان رضوی", "درگز"), "106": ("خراسان رضوی", "گناباد"), "107": ("خراسان رضوی", "کاشمر"), "108": ("خراسان رضوی", "تربت جام"),
    "205": ("مازندران", "آمل"), "206": ("مازندران", "بابل"), "208": ("مازندران", "بهشهر"), "209": ("مازندران", "تنکابن"), "211": ("مازندران", "جویبار"), "212": ("مازندران", "چالوس"), "213": ("مازندران", "رامسر"), "214": ("مازندران", "ساری"), "215": ("مازندران", "ساری"), "216": ("مازندران", "قائم شهر"), "217": ("مازندران", "محمودآباد"), "218": ("مازندران", "نکا"), "219": ("مازندران", "نور"), "220": ("مازندران", "نوشهر"), "221": ("مازندران", "بابلسر"), "222": ("مازندران", "سوادکوه"),
    "258": ("گیلان", "آستارا"), "259": ("گیلان", "آستانه اشرفیه"), "260": ("گیلان", "بندر انزلی"), "261": ("گیلان", "رشت"), "262": ("گیلان", "رشت"), "263": ("گیلان", "رودبار"), "264": ("گیلان", "رودسر"), "265": ("گیلان", "صومعه سرا"), "266": ("گیلان", "طوالش"), "267": ("گیلان", "فومن"), "268": ("گیلان", "لاهیجان"), "269": ("گیلان", "لنگرود"), "271": ("گیلان", "رضوانشهر"), "272": ("گیلان", "ماسال"), "273": ("گیلان", "شفت"),
    "174": ("خوزستان", "اهواز"), "175": ("خوزستان", "اهواز"), "181": ("خوزستان", "آبادان"), "182": ("خوزستان", "خرمشهر"), "183": ("خوزستان", "دزفول"), "184": ("خوزستان", "اندیمشک"), "185": ("خوزستان", "بهبهان"), "186": ("خوزستان", "ایذه"), "187": ("خوزستان", "شوشتر"), "188": ("خوزستان", "مسجد سلیمان"), "189": ("خوزستان", "رامهرمز"), "190": ("خوزستان", "دشت آزادگان"), "191": ("خوزستان", "ماهشهر"), "192": ("خوزستان", "شادگان"), "193": ("خوزستان", "شوش"), "194": ("خوزستان", "باغ ملک"), "195": ("خوزستان", "امیدیه"), "196": ("خوزستان", "لالی"), "197": ("خوزستان", "هندیجان"),
    "324": ("کرمانشاه", "کرمانشاه"), "325": ("کرمانشاه", "کرمانشاه"), "330": ("کرمانشاه", "اسلام آباد غرب"), "331": ("کرمانشاه", "پاوه"), "332": ("کرمانشاه", "سنقر"), "333": ("کرمانشاه", "سرپل ذهاب"), "334": ("کرمانشاه", "کنگاور"), "335": ("کرمانشاه", "جوانرود"), "336": ("کرمانشاه", "قصر شیرین"), "337": ("کرمانشاه", "گیلانغرب"), "338": ("کرمانشاه", "هرسین"), "339": ("کرمانشاه", "صحنه"),
    "406": ("لرستان", "خرم آباد"), "407": ("لرستان", "خرم آباد"), "412": ("لرستان", "بروجرد"), "413": ("لرستان", "الیگودرز"), "416": ("لرستان", "دورود"), "417": ("لرستان", "کوهدشت"), "418": ("لرستان", "دلفان"), "419": ("لرستان", "سلسله"), "420": ("لرستان", "پلدختر"), "421": ("لرستان", "ازنا"),
    "298": ("کرمان", "کرمان"), "299": ("کرمان", "کرمان"), "301": ("کرمان", "رفسنجان"), "302": ("کرمان", "سیرجان"), "303": ("کرمان", "بفت"), "304": ("کرمان", "بم"), "305": ("کرمان", "جیرفت"), "306": ("کرمان", "شهربابک"), "307": ("کرمان", "زرند"), "308": ("کرمان", "کهنوج"), "309": ("کرمان", "بافت"), "310": ("کرمان", "بردسیر"), "311": ("کرمان", "راور"), "312": ("کرمان", "منوجان"), "313": ("کرمان", "عنبرآباد"), "314": ("کرمان", "قلعه گنج"), "315": ("کرمان", "رودبار جنوب"),
    "386": ("همدان", "همدان"), "387": ("همدان", "همدان"), "392": ("همدان", "ملایر"), "393": ("همدان", "نهاوند"), "394": ("همدان", "تویسرکان"), "395": ("همدان", "کبودرآهنگ"), "396": ("همدان", "رزن"), "397": ("همدان", "اسدآباد"), "398": ("همدان", "بهار"), "399": ("همدان", "فامنین"),
    "037": ("قم", "قم"), "038": ("قم", "قم"),
    "431": ("قزوین", "قزوین"), "432": ("قزوین", "قزوین"), "509": ("قزوین", "تاکستان"), "538": ("قزوین", "بوئین زهرا"), "539": ("قزوین", "آبیک"),
    "427": ("زنجان", "زنجان"), "428": ("زنجان", "زنجان"), "429": ("زنجان", "ابهر"), "440": ("زنجان", "خدابنده"), "518": ("زنجان", "طارم"),
    "456": ("سمنان", "سمنان"), "457": ("سمنان", "شاهرود"), "458": ("سمنان", "دامغان"), "459": ("سمنان", "گرمسار"), "460": ("سمنان", "مهدی شهر"),
    "052": ("مرکزی", "اراک"), "053": ("مرکزی", "اراک"), "055": ("مرکزی", "ساوه"), "056": ("مرکزی", "خمین"), "057": ("مرکزی", "محلات"), "058": ("مرکزی", "دلیجان"), "059": ("مرکزی", "تفرش"), "060": ("مرکزی", "آشتیان"), "061": ("مرکزی", "شازند"), "062": ("مرکزی", "زرندیه"),
    "449": ("ایلام", "ایلام"), "450": ("ایلام", "ایلام"), "533": ("ایلام", "مهران"), "534": ("ایلام", "دهلران"),
    "461": ("چهارمحال و بختیاری", "شهرکرد"), "462": ("چهارمحال و بختیاری", "شهرکرد"), "465": ("چهارمحال و بختیاری", "بروجن"), "466": ("چهارمحال و بختیاری", "لردگان"), "467": ("چهارمحال و بختیاری", "فارسان"), "468": ("چهارمحال و بختیاری", "اردل"),
    "424": ("کهگیلویه و بویراحمد", "یاسوج"), "425": ("کهگیلویه و بویراحمد", "دوگنبدان"), "426": ("کهگیلویه و بویراحمد", "دهدشت"), "555": ("کهگیلویه و بویراحمد", "بهمئی"),
    "081": ("خراسان جنوبی", "بیرجند"), "082": ("خراسان جنوبی", "بیرجند"), "083": ("خراسان جنوبی", "فردوس"), "084": ("خراسان جنوبی", "طبس"), "562": ("خراسان جنوبی", "قائنات"), "563": ("خراسان جنوبی", "نهبندان"), "564": ("خراسان جنوبی", "سرایان"),
    "063": ("خراسان شمالی", "بجنورد"), "064": ("خراسان شمالی", "بجنورد"), "067": ("خراسان شمالی", "شیروان"), "068": ("خراسان شمالی", "اسفراین"), "074": ("خراسان شمالی", "جاجرم"), "075": ("خراسان شمالی", "مانه و سملقان"), "076": ("خراسان شمالی", "جاجرم"), "590": ("خراسان شمالی", "فاروج")
}

_LANDLINE_AREA_CODES = {
    "11": "مازندران", "13": "گیلان", "17": "گلستان",
    "21": "تهران", "23": "سمنان", "24": "زنجان", "25": "قم", "26": "البرز", "28": "قزوین",
    "31": "اصفهان", "34": "کرمان", "35": "یزد", "38": "چهارمحال و بختیاری",
    "41": "آذربایجان شرقی", "44": "آذربایجان غربی", "45": "اردبیل",
    "51": "خراسان رضوی", "54": "سیستان و بلوچستان", "56": "خراسان جنوبی", "58": "خراسان شمالی",
    "61": "خوزستان", "66": "لرستان",
    "71": "فارس", "74": "کهگیلویه و بویراحمد", "76": "هرمزگان", "77": "بوشهر",
    "81": "همدان", "83": "کرمانشاه", "84": "ایلام", "86": "مرکزی", "87": "کردستان"
}


def is_valid_national_code(code: str) -> bool:
    """Check if the provided code is a valid 10-digit Iranian National Code."""
    if not code:
        return False

    clean = "".join(c for c in str(code).translate(_TO_ENGLISH) if c.isdigit())

    if len(clean) < 10:
        clean = clean.zfill(10)
    elif len(clean) > 10:
        return False

    if len(set(clean)) == 1:
        return False

    digits = [int(d) for d in clean]
    check_digit = digits[-1]

    s = sum(digits[i] * (10 - i) for i in range(9))
    r = s % 11

    if r < 2:
        return check_digit == r
    
    return check_digit == (11 - r)


def format_national_code(code: str) -> str:
    """Format national code into standardized format (e.g. XXX-XXXXXX-X)."""
    clean = "".join(c for c in str(code).translate(_TO_ENGLISH) if c.isdigit())
    
    if len(clean) < 10:
        clean = clean.zfill(10)
    elif len(clean) > 10:
        raise ValueError("National code must not exceed 10 digits.")
        
    return f"{clean[:3]}-{clean[3:9]}-{clean[9]}"


def detect_national_code_location(code: str) -> dict[str, str] | None:
    """Detect the province and city of issue of an Iranian national code."""
    clean = "".join(c for c in str(code).translate(_TO_ENGLISH) if c.isdigit()).zfill(10)
    if len(clean) != 10:
        return None
    prefix = clean[:3]
    location = _NATIONAL_CODE_PREFIXES.get(prefix)
    if location:
        return {"province": location[0], "city": location[1]}
    return None


def is_valid_mobile(phone: str) -> bool:
    """Validate Iranian mobile numbers (supports +98, 0098, 98, 0 and bare prefixes)."""
    if not phone:
        return False
    clean = "".join(c for c in str(phone).translate(_TO_ENGLISH) if c.isdigit() or c == "+")
    pattern = re.compile(r"^(?:\+98|0098|98|0)?9\d{9}$")
    return bool(pattern.match(clean))


def normalize_mobile(
    phone: str, 
    prefix: Literal["0", "+98", "98", "0098", ""] = "0"
) -> str:
    """Standardize mobile formats to specified layout prefixes."""
    if not is_valid_mobile(phone):
        raise ValueError("Invalid Iranian mobile number layout.")
        
    clean = "".join(c for c in str(phone).translate(_TO_ENGLISH) if c.isdigit())
    base = clean[-10:]
    
    if prefix == "0":
        return f"0{base}"
    elif prefix == "+98":
        return f"+98{base}"
    elif prefix == "98":
        return f"98{base}"
    elif prefix == "0098":
        return f"0098{base}"
    elif prefix == "":
        return base
    
    raise ValueError("Unsupported prefix format. Choose '0', '+98', '98', '0098', or ''.")


def is_valid_landline(phone: str) -> bool:
    """Validate Iranian fixed-line (landline) phone numbers (e.g., 02188888888, +982188888888)."""
    if not phone:
        return False
    clean = "".join(c for c in str(phone).translate(_TO_ENGLISH) if c.isdigit() or c == "+")
    pattern = re.compile(r"^(?:\+98|0098|98|0)?[1-8]\d{9}$")
    return bool(pattern.match(clean))


def normalize_landline(
    phone: str, 
    prefix: Literal["0", "+98", "98", "0098", ""] = "0"
) -> str:
    """Normalize a fixed landline number to a standardized prefix form."""
    if not is_valid_landline(phone):
        raise ValueError("Invalid Iranian fixed landline phone number.")
    clean = "".join(c for c in str(phone).translate(_TO_ENGLISH) if c.isdigit())
    base = clean[-10:]
    
    if prefix == "0":
        return f"0{base}"
    elif prefix == "+98":
        return f"+98{base}"
    elif prefix == "98":
        return f"98{base}"
    elif prefix == "0098":
        return f"0098{base}"
    elif prefix == "":
        return base
    
    raise ValueError("Unsupported prefix. Choose '0', '+98', '98', '0098', or ''.")


def detect_landline_province(phone: str) -> str | None:
    """Detect the province of an Iranian landline phone number based on its area code."""
    try:
        norm = normalize_landline(phone, prefix="")
        area_code = norm[:2]
        return _LANDLINE_AREA_CODES.get(area_code)
    except ValueError:
        return None


def is_valid_card_number(card: str) -> bool:
    """Validate 16-digit bank card numbers using Luhn checksum algorithm."""
    if not card:
        return False
    clean = "".join(c for c in str(card).translate(_TO_ENGLISH) if c.isdigit())
    
    if len(clean) != 16:
        return False
        
    digits = [int(x) for x in clean]
    for i in range(0, 16, 2):
        val = digits[i] * 2
        if val > 9:
            val -= 9
        digits[i] = val
        
    return sum(digits) % 10 == 0


def format_card_number(card: str, separator: str = "-") -> str:
    """Format bank card numbers into standard four-chunk groups."""
    clean = "".join(c for c in str(card).translate(_TO_ENGLISH) if c.isdigit())
    if len(clean) != 16:
        raise ValueError("Card number must contain exactly 16 digits.")
    return separator.join([clean[i:i+4] for i in range(0, 16, 4)])


def is_valid_sheba(sheba: str) -> bool:
    """Validate Iranian Sheba (IBAN) format (starts with IR followed by 24 digits)."""
    if not sheba:
        return False
    
    clean = "".join(c for c in str(sheba).translate(_TO_ENGLISH).upper() if c.isdigit() or ('A' <= c <= 'Z'))

    if len(clean) == 24 and clean.isdigit():
        clean = "IR" + clean

    if len(clean) != 26 or not clean.startswith("IR") or not clean[2:].isdigit():
        return False

    rearranged = clean[4:] + clean[:4]
    
    num_str = ""
    for char in rearranged:
        if char.isalpha():
            num_str += str(ord(char) - ord('A') + 10)
        else:
            num_str += char

    try:
        return int(num_str) % 97 == 1
    except ValueError:
        return False


def format_sheba(
    sheba: str, 
    format_type: Literal["spaced", "clean"] = "spaced"
) -> str:
    """Format Sheba values cleanly or into four-character readable blocks."""
    clean = "".join(c for c in str(sheba).translate(_TO_ENGLISH).upper() if c.isdigit() or ('A' <= c <= 'Z'))

    if len(clean) == 24 and clean.isdigit():
        clean = "IR" + clean

    if len(clean) != 26 or not clean.startswith("IR") or not clean[2:].isdigit():
        raise ValueError("Invalid Sheba structure.")

    if format_type == "clean":
        return clean

    return " ".join([clean[i:i+4] for i in range(0, 26, 4)])


def extract_account_number_from_sheba(sheba: str) -> str:
    """Extract the embedded bank account number from a valid Iranian Sheba (IBAN)."""
    if not is_valid_sheba(sheba):
        raise ValueError("Invalid Sheba structure.")
    clean = "".join(c for c in str(sheba).translate(_TO_ENGLISH).upper() if c.isalnum())
    if clean.startswith("IR"):
        clean = clean[2:]
    
    # The last 18 digits represent the account number
    account_part = clean[-18:]
    return account_part.lstrip("0")


def is_valid_corporate_id(code: str) -> bool:
    """Validate 11-digit Iranian Legal Entity National ID."""
    if not code:
        return False
    
    clean = "".join(c for c in str(code).translate(_TO_ENGLISH) if c.isdigit())
    
    if len(clean) != 11:
        return False
        
    if len(set(clean)) == 1:
        return False
        
    d = int(clean[9]) + 2
    z = [29, 27, 23, 19, 17]
    s = sum((int(clean[i]) + d) * z[i % 5] for i in range(10))
    rem = s % 11
    if rem == 10:
        rem = 0
    
    check_digit = int(clean[10])
    return check_digit == rem


def detect_mobile_operator(phone: str) -> str | None:
    """Detect the telecom operator of an Iranian mobile phone number."""
    try:
        normalized = normalize_mobile(phone, prefix="0")
    except ValueError:
        return None
        
    prefix = normalized[:4]
    
    mci_prefixes = {
        "0910", "0911", "0912", "0913", "0914", "0915", "0916", "0917", "0918", "0919",
        "0990", "0991", "0992", "0993", "0994", "0996"
    }
    irancell_prefixes = {
        "0930", "0933", "0935", "0936", "0937", "0938", "0939",
        "0901", "0902", "0903", "0904", "0905", "0900", "0941"
    }
    rightel_prefixes = {"0920", "0921", "0922", "0923"}
    shatel_prefixes = {"0998"}
    samantel_prefixes = {"0999"}
    taliya_prefixes = {"0932"}
    tkc_prefixes = {"0934"}
    
    if prefix in mci_prefixes:
        return "MCI"
    elif prefix in irancell_prefixes:
        return "Irancell"
    elif prefix in rightel_prefixes:
        return "RighTel"
    elif prefix in shatel_prefixes:
        return "Shatel Mobile"
    elif prefix in samantel_prefixes:
        return "SamanTel"
    elif prefix in taliya_prefixes:
        return "Taliya"
    elif prefix in tkc_prefixes:
        return "TKC"
        
    return None


def detect_bank_from_card(card: str) -> BankDetails | None:
    """Detect the bank details from a 16-digit card number or its 6-digit prefix (BIN)."""
    if not card:
        return None
    clean = "".join(c for c in str(card).translate(_TO_ENGLISH) if c.isdigit())
    if len(clean) < 6:
        return None
    return _CARD_BIN_TO_BANK.get(clean[:6])


def detect_bank_from_sheba(sheba: str) -> BankDetails | None:
    """Detect the bank details from a Sheba (IBAN) code or its prefix."""
    if not sheba:
        return None
    clean = "".join(c for c in str(sheba).translate(_TO_ENGLISH).upper() if c.isdigit() or ('A' <= c <= 'Z'))
    if len(clean) == 24 and clean.isdigit():
        clean = "IR" + clean
    if len(clean) < 7 or not clean.startswith("IR"):
        return None
    bank_code = clean[4:7]
    return _SHEBA_CODE_TO_BANK.get(bank_code)


def is_valid_postal_code(postal_code: str) -> bool:
    """Validate 10-digit Iranian Postal Code."""
    if not postal_code:
        return False
    clean = "".join(c for c in str(postal_code).translate(_TO_ENGLISH) if c.isdigit())
    if len(clean) != 10:
        return False
    first_five = clean[:5]
    if '0' in first_five or '2' in first_five:
        return False
    return True


def format_postal_code(postal_code: str) -> str:
    """Format postal code cleanly as XXXXX-XXXXX."""
    clean = "".join(c for c in str(postal_code).translate(_TO_ENGLISH) if c.isdigit())
    if len(clean) != 10:
        raise ValueError("Postal code must contain exactly 10 digits.")
    return f"{clean[:3]}-{clean[3:9]}-{clean[9]}"


def _calculate_mod11_bill_checksum(digits_str: str) -> int:
    """Calculate modulo 11 checksum for Iranian bills."""
    weights = [2, 3, 4, 5, 6, 7]
    total = 0
    for i, char in enumerate(reversed(digits_str)):
        weight = weights[i % 6]
        total += int(char) * weight
    rem = total % 11
    if rem == 0 or rem == 1:
        return 0
    return 11 - rem


def is_valid_bill_and_payment(bill_id: str, pay_id: str) -> bool:
    """Validate Iranian Bill ID and Payment ID using standard Modulo 11 check digits."""
    _TO_ENGLISH_LOCAL = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    b = "".join(c for c in str(bill_id).translate(_TO_ENGLISH_LOCAL) if c.isdigit())
    p = "".join(c for c in str(pay_id).translate(_TO_ENGLISH_LOCAL) if c.isdigit())
    
    if len(b) < 6 or len(p) < 6:
        return False
        
    if _calculate_mod11_bill_checksum(b[:-1]) != int(b[-1]):
        return False
        
    if _calculate_mod11_bill_checksum(p[:-2]) != int(p[-2]):
        return False
        
    combined = b.lstrip('0') + p[:-1].lstrip('0')
    if _calculate_mod11_bill_checksum(combined) != int(p[-1]):
        return False
        
    return True


def extract_bill_details(bill_id: str, pay_id: str) -> BillDetails | None:
    """Validate and extract payment details and type from Iranian Bill & Payment IDs."""
    _TO_ENGLISH_LOCAL = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    b = "".join(c for c in str(bill_id).translate(_TO_ENGLISH_LOCAL) if c.isdigit())
    p = "".join(c for c in str(pay_id).translate(_TO_ENGLISH_LOCAL) if c.isdigit())
    
    if len(b) < 6 or len(p) < 6:
        return None
        
    is_valid_flag = is_valid_bill_and_payment(b, p)
    
    type_code = b[-2]
    bill_type = _BILL_TYPES.get(type_code, "سایر قبوض")
    
    amount_base_str = p[:-2]
    try:
        amount_base = int(amount_base_str)
        amount_rial = amount_base * 1000
        amount_toman = amount_rial // 10
    except ValueError:
        amount_rial = 0
        amount_toman = 0
        
    return {
        "is_valid": is_valid_flag,
        "amount_rial": amount_rial,
        "amount_toman": amount_toman,
        "type": bill_type,
        "type_code": type_code,
    }


def parse_plate(plate_str: str) -> PlateDetails | None:
    """Parse an Iranian National Vehicle Plate (پلاک ملی) and extract details."""
    _TO_ENGLISH_LOCAL = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    s = str(plate_str).translate(_TO_ENGLISH_LOCAL).strip()
    s = s.replace("ایران", "").replace("-", "").replace(" ", "")
    
    plate_regex = re.compile(r"^(\d{2})([بجدسصطقلمنوهیتعپثشزفکگژDS]|الف)(\d{3})(\d{2})$")
    match = plate_regex.match(s)
    if not match:
        return None
        
    p1, letter, p2, p3 = match.groups()
    category = _PLATE_CATEGORIES.get(letter, "شخصی")
    province = _PROVINCE_CODES.get(p3, "نامشخص")
    
    _TO_PERSIAN_LOCAL = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
    p1_fa = p1.translate(_TO_PERSIAN_LOCAL)
    p2_fa = p2.translate(_TO_PERSIAN_LOCAL)
    p3_fa = p3.translate(_TO_PERSIAN_LOCAL)
    
    return {
        "part1": p1_fa,
        "letter": letter,
        "part2": p2_fa,
        "province_code": p3_fa,
        "province": province,
        "category": category,
    }


def is_valid_plate(plate_str: str) -> bool:
    """Check if the given string is a structurally valid Iranian Vehicle Plate."""
    return parse_plate(plate_str) is not None


def format_plate(
    plate_str: str, 
    format_type: Literal["readable", "clean"] = "readable"
) -> str:
    """Format an Iranian Vehicle Plate into a standard readable or clean layout."""
    parsed = parse_plate(plate_str)
    if not parsed:
        raise ValueError(f"Invalid Iranian plate structure '{plate_str}'")
        
    if format_type == "clean":
        return f"{parsed['part1']}{parsed['letter']}{parsed['part2']}{parsed['province_code']}"
        
    return f"{parsed['part1']} {parsed['letter']} {parsed['part2']} - ایران {parsed['province_code']}"