(function(){
  function init(){
    document.querySelectorAll('.nav-links .dropdown').forEach(function(dd){
      var trigger = dd.querySelector(':scope > a');
      if(!trigger) return;
      trigger.addEventListener('click', function(e){
        if(window.innerWidth < 980 || !window.matchMedia('(hover: hover)').matches || e.target.closest('.dropdown-menu')) return;
        var isOpen = dd.classList.contains('open');
        document.querySelectorAll('.nav-links .dropdown.open').forEach(function(o){ if(o!==dd) o.classList.remove('open'); });
        if(!isOpen){ e.preventDefault(); dd.classList.add('open'); }
        else { dd.classList.remove('open'); }
      });
    });
    document.addEventListener('click', function(e){
      if(!e.target.closest('.nav-links .dropdown')){
        document.querySelectorAll('.nav-links .dropdown.open').forEach(function(o){ o.classList.remove('open'); });
      }
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape'){
        document.querySelectorAll('.nav-links .dropdown.open').forEach(function(o){ o.classList.remove('open'); });
      }
    });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
