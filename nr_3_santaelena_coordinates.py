# На странице каждого города переходим на страницу с магазинами на карте. Смотрим, есть ли у магазина ссылка на гугл-карту.
# Если есть, переходим на гугл-карту и копируем ссылку с координатами в список, если нет - добавляем в список пустую строку.
# Ссылки с координатами добавляем в список в том порядке, в каком магазины идут на странице каждого города
# Формируем списки координат по всем городам

medellin_coord_list = [
    "",
    "https://www.google.com/maps/place/Cl.+51+Sur+%2348-57,+Sabaneta,+Antioquia,+%D0%9A%D0%BE%D0%BB%D1%83%D0%BC%D0%B1%D0%B8%D1%8F/@6.161696,-75.6051034,17z/data=!3m1!4b1!4m6!3m5!1s0x8e4683ce9fe68473:0xb3529ebb7af083a2!8m2!3d6.161696!4d-75.6051034!16s%2Fg%2F11gfgrkhrp?entry=ttu",
    "https://www.google.com/maps/place/Cl.+6+Sur+%2315,+El+Poblado,+Medell%C3%ADn,+El+Poblado,+Medell%C3%ADn,+Antioquia,+%D0%9A%D0%BE%D0%BB%D1%83%D0%BC%D0%B1%D0%B8%D1%8F/@6.199538,-75.5745284,17z/data=!3m1!4b1!4m6!3m5!1s0x8e468287870dbd31:0x6cb35a92780263c7!8m2!3d6.199538!4d-75.5745284!16s%2Fg%2F11h4kd1wlc?entry=ttu",
    "https://www.google.com/maps/place/Cra+66B+%2334A-76,+Laureles+-+Estadio,+Medell%C3%ADn,+Laureles,+Medell%C3%ADn,+Antioquia,+%D0%9A%D0%BE%D0%BB%D1%83%D0%BC%D0%B1%D0%B8%D1%8F/@6.2410468,-75.5877423,17z/data=!3m1!4b1!4m6!3m5!1s0x8e4429a50a09dd95:0xfb8e8ce27214b927!8m2!3d6.2410468!4d-75.5877423!16s%2Fg%2F11c25_t2l8?entry=ttu",
    "https://www.google.com/maps/place/Mall+La+Frontera,+El+Poblado,+Medell%C3%ADn,+El+Poblado,+Medell%C3%ADn,+Antioquia,+%D0%9A%D0%BE%D0%BB%D1%83%D0%BC%D0%B1%D0%B8%D1%8F/@6.1840903,-75.5789942,17z/data=!3m1!4b1!4m6!3m5!1s0x8e46825e66dc254d:0x6fde1d54edb0382e!8m2!3d6.1840903!4d-75.5789942!16s%2Fg%2F11bymxqyd7?entry=ttu",
    "https://www.google.com/maps/place/Cra.+52+%2343-31,+La+Candelaria,+Medell%C3%ADn,+La+Candelaria,+Medell%C3%ADn,+Antioquia,+%D0%9A%D0%BE%D0%BB%D1%83%D0%BC%D0%B1%D0%B8%D1%8F/@6.2445328,-75.5717495,17z/data=!3m1!4b1!4m6!3m5!1s0x8e44285492b8e2ab:0xb39ec2dcb109ae57!8m2!3d6.2445328!4d-75.5717495!16s%2Fg%2F11hzcr4qf5?entry=ttu",
    "",
    "https://www.google.com/maps/place/Viva+Laureles/@6.2461008,-75.6021567,17z/data=!3m1!4b1!4m6!3m5!1s0x8e44299eeb2545eb:0xf2015365fd844b59!8m2!3d6.2461008!4d-75.6021567!16s%2Fg%2F11bv3rn7b0?entry=ttu",
    "",
    "",
    "https://www.google.com/maps/place/%D0%90%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82+%D0%98%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%81%D1%8C%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C+%D0%A5%D0%BE%D1%81%D0%B5+%D0%9C%D0%B0%D1%80%D0%B8%D1%8F+%D0%9A%D0%BE%D1%80%D0%B4%D0%BE%D0%B2%D0%B0/@6.1714903,-75.4279447,17z/data=!3m1!4b1!4m6!3m5!1s0x8e469e78b840720f:0x9263a9a2a8b8e1b8!8m2!3d6.1714903!4d-75.4279447!16zL20vMDNuc2Nt?entry=ttu",
    "",
    ""
]

