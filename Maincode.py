# -- coding: utf-8 --

from flask import Flask, render_template, request
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

# OpenAI istemcisi
client = OpenAI(api_key=("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"))

app = Flask(__name__)


# MEB Kazanımları

MEB_KAZANIMLARI = {
    "5. Sınıf": {
       "Dosya ve Klasör Yönetimi": "BT.5.1.3.2. Temel dosya ve klasör yönetim işlemlerini yapar.",
        "Etik Kavramları": "BT.5.2.1.1. Etik ve bilişim etiği ile ilgili temel kavramları açıklar.",
        "İnternet Etiği": "BT.5.2.1.2. Bilişim teknolojileri ile İnterneti kullanma ve yönetme sürecinde etik ilkelere uymanın önemini açıklar.",
        "Çevrimiçi Haklar": "BT.5.2.1.3. Çevrimiçi ortamda başkalarının haklarına saygı duyar.",
        "Etik İhlaller": "BT.5.2.1.4. Etik ilkelerin ihlali sonucunda karşılaşılacak durumları fark eder.",
        "Dijital Vatandaşlık": "BT.5.2.2.1. Dijital vatandaşlık uygulamalarının kullanım amaçlarını ve önemini kavrar.",
        "Dijital Kimlik": "BT.5.2.2.2. Dijital kimliklerin gerçeği yansıtmayabileceğini fark eder.",
        "Dijital İzler": "BT.5.2.2.3. Dijital paylaşımların kalıcı olduğunu ve kendisinden geride izler bıraktığını fark eder.",
        "Ağ İletişimi": "BT.5.3.1.1. Bilginin ağlar arasındaki yolculuğunu keşfeder.",
        "Algoritma Geliştirme": "BT.5.5.1.13. Bir problemin çözümü için algoritma geliştirir.",
        "Akış Şeması": "BT.5.5.1.14. Akış şeması bileşenlerini ve işlevlerini açıklar."
    },
    "6. Sınıf": {
        "Yapay Zeka": "BT.6.1.1.2. Bilgisayarların akıllı davranış modellerini kullanma biçimlerini açıklar.",
        "Sağlık Etkileri": "BT.6.1.1.3. Bilişim teknolojilerinin beden ve ruh sağlığına etkilerini yorumlar.",
        "İşletim Sistemi": "BT.6.1.2.1. İşletim sistemi kavramını açıklar.",
        "Dosya Uzantıları": "BT.6.1.3.1. Dosya uzantılarına göre dosyaların temel özelliklerini açıklar.",
        "Siber Zorbalık": "BT.6.2.1.3. Siber zorbalık kavramını açıklayarak korunma amacıyla alınabilecek önlemleri tartışır.",
        "Telif Hakkı": "BT.6.2.1.4. Telif hakkı kavramını ve önemini araştırır.",
        "Bilişim Suçları": "BT.6.2.1.6. Bilişim suçlarının neler olduğunu açıklayarak ilgili kanunları özetler.",
        "Arama Motorları": "BT.6.3.2.1. Arama motorlarını kullanarak ileri düzeyde araştırma yapar.",
        "Zararlı İçerik": "BT.6.3.2.2. Bilgiye ulaşırken zararlı ve gereksiz içerikleri ayırt eder.",
        "Programlama": "BT.6.5.2.5. Doğrusal mantık yapısını içeren programlar oluşturur."
    }
}

