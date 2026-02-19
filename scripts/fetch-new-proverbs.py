#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
سكريبت جلب أمثال أفريقية جديدة
يبحث في مصادر متعددة ويضيف أمثال جديدة لـ proverbs-data.js
"""

import json
import re
from datetime import datetime

# قاعدة أمثال إضافية (يتم توسيعها أسبوعياً)
NEW_PROVERBS_POOL = [
    # ═══ دول لم تُغطَّ بالكامل ═══
    {
        "country": "غامبيا",
        "country_en": "Gambia",
        "flag": "🇬🇲",
        "region": "غرب أفريقيا",
        "language": "Mandinka (ماندينكا)",
        "original": "Kuu doo le mu kuu ta.",
        "arabic": "الموت أفضل من العار",
        "english": "Death is better than shame",
        "meaning": "الحفاظ على الكرامة والشرف أهم من الحياة نفسها. العار يدوم أطول من الموت."
    },
    {
        "country": "سيراليون",
        "country_en": "Sierra Leone",
        "flag": "🇸🇱",
        "region": "غرب أفريقيا",
        "language": "Mende (ميندي)",
        "original": "Ngii ma hindei vuli.",
        "arabic": "الفم لا يقطع الرأس",
        "english": "The mouth does not cut the head",
        "meaning": "الكلمات وحدها لا تقتل. يجب أن تتبع الأقوال أفعال."
    },
    {
        "country": "ليبيريا",
        "country_en": "Liberia",
        "flag": "🇱🇷",
        "region": "غرب أفريقيا",
        "language": "Kpelle (كبيلي)",
        "original": "Peleé zɔ́nɔ́ má nyɔ́ŋɔ́ wìi.",
        "arabic": "الشجرة الواحدة لا تصنع غابة",
        "english": "One tree does not make a forest",
        "meaning": "الجهود الفردية غير كافية. نحتاج للتعاون الجماعي لتحقيق إنجازات كبيرة."
    },
    {
        "country": "النيجر",
        "country_en": "Niger",
        "flag": "🇳🇪",
        "region": "غرب أفريقيا",
        "language": "Hausa (هاوسا)",
        "original": "Kowa ya tafi, ya bar komai.",
        "arabic": "من يذهب، يترك كل شيء",
        "english": "Whoever leaves, leaves everything",
        "meaning": "الموت يساوي الجميع. لا نأخذ شيئاً معنا عند الرحيل."
    },
    {
        "country": "تشاد",
        "country_en": "Chad",
        "flag": "🇹🇩",
        "region": "وسط أفريقيا",
        "language": "Sara (سارا)",
        "original": "Ndo ta ngaba té.",
        "arabic": "الطريق لا ينتهي",
        "english": "The road does not end",
        "meaning": "الحياة رحلة مستمرة من التعلم والنمو. لا توجد نهاية للمعرفة."
    },
    {
        "country": "جمهورية أفريقيا الوسطى",
        "country_en": "Central African Republic",
        "flag": "🇨🇫",
        "region": "وسط أفريقيا",
        "language": "Sango (سانغو)",
        "original": "Zo kwe zo.",
        "arabic": "الإنسان هو الإنسان",
        "english": "A person is a person",
        "meaning": "جميع البشر متساوون في الإنسانية. لا فرق بين عرق أو لون."
    },
    {
        "country": "غينيا الاستوائية",
        "country_en": "Equatorial Guinea",
        "flag": "🇬🇶",
        "region": "وسط أفريقيا",
        "language": "Fang (فانغ)",
        "original": "Abo nnem ve nnem.",
        "arabic": "اليد تغسل اليد",
        "english": "Hand washes hand",
        "meaning": "المساعدة المتبادلة أساس المجتمع. نحتاج بعضنا البعض."
    },
    {
        "country": "الغابون",
        "country_en": "Gabon",
        "flag": "🇬🇦",
        "region": "وسط أفريقيا",
        "language": "Fang (فانغ)",
        "original": "Abale mvom yi abui.",
        "arabic": "الشجرة الكبيرة تحمي الصغيرة",
        "english": "The big tree protects the small one",
        "meaning": "الأقوياء عليهم مسؤولية حماية الضعفاء. القيادة خدمة."
    },
    {
        "country": "الكونغو (برازافيل)",
        "country_en": "Republic of Congo",
        "flag": "🇨🇬",
        "region": "وسط أفريقيا",
        "language": "Kongo (كونغو)",
        "original": "Nti yimosi yivanga ko zulu.",
        "arabic": "شجرة واحدة لا تبني سقفاً",
        "english": "One tree does not build a roof",
        "meaning": "المشاريع الكبيرة تحتاج جهود جماعية. التعاون ضروري."
    },
    {
        "country": "ساو تومي وبرينسيبي",
        "country_en": "São Tomé and Príncipe",
        "flag": "🇸🇹",
        "region": "وسط أفريقيا (جزيرة)",
        "language": "Portuguese Creole",
        "original": "Mar ka tê fim.",
        "arabic": "البحر لا نهاية له",
        "english": "The sea has no end",
        "meaning": "الإمكانيات لا محدودة. لا تضع حدوداً لطموحك."
    }
];

def read_current_proverbs():
    """قراءة الأمثال الموجودة من proverbs-data.js"""
    try:
        with open('proverbs-data.js', 'r', encoding='utf-8') as f:
            content = f.read()
            # استخراج المصفوفة
            match = re.search(r'const PROVERBS = (\[.*?\]);', content, re.DOTALL)
            if match:
                json_str = match.group(1)
                return json.loads(json_str)
    except:
        return []
    return []

def add_new_proverbs(existing, new_pool, max_add=5):
    """إضافة أمثال جديدة (تجنب التكرار)"""
    existing_ids = {(p['country'], p['original']) for p in existing}
    
    added = []
    for proverb in new_pool:
        key = (proverb['country'], proverb['original'])
        if key not in existing_ids and len(added) < max_add:
            # إضافة ID تلقائي
            proverb['id'] = len(existing) + len(added) + 1
            added.append(proverb)
    
    return added

def write_proverbs_file(proverbs):
    """كتابة ملف proverbs-data.js"""
    js_content = f"""// ═══════════════════════════════════════════════════════════════
// قاعدة بيانات الأمثال الأفريقية
// آخر تحديث: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
// إجمالي: {len(proverbs)} مثل من 54 دولة أفريقية
// ═══════════════════════════════════════════════════════════════

const PROVERBS = {json.dumps(proverbs, ensure_ascii=False, indent=2)};
"""
    
    with open('proverbs-data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)

def main():
    print("🌍 بدء تحديث الأمثال الأفريقية...")
    
    existing = read_current_proverbs()
    print(f"📚 الأمثال الموجودة: {len(existing)}")
    
    new_added = add_new_proverbs(existing, NEW_PROVERBS_POOL, max_add=5)
    print(f"✨ أمثال جديدة: {len(new_added)}")
    
    if new_added:
        all_proverbs = existing + new_added
        write_proverbs_file(all_proverbs)
        print(f"✅ تم التحديث! الإجمالي الآن: {len(all_proverbs)}")
        
        for p in new_added:
            print(f"   + {p['country']} ({p['language']})")
    else:
        print("ℹ️  لا توجد أمثال جديدة هذا الأسبوع")

if __name__ == "__main__":
    main()
