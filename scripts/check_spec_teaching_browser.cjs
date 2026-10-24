#!/usr/bin/env node
/* Local-only development verification of scoped, built teaching pages. */
const fs=require('fs'),path=require('path'),http=require('http');
const {chromium}=require(process.env.PCIE_PLAYWRIGHT_PATH||'playwright');
const args=Object.fromEntries(process.argv.slice(2).reduce((out,value,index,all)=>{
  if(value.startsWith('--'))out.push([value.slice(2),all[index+1]]);return out;
},[]));
if(!args.root||!args.output)throw new Error('--root and --output are required');
const root=path.resolve(args.root),output=path.resolve(args.output);
fs.mkdirSync(output,{recursive:true});
const entries=[];
function collect(directory){
  for(const item of fs.readdirSync(directory,{withFileTypes:true})){
    const file=path.join(directory,item.name);
    if(item.isDirectory()){
      if(!['assets','node_modules','.git'].includes(item.name))collect(file);
    }else if(item.isFile()&&item.name.endsWith('.html')){
      const text=fs.readFileSync(file,'utf8');
      const head=(text.match(/<head\b[\s\S]*?<\/head>/i)||[''])[0];
      if(!/spec-teaching\.css|--st-paper/.test(head))continue;
      const match=text.match(/<(?:body|main|div)\b[^>]*class="[^"]*\bspec-teaching\b[^>]*data-spec-series="(pcie|nvme)"/);
      if(match&&(!args.series||match[1]===args.series))entries.push({file,series:match[1],url:'/'+path.relative(root,file).split(path.sep).join('/')});
    }
  }
}
collect(root);
const server=http.createServer((req,res)=>{
  let requested;
  try{requested=decodeURIComponent(req.url.split('?')[0]);}catch{res.writeHead(400).end();return;}
  let file=path.resolve(root,'.'+requested);
  if(file!==root&&!file.startsWith(root+path.sep)){res.writeHead(403).end();return;}
  if(requested.endsWith('/'))file=path.join(file,'index.html');
  fs.readFile(file,(error,data)=>{
    if(error){res.writeHead(404).end();return;}
    res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.svg':'image/svg+xml'})[path.extname(file)]||'application/octet-stream');
    res.end(data);
  });
});
function sample(entry){return /DOCS\/(?:nvme-question-bank\/identify|nvme-quick-reference\/identify|nvme-spec-report\/(?:pcie-transport-1\.4|nvm-command-set-1\.3)\/tutorial-zh-tw)\.html$/.test(entry.url);}
(async()=>{
 const results=[];let browser;
 try{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const origin='http://127.0.0.1:'+server.address().port;
  browser=await chromium.launch({headless:true,...(process.env.PCIE_BROWSER?{executablePath:process.env.PCIE_BROWSER}:{})});
  for(const entry of entries){
   const dimensions=[['desktop',1440,1000,'light'],['phone',390,844,'dark']];
   if(sample(entry))dimensions.push(['tablet',834,1194,'light'],['landscape',1194,834,'dark']);
   for(const [device,width,height,theme] of dimensions){
    const page=await browser.newPage({viewport:{width,height},colorScheme:theme,javaScriptEnabled:false,reducedMotion:'reduce'});
    await page.route('**/*',route=>route.request().url().startsWith(origin)?route.continue():route.abort());
    const result={url:entry.url,series:entry.series,device,theme,failures:[]};
    const response=await page.goto(origin+entry.url,{waitUntil:'domcontentloaded'});
    if(response.status()!==200)result.failures.push('HTTP '+response.status());
    await page.evaluate(value=>document.documentElement.setAttribute('data-theme',value),theme);
    const scope=page.locator('.spec-teaching[data-spec-series]').first();
    const metrics=await scope.evaluate(el=>{
      const style=getComputedStyle(el);
      const invalidSvg=[];
      for(const svg of el.querySelectorAll('svg')){
        if(!svg.getClientRects().length)continue;
        const view=svg.viewBox.baseVal;
        if(!view.width)continue;
        for(const text of svg.querySelectorAll('text')){
          if(!text.getClientRects().length)continue;
          const b=text.getBBox();
          if(b.x<view.x-3||b.y<view.y-3||b.x+b.width>view.x+view.width+3||b.y+b.height>view.y+view.height+3)invalidSvg.push(text.textContent.slice(0,70));
        }
      }
      return {overflow:document.documentElement.scrollWidth-innerWidth,accent:style.getPropertyValue('--st-accent').trim(),
        collapsed:[...el.querySelectorAll('details.qa-answer,details.qr-answer,details.review-question')].filter(d=>!d.open).length,
        invalidSvg,heading:el.querySelector('h2')?getComputedStyle(el.querySelector('h2')).color:null,ink:style.color};
    });
    const expected=entry.series==='nvme'?(theme==='dark'?'#79d8b4':'#086b56'):(theme==='dark'?'#81bdf0':'#145f9d');
    if(metrics.overflow>2)result.failures.push('Page overflow '+metrics.overflow);
    if(metrics.accent!==expected)result.failures.push('Series accent '+metrics.accent);
    if(metrics.collapsed)result.failures.push('Core explanations collapsed: '+metrics.collapsed);
    if(metrics.invalidSvg.length)result.failures.push('SVG labels outside view: '+metrics.invalidSvg.join('; '));
    if(metrics.heading&&metrics.heading!==metrics.ink)result.failures.push('Heading inherited an unrelated site color');
    const source=scope.locator('details.st-source,details.source-note,details.qa-source-links').first();
    if(await source.count()&&!await source.evaluate(el=>el.open)){
      await source.locator('summary').first().click();
      if(!await source.evaluate(el=>el.open))result.failures.push('Native source disclosure failed');
    }
    if(sample(entry)||result.failures.length){
      const first=scope.locator('.st-route,.diagram,.qa-overview').first();
      if(await first.count())await first.scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(output,entry.url.replace(/[^a-zA-Z0-9.-]/g,'_')+'-'+device+'-'+theme+'.png'),animations:'disabled'});
    }
    if(device==='desktop'){
      await page.emulateMedia({media:'print'});
      if(await scope.evaluate(el=>[...el.querySelectorAll('.qa-answer,.qr-answer')].some(n=>getComputedStyle(n).display==='none')))result.failures.push('Print hides a main explanation');
    }
    results.push(result);await page.close();
   }
   if(results.length%30===0)console.log('Verified '+results.length+' browser cases');
  }
  const searchable=entries.find(entry=>entry.url.endsWith('/DOCS/nvme-question-bank/identify.html'));
  if(searchable){
    const page=await browser.newPage({javaScriptEnabled:true});
    await page.route('**/*',route=>route.request().url().startsWith(origin)?route.continue():route.abort());
    await page.goto(origin+searchable.url,{waitUntil:'domcontentloaded'});
    await page.locator('#qa-search').fill('<img src=x onerror="window.__stXss=1">');
    const safe=await page.evaluate(()=>window.__stXss===undefined&&!document.querySelector('.qa-controls img'));
    results.push({url:searchable.url,device:'search-input',failures:safe?[]:['Search interpreted HTML input']});
    await page.close();
  }
 }finally{
  fs.writeFileSync(path.join(output,'browser-results.json'),JSON.stringify(results,null,2));
  if(browser)await browser.close();server.close();
 }
 const failures=results.filter(result=>result.failures.length);
 console.log(JSON.stringify({pages:entries.length,cases:results.length,failures},null,2));
 if(failures.length)process.exitCode=1;
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
