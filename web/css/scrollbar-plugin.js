$.scrollbar = function(scrollbarAdded) {
	var scrollbarTop = "0px";
	var animatingOut = false;
	var animateOutTimer;
	var animateOut = function() {
		$(".scrollbar").stop();
		if (animatingOut) {
			clearTimeout(animateOutTimer);
		}
		animatingOut = true;
		$(".scrollbar").css("opacity", "1");
		animateOutTimer = setTimeout(function() {
			$(".scrollbar").animate({
				opacity: 0
			}, 2000, undefined, function() {
				animatingOut = false;
			});
		}, 3000);
	}
	var winHeight = $(window).innerHeight();
	var docHeight = $(document).height();
	if (!scrollbarAdded) {
		$.scrollbar.addEvents();
		$("body").prepend('<div class="scrollbar-track"><div class="scrollbar"></div></div>');
	}
	var trackHeight = $(".scrollbar-track").height();
	var scrollbarHeight = (winHeight / docHeight) * trackHeight - 10
	$(".scrollbar").height(scrollbarHeight).css("top", scrollbarTop).draggable({
		axis: 'y',
		containment: 'parent',
		drag: function() {
			var scrollbarTop = parseInt($(this).css('top'));
			var scrollTopNew = (scrollbarTop / (trackHeight)) * docHeight;
			$(window).scrollTop(scrollTopNew);
			animateOut();
		}
	});
	$("body").unbind("mousewheel"); 
	$("body").bind("mousewheel", function (event, delta) {
		var scrollTop = $(window).scrollTop();
		var scrollTopNew = scrollTop - (delta * 40);
		$(window).scrollTop(scrollTopNew);
		var scrollbarTop = ($(window).scrollTop() / docHeight) * trackHeight;
		$('.scrollbar').css({
			top: scrollbarTop
		});
		animateOut();
	});
	$(".scrollbar").css({
		top: ($(window).scrollTop() / docHeight) * trackHeight
	});
	$(document).mousemove(animateOut);
	animateOut();
}
$.scrollbar.addEvents = function() {
	$(window).resize(function() {
		$.scrollbar(true);
	});
	$(document).resize(function() {
		$.scrollbar(true);
	});
}
