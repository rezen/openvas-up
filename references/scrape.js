'use strict';

const puppeteer = require('puppeteer');

// Absolute mess ... but it works ...
// @todo change to a scraper like cheerio

const url = 'http://docs.greenbone.net/API/OMP/omp-7.0.html';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto(url);

  // Get the "viewport" of the page, as reported by the page.
  const dimensions = await page.evaluate(() => {
    function getDepth(node) {
    let depth = 1;
    let pointer = node.parentNode || {};
    while (pointer.parentNode) {
        pointer = pointer.parentNode;
        depth++;
    }
    return depth;
}
function lineToData(line) {
    let tmp = line.split(' ');
    let name = tmp[0];
    let description = tmp.slice(1).join(' ');
    const match = /\(([a-z_]+)\)/.exec(description);
    let d = {name, description};
    d.label = d.name.replace(/[\@\<\>]/g, '');

    if (d.label === 'column' || d.label === 'option') {
        tmp = description.split(' ');
        d.label = d.name = tmp[0];
        d.description = description = tmp.slice(1).join(' ');

        if (d.label === 'option') {
            d.isOption = true;
        } else {
            d.isColumn = true;
        }
    }

    if (d.description[0] === '?') {
        d.description = d.description.slice(1);
        d.optional = true;
    }

    if (match) {
        d.description = d.description.replace(match[0], '').trim();
        d.dtype = match[1];
    }
    
    if (d.dtype === 'text' && d.label === 'filter') {
        d.isFilter = true;
    }

    return d;
  }

  // get_assets
  function regroup(data) {
    let aggr = [];
    let last = {};
    let items = [];

    if (!data) {
        return [];
    }

    if (Array.isArray(data)) {
        items = data;
    } else if (Array.isArray(data.kids)) {
        items = data.kids;
    } else {
        if (data.text) {
            let tmp =  lineToData(data.text);
            for (let attr in tmp) {
                data[attr] = tmp[attr];
            }
            return data;
        }

        return data;
    }

    last = items[0];

    items.map(k => {
        let currentDepth = k.depth;

        if (currentDepth != last.depth) {

            if (!last.$attrs) {
                last.$attrs = [];
            }
            last.$attrs = last.$attrs.concat(regroup(k));
            return;
        } else {
           aggr = aggr.concat(regroup(k));
        }

        last = k;
    });
    return aggr;
  }

function fixElement(node) {
    let el = document.createElement(node.nodeName)
    el.innerHTML = node.innerHTML.replace(new RegExp('<ul style="list-style: none"><\/ul>', 'g'), '')
    .replace(/<\/?b>/g, '')
    .replace(/<\/?i>/g, '')
    .replace(/\s\s+/, ' ')
    .replace(/<a href="\#type_"><\/a>/g, '')
    .replace(/<a href="\#[a-z_]+">([a-z_-]+)<\/a>/g, '$1')
    .replace(new RegExp('<div style="margin-left: 15px; display: inline;">([A-Za-z"\'\s,\.]+)<\/div>', 'g'), '$1')
    .replace(/\n/g, ' ')
    return el;
}


function dToS(d, baseDepth) {
    if (!d.kids) {
        return d.replace(/[\n]+/g, ' ').replace(/\s\s+/, ' ')
    }

    if (d.kids.length === 0) {
        return '';
    }

    if (!baseDepth) {
        baseDepth = 0 + d.depth;
    }

    let repeats = d.depth - baseDepth;
    return  d.kids.reduce((aggr, k) => {
        line  = dToS(k, baseDepth);
        if (line.length > 0) {
            aggr += line;
        }
        return aggr;
    }, "\n" + '\t'.repeat(repeats )) + "\n"
}

function fixLine(line) {

    return line
    .replace('>', '> ')
    .replace('(', ' (')
    .replace(/\n/g, ' ')
    .replace(/\s\s+/g, ' ')
    .replace('()', '')
}

function elementData(el) {
    depth =  getDepth(el)
    let d = { nodeName: el.nodeName,  depth, kids: [],};

    if (!el) {
        return d;
    }

    if (el.nodeType === 3 && el.wholeText !== '') {
        return {text: el.wholeText.trim(), depth};
     }
     
     if (el.children.length === 0 && el.innerText !== '') {
        return {text: fixLine(el.innerText.trim()), depth};
     }
    
     if (el.childNodes) {
        let pointer = {text:"", depth};

        d.kids = Array.from(el.childNodes).reduce((aggr2, k) => {
           let d2 =  elementData(k);
            if (d2.text !== undefined) {
                if(k.nodeName === '#text' || k.nodeName === 'DIV') {
                pointer.text += d2.text;
                return aggr2;
                }

                if (d2.text.length === 0) {
                    return aggr2;
                }
            }
            pointer.text = fixLine(pointer.text);
            if (pointer.text.length > 0) {
                aggr2.push(Object.assign({}, pointer));
                pointer = {text:"", depth };
            }

            aggr2.push(d2);
           return aggr2;
         }, []);

        pointer.text = fixLine(pointer.text);
        
        if (pointer.text.length !== 0) {    
           d.kids.push(pointer);
         }
     
        const ignore = ['Response','Command', '']
         d.kids = d.kids
            .filter(k => 
                !k.text || (k.text.trim() !== '' && 
                ignore.indexOf(k.text.trim()) === -1) && 
                k.text.indexOf('Keywords') === -1  && 
                k.text.indexOf('Empty') === -1 &&
                k.text.indexOf('One of') == -1
            )

         if (d.kids.length === 1 ) { 
            d = d.kids[0];

            if (d.kids) {
                d.kids = d.kids
                .filter(k => !k.text || (k.text.trim() !== '' && ignore.indexOf(k.text.trim()) === -1))
            }
         }
     }
     return d;
}

    function getExampleFromParent(parent) {
        let res = '';
        let req = '';
        try {
            req =  Array.from(parent.children).pop().children[1].innerText;
        } catch(e) {}

        try {
            res =  Array.from(parent.children).pop().children[3].innerText;
        } catch(e) {}

        return {req, res};
    }

    Array.from(document.querySelectorAll('pre')).map(p => {
        if (p.innerText.trim()[0] !== '<') {
            p.parentNode.removeChild(p)
        }
    })

    return Array
        .from(document.querySelectorAll('div > h3[id]'))
        .filter(el => el.getAttribute('id').indexOf('command_') !== -1)
        .map(function(el) {
            return {
                parent: el.parentNode.parentNode, 
                label: el.getAttribute('id'),
                list: []
            }
        })
        .filter(el => el.label.indexOf('command_') === 0)
        .map(el => {
            el.label = el.label.replace('command_', '');
            const parts = el.label.split('_');
            el.action = parts.shift()
            el.entity = parts.join('_');

            if (el.action === 'get' && el.entity.substr(-1) === 's' && el.entity.substr(-2) !== 'es') {
                el.entity = el.entity.slice(0, -1);
            }

            el.request = Array.from(el.parent.children)
                .filter(c => c.nodeName === 'UL')
                .map(c => {
                    let dmz = {
                        req: regroup(elementData(fixElement(c.children[0]))),
                        res: regroup(elementData(fixElement(c.children[1]))),
                    };
                    return dmz;

                }).pop();
           
            el.example = getExampleFromParent(el.parent);
            delete el.parent;
            return el;
        });
  });

  const REGEX_TYPE = /\(([a-z_]+)\)/;

  function lineToData(line) {
    let tmp = line.replace(/\n/g, ' ').replace('()', '').split(' ');
    let name = tmp[0];
    let description = tmp.slice(1).join(' ');
    const match = REGEX_TYPE.exec(description);
    let d = {name, description};
    d.label = d.name.replace(/[\@\<\>]/g, '');

    if (d.description[0] === '?') {
        d.description = d.description.slice(1);
        d.optional = true;
    }

    if (match) {
        d.description = d.description.replace(match[0], '').trim();
        d.dtype = match[1];
    } else {
        d.dtype = d.label;
    }
    
    if (d.dtype === 'text' && d.label === 'filter') {
        d.isFilter = true;
    }

    return d;
  }

  let z = dimensions.reduce((aggregate, d) => {

    if (!aggregate[d.entity]) {
        aggregate[d.entity] = [];
    }

    aggregate[d.entity].push(d);
    return aggregate;
  }, {})

  console.log(JSON.stringify(z, null, 2));

  browser.close();
  
})();