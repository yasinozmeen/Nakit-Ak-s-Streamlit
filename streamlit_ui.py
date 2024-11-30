import streamlit as st
import pandas as pd
import datetime
import os

# Sayfa Yapısı ve Ayarlar
st.set_page_config(page_title="Geliştirilmiş Arayüz Tasarımı", layout="wide")

# Profil Listesi
st.sidebar.header("Profiller")

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
        from_location = st.text_input("Nereden")
    with col2:
        to_location = st.text_input("Nereye")
    col3, col4 = st.columns(2)
    with col3:
        amount = st.text_input("Tutar")
    with col4:
        category = st.selectbox("Kategori Seçiniz", ["Kategori 1", "Kategori 2", "Kategori 3"])
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
    if os.path.exists(csv_file_name):
        try:
            # CSV dosyasının boş olup olmadığını kontrol et
            if os.path.getsize(csv_file_name) > 0:
                df_existing = pd.read_csv(csv_file_name)
                df_combined = pd.concat([df_existing, df], ignore_index=True)
            else:
                df_combined = df
            df_combined.to_csv(csv_file_name, index=False)
        except Exception as e:
            st.error(f"Mevcut dosya okunurken bir hata oluştu: {e}")
            df.to_csv(csv_file_name, index=False)
    else:
        df.to_csv(csv_file_name, index=False)