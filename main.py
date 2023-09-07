import os
import re
from unicodedata import normalize
import zipfile
import config as cfg
import datetime as dt

URL_ELO_FIDE = "http://ratings.fide.com/download/players_list.zip"
PATH_ZIP = "./assets/zips/"
FILE_ZIP = "players_list.zip"
FILE_UNZIP = "players_list_foa.txt"
PATH_DOCS = "./assets/docs/"
FILENAME_AGORA = "./assets/docs/agora_members.txt"
FILENAME_AGORA_CLEANED = "./assets/docs/agora_members_clean.txt"
FILENAME_ELO_FIDE = "./assets/docs/players_list_foa.txt"
FILENAME_AGORA_ELO = "./assets/docs/agora_members_ELO.txt"

# MODES
# r: open an existing file for a read operation.
# w: open an existing file for a write operation. If the file already contains some data then it will be overridden but if the file is not present then it creates the file as well.
# a:  open an existing file for append operation. It won’t override existing data.
#  r+:  To read and write data into the file. The previous data in the file will be overridden.
# w+: To write and read data. It will override existing data.
# a+: To append and read data from the file. It won’t override existing data.


def write_file(filename, content):
    try:
        with open(filename, "w") as f:
            f.write(content)
        print("File " + filename + " written successfully.\n")
    except IOError:
        print("Error: could not write in the file " + filename + "\n")


def load_file(filename):
    contents = ""
    try:
        with open(filename, "r", encoding="utf8") as f:
            contents = f.read()
    except IOError:
        print("Error: could not read file " + filename + "\n")
    return contents


def read_file(filename):
    try:
        with open(filename, "r", encoding="utf8") as f:
            contents = f.read()
            print(contents + "\n")
    except IOError:
        print("Error: could not read file " + filename + "\n")


def clean_file(_filename, _destination):
    s = load_file(_filename)
    # for line in temp_file:
    # -> NFD y eliminar diacríticos
    s = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+",
        r"\1",
        normalize("NFD", s),
        0,
        re.I,
    )

    # -> NFC
    s = normalize("NFC", s)
    # -> Eliminar caracteres especiales
    s = re.sub(r"[^a-zA-Z\n ]", "", s)
    # -> Eliminar espacios en blanco
    _s = ""
    for line in s.split("\n"):
        _s = _s + "\n" + " ".join(line.split())
    s = _s[1:]
    write_file(_destination, s)


def getAgoraMembersELO(_agora_members, _elo_fide):
    agora_clean = load_file(_agora_members)
    foa_ELO_Fide = "\n".join(load_file(_elo_fide).split("\n"))
    result = ""
    for line in foa_ELO_Fide.split("\n"):
        lastName = " ".join(line.split(",")[0].split()[1:])
        if lastName.upper() in agora_clean:
            if len(line.split(",")) > 1:
                name = " ".join(line.split(",")[1].split()[:1])
                if name.upper() in agora_clean:
                    result = result + "\n" + line
            else:
                result = result + "\n" + line

    return result


def isUpdateNeeded():
    cfg_date = dt.datetime(
        *map(int, cfg.get_INTERNAL_CONFIG("lastUpdate_ELO_FIDE").split("-"))
    )
    now = dt.datetime.now()
    fide_update_date = dt.datetime(now.year, now.month, 1)

    return cfg_date <= fide_update_date


def send_email(subject, message):
    # Code to send an email using an email sending service or library
    password = input("\tType your password and press enter: ")

    print("\tpassword: " + password)
    pass


def download_ELO_FIDE():
    if not isUpdateNeeded():
        print("\tNo need to update '" + FILE_UNZIP + "' file.")
    else:
        print("\tUpdating '" + FILE_UNZIP + "' file..")

        retry_count = 0
        max_retries = 3

        while retry_count < max_retries:
            try:
                # Se realiza la descarga a la URL y se guarda el archivo de manera local con el nombre especificado
                print("\tDownloading form '" + URL_ELO_FIDE + "' ..")
                request.urlretrieve(URL_ELO_FIDE, PATH_ZIP + FILE_ZIP)
                simulateLoading(1)
                cfg.set_INTERNAL_CONFIG(
                    "lastUpdate_ELO_FIDE", dt.datetime.now().strftime("%Y-%m-%d")
                )
                print("\tFinish donwload. File: '" + PATH_ZIP + FILE_ZIP + "'\n")
                break
            except Exception as e:
                retry_count += 1
                if retry_count == max_retries:
                    send_email("Invalid URL Error", f"Failed to download file: {e}")
                    print(f"\tFailed to download file: {e}\n")
                else:
                    print(f"\tConnection error, retrying in 30 seconds...")
                    time.sleep(30)


def unZipFile(fileNameZip, fileNameUnZip):
    try:
        archivos_zip = zipfile.ZipFile(PATH_ZIP + fileNameZip, "r")
        print("\tZip files content:", archivos_zip.namelist())
        archivos_zip.extract(fileNameUnZip, PATH_DOCS)
        print("\tFile '" + fileNameUnZip + "' was extracted in '" + PATH_DOCS + "'")
        archivos_zip.close()
    except:
        print("\tUnable to unzip '" + fileNameZip + "'\n")
        pass


# __main__
download_ELO_FIDE()
unZipFile(FILE_ZIP, FILE_UNZIP)
clean_file(FILENAME_AGORA, FILENAME_AGORA_CLEANED)
write_file(
    FILENAME_AGORA_ELO, getAgoraMembersELO(FILENAME_AGORA_CLEANED, FILENAME_ELO_FIDE)
)