# 🎯 Her konu için özel promptlar
# 5. Sınıf Promptları
KAZANIM_PROMPTLARI = {  "Dosya ve Klasör Yönetimi": """
Aşağıdaki konuda ortaokul 5. Sınıf öğrencileri için orta zorlukta 7 tane çoktan seçmeli soru üret:
Konu: Dosya ve Klasör Yönetimi: "BT.5.1.3.2. Temel dosya ve klasör yönetim işlemlerini yapar."
Her sorunun 4 seçeneği ve doğru cevabı olsun.
JSON formatında dön:
{{
  "sorular": [
    {{"soru": "...", "cevap": "...", "secenekler": ["...", "...", "...", "..."]}},
    ...
  ]
}}

""",
###
    "Etik Kavramları": """
Aşağıdaki konuda ortaokul 5. Sınıf öğrencileri için orta zorlukta 7 tane doğru-yanlış sorusu üret:
Konu: Etik Kavramlar
Kazanım: Etik Kavramları": "BT.5.2.1.1. Etik ve bilişim etiği ile ilgili temel kavramları açıklar.
Her sorunun doğru cevabı ve 2 seçenek ("Doğru", "Yanlış") olsun.
Cevabı şu JSON formatında dön:
{
  "sorular": [
    {"soru": "...", "cevap": "Doğru", "secenekler": ["Doğru", "Yanlış"]},
    ...
  ]
}
Sadece JSON döndür, başka açıklama yazma.
""",
###
    "İnternet Etiği": """

Aşağıdaki konuda ortaokul 5. Sınıf öğrencileri için orta zorlukta 7 tane doğru-yanlış sorusu üret:
Konu: İnternet Etiği
Kazanım: BT.5.2.1.2. Bilişim teknolojileri ile İnterneti kullanma ve yönetme sürecinde etik ilkelere uymanın önemini açıklar.
Her sorunun doğru cevabı ve 2 seçenek ("Doğru", "Yanlış") olsun.
Cevabı şu JSON formatında dön:
{
  "sorular": [
    {"soru": "...", "cevap": "Doğru", "secenekler": ["Doğru", "Yanlış"]},
    ...
  ]
}
Sadece JSON döndür, başka açıklama yazma.

""",

  "Çevrimiçi Haklar": """
Aşağıdaki konuda ortaokul 5. Sınıf öğrencileri için 5 tane kavram-eşleştirme sorusu üret:
Konu: Çevrimiçi Haklar (BT.5.2.1.3. Çevrimiçi ortamda başkalarının haklarına saygı duyar.)
Her soruda eşleştirilmesi gereken bir kavram ve dört farklı tanım ver. Bir tanesi doğru olsun.
Cevabı şu JSON formatında dön:
{
  "sorular": [
    {
      "terim": "...",
      "tanımlar": ["...", "...", "...", "..."],
      "dogru": "..."
    },
    ...
  ]
}
Sadece JSON döndür.
""",

"Etik İhlaller": """
Aşağıdaki konuda ortaokul 5. Sınıf öğrencileri için 5 tane açık uçlu düşünme sorusu üret:
Konu: Etik İhlaller (BT.5.2.1.4. Etik ilkelerin ihlali sonucunda karşılaşılacak durumları fark eder.)
JSON formatında dön:
{
  "sorular": [
    {"soru": "..."},
    {"soru": "..."},
    ...
  ]
}
Sadece JSON döndür.

""",
###
   "Dijital Vatandaşlık": """
Rol: Aşağıdaki konuda ortaokul 5. Sınıf öğrencileri için 7 tane boşluk doldurma sorusu üret:
Konu: Dijital Vatandaşlık": "BT.5.2.2.1. Dijital vatandaşlık uygulamalarının kullanım amaçlarını ve önemini kavrar.
Her soruda cümlenin bir kısmı eksik olsun ve 4 seçenek verilsin.
Cevabı şu JSON formatında dön:
{
  "sorular": [
    {"soru": "Bilgisayarda ______ kullanmak etik değildir.", "cevap": "Yasadışı yazılım", "secenekler": ["Yasadışı yazılım", "Güçlü parola", "Yedekleme", "Güncelleme"]},
    ...
  ]
}
Sadece JSON döndür.
""",
###
"Dijital Kimlik": """
Rol: Aşağıdaki konuda ortaokul 5. Sınıf öğrencileri için 3 tane senaryo tabanlı karar verme sorusu üret:
Konu: Dijital Kimlik (BT.5.2.2.2. Dijital kimliklerin gerçeği yansıtmayabileceğini fark eder.)
Her soruda kısa bir hikaye anlat ve 3 seçenek sun.
JSON formatında dön:
{
  "sorular": [
    {
      "senaryo": "...",
      "secenekler": ["...", "...", "..."],
      "dogru": "..."
    },
    ...
  ]
}
Sadece JSON döndür.

""",
###

"Dijital İzler": """
Rol: Aşağıdaki konuda ortaokul 5. Sınıf öğrencileri için 7 tane sıralama sorusu üret:
Konu: Dijital İzler (BT.5.2.2.3. Dijital paylaşımların kalıcı olduğunu ve kendisinden geride izler bıraktığını fark eder.)
Her soruda 4 adımı karışık sırada ver ve öğrencinin doğru sıralaması istenir.
JSON formatında dön:
{
  "sorular": [
    {
      "adimlar": ["...", "...", "...", "..."],
      "dogru_sira": ["...", "...", "...", "..."]
    },
    ...
  ]
}
Sadece JSON döndür.


""",

"Ağ İletişimi": """
Rol: Aşağıdaki konuda ortaokul 5. Sınıf öğrencileri için orta zorlukta 7 tane çoktan seçmeli soru üret:
Konu: Ağ İletişimi (BT.5.3.1.1. Bilginin ağlar arasındaki yolculuğunu keşfeder.)
Her sorunun 4 seçeneği ve doğru cevabı olsun.
JSON formatında dön:
{
  "sorular": [
    {
      "soru": "...",
      "cevap": "...",
      "secenekler": ["...", "...", "...", "..."]
    },
    ...
  ]
}
Sadece JSON döndür.
""",

"Algoritma Geliştirme": """
Aşağıdaki konuda ortaokul öğrencileri için 7 tane boşluk doldurma sorusu üret:
Konu: Algoritma Geliştirme (BT.5.5.1.13. Bir problemin çözümü için algoritma geliştirir.)
Her soruda cümlenin bir kısmı eksik olsun ve 4 seçenek verilsin.
Cevabı şu JSON formatında dön:
{
  "sorular": [
    {
      "soru": "...",
      "cevap": "...",
      "secenekler": ["...", "...", "...", "..."]
    },
    ...
  ]
}
Sadece JSON döndür.

""",

"Akış Şeması": """
Aşağıdaki konuda ortaokul öğrencileri için 5 tane kavram-eşleştirme sorusu üret:
Konu: Akış Şeması (BT.5.5.1.14. Akış şeması bileşenlerini ve işlevlerini açıklar.)
Her soruda eşleştirilmesi gereken bir terim ve 4 tanım ver.
Cevabı şu JSON formatında dön:
{
  "sorular": [
    {
      "terim": "...",
      "tanımlar": ["...", "...", "...", "..."],
      "dogru": "..."
    },
    ...
  ]
}
Sadece JSON döndür.


""",
#####################################################
# 6. Sınıf Promptları
"Yapay Zeka": """
Aşağıdaki konuda ortaokul öğrencileri için orta zorlukta 5 tane doğru-yanlış türünde soru üret:
Konu: Yapay Zeka (BT.6.1.1.2. Bilgisayarların akıllı davranış modellerini kullanma biçimlerini açıklar.)
JSON formatında dön:
{
  "sorular": [
    {
      "soru": "...",
      "cevap": "...",
      "secenekler": ["Doğru", "Yanlış"]
    },
    ...
  ]
}
Sadece JSON döndür.
""",

"Sağlık Etkileri": """
Aşağıdaki konuda ortaokul öğrencileri için orta zorlukta 5 tane çoktan seçmeli soru üret:
Konu: Sağlık Etkileri (BT.6.1.1.3. Bilişim teknolojilerinin beden ve ruh sağlığına etkilerini yorumlar.)
Her sorunun 4 seçeneği ve doğru cevabı olsun.
JSON formatında dön:
{
  "sorular": [
    {
      "soru": "...",
      "cevap": "...",
      "secenekler": ["...", "...", "...", "..."]
    },
    ...
  ]
}
Sadece JSON döndür.

""",

"İşletim Sistemi": """
Aşağıdaki konuda ortaokul öğrencileri için orta zorlukta 5 tane boşluk doldurma sorusu üret:
Konu: İşletim Sistemi (BT.6.1.2.1. İşletim sistemi kavramını açıklar.)
Her soruda bir kelimelik bir boşluk bırak. Cevapları JSON formatında döndür:
{
  "sorular": [
    {
      "soru": "... ____ ...",
      "cevap": "..."
    },
    ...
  ]
}
Sadece JSON döndür.
""",
"Dosya Uzantıları": """
Aşağıdaki konuda ortaokul öğrencileri için 3 tane senaryo tabanlı karar verme sorusu üret:
Konu: Dosya Uzantıları (BT.6.1.3.1. Dosya uzantılarına göre dosyaların temel özelliklerini açıklar.)
Her soruda kısa bir hikaye anlat ve 3 seçenek sun.
JSON formatında dön:
{
  "sorular": [
    {
      "senaryo": "...",
      "secenekler": ["...", "...", "..."],
      "dogru": "..."
    },
    ...
  ]
}
Sadece JSON döndür.
""",

"Siber Zorbalık": """
Aşağıdaki konuda ortaokul öğrencileri için 3 tane açık uçlu düşünme sorusu üret:
Konu: Siber Zorbalık (BT.6.2.1.3. Siber zorbalık kavramını açıklayarak korunma amacıyla alınabilecek önlemleri tartışır.)
JSON formatında dön:
{
  "sorular": [
    {"soru": "..."},
    {"soru": "..."},
    {"soru": "..."}
  ]
}
Sadece JSON döndür.

""",

"Telif Hakkı": """
Aşağıdaki konuda ortaokul öğrencileri için 5 tane boşluk doldurma sorusu üret:
Konu: Telif Hakkı (BT.6.2.1.4. Telif hakkı kavramını ve önemini araştırır.)
Her soruda cümlenin bir kısmı eksik olsun ve 4 seçenek verilsin.
Cevabı şu JSON formatında dön:
{
  "sorular": [
    {"soru": "...", "cevap": "...", "secenekler": ["...", "...", "...", "..."]},
    ...
  ]
}
Sadece JSON döndür.
""",

"Bilişim Suçları": """
Aşağıdaki konuda ortaokul öğrencileri için 3 tane sıralama sorusu üret:
Konu: Bilişim Suçları (BT.6.2.1.6. Bilişim suçlarının neler olduğunu açıklayarak ilgili kanunları özetler.)
Her soruda 4 adımı karışık sırada ver ve öğrencinin doğru sıralaması istenir.
Cevabı şu JSON formatında dön:
{
  "sorular": [
    {
      "adimlar": ["Adım 1", "Adım 2", "Adım 3", "Adım 4"],
      "dogru_sira": ["Adım 1", "Adım 2", "Adım 3", "Adım 4"]
    },
    ...
  ]
}
Sadece JSON döndür.



""",
"Arama Motorları": """
Aşağıdaki konuda ortaokul öğrencileri için 3 tane açık uçlu düşünme sorusu üret:
Konu: Arama Motorları (BT.6.3.2.1. Arama motorlarını kullanarak ileri düzeyde araştırma yapar.)
Cevabı şu JSON formatında dön:
{
  "sorular": [
    {"soru": "..."},
    {"soru": "..."},
    {"soru": "..."}
  ]
}
Sadece JSON döndür.

""",
"Zararlı İçerik": """
Aşağıdaki konuda ortaokul öğrencileri için 5 tane boşluk doldurma sorusu üret:
Konu: Zararlı İçerik (BT.6.3.2.2. Bilgiye ulaşırken zararlı ve gereksiz içerikleri ayırt eder.)
Her soruda cümlenin bir kısmı eksik olsun ve 4 seçenek verilsin.
Cevabı şu JSON formatında dön:
{
  "sorular": [
    {"soru": "...", "cevap": "...", "secenekler": ["...", "...", "...", "..."]},
    ...
  ]
}
Sadece JSON döndür.
""",

"Programlama": """
Aşağıdaki konuda ortaokul öğrencileri için 3 tane sıralama sorusu üret:
Konu: Programlama (BT.6.5.2.5. Doğrusal mantık yapısını içeren programlar oluşturur.)
Her soruda 4 adımı karışık sırada ver ve öğrencinin doğru sıralamayı yapması istenir.
Cevabı şu JSON formatında dön:
{
  "sorular": [
    {
      "adimlar": ["Adım 1", "Adım 2", "Adım 3", "Adım 4"],
      "dogru_sira": ["Adım 1", "Adım 2", "Adım 3", "Adım 4"]
    },
    ...
  ]
}
Sadece JSON döndür.
"""



###
 

}


