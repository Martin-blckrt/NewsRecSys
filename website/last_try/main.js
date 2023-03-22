// resize header to size of browser window

var ready = (callback) => {
	if (document.readyState != "loading") callback();
	else document.addEventListener("DOMContentLoaded", callback);
}

ready(() => {

})

window.addEventListener('load', function () {
	ifr = document.querySelectorAll(".embedly-card iframe");
	for (let i = 0; i < ifr.length; i++) {
		let qu = ifr[i].contentWindow.document.querySelector('.reddit-post');
		qu.style.border = 'none'
	}
})
