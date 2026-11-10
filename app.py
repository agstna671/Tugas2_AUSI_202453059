import streamlit as st
import pandas as pd

# Konfigurasi Halaman Web
st.set_page_config(page_title="Form Audit SI COBIT 5", layout="wide")

# Header Asli Tugas 1
st.title("Form Audit Sistem Informasi COBIT 5")
st.subheader("PT RodaLink Indonesia (Rodalink Kudus)")
st.write("**Objek Audit:** Pengelolaan Sistem Informasi untuk Mendukung Penjualan dan Persediaan")
st.info("Aplikasi prototipe untuk pembelajaran. Hasil pengisian bukan hasil audit resmi perusahaan.")
st.caption("Disusun oleh: Agustina Rahmatika Sari (NIM: 202453059) | Kelas A")
st.markdown("---")

# 1. Identitas Audit
st.header("1. Identitas Audit")
col1, col2 = st.columns(2)
with col1:
    nama_auditor = st.text_input("Nama Auditor", value="Agustina Rahmatika Sari")
    nim_auditor = st.text_input("NIM Auditor", value="202453059")
with col2:
    nama_responden = st.text_input("Nama Responden", value="")
    unit_kerja = st.text_input("Bagian atau Unit Kerja", value="")

st.markdown("---")
st.header("2. Form Instrumen Audit Sistem Informasi")

# Data 10 Pertanyaan dari Form Tugas 1
daftar_pertanyaan = [
    {"No": 1, "Domain": "EDM", "Pertanyaan": "Apakah penggunaan teknologi informasi diawasi oleh pihak yang bertanggung jawab?", "Bukti": "Dokumen pengawasan, pembagian tanggung jawab, atau catatan evaluasi TI.", "Target": 4},
    {"No": 2, "Domain": "EDM", "Pertanyaan": "Apakah manfaat dan risiko penggunaan teknologi informasi dievaluasi secara berkala?", "Bukti": "Dokumen evaluasi, laporan risiko, atau notulen rapat terkait TI.", "Target": 4},
    {"No": 3, "Domain": "APO", "Pertanyaan": "Apakah terdapat perencanaan penggunaan teknologi informasi untuk mendukung kegiatan operasional?", "Bukti": "Rencana kerja TI, rencana operasional, atau dokumen perencanaan terkait.", "Target": 4},
    {"No": 4, "Domain": "APO", "Pertanyaan": "Apakah pengelolaan hak akses terhadap data perusahaan telah diatur?", "Bukti": "Kebijakan keamanan informasi, SOP hak akses, atau daftar kewenangan pengguna.", "Target": 4},
    {"No": 5, "Domain": "BAI", "Pertanyaan": "Apakah perubahan atau pembaruan sistem informasi diuji sebelum digunakan?", "Bukti": "Dokumentasi pengujian sistem, catatan perubahan, atau persetujuan penerapan.", "Target": 3},
    {"No": 6, "Domain": "BAI", "Pertanyaan": "Apakah pengguna memperoleh panduan penggunaan sistem informasi yang diterapkan?", "Bukti": "Panduan penggunaan, SOP, materi pelatihan, atau dokumentasi sosialisasi.", "Target": 4},
    {"No": 7, "Domain": "DSS", "Pertanyaan": "Apakah terdapat prosedur penanganan gangguan sistem informasi?", "Bukti": "SOP penanganan gangguan, catatan insiden, atau dokumentasi tindak lanjut.", "Target": 4},
    {"No": 8, "Domain": "DSS", "Pertanyaan": "Apakah pencadangan data penting dilakukan secara berkala?", "Bukti": "Jadwal pencadangan, catatan backup, atau laporan keberhasilan pencadangan.", "Target": 4},
    {"No": 9, "Domain": "MEA", "Pertanyaan": "Apakah kinerja sistem informasi dipantau secara berkala?", "Bukti": "Laporan pemantauan, catatan pemeriksaan, atau laporan kinerja sistem.", "Target": 3},
    {"No": 10, "Domain": "MEA", "Pertanyaan": "Apakah pengelolaan sistem informasi dievaluasi untuk mengetahui hal yang perlu diperbaiki?", "Bukti": "Laporan evaluasi, catatan temuan, atau dokumentasi tindakan perbaikan.", "Target": 4}
]

# Konversi Jawaban Form menjadi Skor Kematangan
skor_map = {
    "Ya": 4,
    "Tidak Diketahui": 2,
    "Tidak": 1
}

# Form Input Pertanyaan
jawaban_user = []

with st.form(key="form_audit_cobit_5"):
    st.write("Silakan isi instrumen audit berdasarkan kondisi riil dan bukti yang ada:")
    
    for item in daftar_pertanyaan:
        st.write(f"**{item['No']}. Domain {item['Domain']}**")
        st.write(f"**Pertanyaan:** {item['Pertanyaan']}")
        st.caption(f"Bukti yang diharapkan: {item['Bukti']}")
        
        pilihan = st.radio(
            f"Jawaban Soal {item['No']}:",
            options=["Ya", "Tidak", "Tidak Diketahui"],
            index=0,
            key=f"q_{item['No']}",
            horizontal=True
        )
        catatan = st.text_input(f"Keterangan / Bukti Tambahan (Soal {item['No']}):", key=f"c_{item['No']}")
        st.write("---")
        
        jawaban_user.append({
            "No": item["No"],
            "Domain": item["Domain"],
            "Pertanyaan": item["Pertanyaan"],
            "Jawaban": pilihan,
            "Nilai_Current": skor_map[pilihan],
            "Target": item["Target"],
            "Keterangan/Bukti": catatan
        })
    
    btn_submit = st.form_submit_button(label="Simpan Hasil Audit & Tampilkan Grafik")

# 3. HASIL DAN GRAFIK (Muncul SETELAH tombol diklik)
if btn_submit:
    st.success(f"Data Hasil Audit untuk Responden '{nama_responden}' ({unit_kerja}) Berhasil Disimpan!")
    
    df_hasil = pd.DataFrame(jawaban_user)
    
    st.markdown("---")
    st.header("3. Hasil Pengisian & Grafik Analisis Gap Audit")
    
    tab_tabel, tab_grafik = st.tabs(["Ringkasan Hasil Audit", "Grafik & Selisih Gap"])
    
    with tab_tabel:
        st.subheader("Tabel Detail Hasil Pengisian Instrumen Audit")
        st.dataframe(df_hasil[["No", "Domain", "Pertanyaan", "Jawaban", "Nilai_Current", "Target", "Keterangan/Bukti"]], use_container_width=True)
    
    with tab_grafik:
        st.subheader("Analisis Perbandingan Level (Current vs Target)")
        rekap = df_hasil.groupby("Domain")[["Nilai_Current", "Target"]].mean()
        rekap["Gap"] = rekap["Target"] - rekap["Nilai_Current"]
        
        st.bar_chart(rekap[["Nilai_Current", "Target"]], stack=False)
        
        st.subheader("Tabel Analisis Gap per Domain")
        st.dataframe(rekap, use_container_width=True)