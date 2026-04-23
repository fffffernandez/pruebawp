<?php
/**
 * Header template.
 *
 * @package VisionPlus
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$brand_mark     = vision_plus_get_theme_mod( 'brand_mark_url' );
$phone_landline = vision_plus_get_theme_mod( 'phone_landline' );
$phone_whatsapp = vision_plus_get_theme_mod( 'phone_whatsapp' );
$email          = vision_plus_get_theme_mod( 'email' );
$instagram_url  = vision_plus_get_theme_mod( 'instagram_url' );
$tiktok_url     = vision_plus_get_theme_mod( 'tiktok_url' );
?>
<!doctype html>
<html <?php language_attributes(); ?>>
<head>
	<meta charset="<?php bloginfo( 'charset' ); ?>">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>
<a class="skip-link" href="#contenido"><?php esc_html_e( 'Saltar al contenido', 'vision-plus' ); ?></a>

<div class="top-contact-bar">
	<div class="shell top-contact-bar__inner">
		<a href="<?php echo esc_url( 'tel:' . vision_plus_normalize_phone( $phone_landline ) ); ?>"><?php echo esc_html( $phone_landline ); ?></a>
		<a class="top-contact-bar__whatsapp" href="<?php echo esc_url( vision_plus_whatsapp_link() ); ?>" target="_blank" rel="noreferrer"><?php echo esc_html( $phone_whatsapp ); ?></a>
		<a href="<?php echo esc_url( 'mailto:' . antispambot( $email ) ); ?>"><?php echo esc_html( antispambot( $email ) ); ?></a>
	</div>
</div>

<header class="site-header">
	<div class="shell site-header__inner">
		<a class="brand-mark" href="<?php echo esc_url( home_url( '/' ) ); ?>" aria-label="<?php bloginfo( 'name' ); ?>">
			<?php if ( $brand_mark ) : ?>
				<img src="<?php echo esc_url( $brand_mark ); ?>" alt="<?php bloginfo( 'name' ); ?>">
			<?php else : ?>
				<span><?php bloginfo( 'name' ); ?></span>
			<?php endif; ?>
		</a>

		<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="primary-menu">
			<span></span>
			<span></span>
			<span></span>
			<span class="screen-reader-text"><?php esc_html_e( 'Abrir menu', 'vision-plus' ); ?></span>
		</button>

		<nav class="site-navigation" id="primary-menu" aria-label="<?php esc_attr_e( 'Principal', 'vision-plus' ); ?>">
			<?php
			wp_nav_menu(
				array(
					'theme_location' => 'primary',
					'container'      => false,
					'menu_class'     => 'site-menu',
					'fallback_cb'    => 'vision_plus_fallback_menu',
				)
			);
			?>
		</nav>

		<div class="site-social">
			<?php if ( $instagram_url ) : ?>
				<a href="<?php echo esc_url( $instagram_url ); ?>" target="_blank" rel="noreferrer">Instagram</a>
			<?php endif; ?>
			<?php if ( $tiktok_url ) : ?>
				<a href="<?php echo esc_url( $tiktok_url ); ?>" target="_blank" rel="noreferrer">TikTok</a>
			<?php endif; ?>
		</div>
	</div>
</header>

