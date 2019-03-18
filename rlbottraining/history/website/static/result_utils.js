
export function formatDate(d) {
  return d.getFullYear() + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-" + ("0" + d.getDate()).slice(-2) +
      "\u2007" + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2) + ":" + ("0" + d.getSeconds()).slice(-2);
}

export function formatClassName(class_name) {
  const parts = class_name.split('.');
  if (parts.length < 2) {
    return class_name;
  }
  return `
    <span class="not-important">
      ${parts.slice(0, parts.length-1).join('.') + '.'}` +
    `</span>` +
    `<span>` +  // deliberately not leaving whitespace here
      `${parts[parts.length-1]}`+
    `</span>`
}


// XSS prevention stuff
$.extend(true, $.fn.dataTable.defaults, {
  column: {
    render(data) {  return escapeText(data);  },
  }
});
export const escapeText = $.fn.dataTable.render.text().display;
