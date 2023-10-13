// Fills in <header> content for html pages with header_content to connect js to html
// -> .js file inserts header_content into .html file -> header appears on website pages

//1. finds header by class=headercontent in html file
const header = document.querySelector(".headercontent");

//2. writes in header_content
const header_content = `
<div>
  <span class="siteheader logo">
    <a href="index.html"><img src="Images/header_logo.png" alt="Liu Group Logo"></a>
  </span>
  <ul>
    <li><a href="index.html">HOME</a></li>
    <li><a href="search.html">SEARCH</a></li>
    <li><a href="about.html">ABOUT</a></li>
    <li><a href="news.html">NEWS</a></li>
  </ul>
</div>
<br>
  `;

//test to see if js is connected to html
// const test_content = `<p>hello</p>`;
// can combine `` variables, then send to html file
// const test_content_two = `<h1>hi<h1>`;
// var combined_content = test_content + test_content_two;

//3. returns table_content inside <header> on html file
header.innerHTML = header_content;

// to not completely replace main, use document.createElement("stuff");
// add things
// stuff.innerHTML = content;
// main.append(stuff);