# AI destekli oyun üretici
def oyun_uret_ai(konu):
    prompt = KAZANIM_PROMPTLARI.get(konu)

    if not prompt:
        # Eğer özel prompt yoksa basit soru üretme iste
        prompt = f"""
Aşağıdaki konuda ortaokul öğrencileri için orta zorlukta 5 tane çoktan seçmeli soru üret:
Konu: {konu}
Her sorunun 4 seçeneği ve doğru cevabı olsun.
JSON formatında dön:
{{
  "sorular": [
    {{"soru": "...", "cevap": "...", "secenekler": ["...", "...", "...", "..."]}},
    ...
  ]
}}
"""

  

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sen ortaokul öğretmenleri için eğitim oyunları hazırlayan bir asistansın."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
        
    )

    text = completion.choices[0].message.content.strip()

    # Eğer JSON formatlı yanıt gelirse parse et
    try:
        parsed = json.loads(text)
        sorular = parsed["sorular"]
        # Soru formatlı bir çıktı
        return {
            "oyun_adi": f"{konu} Test Oyunu",
            "aciklama": f"{konu} konusunu pekiştirmek için hazırlanmış test.",
            "sorular": sorular
        }
    except Exception:
        # JSON değilse, düz yazı olarak oyun fikri
        return {
            "oyun_adi": f"{konu} Eğitim Oyunları",
            "aciklama": f"{konu} konusunu öğretmek için önerilen oyun konseptleri.",
            "metin": text
        }

# Basit fallback oyun
def oyun_uret_default(konu):
    return {
        "oyun_adi": f"{konu} Basit Oyun",
        "aciklama": f"{konu} konusunu öğrenmek için hazırlanan temel test.",
        "sorular": [
            {"soru": f"{konu} hakkında bu doğru mu?", "cevap": "Doğru", "secenekler": ["Doğru", "Yanlış", "Belki", "Bilmiyorum"]}
        ]
    }

@app.route("/", methods=["GET", "POST"])
def index2():
    tum_konular = [(s, k) for s, konular in MEB_KAZANIMLARI.items() for k in konular]
    oyun = None
    selected_konu = None

    if request.method == "POST":
        sinif = request.form.get("sinif")
        konu = request.form.get("konu")
        selected_konu = (sinif, konu)

        try:
            oyun = oyun_uret_ai(konu)
        except Exception as e:
            print("AI üretim hatası:", e)
            oyun = oyun_uret_default(konu)

    return render_template("index2.html", konular=tum_konular, oyun=oyun, selected_konu=selected_konu)
def run_app():
    app.run(debug=True, port=5000)

if __name__ == "__main__":
    run_app()
