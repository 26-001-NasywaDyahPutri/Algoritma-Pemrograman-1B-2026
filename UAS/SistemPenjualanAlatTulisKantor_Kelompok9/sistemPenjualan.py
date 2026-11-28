# Dictionary untuk menyimpan akun
akun = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"}
}

# List berisi dictionary produk
produk = [
    {"id": 1, "nama": "Pulpen", "harga": 3000, "stok": 50},
    {"id": 2, "nama": "Buku Tulis", "harga": 5000, "stok": 40},
    {"id": 3, "nama": "Pensil", "harga": 2000, "stok": 60},
    {"id": 4, "nama": "Penghapus", "harga": 1500, "stok": 30},
    {"id": 5, "nama": "Penggaris", "harga": 4000, "stok": 25}
]

# Tuple: pilihan role yang tersedia
ROLES = ("admin", "user")

# Set: menyimpan kategori unik
kategori_produk = {"Alat Tulis", "Buku", "Perlengkapan"}

# Dictionary keranjang belanja
keranjang = {}

# ---------- FUNCTION VALIDASI ----------

def input_angka(pesan):
    """Validasi input agar harus berupa angka."""
    while True:
        try:
            angka = int(input(pesan))
            if angka >= 0:
                return angka
            else:
                print("Input tidak boleh negatif!")
        except ValueError:
            print("Input harus berupa angka!")


def input_teks(pesan):
    """Validasi teks agar tidak kosong."""
    while True:
        teks = input(pesan).strip()
        if teks != "":
            return teks
        print("Input tidak boleh kosong!")


def cari_produk(id_produk):
    """Mencari produk berdasarkan ID."""
    for item in produk:
        if item["id"] == id_produk:
            return item
    return None


# ---------- FUNCTION MENAMPILKAN PRODUK ----------

def tampilkan_produk():
    print("\n========== DAFTAR PRODUK ATK ==========")

    if len(produk) == 0:
        print("Belum ada produk.")
        return

    print("-" * 55)
    print(f"{'ID':<5} {'Nama':<20} {'Harga':<15} {'Stok':<10}")
    print("-" * 55)

    for item in produk:
        print(
            f"{item['id']:<5} "
            f"{item['nama']:<20} "
            f"Rp{item['harga']:<13} "
            f"{item['stok']:<10}"
        )

    print("-" * 55)


# ---------- CRUD ADMIN ----------

def tambah_produk():
    print("\n--- TAMBAH PRODUK ---")

    id_produk = max([p["id"] for p in produk], default=0) + 1
    nama = input_teks("Nama produk: ")
    harga = input_angka("Harga produk: Rp")
    stok = input_angka("Jumlah stok: ")

    produk_baru = {
        "id": id_produk,
        "nama": nama,
        "harga": harga,
        "stok": stok
    }

    produk.append(produk_baru)

    print("Produk berhasil ditambahkan!")


def ubah_produk():
    tampilkan_produk()

    id_produk = input_angka("Masukkan ID produk yang ingin diubah: ")
    item = cari_produk(id_produk)

    if item is None:
        print("Produk tidak ditemukan!")
        return

    print("Kosongkan input jika tidak ingin mengubahnya.")

    nama_baru = input("Nama baru: ").strip()
    if nama_baru != "":
        item["nama"] = nama_baru

    harga_baru = input("Harga baru: Rp").strip()
    if harga_baru != "":
        item["harga"] = harga_baru

    stok_baru = input("Stok baru: ").strip()
    if stok_baru != "":
        item["stok"] = stok_baru

    print("Produk berhasil diperbarui!")


def hapus_produk():
    tampilkan_produk()

    id_produk = input_angka("Masukkan ID produk yang akan dihapus: ")
    item = cari_produk(id_produk)

    if item is None:
        print("Produk tidak ditemukan!")
        return

    konfirmasi = input(
        f"Yakin menghapus {item['nama']}? (y/n): "
    ).lower()

    if konfirmasi == "y":
        produk.remove(item)

        # Hapus produk dari keranjang jika ada
        if id_produk in keranjang:
            del keranjang[id_produk]

        print("Produk berhasil dihapus!")
    else:
        print("Penghapusan dibatalkan.")


# ---------- MENU ADMIN ----------