bogota_coord_list = [
    "",
    "",
    "",
    "",
    "",
    "https://www.google.com/maps/place/Cl.+95+%2313-55,+Bogot%C3%A1,+%D0%9A%D0%BE%D0%BB%D1%83%D0%BC%D0%B1%D0%B8%D1%8F/@4.68007,-74.0486016,17z/data=!3m1!4b1!4m6!3m5!1s0x8e3f9a93e938eb65:0x7ff36128fa7c09a6!8m2!3d4.68007!4d-74.0486016!16s%2Fg%2F11gfcyk4qt?entry=ttu",
    "",
    "",
    "",
    "",
    ""
]

monteria_coord_list = [
    "https://www.google.com/maps/place/%D0%90%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82+%D0%9B%D0%BE%D1%81+%D0%93%D0%B0%D1%80%D1%81%D0%BE%D0%BD%D0%B5%D1%81+-+%D0%9C%D0%BE%D0%BD%D1%82%D0%B5%D1%80%D0%B8%D1%8F/@8.8251965,-75.8240127,17z/data=!3m1!4b1!4m6!3m5!1s0x8e5a2eb4052f38fd:0xbcabff5d94ad3a74!8m2!3d8.8251965!4d-75.8240127!16s%2Fm%2F0404x94?entry=ttu",
    "https://www.google.com/maps/place/%D0%90%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82+%D0%9B%D0%BE%D1%81+%D0%93%D0%B0%D1%80%D1%81%D0%BE%D0%BD%D0%B5%D1%81+-+%D0%9C%D0%BE%D0%BD%D1%82%D0%B5%D1%80%D0%B8%D1%8F/@8.8251965,-75.8240127,17z/data=!3m1!4b1!4m6!3m5!1s0x8e5a2eb4052f38fd:0xbcabff5d94ad3a74!8m2!3d8.8251965!4d-75.8240127!16s%2Fm%2F0404x94?entry=ttu"
]

pereira_coord_list = [
    "https://www.google.com/maps/place/%D0%90%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82+%D0%98%D0%BD%D1%82%D0%B5%D1%80%D0%BD%D0%B0%D1%81%D1%8C%D0%BE%D0%BD%D0%B0%D0%BB%D1%8C+%D0%9C%D0%B0%D1%82%D0%B5%D0%BA%D0%B0%D0%BD%D1%8C%D1%8F/@4.8151963,-75.7362559,17z/data=!3m1!4b1!4m6!3m5!1s0x8e387de79024b6c7:0x817d2126f2ddb5b5!8m2!3d4.8151963!4d-75.7362559!16zL20vMDdmcjJ5?entry=ttu"
]

barranquilla_coord_list = [
    "https://www.google.com/maps/place/%D0%AD%D1%80%D0%BD%D0%B5%D1%81%D1%82%D0%BE+%D0%9A%D0%BE%D1%80%D1%82%D0%B8%D1%81%D0%BE%D1%81+%D0%B0%D1%8D%D1%80%D0%BE%D0%BF%D0%BE%D1%80%D1%82%D1%83/@10.8865373,-74.776479,17z/data=!3m1!4b1!4m6!3m5!1s0x8ef5cd8aebfe1d83:0x916964b712ae67b!8m2!3d10.8865373!4d-74.776479!16zL20vMDE1cmZq?entry=ttu"
]

# Объявляем функцию, которая преобразует списки координат в нужный нам формат
def get_coords(coords_list):
    latlon = []
    for item in coords_list:
        if "@" in item:
            coordinates = item.split('@')[1].split('/')[0].split(",")[0:2]
            coordinates = [float(item) for item in coordinates]
            latlon.append(coordinates)
        else:
            coordinates = None
            latlon.append(coordinates)
    return latlon

# Вызываем функцию для каждого города и присваиваем ее значение соответствующей переменной
coords_medellin = get_coords(medellin_coord_list)
coords_bogota = get_coords(bogota_coord_list)
coords_monteria = get_coords(monteria_coord_list)
coords_pereira = get_coords(pereira_coord_list)
coords_barranquilla = get_coords(barranquilla_coord_list)