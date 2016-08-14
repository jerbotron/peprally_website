$(document).ready(function(){
		$('.navBtn').each(attachScrollListener);

		function attachScrollListener(index, element){
				element.addEventListener('click', function() {
						jQuery.scrollTo($('#' + element.getAttribute('scroll-to')), { duration: 500, offset: -50});
				});
		}
});