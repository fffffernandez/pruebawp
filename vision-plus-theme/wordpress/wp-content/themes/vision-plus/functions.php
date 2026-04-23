<?php
/**
 * Theme bootstrap.
 *
 * @package VisionPlus
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function vision_plus_defaults() {
	return array(
		'brand_mark_url'          => 'https://www.figma.com/api/mcp/asset/d3ba253f-ab81-4e6d-ab00-51b268384a1e',
		'footer_logo_url'         => 'https://www.figma.com/api/mcp/asset/ca07da72-906f-4907-94fa-ed00444f6444',
		'hero_image_url'          => 'https://www.figma.com/api/mcp/asset/af01da79-b83b-465a-8405-02c342013b1c',
		'about_founder_image_url' => 'https://www.figma.com/api/mcp/asset/9066c010-c384-49ab-93c4-50bffa87a701',
		'about_detail_image_url'  => 'https://www.figma.com/api/mcp/asset/fce9499f-1cc2-4580-b6dc-a126f43c5d19',
		'map_image_url'           => 'https://www.figma.com/api/mcp/asset/db4da832-f220-4d44-ba41-c19f0da359a1',
		'claim_image_url'         => 'https://www.figma.com/api/mcp/asset/a8e473df-dadc-4013-aebd-38f640061f71',
		'faq_image_url'           => 'https://www.figma.com/api/mcp/asset/69f0692a-e945-4f6c-9298-41987b251864',
		'testimonial_badge_url'   => 'https://www.figma.com/api/mcp/asset/ef648f3d-1148-4581-97f6-9fadb97f3aa6',
		'phone_landline'          => '953 086 858',
		'phone_whatsapp'          => '649 720 346',
		'email'                   => 'centro.opticovision@hotmail.com',
		'address'                 => 'C/ de la Rioja, 1 | 23009 Jaen',
		'map_query'               => 'Calle Rioja 1, 23009 Jaen, Espana',
		'maps_url'                => 'https://maps.app.goo.gl/LujwUDVSLFa55WNt6',
		'whatsapp_message'        => 'Hola Optica Vision+, me gustaria hacer una consulta sobre vuestros servicios.',
		'instagram_url'           => 'https://www.instagram.com/centro.opticovision/',
		'tiktok_url'              => '',
		'weekday_hours'           => '9:30 a 13:30, 17:00 a 20:30',
		'saturday_hours'          => '10:00 a 13:30',
		'about_intro'             => 'Desde que empece la carrera, siempre sone con crear un centro propio donde la vision del paciente estuviera en el centro de todo. No queria que fuese una optica centrada unicamente en vender gafas, sino un lugar donde cada persona pudiera recibir la solucion que realmente necesita.',
		'about_signature'         => 'Mariloli Ruiz de la Torre | Fundadora de Centro Optico Vision+',
		'about_secondary'         => 'Me considero una verdadera apasionada de la profesion, especialmente en miopia, contactologia y terapia visual. Estoy constantemente formandome y siguiendo las ultimas novedades y tratamientos del sector para ofrecer alternativas reales y actualizadas a cada paciente.',
		'location_intro'          => 'En Optica Vision+, en la calle Rioja, 1 en Jaen, realizamos revisiones visuales completas para detectar cualquier problema y ofrecerte la mejor solucion adaptada a tu caso.',
		'testimonial_text'        => 'En Centro Optico Vision+ te vas a sentir como en casa. Son muy amables, te escuchan con atencion y buscan la mejor solucion para ti. He estado en muchas opticas y aqui, por primera vez, senti que realmente encontraron una alternativa hecha a mi medida.',
		'testimonial_author'      => 'Sonia Valdivia',
		'claim_text'              => 'Mas que gafas, soluciones visuales',
	);
}

function vision_plus_get_theme_mod( $key ) {
	$defaults = vision_plus_defaults();
	$default  = isset( $defaults[ $key ] ) ? $defaults[ $key ] : '';

	return get_theme_mod( $key, $default );
}

function vision_plus_normalize_phone( $phone ) {
	return preg_replace( '/[^0-9+]/', '', (string) $phone );
}

function vision_plus_whatsapp_link() {
	$number  = vision_plus_normalize_phone( vision_plus_get_theme_mod( 'phone_whatsapp' ) );
	$message = rawurlencode( vision_plus_get_theme_mod( 'whatsapp_message' ) );

	if ( empty( $number ) ) {
		return '#';
	}

	return sprintf( 'https://wa.me/34%s?text=%s', ltrim( $number, '+' ), $message );
}

function vision_plus_setup() {
	add_theme_support( 'title-tag' );
	add_theme_support( 'post-thumbnails' );
	add_theme_support(
		'html5',
		array(
			'comment-form',
			'comment-list',
			'gallery',
			'caption',
			'search-form',
			'script',
			'style',
		)
	);

	register_nav_menus(
		array(
			'primary' => __( 'Menu principal', 'vision-plus' ),
			'footer'  => __( 'Menu footer', 'vision-plus' ),
			'legal'   => __( 'Menu legal', 'vision-plus' ),
		)
	);
}
add_action( 'after_setup_theme', 'vision_plus_setup' );

function vision_plus_enqueue_assets() {
	$theme = wp_get_theme();

	wp_enqueue_style(
		'vision-plus-fonts',
		'https://fonts.googleapis.com/css2?family=Open+Sans:wght@400&family=Raleway:wght@400;500;600;700;900&display=swap',
		array(),
		null
	);

	wp_enqueue_style(
		'vision-plus-main',
		get_stylesheet_uri(),
		array(),
		$theme->get( 'Version' )
	);

	wp_enqueue_style(
		'vision-plus-theme',
		get_template_directory_uri() . '/assets/css/theme.css',
		array( 'vision-plus-main', 'vision-plus-fonts' ),
		filemtime( get_template_directory() . '/assets/css/theme.css' )
	);

	wp_enqueue_script(
		'vision-plus-theme',
		get_template_directory_uri() . '/assets/js/theme.js',
		array(),
		filemtime( get_template_directory() . '/assets/js/theme.js' ),
		true
	);
}
add_action( 'wp_enqueue_scripts', 'vision_plus_enqueue_assets' );

function vision_plus_customize_partial_render() {
	bloginfo( 'name' );
}

function vision_plus_fallback_menu() {
	echo '<ul class="menu-fallback">';
	echo '<li><a href="#servicios">' . esc_html__( 'Servicios', 'vision-plus' ) . '</a></li>';
	echo '<li><a href="#sobre-mi">' . esc_html__( 'Sobre mi', 'vision-plus' ) . '</a></li>';
	echo '<li><a href="#donde-estamos">' . esc_html__( 'Donde estamos', 'vision-plus' ) . '</a></li>';
	echo '<li><a href="#faq">' . esc_html__( 'FAQ', 'vision-plus' ) . '</a></li>';
	echo '</ul>';
}

require get_template_directory() . '/inc/customizer.php';

