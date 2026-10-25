(()=>{
 'use strict';
 const $=s=>document.querySelector(s);
 const toggle=$('.menu-toggle'),nav=$('nav');
 const closeMenu=()=>{nav?.classList.remove('open');toggle?.setAttribute('aria-expanded','false');toggle?.setAttribute('aria-label','Menüyü aç');};
 toggle?.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Menüyü kapat':'Menüyü aç');nav?.classList.toggle('open',open);});
 nav?.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
 document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeMenu();}});
 const when=$('#when'),from=$('#from'),to=$('#to'),result=$('#trip-result');
 let note='';
 const localMinute=()=>{const d=new Date();d.setMinutes(d.getMinutes()-d.getTimezoneOffset());return d.toISOString().slice(0,16);};
 if(when){when.min=localMinute();when.addEventListener('focus',()=>{when.min=localMinute();});}
 [when,from,to].forEach(input=>input?.addEventListener('input',()=>{input.setCustomValidity('');if(result)result.hidden=true;}));
 $('#passengers')?.addEventListener('change',()=>{if(result)result.hidden=true;});
 $('#trip-form')?.addEventListener('submit',e=>{
  e.preventDefault();
  const date=new Date(when.value);
  for(const input of [from,to]){
   if(!input.value.trim()){input.setCustomValidity('Lütfen bir adres veya buluşma noktası yazın.');input.reportValidity();return;}
  }
  if(!Number.isFinite(date.getTime())||date<new Date()){
   when.setCustomValidity('Lütfen gelecek bir tarih ve saat seçin.');when.reportValidity();return;
  }
  note=`Merhaba, Seferihisar Taksi 7/24 için yolculuk talebim var.\nHareket: ${from.value.trim()}\nVarış: ${to.value.trim()}\nTarih: ${date.toLocaleString('tr-TR')}\nYolcu: ${$('#passengers').value}\nAraç ve saat uygunluğunu öğrenmek istiyorum.`;
  $('#trip-text').textContent=note;
  $('#send-whatsapp').href='https://wa.me/905512182244?text='+encodeURIComponent(note);
  $('#copy').textContent='Notu kopyala ↗';
  result.hidden=false;
 });
 $('#copy')?.addEventListener('click',async e=>{
  try{await navigator.clipboard.writeText(note);e.target.textContent='Kopyalandı ✓';}
  catch{e.target.textContent='Metni seçip kopyalayabilirsiniz';const range=document.createRange();range.selectNodeContents($('#trip-text'));const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);}
 });
 const reduced=window.matchMedia('(prefers-reduced-motion: reduce)');
 const revealTargets=document.querySelectorAll('.section-heading,.services article,.regions-intro,.region-links,.planner>div,.planner form,.faq>div,.local>div,.statement,.contact>div');
 if(!reduced.matches&&'IntersectionObserver' in window){
  revealTargets.forEach(el=>el.classList.add('reveal'));
  const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('visible');observer.unobserve(entry.target);}}),{threshold:.08,rootMargin:'0px 0px -20px 0px'});
  revealTargets.forEach(el=>observer.observe(el));
  document.documentElement.classList.add('motion-ready');
  // Content always returns if motion preference changes at runtime.
  reduced.addEventListener('change',()=>{document.documentElement.classList.remove('motion-ready');});
 }
 const progress=$('.scroll-progress');let scheduled=false;
 const updateScroll=()=>{scheduled=false;const extent=document.documentElement.scrollHeight-window.innerHeight;if(progress)progress.style.transform=`scaleX(${extent>0?Math.min(1,Math.max(0,window.scrollY/extent)):0})`;};
 window.addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(updateScroll);}},{passive:true});
 updateScroll();
 const art=$('.hero-art');let artFrame=0;
 if(art&&!reduced.matches&&matchMedia('(pointer:fine)').matches){
  art.addEventListener('pointermove',e=>{if(artFrame)return;const x=e.clientX,y=e.clientY;artFrame=requestAnimationFrame(()=>{const r=art.getBoundingClientRect();art.style.animation='none';art.style.transform=`perspective(1200px) rotateY(${(x-r.left)/r.width*10-10}deg) rotateX(${4-(y-r.top)/r.height*6}deg)`;artFrame=0;});});
  art.addEventListener('pointerleave',()=>{if(artFrame){cancelAnimationFrame(artFrame);artFrame=0;}art.style.transform='';});
 }
})();
