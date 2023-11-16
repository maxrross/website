//const main = document.querySelector(".mainpagecontent");

//const content = `
//<h1>${}</h1>;

//`;

//main.innerHTML = content;

//Intersection Observer
//access documentation for intersection observer here: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API
//used code from Coding in Public's tuturial; access here: https://www.youtube.com/watch?v=m8WLd37Y9Ew
const h1 = document.querySelector("#turnRed"); //TODO
const p = document.querySelector("#turnRed1");

function h1Callback(entries) {
  //hexagon.classList.toggle("opacity-100", !entries[0].isIntersecting);
  //hexagon.classList.toggle("text-myRed", !entries[0].isIntersecting);
  h1.classList.toggle("bg-myRed", !entries[0].isIntersecting);
  p.classList.toggle("bg-myRed", !entries[0].isIntersecting);
  //console.log(entries[0].isIntersecting);
}
const h1Options = {};
const h1Obs = new IntersectionObserver(h1Callback, h1Options);

h1Obs.observe(document.querySelector("header"));

//first hex
const hexagon = document.querySelector("#hex-fade"); //TODO

function hexCallback(entries) {
  //hexagon.classList.toggle("text-myRed", !entries[0].isIntersecting);
  hexagon.classList.toggle("opacity-0", entries[0].isIntersecting);
  //hexagon.classList.toggle("opacity-0", !entries[0].isIntersecting);
  //console.log(entries[0].isIntersecting);
}
const hexOptions = { threshold: 0.5 };
const hexObs = new IntersectionObserver(hexCallback, hexOptions);

hexObs.observe(document.querySelector("section"));

//second hex
const hexagon2 = document.querySelector("#hex-fade2");

function hexCallback2(entries) {
  //hexagon.classList.toggle("text-myRed", !entries[0].isIntersecting);
  hexagon2.classList.toggle("opacity-0", entries[0].isIntersecting);
  //hexagon2.classList.toggle("opacity-0", !entries[0].isIntersecting);
  //console.log(entries[0].isIntersecting);
}
const hexOptions2 = { threshold: 0.85 };
const hexObs2 = new IntersectionObserver(hexCallback2, hexOptions2);

hexObs2.observe(document.querySelector("#hex-fade"));

//third hex
const hexagon3 = document.querySelector("#hex-fade3");

function hexCallback3(entries) {
  //hexagon.classList.toggle("text-myRed", !entries[0].isIntersecting);
  hexagon3.classList.toggle("opacity-0", entries[0].isIntersecting);
  //console.log(entries[0].isIntersecting);
}
const hexOptions3 = { threshold: 0.85 };
const hexObs3 = new IntersectionObserver(hexCallback3, hexOptions3);

hexObs3.observe(document.querySelector("#hex-fade2"));

//fourth hex
const hexagon4 = document.querySelector("#hex-fade4");

function hexCallback4(entries) {
  hexagon4.classList.toggle("opacity-0", entries[0].isIntersecting);
}
const hexOptions4 = { threshold: 0.85 };
const hexObs4 = new IntersectionObserver(hexCallback4, hexOptions4);

hexObs4.observe(document.querySelector("#hex-fade3"));

//fifth hex
const hexagon5 = document.querySelector("#hex-fade5");

function hexCallback5(entries) {
  hexagon5.classList.toggle("opacity-0", entries[0].isIntersecting);
}
const hexOptions5 = { threshold: 0.85 };
const hexObs5 = new IntersectionObserver(hexCallback5, hexOptions5);

hexObs5.observe(document.querySelector("#hex-fade4"));

//sixth hex
const hexagon6 = document.querySelector("#hex-fade6");

function hexCallback6(entries) {
  hexagon6.classList.toggle("opacity-0", entries[0].isIntersecting);
}
const hexOptions6 = { threshold: 0.85 };
const hexObs6 = new IntersectionObserver(hexCallback6, hexOptions6);

hexObs6.observe(document.querySelector("#hex-fade5"));

//first tool
const tool = document.querySelector("#tool");

function toolCallback(entries) {
    tool.classList.toggle("text-myWhite", entries[0].isIntersecting);
  tool.classList.toggle("text-myRed", !entries[0].isIntersecting);
}
const toolOptions = { threshold: 0.9 };
const toolObs = new IntersectionObserver(toolCallback, toolOptions);

toolObs.observe(document.querySelector("#hex-fade6"));

//second tool
const tool2 = document.querySelector("#tool2");

function toolCallback2(entries) {
    tool2.classList.toggle("text-myWhite", entries[0].isIntersecting);
  tool2.classList.toggle("text-myRed", !entries[0].isIntersecting);
}
const toolOptions2 = { threshold: 0.5 };
const toolObs2 = new IntersectionObserver(toolCallback2, toolOptions2);

toolObs2.observe(document.querySelector("#tool"));

//third tool
const tool3 = document.querySelector("#tool3");

function toolCallback3(entries) {
    tool3.classList.toggle("text-myWhite", entries[0].isIntersecting);
  tool3.classList.toggle("text-myRed", !entries[0].isIntersecting);
}
const toolOptions3 = { threshold: 0.5 };
const toolObs3 = new IntersectionObserver(toolCallback3, toolOptions3);

toolObs3.observe(document.querySelector("#tool2"));
