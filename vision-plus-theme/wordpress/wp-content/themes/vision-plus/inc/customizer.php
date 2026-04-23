<?php
/**
 * Theme customizer settings.
 *
 * @package VisionPlus
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

function vision_plus_sanitize_textarea( $value ) {
	return wp_kses_post( $value );
}

function vision_plus_customize_register( $wp_customize ) {
	$defaults = vision_plus_defaults();

	$wp_customize->add_section(
		'vision_plus_contact',
		array(
			'title'       => __( 'Datos del centro', 'vision-plus' ),
			'description' => __( 'Telefono, email, direccion y horarios.', 'vision-plus' ),
			'priority'    => 30,
		)
	);

	$wp_customize->add_section(
		'vision_plus_homepage',
		array(
			'title'       => __( 'Home Vision+', 'vision-plus' ),
			'description' => __( 'Textos e imagenes principales de la portada.', 'vision-plus' ),
			'priority'    => 31,
		)
	);

	$wp_customize->add_section(
		'vision_plus_social',
		array(
			'title'       => __( 'Redes sociales', 'vision-plus' ),
			'description' => __( 'Enlaces sociales visibles en la cabecera.', 'vision-plus' ),
			'priority'    => 32,
		)
	);

	$text_settings = array(
		'phone_landline'     => array( 'section' => 'vision_plus_contact', 'label' => __( 'Telefono fijo', 'vision-plus' ) ),
		'phone_whatsapp'     => array( 'section' => 'vision_plus_contact', 'label' => __( 'Telefono WhatsApp', 'vision-plus' ) ),
		'email'              => array( 'section' => 'vision_plus_contact', 'label' => __( 'Email', 'vision-plus' ) ),
		'address'            => array( 'section' => 'vision_plus_contact', 'label' => __( 'Direccion visible', 'vision-plus' ) ),
		'map_query'          => array( 'section' => 'vision_plus_contact', 'label' => __( 'Direccion para mapa embebido', 'vision-plus' ) ),
		'maps_url'           => array( 'section' => 'vision_plus_contact', 'label' => __( 'URL de Google Maps', 'vision-plus' ), 'type' => 'url' ),
		'weekday_hours'      => array( 'section' => 'vision_plus_contact', 'label' => __( 'Horario entre semana', 'vision-plus' ) ),
		'saturday_hours'     => array( 'section' => 'vision_plus_contact', 'label' => __( 'Horario sabado', 'vision-plus' ) ),
		'whatsapp_message'   => array( 'section' => 'vision_plus_contact', 'label' => __( 'Mensaje por defecto de WhatsApp', 'vision-plus' ), 'type' => 'textarea' ),
		'instagram_url'      => array( 'section' => 'vision_plus_social', 'label' => __( 'Instagram', 'vision-plus' ), 'type' => 'url' ),
		'tiktok_url'         => array( 'section' => 'vision_plus_social', 'label' => __( 'TikTok', 'vision-plus' ), 'type' => 'url' ),
		'about_intro'        => array( 'section' => 'vision_plus_homepage', 'label' => __( 'Texto principal sobre mi', 'vision-plus' ), 'type' => 'textarea' ),
		'about_signature'    => array( 'section' => 'vision_plus_homepage', 'label' => __( 'Firma sobre mi', 'vision-plus' ) ),
		'about_secondary'    => array( 'section' => 'vision_plus_homepage', 'label' => __( 'Texto secundario sobre mi', 'vision-plus' ), 'type' => 'textarea' ),
		'location_intro'     => array( 'section' => 'vision_plus_homepage', 'label' => __( 'Texto ubicacion', 'vision-plus' ), 'type' => 'textarea' ),
		'testimonial_text'   => array( 'section' => 'vision_plus_homepage', 'label' => __( 'Testimonio', 'vision-plus' ), 'type' => 'textarea' ),
		'testimonial_author' => array( 'section' => 'vision_plus_homepage', 'label' => __( 'Autor del testimonio', 'vision-plus' ) ),
		'claim_text'         => array( 'section' => 'vision_plus_homepage', 'label' => __( 'Frase destacada', 'vision-plus' ) ),
	);

	foreach ( $text_settings as $key => $config ) {
		$wp_customize->add_setting(
			$key,
			array(
				'default'           => $defaults[ $key ],
				'sanitize_callback' => isset( $config['type'] ) && 'textarea' === $config['type'] ? 'vision_plus_sanitize_textarea' : ( isset( $config['type'] ) && 'url' === $config['type'] ? 'esc_url_raw' : 'sanitize_text_field' ),
			)
		);

		$control_args = array(
			'label'   => $config['label'],
			'section' => $config['section'],
			'type'    => isset( $config['type'] ) ? $config['type'] : 'text',
		);

		$wp_customize->add_control( $key, $control_args );
	}

	$image_settings = array(
		'brand_mark_url'          => __( 'Logo cabecera', 'vision-plus' ),
		'footer_logo_url'         => __( 'Logo footer', 'vision-plus' ),
		'hero_image_url'          => __( 'Imagen hero', 'vision-plus' ),
		'about_founder_image_url' => __( 'Foto fundadora', 'vision-plus' ),
		'about_detail_image_url'  => __( 'Imagen secundaria sobre mi', 'vision-plus' ),
		'map_image_url'           => __( 'Captura de mapa', 'vision-plus' ),
		'claim_image_url'         => __( 'Imagen fondo claim', 'vision-plus' ),
		'faq_image_url'           => __( 'Imagen FAQ', 'vision-plus' ),
		'testimonial_badge_url'   => __( 'Imagen testimonio', 'vision-plus' ),
	);

	foreach ( $image_settings as $key => $label ) {
		$wp_customize->add_setting(
			$key,
			array(
				'default'           => $defaults[ $key ],
				'sanitize_callback' => 'esc_url_raw',
			)
		);

		$wp_customize->add_control(
			new WP_Customize_Image_Control(
				$wp_customize,
				$key,
				array(
					'label'   => $label,
					'section' => 'vision_plus_homepage',
				)
			)
		);
	}
}
add_action( 'customize_register', 'vision_plus_customize_register' );

