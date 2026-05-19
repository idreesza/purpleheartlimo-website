(function(){
  var CLOSE_DELAY = 600;
  var closeTimer = null;
  function clearTimer(){ if(closeTimer){ clearTimeout(closeTimer); closeTimer = null; } }
  function closeAll(){
    document.querySelectorAll('.nav-links .dropdown.open').forEach(function(o){ o.classList.remove('open'); });
  }
  function scheduleClose(dd){
    clearTimer();
    closeTimer = setTimeout(function(){ dd.classList.remove('open'); }, CLOSE_DELAY);
  }
  function init(){
    document.querySelectorAll('.nav-links .dropdown').forEach(function(dd){
      var trigger = dd.querySelector(':scope > a');
      if(!trigger) return;
      trigger.addEventListener('click', function(e){
        if(window.innerWidth < 980 || !window.matchMedia('(hover: hover)').matches || e.target.closest('.dropdown-menu')) return;
        var isOpen = dd.classList.contains('open');
        document.querySelectorAll('.nav-links .dropdown.open').forEach(function(o){ if(o!==dd) o.classList.remove('open'); });
        clearTimer();
        if(!isOpen){ e.preventDefault(); dd.classList.add('open'); }
        else { dd.classList.remove('open'); }
      });
      dd.addEventListener('mouseenter', function(){ clearTimer(); });
      dd.addEventListener('mouseleave', function(){
        if(dd.classList.contains('open')) scheduleClose(dd);
      });
    });
    document.addEventListener('click', function(e){
      if(!e.target.closest('.nav-links .dropdown')){
        clearTimer();
        closeAll();
      }
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape'){ clearTimer(); closeAll(); }
    });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
