import streamlit as st
import pandas as pd
import datetime
import json
import os

# Sayfa Yapısı ve Ayarlar
st.set_page_config(page_title="Geliştirilmiş Arayüz Tasarımı", layout="wide")

# Profil Listesi
st.sidebar.header("Profiller")

if 'profiles' not in st.session_state:
    csv_files = [f.split('.')[0] for f in os.listdir('.') if f.endswith('.csv')]
    st.session_state.profiles = csv_files if csv_files else ["Profil 1"]

selected_profile = st.sidebar.radio("Bir profil seçiniz:", st.session_state.profiles)

# JSON dosyası ayarları
json_file_name = 'profil_verileri.json'
if not os.path.exists(json_file_name):
    with open(json_file_name, 'w') as f:
        json.dump({}, f)

with open(json_file_name, 'r') as f:
    try:
        profil_verileri = json.load(f)
    except json.JSONDecodeError:
        profil_verileri = {}
        st.warning("profil_verileri.json dosyası bozuktu ve sıfırlandı.")

# Eski verileri yeni yapıya dönüştürme ve anahtarların kontrolü
for profile in profil_verileri:
    # 'NeredenNereye' anahtarının varlığını kontrol edin
    if 'NeredenNereye' not in profil_verileri[profile]:
        # Eski 'Nereden' ve 'Nereye' listelerini birleştirin
        nereden = profil_verileri[profile].get('Nereden', [])
        nereye = profil_verileri[profile].get('Nereye', [])
        nereden_nereye = list(set(nereden + nereye))
        profil_verileri[profile]['NeredenNereye'] = nereden_nereye
        # Eski anahtarları kaldırın
        profil_verileri[profile].pop('Nereden', None)
        profil_verileri[profile].pop('Nereye', None)
    # 'Kategori' anahtarının varlığını kontrol edin
    if 'Kategori' not in profil_verileri[profile]:
        profil_verileri[profile]['Kategori'] = []

# Seçili profil için verileri kontrol edin
if selected_profile not in profil_verileri:
    profil_verileri[selected_profile] = {
        "NeredenNereye": [],
        "Kategori": []
    }

# JSON dosyasını güncelle
with open(json_file_name, 'w') as f:
    json.dump(profil_verileri, f, indent=4)

# Takvim Kısmı
st.header("Takvim")

if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.date.today()

with st.container():
    # Bir gün ileri ve geri gitme butonları
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Bir Gün Geri"):
            st.session_state.selected_date -= datetime.timedelta(days=1)
    with col2:
        if st.button("Bir Gün İleri"):
            st.session_state.selected_date += datetime.timedelta(days=1)
    
    updated_date = st.session_state.selected_date
    st.date_input("Bir tarih seçin", updated_date, key="selected_date_input", format="DD/MM/YYYY")

# Form Alanı
st.header("Bilgi Girişi")
with st.form("input_form"):
    explanation = st.text_area("Açıklama Giriniz", key="'explanation_input'")
    
    col1, col2 = st.columns(2)
    with col1:
        from_location = st.selectbox("Nereden", options=profil_verileri[selected_profile]['NeredenNereye'])
    with col2:
        to_location = st.selectbox("Nereye", options=profil_verileri[selected_profile]['NeredenNereye'])
    
    col3, col4 = st.columns(2)
    with col3:
        amount = st.text_input("Tutar", key='amount_input')
    with col4:
        category = st.selectbox("Kategori", options=profil_verileri[selected_profile]['Kategori'])
    
    submit_button = st.form_submit_button(label="Kaydet")

with st.expander("Yeni Değer Ekleme"):  
    st.subheader("Yeni Değer Ekleme")

    # Yeni Nereden/Nereye Değeri Ekleme
    new_location = st.text_input("Yeni Nereden/Nereye Değeri Girin", value="", key='new_location_input')
    if st.button("Yeni Nereden/Nereye Değeri Ekle", key='new_location_button') and new_location:
        if new_location not in profil_verileri[selected_profile]['NeredenNereye']:
            profil_verileri[selected_profile]['NeredenNereye'].append(new_location)
            with open(json_file_name, 'w') as f:
                json.dump(profil_verileri, f, indent=4)
            st.success(f"'{new_location}' başarıyla eklendi.")
            st.rerun()
    # Yeni Kategori Değeri Ekleme
    new_category = st.text_input("Yeni Kategori Değeri Girin", value="", key='new_category_input')
    if st.button("Yeni Kategori Ekle", key='new_category_button') and new_category:
        if new_category not in profil_verileri[selected_profile]['Kategori']:
            profil_verileri[selected_profile]['Kategori'].append(new_category)
            with open(json_file_name, 'w') as f:
                json.dump(profil_verileri, f, indent=4)
            st.success(f"'{new_category}' başarıyla eklendi.")
            st.rerun()

# Kaydetme Butonu Tıklandığında
if submit_button:
    st.success("Veriler başarıyla kaydedildi.")
    data = {
        'Profil': [selected_profile],
        'Tarih': [st.session_state.selected_date],
        'Açıklama': [st.session_state['explanation_input']],
        'Nereden': [from_location],
        'Nereye': [to_location],
        'Tutar': [st.session_state['amount_input']],
        'Kategori': [category]
    }
    df = pd.DataFrame(data)
    
    # JSON dosyasını güncelle
    with open(json_file_name, 'w') as f:
        json.dump(profil_verileri, f, indent=4)
    st.write("Kaydedilen Veri:")
    st.dataframe(df)
    
    # CSV dosyasına kaydet
    csv_file_name = f"{selected_profile}.csv"
    if not os.path.exists(csv_file_name):
        df.to_csv(csv_file_name, index=False)
    else:
        df_existing = pd.read_csv(csv_file_name)
        df_combined = pd.concat([df_existing, df], ignore_index=True)
        df_combined.to_csv(csv_file_name, index=False)
    
    # Açıklama ve Tutar alanlarını temizle
    st.session_state.form_submitted = True
    
    # Uygulamayı yeniden çalıştırın
    st.rerun()
