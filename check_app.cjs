const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
class Element{
 constructor(){this.value='';this.hidden=true;this.attrs={};this.listeners={};this.validity='';this.textContent='';this.classes=new Set();this.classList={add:x=>this.classes.add(x),remove:x=>this.classes.delete(x),toggle:(x,b)=>b?this.classes.add(x):this.classes.delete(x)};}
 addEventListener(name,fn){(this.listeners[name]??=[]).push(fn);}
 setAttribute(k,v){this.attrs[k]=v;}getAttribute(k){return this.attrs[k];}
 setCustomValidity(s){this.validity=s;}reportValidity(){this.reported=true;}
 querySelectorAll(){return [];}
 fire(name){for(const fn of this.listeners[name]??[])fn({preventDefault(){},target:this});}
}
const selectors=['.menu-toggle','nav','#when','#from','#to','#trip-result','#trip-form','#trip-text','#send-whatsapp','#copy','#passengers','.scroll-progress'];
const el=Object.fromEntries(selectors.map(s=>[s,new Element()]));
const doc={querySelector:s=>el[s]??null,querySelectorAll:()=>[],addEventListener(){},documentElement:{scrollHeight:1000,classList:{remove(){},add(){}}}};
const win={matchMedia:()=>({matches:true,addEventListener(){}}),addEventListener(){},innerHeight:800,scrollY:0};
el['.scroll-progress'].style={};
vm.runInNewContext(fs.readFileSync('dist/app.js','utf8'),{document:doc,window:win,Date,Number,encodeURIComponent,navigator:{clipboard:{writeText:async()=>{}}},requestAnimationFrame:fn=>fn()});
el['.menu-toggle'].fire('click');assert.equal(el['.menu-toggle'].attrs['aria-expanded'],'true');el['.menu-toggle'].fire('click');assert.equal(el['.menu-toggle'].attrs['aria-expanded'],'false');
el['#from'].value='Hıdırlık 70 Sokak No:5';el['#to'].value='Sığacık';el['#passengers'].value='2 kişi';el['#when'].value=new Date(Date.now()+86400000).toISOString().slice(0,16);
el['#trip-form'].fire('submit');
assert.equal(el['#trip-result'].hidden,false);
assert.match(el['#send-whatsapp'].href,/^https:\/\/wa\.me\/905512182244\?text=/);
const msg=decodeURIComponent(el['#send-whatsapp'].href.split('?text=')[1]);assert.ok(msg.includes('Sığacık')&&msg.includes('Hıdırlık 70 Sokak No:5')&&msg.includes('2 kişi'));
el['#from'].fire('input');assert.equal(el['#trip-result'].hidden,true);
el['#from'].value='   ';el['#trip-form'].fire('submit');assert.notEqual(el['#from'].validity,'');assert.equal(el['#trip-result'].hidden,true);
el['#from'].value='Akarca';el['#from'].fire('input');el['#when'].value='2020-01-01T10:00';el['#trip-form'].fire('submit');assert.notEqual(el['#when'].validity,'');
el['#when'].fire('input');assert.equal(el['#when'].validity,'');
console.log('PASS: mobile menu, encoded WhatsApp request, stale result hiding, empty address and past-date validation. No external message sent.');
