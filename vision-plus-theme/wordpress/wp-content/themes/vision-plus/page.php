<?php
/**
 * Generic page template.
 *
 * @package VisionPlus
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();
?>
<main id="contenido" class="shell generic-content">
	<?php while ( have_posts() ) : ?>
		<?php the_post(); ?>
		<article <?php post_class( 'generic-entry' ); ?>>
			<header class="generic-entry__header">
				<h1><?php the_title(); ?></h1>
			</header>
			<div class="copy">
				<?php the_content(); ?>
			</div>
		</article>
	<?php endwhile; ?>
</main>
<?php
get_footer();

