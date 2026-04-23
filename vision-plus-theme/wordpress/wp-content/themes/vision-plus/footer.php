<?php
/**
 * Footer template.
 *
 * @package VisionPlus
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

$footer_logo   = vision_plus_get_theme_mod( 'footer_logo_url' );
$weekday_hours = vision_plus_get_theme_mod( 'weekday_hours' );
$saturday      = vision_plus_get_theme_mod( 'saturday_hours' );
$address       = vision_plus_get_theme_mod( 'address' );
?>
<footer class="site-footer">
	<div class="shell site-footer__grid">
		<div class="site-footer__brand">
			<?php if ( $footer_logo ) : ?>
				<img src="<?php echo esc_url( $footer_logo ); ?>" alt="<?php bloginfo( 'name' ); ?>">
			<?php else : ?>
				<h2><?php bloginfo( 'name' ); ?></h2>
			<?php endif; ?>
			<p><?php echo esc_html( $address ); ?></p>
		</div>

		<div>
			<h2><?php esc_html_e( 'Menu', 'vision-plus' ); ?></h2>
			<?php
			wp_nav_menu(
				array(
					'theme_location' => 'footer',
					'container'      => false,
					'menu_class'     => 'footer-menu',
					'fallback_cb'    => 'vision_plus_fallback_menu',
				)
			);
			?>
		</div>

		<div>
			<h2><?php esc_html_e( 'Horario', 'vision-plus' ); ?></h2>
			<ul class="footer-menu">
				<li><?php esc_html_e( 'Lunes a viernes', 'vision-plus' ); ?></li>
				<li><?php echo esc_html( $weekday_hours ); ?></li>
				<li><?php esc_html_e( 'Sabados', 'vision-plus' ); ?></li>
				<li><?php echo esc_html( $saturday ); ?></li>
			</ul>
		</div>

		<div>
			<h2><?php esc_html_e( 'Legal', 'vision-plus' ); ?></h2>
			<?php
			wp_nav_menu(
				array(
					'theme_location' => 'legal',
					'container'      => false,
					'menu_class'     => 'footer-menu',
					'fallback_cb'    => '__return_empty_string',
				)
			);
			?>
		</div>
	</div>

	<div class="site-footer__bottom">
		<div class="shell site-footer__bottom-inner">
			<p>&copy; <?php echo esc_html( gmdate( 'Y' ) ); ?> <?php bloginfo( 'name' ); ?></p>
			<p><?php esc_html_e( 'Diseno web inspirado en el layout de Figma.', 'vision-plus' ); ?></p>
		</div>
	</div>
</footer>
<?php wp_footer(); ?>
</body>
</html>

