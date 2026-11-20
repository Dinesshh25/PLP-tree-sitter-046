import json
import math
from datetime import datetime
from pathlib import Path


class ManajemenTugas:
    """Mengelola daftar tugas kuliah dan menghitung progres penyelesaian."""

    def __init__(self, nama_mahasiswa, semester):
        self.nama_mahasiswa = nama_mahasiswa
        self.semester = semester
        self.daftar_tugas = []

    def tambah_tugas(self, judul, mata_kuliah, bobot, estimasi_jam):
        """Menambahkan item tugas baru ke dalam daftar."""
        if bobot <= 0 or estimasi_jam <= 0:
            raise ValueError("Bobot dan estimasi jam harus bernilai positif.")

        tugas = {
            "id": len(self.daftar_tugas) + 1,
            "judul": judul,
            "mata_kuliah": mata_kuliah,
            "bobot": bobot,
            "estimasi_jam": estimasi_jam,
            "selesai": False,
            "dibuat_pada": datetime.now().strftime("%Y-%m-%d"),
        }
        self.daftar_tugas.append(tugas)
        print(f"Tugas ditambahkan: {judul} ({mata_kuliah})")
        return tugas

    def tandai_selesai(self, id_tugas):
        """Menandai tugas berdasarkan ID sebagai selesai."""
        for tugas in self.daftar_tugas:
            if tugas["id"] == id_tugas:
                tugas["selesai"] = True
                print(f"Tugas '{tugas['judul']}' telah selesai.")
                return True
        print(f"Tugas dengan ID {id_tugas} tidak ditemukan.")
        return False

    def hitung_persentase_selesai(self):
        """Menghitung persentase penyelesaian berdasarkan bobot tugas."""
        if not self.daftar_tugas:
            return 0.0

        total_bobot = sum(item["bobot"] for item in self.daftar_tugas)
        bobot_selesai = sum(
            item["bobot"] for item in self.daftar_tugas if item["selesai"]
        )
        persentase = (bobot_selesai / total_bobot) * 100
        return round(persentase, 2)

    def estimasi_hari_kerja(self, jam_per_hari=3):
        """Menghitung sisa hari yang dibutuhkan untuk tugas yang belum selesai."""
        sisa_jam = sum(
            item["estimasi_jam"]
            for item in self.daftar_tugas
            if not item["selesai"]
        )
        if sisa_jam == 0:
            return 0
        return math.ceil(sisa_jam / jam_per_hari)

    def filter_per_matkul(self, nama_matkul):
        """Mengambil daftar tugas berdasarkan nama mata kuliah."""
        hasil = []
        for tugas in self.daftar_tugas:
            if tugas["mata_kuliah"].lower() == nama_matkul.lower():
                hasil.append(tugas)
        return hasil

    def simpan_ke_json(self, nama_file):
        """Menyimpan seluruh data tugas ke berkas JSON."""
        data = {
            "mahasiswa": self.nama_mahasiswa,
            "semester": self.semester,
            "progres_persen": self.hitung_persentase_selesai(),
            "tugas": self.daftar_tugas,
        }
        jalur = Path(nama_file)
        jalur.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(f"Data berhasil disimpan ke {jalur}")


def jalankan_simulasi():
    """Menjalankan simulasi pengelolaan tugas untuk pengujian."""
    pengelola = ManajemenTugas("Mahasiswa TI", 3)
    pengelola.tambah_tugas("Tugas 1: Membaca Pohon", "PLP", 10, 2)
    pengelola.tambah_tugas("Tugas 2: Penjelajah Node", "PLP", 15, 3)
    pengelola.tambah_tugas("Tugas 3: Query Pertama", "PLP", 15, 3)
    pengelola.tambah_tugas("Laporan Basis Data", "Basis Data", 20, 5)

    pengelola.tandai_selesai(1)
    pengelola.tandai_selesai(2)

    progres = pengelola.hitung_persentase_selesai()
    sisa_hari = pengelola.estimasi_hari_kerja(jam_per_hari=2)
    tugas_plp = pengelola.filter_per_matkul("PLP")

    print(f"Total tugas PLP: {len(tugas_plp)}")
    print(f"Progres saat ini: {progres}%")
    print(f"Estimasi sisa hari: {sisa_hari} hari")

    try:
        pengelola.simpan_ke_json("ringkasan_tugas.json")
    except OSError as err:
        print(f"Gagal menyimpan berkas: {err}")


if __name__ == "__main__":
    jalankan_simulasi()