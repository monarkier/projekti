
import mysql.connector
from math import radians, sin, cos, sqrt, atan2, pi
import random


def aloita():
    raha = 1000
    bensa = 1000
    print("Tervetuloa lentopeliin! Voit liikkua 10 lähimmälle lentokentälle.")
    lentokentät = haekentät()
    lentokenttä = lentokenttätiedot(arvoLentokenttä())
    kohdekenttä = lentokenttätiedot(arvoLentokenttä())


    while True:
        print(f"{raha}€     tankki:{bensa}l     kohdekenttä: {kohdekenttä[0]},{kohdekenttä[2]}")
        print(f"Tämänhetkinen lentokenttä: {lentokenttä[0]}, {lentokenttä[2]}")

        if raha <= 0 :
            print("GAME OVER")
            print("Raha loppui")
            break
        elif bensa <= 0:
            print("GAME OVER")
            print("Bensa loppui")

        num = 0
        lähtö_lat = lentokenttä[3]
        lähtö_lon = lentokenttä[4]
        lähimmät = etsi_lähimmät_lentokentät(lähtö_lat, lähtö_lon, lentokentät)
        lähimmät.pop(0)


        if lentokenttä == kohdekenttä:
            raha+=100
            raha, kohdekenttä = valitse_rahti(raha)

        for i in lähimmät:
            num += 1
            print(f"{num}. {i[0]} {i[3]}  - Etäisyys: {i[1]:.2f} km")

        vastaus=input("mille lentokentälle haluat mennä?(1-10) vai ostatko bensaa(b)")

        if vastaus in {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}:
            lentokenttä = lentokenttätiedot(lähimmät[int(vastaus) - 1][2])
            bensa -= round(lähimmät[int(vastaus) - 1][1] / 50)
        elif vastaus == "b":
            bensa,raha=tankkaa(bensa,raha)
        else:
            print("väärä input!")

        if lentokenttä == kohdekenttä:
            raha, kohdekenttä = valitse_rahti(raha)


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Maapallon keskimääräinen säde kilometreissä
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    etäisyys = R * c
    return etäisyys


def etsi_lähimmät_lentokentät(lähtö_lat, lähtö_lon, lentokenttä_lista):
    lentokenttä_etäisyydet = []

    for lentokenttä in lentokenttä_lista:
        ident, nimi, iso_maa, iso_alue, lat, lon = lentokenttä
        etäisyys = haversine(lähtö_lat, lähtö_lon, lat, lon)
        maa=maakoodi_maaksi(iso_maa)
        lentokenttä_etäisyydet.append((nimi, etäisyys, ident, maa))

    # Järjestetään lentokentät etäisyyden mukaan
    lähimmät_lentokentät = sorted(lentokenttä_etäisyydet, key=lambda x: x[1])[:11]

    return lähimmät_lentokentät


def arvoLentokenttä():
    yhteys = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='salasana',
                                     database="flight_game", autocommit=True)
    haku = yhteys.cursor()
    sql = "SELECT ident FROM airport WHERE type='large_airport' ORDER BY RAND() LIMIT 1;"
    haku.execute(sql)
    tulos = haku.fetchone()[0]
    haku.close()
    yhteys.close()
    return tulos


def lentokenttätiedot(x):
    yhteys = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='salasana',
                                     database="flight_game", autocommit=True)
    haku = yhteys.cursor()
    icao = x
    sql = "SELECT airport.name, airport.iso_country, country.name, latitude_deg, longitude_deg FROM airport, country WHERE country.iso_country=airport.iso_country and ident ='" + icao + "'"
    haku.execute(sql)
    tulos = haku.fetchall()
    haku.close()
    yhteys.close()
    return tulos[0]


def haekentät():
    yhteys = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='salasana',
                                     database="flight_game", autocommit=True)
    haku = yhteys.cursor()
    sql = "SELECT ident, name, iso_country, iso_region, latitude_deg, longitude_deg FROM airport WHERE type='large_airport'"
    haku.execute(sql)
    tulos = haku.fetchall()
    haku.close()
    yhteys.close()
    return tulos


def tankkaa(bensa, raha):
    x = random.randint(5, 25)
    print(f"bensan hintakerroin on {x}")
    kysymys = int(input("paljonko haluat tankata?: "))
    raha -= kysymys * x
    bensa += kysymys
    return bensa, raha


def valitse_rahti(raha):
    rahti_a = random.randint(1, 25), lentokenttätiedot(arvoLentokenttä())
    rahti_b = random.randint(10, 50), lentokenttätiedot(arvoLentokenttä())
    rahti_c = random.randint(25, 100),lentokenttätiedot(arvoLentokenttä())
    print(f"rahti A(1)  {rahti_a[1][0]}, {rahti_a[1][2]}    {rahti_a[0]}€")
    print(f"rahti B(2)  {rahti_b[1][0]}, {rahti_b[1][2]}  {rahti_b[0]}€")
    print(f"rahti C(3)  {rahti_c[1][0]}, {rahti_c[1][2]}  {rahti_c[0]}€")
    vastaus = input("valitse rahti(1-3)")
    if vastaus == "1":
        raha -= rahti_a[0]
        return raha, rahti_a[1]
    elif vastaus == "2":
        raha -= rahti_b[0]
        return raha, rahti_b[1]
    elif vastaus == "3":
        raha -= rahti_c[0]
        return raha, rahti_c[1]


def maakoodi_maaksi(x):
    yhteys = mysql.connector.connect(host='127.0.0.1', port=3306, user='root', password='salasana',
                                     database="flight_game", autocommit=True)
    haku = yhteys.cursor()
    icao = x
    sql = "SELECT name, continent FROM country WHERE iso_country ='" + icao + "'"
    haku.execute(sql)
    tulos = haku.fetchall()
    haku.close()
    yhteys.close()
    return tulos[0]

aloita()