def menu_admin():
    while True:
        print("\n========== MENU ADMIN ==========")
        print("1. Lihat produk")
        print("2. Tambah produk")
        print("3. Ubah produk")
        print("4. Hapus produk")
        print("5. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_produk()
        elif pilihan == "2":
            tambah_produk()
        elif pilihan == "3":
            ubah_produk()
        elif pilihan == "4":
            hapus_produk()
        elif pilihan == "5":
            print("Admin berhasil logout.")
            break
        else:
            print("Pilihan tidak valid!")


# ---------- KERANJANG USER ----------

def tampilkan_keranjang():
    print("\n========== KERANJANG ==========")

    if len(keranjang) == 0:
        print("Keranjang masih kosong.")
        return

    total = 0

    print("-" * 80)
    print(f"{'ID_Barang':<15} {'Nama':<20} {'Harga':<12} {'Jumlah':<10} {'Subtotal'}")
    print("-" * 80)

    for id_produk, jumlah in keranjang.items():
        item = cari_produk(id_produk)

        if item is not None:
            subtotal = item["harga"] * jumlah
            total += subtotal

            print(
                f"{id_produk:<15} "
                f"{item['nama']:<20} "
                f"Rp{item['harga']:<10,} "
                f"{jumlah:<10} "
                f"Rp{subtotal:,}"
            )

    print("-" * 80)
    print(f"Total belanja: Rp{total:,}")


def tambah_keranjang():
    tampilkan_produk()

    id_produk = input_angka("Masukkan ID produk: ")
    item = cari_produk(id_produk)

    if item is None:
        print("Produk tidak ditemukan!")
        return

    jumlah = input_angka("Jumlah barang: ")

    if jumlah == 0:
        print("Jumlah harus lebih dari 0!")
        return

    jumlah_di_keranjang = keranjang.get(id_produk, 0)
    total_jumlah = jumlah_di_keranjang + jumlah

    # Validasi stok
    if total_jumlah > item["stok"]:
        print("Stok tidak mencukupi!")
        print(f"Stok tersedia: {item['stok']}")
        return

    # Dictionary keranjang
    keranjang[id_produk] = total_jumlah

    print(f"{item['nama']} berhasil ditambahkan ke keranjang!")


def hapus_keranjang():
    tampilkan_keranjang()

    if len(keranjang) == 0:
        return

    id_produk = input_angka("Masukkan ID produk yang ingin dihapus: ")

    if id_produk not in keranjang:
        print("Produk tidak ada di keranjang!")
        return

    del keranjang[id_produk]
    print("Produk berhasil dihapus dari keranjang!")


# ---------- PEMBAYARAN ----------

def pembayaran():
    if len(keranjang) == 0:
        print("Keranjang kosong! Silakan belanja terlebih dahulu.")
        return

    tampilkan_keranjang()

    total = 0

    # Menghitung total menggunakan operator aritmatika
    for id_produk, jumlah in keranjang.items():
        item = cari_produk(id_produk)

        if item is not None:
            total += item["harga"] * jumlah

    print("\n========== PEMBAYARAN ==========")
    print(f"Total belanja : Rp{total:,}")

    while True:
        uang = input_angka("Uang pembayaran: Rp")

        if uang < total:
            print("Uang pembayaran kurang!")
            print(f"Kekurangan: Rp{total - uang:,}")
        else:
            break

    # Operator pengurangan untuk menghitung kembalian
    kembalian = uang - total

    # Mengurangi stok produk
    for id_produk, jumlah in keranjang.items():
        item = cari_produk(id_produk)

        if item is not None:
            item["stok"] -= jumlah

    print("\n" + "=" * 40)
    print("          STRUK PEMBAYARAN")
    print("       TOKO ALAT TULIS KANTOR")
    print("=" * 40)

    print(f"{'Total Belanja':<20}: Rp{total:>12,}")
    print(f"{'Uang Pembayaran':<20}: Rp{uang:>12,}")
    print(f"{'Kembalian':<20}: Rp{kembalian:>12,}")

    print("-" * 40)
    print("         PEMBAYARAN BERHASIL!")
    print("     Terima kasih telah berbelanja")
    print("           Selamat datang kembali!")
    print("=" * 40)

    # print("\n========== STRUK PEMBAYARAN ==========")
    # print(f"Total belanja : Rp{total:,}")
    # print(f"Uang pembayaran: Rp{uang:,}")
    # print(f"Kembalian     : Rp{kembalian:,}")
    # print("Pembayaran berhasil!")
    # print("Terima kasih telah berbelanja.")

    # Mengosongkan keranjang setelah transaksi
    keranjang.clear()


# ---------- MENU USER ----------

def menu_user():
    while True:
        print("\n========== MENU USER ==========")
        print("1. Lihat daftar produk")
        print("2. Tambah barang ke keranjang")
        print("3. Lihat keranjang")
        print("4. Hapus barang dari keranjang")
        print("5. Pembayaran / Checkout")
        print("6. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkan_produk()
        elif pilihan == "2":
            tambah_keranjang()
        elif pilihan == "3":
            tampilkan_keranjang()
        elif pilihan == "4":
            hapus_keranjang()
        elif pilihan == "5":
            pembayaran()
        elif pilihan == "6":
            print("User berhasil logout.")
            break
        else:
            print("Pilihan tidak valid!")


# ---------- AUTENTIKASI ----------

def login():
    print("\n========== LOGIN ==========")

    username = input_teks("Username: ")
    password = input_teks("Password: ")

    if username in akun:
        if akun[username]["password"] == password:
            role = akun[username]["role"]

            # Tuple digunakan untuk validasi role
            if role in ROLES:
                print(f"\nLogin berhasil! Selamat datang {username}.")

                if role == "admin":
                    menu_admin()
                elif role == "user":
                    menu_user()

            else:
                print("Role tidak valid!")
        else:
            print("Password salah!")
    else:
        print("Username tidak ditemukan!")


# ---------- PROGRAM UTAMA ----------

def main():
    while True:
        print("\n====================================")
        print("   SISTEM PENJUALAN ATK")
        print("====================================")
        print("1. Login")
        print("2. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            login()
        elif pilihan == "2":
            print("Program selesai. Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!")


# Menjalankan program
if __name__ == "__main__":
    main()
