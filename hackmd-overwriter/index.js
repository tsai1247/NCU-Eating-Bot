const puppeteer = require("puppeteer");
const fs = require("fs");
var service = {
  browser: null,
  page:    null,
  init:   false,
  url:undefined,
};


async function overwrite( { url, md } ){

  if( url != undefined )
    service.url = url;

  if(service.browser==null || refresh )
    service.browser = await puppeteer.launch();

  if( service.page == null || refresh )
    service.page = await service.browser.newPage();

  if( service.url == undefined )
    throw new Error("URL is not exist");
  await service.page.goto( service.url );
  await service.page.click('label.ui-edit');
  for(let i = 0 ; i < 9 ; i++ )
    await service.page.keyboard.press("Tab");

  await service.page.keyboard.down('Control');
  await service.page.keyboard.press('A');
  await service.page.keyboard.up('Control');
  await service.page.keyboard.press('Delete');

  let data = fs.readFileSync(md, 'utf8');
  await service.page.keyboard.type( data );
  await delay(1000);
  await service.browser.close();
}

function delay(time) {
   return new Promise(function(resolve) {
       setTimeout(resolve, time)
   });
}

exports.overwrite = overwrite;