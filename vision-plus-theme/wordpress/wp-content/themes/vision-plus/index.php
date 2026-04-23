<?php
/**
 * Fallback template.
 *
 * @package VisionPlus
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>
<main id="contenido" class="shell generic-content">
	<?php if ( have_posts() ) : ?>
		<?php while ( have_posts() ) : ?>
			<?php the_post(); ?>
			<article <?php post_class( 'generic-entry' ); ?>>
				<h1><?php the_title(); ?></h1>
				<div class="copy">
					<?php the_content(); ?>
				</div>
			</article>
		<?php endwhile; ?>
	<?php else : ?>
		<p><?php esc_html_e( 'No hay contenido disponible.', 'vision-plus' ); ?></p>
	<?php endif; ?>
</main>
<?php
get_footer();

