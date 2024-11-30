import streamlit as st
import pandas as pd
import datetime

# Sayfa Yapısı ve Ayarlar
st.set_page_config(page_title="Geliştirilmiş Arayüz Tasarımı", layout="wide")

# Profil Listesi
st.sidebar.header("Profiller")


import os

if 'profiles' not in st.session_state:
    csv_files = [f.split('.')[0] for f in os.listdir('.') if f.endswith('.csv')]
    st.session_state.profiles = csv_files if csv_files else ["Profil 1"]
selected_profile = st.sidebar.radio("Bir profil seçiniz:", st.session_state.profiles)

if st.sidebar.button("Profil Adını Değiştir"):
    if selected_profile:
        new_name = st.sidebar.text_input("Yeni Profil Adı", value=selected_profile, key='new_name_input')
        update_name = st.sidebar.button("Adı Güncelle", key='update_name_button')
        if update_name:
            index = st.session_state.profiles.index(selected_profile)
            st.session_state.profiles[index] = new_name
            st.experimental_rerun()
            index = st.session_state.profiles.index(selected_profile)
            st.session_state.profiles[index] = new_name

if st.sidebar.button("Yeni Profil Ekle"):
    new_profile_name = f"Profil {len(st.session_state.profiles) + 1}"
    st.session_state.profiles.append(new_profile_name)

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
        from_location = st.selectbox("Nereden", options=["X", "Y", "Z", "Yeni Ekle"], key='from_location_select')
        if from_location == "Yeni Ekle":
            from_location = st.text_input("Yeni Nereden Giriniz", key='new_from_location')
    with col2:
        to_location = st.selectbox("Nereye", options=["X", "Y", "Z", "Yeni Ekle"], key='to_location_select')
        if to_location == "Yeni Ekle":
            to_location = st.text_input("Yeni Nereye Giriniz", key='new_to_location')
    col3, col4 = st.columns(2)
    with col3:
        amount = st.text_input("Tutar")
    with col4:
        category = st.selectbox("Kategori Seçiniz", options=["Kategori A", "Kategori B", "Kategori C", "Yeni Ekle"], key='category_select')
        if category == "Yeni Ekle":
            category = st.text_input("Yeni Kategori Giriniz", key='new_category')
    submit_button = st.form_submit_button(label="Kaydet & Kapat")

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
    st.write("Kaydedilen Veri:")
    st.dataframe(df)
    
    # CSV dosyasına kaydet
    csv_file_name = f"{selected_profile}.csv"
    if not os.path.exists(csv_file_name):
        df.to_csv(csv_file_name, index=False)
    else:
        df_existing = pd.read_csv(csv_file_name)
        df_combined = pd.concat([df_existing, df])
        df_combined.to_csv(csv_file_name, index=False)
