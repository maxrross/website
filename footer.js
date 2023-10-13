// Fills in <footer> content for html pages with footer_content to connect js to html
// -> .js file inserts footer_content into .html file -> footer appears on website pages

//1. finds footer by class=footercontent in html file
const footer = document.querySelector(".footercontent");

//2. writes in footer_content
const footer_content = `
        <p>
          Created by Liu Research Group at University of Florida
          <hr>
          <a href="https://liu.chem.ufl.edu/research/">Learn more about our research</a>
        </p>
`;

//test to see if js is connected to html
// const test_content = `<p>hello</p>`;
// can combine `` variables, then send to html file
// const test_content_two = `<h1>hi<h1>`;
// var combined_content = test_content + test_content_two;

//3. returns table_content inside <footer> on html file
footer.innerHTML = footer_content;

// to not completely replace main, use document.createElement("stuff");
// add things
// stuff.innerHTML = content;
// main.append(stuff);
