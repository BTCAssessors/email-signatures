/**
 * Resizes an iframe passed as argument, based on its content, plus a margin
 */
function resizeIframe(obj, margin = 20) {
  obj.style.height =
    obj.contentWindow.document.body.scrollHeight + margin + 'px';
  obj.style.width =
    obj.contentWindow.document.body.scrollWidth + margin + 'px';
}

/**
 * Given the _id_ of an `iframe`, creates a link after this `iframe`
 * that allows to download the _HTML_ source code of this `iframe`.
 *
 * _name_ argument allows to set the downloaded file name
 *        .html extension is added automagically
 * _text_ argument sets the link text
 * _classes_ allow to specify the links classes
 */
function create_signature_download_link(id, name, text, classes = "") {
  // Get iframe's code
  var iframe = document.getElementById(id);
  var html_code = iframe.contentWindow.document.body.innerHTML;
  // Create link
  var link = document.createElement('a');
  link.setAttribute('download', name + ".html");
  link.setAttribute('href', 'data:text/html;charset=utf-8,' +
    encodeURIComponent(html_code));
  link.setAttribute("class", classes);
  link.innerHTML = text;
  // Append link
  iframe.parentNode.appendChild(link);
}
