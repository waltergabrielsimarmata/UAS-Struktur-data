import csv
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# -----------------------------
# NODE UNTUK LINKED LIST
# -----------------------------

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node

    def to_list(self):
        result = []
        curr = self.head
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def find_by_code(self, kode):
        curr = self.head
        while curr:
            if curr.data["kode"] == kode:
                return curr
            curr = curr.next
        return None

    def delete_by_code(self, kode):
        curr = self.head
        prev = None
        while curr:
            if curr.data["kode"] == kode:
                if prev:
                    prev.next = curr.next
                else:
                    self.head = curr.next
                return True
            prev = curr
            curr = curr.next
        return False

# Stack
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, data):
        self.stack.append(data)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        else:
            return None

    def is_empty(self):
        return len(self.stack) == 0

# -----------------------------
# FUNGSI CRUD CSV
# -----------------------------

def load_data(filename):
    produk_list = LinkedList()
    try:
        with open(filename, mode="r", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["stok"] = int(row["stok"])
                row["harga"] = int(row["harga"])
                produk_list.append(row)
    except FileNotFoundError:
        pass
    return produk_list

def simpan_data(filename, produk_list):
    with open(filename, mode="w", newline='', encoding='utf-8') as f:
        fieldnames = ["kode", "nama_produk", "stok", "harga"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for data in produk_list.to_list():
            writer.writerow(data)

def load_penjualan(filename):
    penjualan_list = LinkedList()
    try:
        with open(filename, mode="r", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["jumlah"] = int(row["jumlah"])
                row["total"] = int(row["total"])
                row["tanggal"] = datetime.datetime.strptime(row["tanggal"], "%Y-%m-%d").date()
                penjualan_list.append(row)
    except FileNotFoundError:
        pass
    return penjualan_list

def simpan_penjualan(filename, penjualan_list):
    with open(filename, mode="w", newline='', encoding='utf-8') as f:
        fieldnames = ["kode", "nama_produk", "jumlah", "total", "tanggal"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for data in penjualan_list.to_list():
            data_copy = dict(data)
            data_copy["tanggal"] = data_copy["tanggal"].strftime("%Y-%m-%d")
            writer.writerow(data_copy)

# -----------------------------
# APLIKASI TKINTER
# -----------------------------

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Manajemen Stok Toko")
        self.root.geometry("500x600")
        self.root.resizable(False, False)

        self.file_produk = "produk.csv"
        self.file_penjualan = "penjualan.csv"

        self.produk_list = load_data(self.file_produk)
        self.penjualan_list = load_penjualan(self.file_penjualan)
        self.stack_penjualan = Stack()

        # Frame utama
        main_frame = ttk.Frame(root, padding=(20, 20))
        main_frame.pack(fill="both", expand=True)

        # Judul
        title_label = ttk.Label(
            main_frame,
            text="Manajemen Stok Toko",
            font=("Helvetica", 18, "bold")
        )
        title_label.pack(pady=(0, 20))

        # Frame tombol
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack()

        buttons = [
            ("Tambah Produk", self.tambah_produk),
            ("Lihat Produk", self.lihat_produk),
            ("Update Produk", self.update_produk),
            ("Hapus Produk", self.hapus_produk),
            ("Cari Produk", self.cari_produk),
            ("Catat Penjualan", self.catat_penjualan),
            ("Undo Penjualan", self.undo_penjualan),
            ("Laporan Penjualan", self.laporan_penjualan),
            ("Simpan ke CSV", self.simpan_csv),
            ("Keluar", self.keluar)
        ]

        # Buat tombol dalam grid, 2 kolom
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(buttons_frame, text=text, width=25, command=command)
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        buttons_frame.columnconfigure(0, weight=1)
        buttons_frame.columnconfigure(1, weight=1)

    def tambah_produk(self):
        kode = simpledialog.askstring("Input", "Kode produk:")
        if not kode:
            return
        nama = simpledialog.askstring("Input", "Nama produk:")
        if not nama:
            return
        stok = self.ask_integer("Stok:")
        harga = self.ask_integer("Harga:")

        new_data = {
            "kode": kode,
            "nama_produk": nama,
            "stok": stok,
            "harga": harga
        }
        self.produk_list.append(new_data)
        messagebox.showinfo("Info", "Produk berhasil ditambahkan.")

    def lihat_produk(self):
        top = tk.Toplevel(self.root)
        top.title("Data Produk")

        cols = ("Kode", "Nama Produk", "Stok", "Harga")
        tree = ttk.Treeview(top, columns=cols, show="headings")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill="both", expand=True)

        data = self.produk_list.to_list()
        for d in data:
            tree.insert("", "end", values=(
                d["kode"], d["nama_produk"], d["stok"], d["harga"]
            ))

    def update_produk(self):
        kode = simpledialog.askstring("Input", "Masukkan kode produk yang akan diupdate:")
        if not kode:
            return
        node = self.produk_list.find_by_code(kode)
        if node:
            nama = simpledialog.askstring("Input", "Nama produk baru (kosong jika tidak diubah):")
            stok = simpledialog.askstring("Input", "Stok baru (kosong jika tidak diubah):")
            harga = simpledialog.askstring("Input", "Harga baru (kosong jika tidak diubah):")

            if nama:
                node.data["nama_produk"] = nama
            if stok:
                node.data["stok"] = int(stok)
            if harga:
                node.data["harga"] = int(harga)

            messagebox.showinfo("Info", "Data produk berhasil diupdate.")
        else:
            messagebox.showwarning("Peringatan", "Produk tidak ditemukan.")

    def hapus_produk(self):
        kode = simpledialog.askstring("Input", "Masukkan kode produk yang akan dihapus:")
        if not kode:
            return
        result = self.produk_list.delete_by_code(kode)
        if result:
            messagebox.showinfo("Info", "Produk berhasil dihapus.")
        else:
            messagebox.showwarning("Peringatan", "Produk tidak ditemukan.")

    def cari_produk(self):
        keyword = simpledialog.askstring("Input", "Masukkan kata kunci pencarian:")
        if not keyword:
            return
        keyword = keyword.lower()

        found = False
        data = self.produk_list.to_list()
        result = []
        for d in data:
            if keyword in d["kode"].lower() or keyword in d["nama_produk"].lower():
                found = True
                result.append(d)

        if found:
            top = tk.Toplevel(self.root)
            top.title("Hasil Pencarian")

            cols = ("Kode", "Nama Produk", "Stok", "Harga")
            tree = ttk.Treeview(top, columns=cols, show="headings")
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            tree.pack(fill="both", expand=True)

            for d in result:
                tree.insert("", "end", values=(
                    d["kode"], d["nama_produk"], d["stok"], d["harga"]
                ))
        else:
            messagebox.showinfo("Hasil", "Data tidak ditemukan.")

    def catat_penjualan(self):
        kode = simpledialog.askstring("Input", "Masukkan kode produk yang dijual:")
        if not kode:
            return
        node = self.produk_list.find_by_code(kode)
        if node:
            jumlah = self.ask_integer("Jumlah yang dijual:")
            if jumlah > node.data["stok"]:
                messagebox.showerror("Error", "Stok tidak cukup!")
                return
            node.data["stok"] -= jumlah
            total = jumlah * node.data["harga"]

            data_penjualan = {
                "kode": kode,
                "nama_produk": node.data["nama_produk"],
                "jumlah": jumlah,
                "total": total,
                "tanggal": datetime.date.today()
            }
            self.penjualan_list.append(data_penjualan)
            self.stack_penjualan.push((kode, jumlah))
            messagebox.showinfo("Info", f"Penjualan berhasil dicatat. Total: {total}")
        else:
            messagebox.showwarning("Peringatan", "Produk tidak ditemukan.")

    def undo_penjualan(self):
        last = self.stack_penjualan.pop()
        if last:
            kode, jumlah = last
            node = self.produk_list.find_by_code(kode)
            if node:
                node.data["stok"] += jumlah

                prev = None
                curr = self.penjualan_list.head
                while curr:
                    if curr.data["kode"] == kode and curr.data["jumlah"] == jumlah:
                        if prev:
                            prev.next = curr.next
                        else:
                            self.penjualan_list.head = curr.next
                        messagebox.showinfo("Info", f"Undo berhasil. Stok {kode} dikembalikan sebanyak {jumlah}.")
                        return
                    prev = curr
                    curr = curr.next
                messagebox.showwarning("Peringatan", "Data penjualan tidak ditemukan saat undo.")
            else:
                messagebox.showwarning("Peringatan", "Produk tidak ditemukan saat undo.")
        else:
            messagebox.showinfo("Info", "Tidak ada data penjualan yang dapat di-undo.")

    def laporan_penjualan(self):
        pilihan = simpledialog.askinteger("Laporan", "Pilih laporan:\n1. Harian\n2. Mingguan\n3. Bulanan")
        if pilihan not in [1, 2, 3]:
            messagebox.showerror("Error", "Pilihan tidak valid.")
            return

        data = self.penjualan_list.to_list()
        if not data:
            messagebox.showinfo("Info", "Belum ada data penjualan.")
            return

        today = datetime.date.today()
        if pilihan == 1:
            filtered = [d for d in data if d["tanggal"] == today]
            label = f"Harian ({today})"
        elif pilihan == 2:
            start_week = today - datetime.timedelta(days=today.weekday())
            end_week = start_week + datetime.timedelta(days=6)
            filtered = [d for d in data if start_week <= d["tanggal"] <= end_week]
            label = f"Mingguan ({start_week} s/d {end_week})"
        elif pilihan == 3:
            filtered = [d for d in data if d["tanggal"].month == today.month and d["tanggal"].year == today.year]
            label = f"Bulanan ({today.strftime('%B %Y')})"

        if not filtered:
            messagebox.showinfo("Info", f"Tidak ada penjualan untuk laporan {label}.")
        else:
            top = tk.Toplevel(self.root)
            top.title(f"Laporan Penjualan {label}")
            cols = ("Kode", "Nama Produk", "Jumlah", "Total", "Tanggal")
            tree = ttk.Treeview(top, columns=cols, show="headings")
            for col in cols:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            tree.pack(fill="both", expand=True)

            for d in filtered:
                tree.insert("", "end", values=(
                    d["kode"], d["nama_produk"], d["jumlah"], d["total"],
                    d["tanggal"].strftime("%Y-%m-%d")
                ))

    def simpan_csv(self):
        simpan_data(self.file_produk, self.produk_list)
        simpan_penjualan(self.file_penjualan, self.penjualan_list)
        messagebox.showinfo("Info", "Data berhasil disimpan ke CSV.")

    def keluar(self):
        self.simpan_csv()
        self.root.quit()

    def ask_integer(self, prompt):
        while True:
            val = simpledialog.askstring("Input", prompt)
            if val is None:
                return 0
            try:
                return int(val)
            except ValueError:
                messagebox.showerror("Error", "Input harus angka!")

# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
