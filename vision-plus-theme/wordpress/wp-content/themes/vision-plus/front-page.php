<?php
/**
 * Front page template.
 *
 * @package VisionPlus
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$services = array(
	__( 'Revision visual', 'vision-plus' ),
	__( 'Terapia visual', 'vision-plus' ),
	__( 'Asesoramiento', 'vision-plus' ),
	__( 'Contactologia avanzada', 'vision-plus' ),
	__( 'Control y tratamiento de miopia', 'vision-plus' ),
	__( 'Salud visual', 'vision-plus' ),
);

$faqs = array(
	array(
		'q' => __( 'Donde puedo revisarme la vista en Jaen?', 'vision-plus' ),
		'a' => __( 'En Optica Vision+, en la calle Rioja 1, realizamos revisiones visuales completas para detectar cualquier problema y ofrecerte la mejor solucion adaptada a tu caso.', 'vision-plus' ),
	),
	array(
		'q' => __( 'Solo vendeis gafas o haceis algo mas?', 'vision-plus' ),
		'a' => __( 'No solo vendemos gafas. Trabajamos terapia visual, contactologia avanzada, salud visual y control de miopia con un enfoque personalizado.', 'vision-plus' ),
	),
	array(
		'q' => __( 'Teneis tratamiento para la miopia en ninos en Jaen?', 'vision-plus' ),
		'a' => __( 'Si. Estudiamos cada caso y planteamos seguimiento y opciones adaptadas para el control de la miopia infantil.', 'vision-plus' ),
	),
	array(
		'q' => __( 'Que es la terapia visual y para quien es?', 'vision-plus' ),
		'a' => __( 'La terapia visual ayuda a mejorar problemas como fatiga visual, dificultades de lectura o coordinacion binocular mediante planes personalizados.', 'vision-plus' ),
	),
	array(
		'q' => __( 'Puedo ponerme lentillas si tengo un problema ocular?', 'vision-plus' ),
		'a' => __( 'Trabajamos soluciones de contactologia avanzada, incluidas adaptaciones especiales, segun la situacion visual de cada paciente.', 'vision-plus' ),
	),
	array(
		'q' => __( 'Donde esta la optica?', 'vision-plus' ),
		'a' => __( 'Estamos en C/ de la Rioja, 1, 23009 Jaen.', 'vision-plus' ),
	),
);

$hero_image      = vision_plus_get_theme_mod( 'hero_image_url' );
$founder_image   = vision_plus_get_theme_mod( 'about_founder_image_url' );
$about_image     = vision_plus_get_theme_mod( 'about_detail_image_url' );
$map_image       = vision_plus_get_theme_mod( 'map_image_url' );
$claim_image     = vision_plus_get_theme_mod( 'claim_image_url' );
$faq_image       = vision_plus_get_theme_mod( 'faq_image_url' );
$testimonial_img = vision_plus_get_theme_mod( 'testimonial_badge_url' );
$address         = vision_plus_get_theme_mod( 'address' );
$maps_url        = vision_plus_get_theme_mod( 'maps_url' );
$map_query       = vision_plus_get_theme_mod( 'map_query' );
$phone_landline  = vision_plus_get_theme_mod( 'phone_landline' );
$phone_whatsapp  = vision_plus_get_theme_mod( 'phone_whatsapp' );
$email           = vision_plus_get_theme_mod( 'email' );

get_header();
?>
<main id="contenido">
	<section class="hero">
		<div class="hero__media" style="background-image: url('<?php echo esc_url( $hero_image ); ?>');"></div>
		<div class="hero__overlay shell">
			<h1 class="screen-reader-text"><?php bloginfo( 'name' ); ?></h1>
		</div>
	</section>

	<section class="section section--services shell" id="servicios">
		<div class="section-heading">
			<span class="section-heading__line"></span>
			<div>
				<p><?php esc_html_e( 'nuestros', 'vision-plus' ); ?></p>
				<h2><?php esc_html_e( 'servicios', 'vision-plus' ); ?></h2>
			</div>
		</div>
		<div class="services-grid">
			<?php foreach ( $services as $service ) : ?>
				<a class="service-card" href="<?php echo esc_url( home_url( '/contacto/' ) ); ?>">
					<span><?php echo esc_html( $service ); ?></span>
				</a>
			<?php endforeach; ?>
		</div>
	</section>

	<section class="section about-section" id="sobre-mi">
		<div class="about-section__primary shell">
			<div class="section-heading section-heading--light">
				<span class="section-heading__line"></span>
				<div>
					<p><?php esc_html_e( 'sobre', 'vision-plus' ); ?></p>
					<h2><?php esc_html_e( 'mi', 'vision-plus' ); ?></h2>
				</div>
			</div>
			<div class="about-section__grid">
				<div>
					<div class="copy copy--light"><?php echo wpautop( wp_kses_post( vision_plus_get_theme_mod( 'about_intro' ) ) ); ?></div>
					<p class="about-section__signature"><?php echo esc_html( vision_plus_get_theme_mod( 'about_signature' ) ); ?></p>
				</div>
				<?php if ( $founder_image ) : ?>
					<div class="about-section__portrait">
						<img src="<?php echo esc_url( $founder_image ); ?>" alt="<?php esc_attr_e( 'Fundadora del centro', 'vision-plus' ); ?>">
					</div>
				<?php endif; ?>
			</div>
		</div>

		<div class="about-section__secondary shell">
			<?php if ( $about_image ) : ?>
				<div class="about-section__detail-photo">
					<img src="<?php echo esc_url( $about_image ); ?>" alt="<?php esc_attr_e( 'Atencion en consulta', 'vision-plus' ); ?>">
				</div>
			<?php endif; ?>
			<div class="about-section__circle" aria-hidden="true"></div>
			<div class="copy copy--light"><?php echo wpautop( wp_kses_post( vision_plus_get_theme_mod( 'about_secondary' ) ) ); ?></div>
		</div>
	</section>

	<section class="section shell" id="donde-estamos">
		<div class="section-heading">
			<span class="section-heading__line"></span>
			<div>
				<p><?php esc_html_e( 'donde', 'vision-plus' ); ?></p>
				<h2><?php esc_html_e( 'estamos', 'vision-plus' ); ?></h2>
			</div>
		</div>

		<div class="location-card">
			<div class="location-card__map">
				<iframe
					title="<?php esc_attr_e( 'Mapa de ubicacion', 'vision-plus' ); ?>"
					src="<?php echo esc_url( 'https://www.google.com/maps?q=' . rawurlencode( $map_query ) . '&output=embed' ); ?>"
					loading="lazy"
					referrerpolicy="no-referrer-when-downgrade"
				></iframe>
				<?php if ( $map_image ) : ?>
					<img class="location-card__fallback" src="<?php echo esc_url( $map_image ); ?>" alt="<?php esc_attr_e( 'Mapa del centro', 'vision-plus' ); ?>">
				<?php endif; ?>
			</div>
			<a class="location-card__cta" href="<?php echo esc_url( $maps_url ); ?>" target="_blank" rel="noreferrer">
				<span><?php echo esc_html( $address ); ?></span>
			</a>
		</div>

		<p class="location-copy"><?php echo esc_html( vision_plus_get_theme_mod( 'location_intro' ) ); ?></p>
	</section>

	<section class="section shell testimonials">
		<?php if ( $testimonial_img ) : ?>
			<div class="testimonials__badge">
				<img src="<?php echo esc_url( $testimonial_img ); ?>" alt="<?php esc_attr_e( 'Valoraciones del centro', 'vision-plus' ); ?>">
			</div>
		<?php endif; ?>
		<div class="testimonials__content">
			<div class="rating" aria-hidden="true">★★★★★</div>
			<div class="copy"><?php echo wpautop( wp_kses_post( vision_plus_get_theme_mod( 'testimonial_text' ) ) ); ?></div>
			<p class="testimonials__author"><?php echo esc_html( vision_plus_get_theme_mod( 'testimonial_author' ) ); ?></p>
		</div>
	</section>

	<section class="claim-band" style="background-image: linear-gradient(rgba(38, 38, 38, 0.62), rgba(38, 38, 38, 0.62)), url('<?php echo esc_url( $claim_image ); ?>');">
		<div class="shell">
			<p class="claim-band__plus">+</p>
			<h2><?php echo esc_html( vision_plus_get_theme_mod( 'claim_text' ) ); ?></h2>
		</div>
	</section>

	<section class="section shell faq-section" id="faq">
		<div class="faq-section__content">
			<div class="section-heading section-heading--right">
				<div>
					<p><?php esc_html_e( 'preguntas', 'vision-plus' ); ?></p>
					<h2><?php esc_html_e( 'frecuentes', 'vision-plus' ); ?></h2>
				</div>
				<span class="section-heading__line"></span>
			</div>

			<div class="faq-list">
				<?php foreach ( $faqs as $index => $faq ) : ?>
					<details class="faq-item" <?php echo 0 === $index ? 'open' : ''; ?>>
						<summary><?php echo esc_html( $faq['q'] ); ?></summary>
						<div class="faq-item__body">
							<p><?php echo esc_html( $faq['a'] ); ?></p>
						</div>
					</details>
				<?php endforeach; ?>
			</div>
		</div>

		<?php if ( $faq_image ) : ?>
			<div class="faq-section__image">
				<img src="<?php echo esc_url( $faq_image ); ?>" alt="<?php esc_attr_e( 'Interior de la optica', 'vision-plus' ); ?>">
			</div>
		<?php endif; ?>
	</section>

	<section class="contact-strip shell">
		<a class="contact-strip__item contact-strip__item--dark" href="<?php echo esc_url( 'tel:' . vision_plus_normalize_phone( $phone_landline ) ); ?>">
			<span><?php echo esc_html( $phone_landline ); ?></span>
		</a>
		<a class="contact-strip__item contact-strip__item--green" href="<?php echo esc_url( vision_plus_whatsapp_link() ); ?>" target="_blank" rel="noreferrer">
			<span><?php echo esc_html( $phone_whatsapp ); ?></span>
		</a>
		<a class="contact-strip__item contact-strip__item--sand" href="<?php echo esc_url( 'mailto:' . antispambot( $email ) ); ?>">
			<span><?php echo esc_html( antispambot( $email ) ); ?></span>
		</a>
	</section>
</main>
<?php
get_footer();

