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
    profil_verileri = json.load(f)

# Seçili profil için JSON verilerini kontrol et
if selected_profile not in profil_verileri:
    profil_verileri[selected_profile] = {
        "Nereden": [],
        "Nereye": [],
        "Kategori": []
    }

with open(json_file_name, 'w') as f:
    json.dump(profil_verileri, f, indent=4)

# Profil Adını Değiştirme
new_name = st.sidebar.text_input("Yeni Profil Adı", value=selected_profile, key='new_name_input')
if st.sidebar.button("Profil Adını Değiştir", key='update_name_button') and new_name:
    index = st.session_state.profiles.index(selected_profile)
    st.session_state.profiles[index] = new_name
    profil_verileri[new_name] = profil_verileri.pop(selected_profile)
    if os.path.exists(f"{selected_profile}.csv"):
        os.rename(f"{selected_profile}.csv", f"{new_name}.csv")
    with open(json_file_name, 'w') as f:
        json.dump(profil_verileri, f, indent=4)
    st.rerun()

# Yeni Profil Ekleme
if st.sidebar.button("Yeni Profil Ekle"):
    new_profile_name = f"Profil {len(st.session_state.profiles) + 1}"
    if new_profile_name not in st.session_state.profiles:
        st.session_state.profiles.append(new_profile_name)
        profil_verileri[new_profile_name] = {
            "Nereden": [],
            "Nereye": [],
            "Kategori": []
        }
        with open(json_file_name, 'w') as f:
            json.dump(profil_verileri, f, indent=4)
        st.rerun()

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
    explanation = st.text_area("Açıklama Giriniz")
    col1, col2 = st.columns(2)
    with col1:
        from_location = st.selectbox("Nereden", options=profil_verileri[selected_profile]['Nereden'])
    with col2:
        to_location = st.selectbox("Nereye", options=profil_verileri[selected_profile]['Nereye'])
    col3, col4 = st.columns(2)
    with col3:
        amount = st.text_input("Tutar")
    with col4:
        category = st.selectbox("Kategori", options=profil_verileri[selected_profile]['Kategori'])
    submit_button = st.form_submit_button(label="Kaydet & Kapat")

# Yeni Değer Ekleme Butonları
st.subheader("Yeni Değer Ekleme")

new_from_location = st.text_input("Yeni Nereden Değeri Girin", value="", key='new_from_location_input')
if st.button("Yeni Nereden Değeri Ekle", key='new_from_location_button') and new_from_location:
    if new_from_location not in profil_verileri[selected_profile]['Nereden']:
        profil_verileri[selected_profile]['Nereden'].append(new_from_location)
        with open(json_file_name, 'w') as f:
            json.dump(profil_verileri, f, indent=4)
        st.success(f"'{new_from_location}' başarıyla eklendi.")
        st.rerun()

new_to_location = st.text_input("Yeni Nereye Değeri Girin", value="", key='new_to_location_input')
if st.button("Yeni Nereye Değeri Ekle", key='new_to_location_button') and new_to_location:
    if new_to_location not in profil_verileri[selected_profile]['Nereye']:
        profil_verileri[selected_profile]['Nereye'].append(new_to_location)
        with open(json_file_name, 'w') as f:
            json.dump(profil_verileri, f, indent=4)
        st.success(f"'{new_to_location}' başarıyla eklendi.")
        st.rerun()

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
        'Açıklama': [explanation],
        'Nereden': [from_location],
        'Nereye': [to_location],
        'Tutar': [amount],
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

    # Formu sıfırla
    st.rerun()
