from django.db import migrations


PRODUCT_IMAGES = {
    'Martillo carpintero 16 oz mango fibra': (
        'https://upload.wikimedia.org/wikipedia/commons/4/49/Carpenter%27s_hammer.JPG',
        'https://commons.wikimedia.org/w/index.php?curid=23873956',
        "Carpenter's hammer, Kszapsza, CC BY-SA 3.0.",
    ),
    'Alicate universal 8 pulgadas': (
        'https://upload.wikimedia.org/wikipedia/commons/2/23/05-02_combination_pliers_big.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=45199120',
        '05-02 combination pliers big, Mansurbiohazard, CC BY-SA 4.0.',
    ),
    'Set de destornilladores 6 piezas': (
        'https://upload.wikimedia.org/wikipedia/commons/d/d3/Robertson_screwdriver_set.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=379099',
        'Robertson screwdriver set, Luigi Zanasi, CC BY-SA 2.0.',
    ),
    'Llave ajustable cromada 10 pulgadas': (
        'https://upload.wikimedia.org/wikipedia/commons/5/5f/Adjustable_spanner.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=81769773',
        'Adjustable spanner, Mike Peel, CC BY-SA 4.0.',
    ),
    'Huincha metálica 5 m': (
        'https://upload.wikimedia.org/wikipedia/commons/f/f3/Stanley_PowerLock_tape_measure_on_tool_box.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=32929511',
        'Stanley PowerLock tape measure on tool box, J.C. Fields, CC BY-SA 3.0.',
    ),
    'Nivel de aluminio 60 cm': (
        'https://upload.wikimedia.org/wikipedia/commons/f/fa/A_bright_red_leveling_tool_is_positioned_on_a_surface.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=197293154',
        'A bright red leveling tool is positioned on a surface, Shixart1985, CC BY 2.0.',
    ),
    'Serrucho carpintero 20 pulgadas': (
        'https://live.staticflickr.com/2088/2277582023_c6d78d2ffd_b.jpg',
        'https://www.flickr.com/photos/17912374@N06/2277582023',
        'Natural Hand Saw, Anderson Mancini, CC BY 2.0.',
    ),
    'Combo llave punta corona 8 piezas': (
        'https://upload.wikimedia.org/wikipedia/commons/4/4c/Stanley-Combination-Wrench-Set_274710-480x360_%284904404909%29.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=38382843',
        'Stanley combination wrench set, Emilian Robert Vicol, CC BY 2.0.',
    ),
    'Taladro percutor 650 W': (
        'https://upload.wikimedia.org/wikipedia/commons/e/e4/Vintage_Power_Tool_-_Black_%26_Decker_P80-38_Rotary_Hammer_Drill_-_5011437838.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=148866342',
        'Black & Decker rotary hammer drill, toolstop, CC BY 2.0.',
    ),
    'Esmeril angular 4 1/2 pulgadas 750 W': (
        'https://upload.wikimedia.org/wikipedia/commons/2/20/Linked_mall_indoor_air_pollution_angle_grinder_03.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=175086880',
        'Linked mall indoor air pollution angle grinder 03, Waydwaid, CC0 1.0.',
    ),
    'Sierra circular 7 1/4 pulgadas 1400 W': (
        'https://upload.wikimedia.org/wikipedia/commons/5/55/DeWalt_circular_saw_in_use.jpg',
        'https://commons.wikimedia.org/wiki/File:DeWalt_circular_saw_in_use.jpg',
        'DeWalt circular saw in use, simplicity hunter, CC BY 2.0.',
    ),
    'Atornillador inalámbrico 12 V con batería': (
        'https://upload.wikimedia.org/wikipedia/commons/f/fd/MacAllister_cordless_screwdriver_02.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=115501138',
        'MacAllister cordless screwdriver 02, LoMit, CC BY-SA 4.0.',
    ),
    'Rotomartillo SDS Plus 800 W': (
        'https://upload.wikimedia.org/wikipedia/commons/8/88/Bosch_GBH2-26_professional_Rotary_Hammer_Drill_PICT4578.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=1624831',
        'Bosch GBH2-26 professional Rotary Hammer Drill, CBX, CC BY-SA 3.0.',
    ),
    'Lijadora orbital 240 W': (
        'https://upload.wikimedia.org/wikipedia/commons/4/4b/Makita_BO5041_Random_Orbit_Sander_%286169695568%29.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=148868040',
        'Makita BO5041 Random Orbit Sander, Mark Hunter, CC BY 2.0.',
    ),
    'Caja tornillos volcanita 6 x 1 1/4 500 unidades': (
        'https://upload.wikimedia.org/wikipedia/commons/9/9a/Skruvar.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=1067741',
        'Skruvar, User DaRy, CC BY-SA 3.0.',
    ),
    'Clavo corriente 2 pulgadas kilo': (
        'https://upload.wikimedia.org/wikipedia/commons/1/1e/Double-headed_nail.agr.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=139587138',
        'Double-headed nail, ArnoldReinhold, CC BY-SA 4.0.',
    ),
    'Perno coche galvanizado 3/8 x 3 pulgadas': (
        'https://upload.wikimedia.org/wikipedia/commons/d/d4/AFS_-_fasteners_picture.JPG',
        'https://commons.wikimedia.org/w/index.php?curid=4682631',
        'AFS fasteners picture, Neville Street, public domain.',
    ),
    'Tarugo nylon 8 mm con tornillo pack 50': (
        'https://upload.wikimedia.org/wikipedia/commons/c/c2/Tarugos.JPG',
        'https://commons.wikimedia.org/w/index.php?curid=16968804',
        'Tarugos, Canopus49, CC BY-SA 4.0.',
    ),
    'Tornillo autoperforante zincado pack 100': (
        'https://upload.wikimedia.org/wikipedia/commons/5/57/Hex-head-self-drilling-screw-1614969_340.png',
        'https://commons.wikimedia.org/w/index.php?curid=99564004',
        'Hex-head-self-drilling-screw, Zheer16, CC0 1.0.',
    ),
    'Candado de acero 50 mm': (
        'https://upload.wikimedia.org/wikipedia/commons/2/26/Steel_Cable_Padlock.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=97940688',
        'Steel Cable Padlock, Chole Wu, CC BY-SA 4.0.',
    ),
    'Pintura látex interior blanca 1 galón': (
        'https://live.staticflickr.com/3543/3413845072_5a9fda8bc9_b.jpg',
        'https://www.flickr.com/photos/61926883@N00/3413845072',
        'Paint cans, DBduo Photography, CC BY-SA 2.0.',
    ),
    'Esmalte al agua blanco 1 galón': (
        'https://upload.wikimedia.org/wikipedia/commons/8/83/Paint_bucket_and_brush.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=127866937',
        'Paint bucket and brush, Ionenlaser, CC0 1.0.',
    ),
    'Anticorrosivo gris 1 galón': (
        'https://live.staticflickr.com/4/9157418_4f46ca3bbe.jpg',
        'https://www.flickr.com/photos/11399912@N00/9157418',
        'Paint, basykes, CC BY 2.0. Foto referencial de pintura en tarro.',
    ),
    'Silicona neutra transparente 280 ml': (
        'https://live.staticflickr.com/4141/4817475284_c26acfc1d8.jpg',
        'https://www.flickr.com/photos/28958738@N06/4817475284',
        'Silicone-Sealant-1001U_43333-480x360, Public Domain Photos, CC BY 2.0.',
    ),
    'Adhesivo cerámico saco 25 kg': (
        'https://upload.wikimedia.org/wikipedia/commons/0/0b/A_bags_of_Cement_in_Awka.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=189985789',
        'A bags of Cement in Awka, Johnnybam, CC BY-SA 4.0. Foto referencial de saco de material cementicio.',
    ),
    'Cinta teflón para gasfitería 12 mm': (
        'https://upload.wikimedia.org/wikipedia/commons/4/4d/PTFE_seal_tape.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=3783319',
        'PTFE seal tape, CC BY-SA 3.0.',
    ),
    'Llave de paso bronce 1/2 pulgada': (
        'https://upload.wikimedia.org/wikipedia/commons/3/39/Close-up_of_brass_plumbing_valves_with_red_handles_in_a_home_installation.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=195963586',
        'Close-up of brass plumbing valves with red handles, Shixart1985, CC BY 2.0.',
    ),
    'Flexible para lavaplatos 1/2 x 1/2 40 cm': (
        'https://upload.wikimedia.org/wikipedia/commons/7/7e/Flexible_Metal-Wrapped_Plumbing_Water_Line_%2839935416743%29.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=77734706',
        'Flexible Metal-Wrapped Plumbing Water Line, Tony Webster, CC BY 2.0.',
    ),
    'Cable eléctrico EVA 2,5 mm² rollo 10 m': (
        'https://upload.wikimedia.org/wikipedia/commons/5/50/DZ6_2542_A_narrow_cluttered_electronics_shop_aisle_lined_with_shelves_of_components_spools_of_wire_and_glass_display_cases_overflowing_with_parts.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=189044295',
        'Electronics shop aisle with spools of wire, PattayaPatrol, CC BY-SA 4.0.',
    ),
    'Enchufe doble embutido blanco': (
        'https://upload.wikimedia.org/wikipedia/commons/4/44/Electrical-Outlet-8830c.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=18750567',
        'Electrical-Outlet-8830c, Loadmaster (David R. Tribble), CC BY-SA 3.0.',
    ),
    'Automático termomagnético 16 A': (
        'https://upload.wikimedia.org/wikipedia/commons/a/a9/Electric_circuit_breaker_fuse_box_in_private_home.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=194443091',
        'Electric circuit breaker fuse box in private home, Shixart1985, CC BY 2.0.',
    ),
    'Guantes cabritilla reforzados talla L': (
        'https://upload.wikimedia.org/wikipedia/commons/7/7c/Leather_work_gloves_composite_P1010224_copy.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=115130357',
        'Leather work gloves composite, el cajon yacht club, CC BY 2.0.',
    ),
    'Lentes de seguridad transparentes antiempañantes': (
        'https://upload.wikimedia.org/wikipedia/commons/a/a9/Wiley-X_PT-1_3-lens.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=1765422',
        'Wiley-X PT-1 3-lens, flip619, CC BY-SA 3.0.',
    ),
    'Casco de seguridad blanco con ajuste': (
        'https://upload.wikimedia.org/wikipedia/commons/a/ae/Cologne_Germany_Safety-helmet-with-headset-01.jpg',
        'https://commons.wikimedia.org/wiki/File:Cologne_Germany_Safety-helmet-with-headset-01.jpg',
        'Cologne Germany Safety-helmet-with-headset-01, CEphoto, Uwe Aranas, CC BY-SA 3.0.',
    ),
    'Protector auditivo tipo copa 25 dB': (
        'https://upload.wikimedia.org/wikipedia/commons/a/a7/Over_the_head_earmuffs_and_other_ear_protection_gear_in_German_hardware_store_%28cropped%29.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=141333694',
        'Over the head earmuffs and other ear protection gear in German hardware store, Pittigrilli, CC0 1.0.',
    ),
    'Botín de seguridad cuero talla 42': (
        'https://upload.wikimedia.org/wikipedia/commons/e/e4/Steel-toe_boots.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=1250663',
        'Steel-toe boots, Liftarn, CC BY-SA 3.0.',
    ),
    'Pala punta huevo con mango': (
        'https://upload.wikimedia.org/wikipedia/commons/f/f5/Giant_Spade_St_Mellons.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=161581269',
        'Giant Spade St Mellons, Sionk, CC BY-SA 4.0. Foto referencial de pala de jardín.',
    ),
    'Manguera jardín reforzada 1/2 pulgada 20 m': (
        'https://upload.wikimedia.org/wikipedia/commons/5/5f/Blue_hose_coiled_around_a_manhole_cover_in_a_grassy_outdoor_area.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=189918876',
        'Blue hose coiled around a manhole cover in a grassy outdoor area, Shixart1985, CC BY 2.0.',
    ),
    'Tijera de podar bypass 8 pulgadas': (
        'https://live.staticflickr.com/5530/30173721920_68206c2824_b.jpg',
        'https://www.flickr.com/photos/60944636@N00/30173721920',
        "THOR's hammer, garden trowel, weed digger and pruning shears, el cajon yacht club, CC BY 2.0.",
    ),
    'Carretilla construcción 90 litros': (
        'https://upload.wikimedia.org/wikipedia/commons/1/1f/2008-07-15_Construction_wheelbarrow_at_Duke.jpg',
        'https://commons.wikimedia.org/w/index.php?curid=4386851',
        'Construction wheelbarrow at Duke, Ildar Sagdejev, CC BY-SA 4.0.',
    ),
}


def assign_product_images(apps, schema_editor):
    Producto = apps.get_model('productos', 'Producto')

    for producto in Producto.objects.all().iterator():
        image_data = PRODUCT_IMAGES.get(producto.nombre)
        if image_data and not producto.imagen_archivo and not producto.imagen_url:
            producto.imagen_url, producto.imagen_fuente_url, producto.imagen_credito = image_data
            producto.save(
                update_fields=('imagen_url', 'imagen_fuente_url', 'imagen_credito')
            )


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_producto_imagen_archivo_producto_imagen_credito_and_more'),
    ]

    operations = [
        migrations.RunPython(assign_product_images, migrations.RunPython.noop),
    ]
