const fs=require('fs');const s=fs.readFileSync(process.argv[2],'utf8');
const re=/<script(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)<\/script>/gi;let m,i=0,bad=[];
while((m=re.exec(s))){i++; if(/type=["'](?!text\/javascript|module)/i.test(m[1]))continue; try{new Function(m[2])}catch(e){bad.push(i+':'+e.message.slice(0,60))}}
console.log('scripts',i,'bad',bad.length,bad.join(' | '));
