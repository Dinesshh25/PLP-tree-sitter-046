import sys
import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))


# Versi 1: Penelusuran rekursif (DFS)
def jelajah_rekursif(node, kedalaman=0, field=None):
    baris, kolom = node.start_point
    label = f"{field}: " if field else ""
    print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")

    for i, child in enumerate(node.children):
        if child.is_named:
            nama_field = node.field_name_for_child(i)
            jelajah_rekursif(child, kedalaman + 1, nama_field)


# Versi 2 [Pengayaan]: Penelusuran menggunakan TreeCursor
def jelajah_cursor(tree):
    cursor = tree.walk()
    kedalaman = 0
    kembali_dari_anak = False

    while True:
        node = cursor.node
        if not kembali_dari_anak:
            if node.is_named:
                baris, kolom = node.start_point
                field = cursor.field_name
                label = f"{field}: " if field else ""
                print("  " * kedalaman + f"{label}{node.type} [{baris + 1}:{kolom}]")

            if cursor.goto_first_child():
                kedalaman += 1
                kembali_dari_anak = False
                continue

        if cursor.goto_next_sibling():
            kembali_dari_anak = False
        elif cursor.goto_parent():
            kedalaman -= 1
            kembali_dari_anak = True
        else:
            break


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Penggunaan: python jelajah.py <file_python.py> [--cursor]")
        sys.exit(1)

    with open(sys.argv[1], "rb") as f:
        tree = parser.parse(f.read())

    if "--cursor" in sys.argv:
        jelajah_cursor(tree)
    else:
        jelajah_rekursif(tree.root_node)