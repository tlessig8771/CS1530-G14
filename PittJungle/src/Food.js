import React from 'react';
import Navbar from "./Navbar";
import './Format.css';

// Fast food Import statements
import wendy from "./images/Food/Wendy.jpg";
import McD from "./images/Food/Mcdonald.png";
import TB from "./images/Food/Tacobell.png";
import piada from "./images/Food/Piada.png";
import Chip from "./images/Food/Chipotle.png";
import CFA from "./images/Food/chickfila.jpg";
import PB from "./images/Food/PB.jpg";
import BK from "./images/Food/Burger-King.jpg";

//Pizza import statement
import ph from "./images/Food/pizzahut.jpg";
import Sr from "./images/Food/Sorrentos.jfif";
import pr from "./images/Food/pieexpress.jpg";
import lot from "./images/Food/lotsa.jpg";

//Chinese/Korean import
import sf from "./images/Food/sushifuku.jpg";
import gpb from "./images/Food/GPB.jfif";
import cb from "./images/Food/cb.jpeg";
import ob from "./images/Food/bento.jfif";

//Dine In imports
import mm from "./images/Food/madmex.png";
import std from "./images/Food/stackd.jpg";
import prim from "./images/Food/primantis.jpg";
import noods from "./images/Food/noods.png";



function Food() {
    return (
      <div class = "food">
        <Navbar/>
        <h2 class= "Heading">Let's Eat!</h2>   

        <p>--------------------------------------------------------------------
          --------------------------------------------------------------------</p>
        <div class= "sec1"> 
        <h3>Fast Food</h3>
        <div class = "row">
        <div class = "element"><img class = "item" src = {wendy}></img></div>
        <div class = "element"><img class = "item" src = {McD}></img></div>
        <div class = "element"><img class = "item" src = {TB}></img></div>
        <div class = "element"><img class = "item" src = {piada}></img></div>
        <div class = "element"><img class = "item" src = {BK}></img></div>
        <div class = "element"><img class = "item" src = {Chip}></img></div>
        <div class = "element"><img class = "item" src = {CFA}></img></div>
        <div class = "element"><img class = "item" src = {PB}></img></div>
        </div>
        </div>

        <div class= "sec2"> 
        <h3>Pizza</h3>
        <div class = "row">
        <div class = "element"><img class = "item" src = {ph}></img></div>
        <div class = "element"><img class = "item" src = {Sr}></img></div>
        <div class = "element"><img class = "item" src = {pr}></img></div>
        <div class = "element"><img class = "item" src = {lot}></img></div>
        </div>
        </div>


        <div class= "sec3"> 
        <h3>Chinese/Korean</h3>
        <div class = "row">
        <div class = "element"><img class = "item" src = {sf}></img></div>
        <div class = "element"><img class = "item" src = {gpb}></img></div>
        <div class = "element"><img class = "item" src = {cb}></img></div>
        <div class = "element"><img class = "item" src = {ob}></img></div>
        </div>
        </div>

        <div class= "sec4"> 
        <h3>Dine-In</h3>
        <div class = "row">
        <div class = "element"><img class = "item" src = {mm}></img></div>
        <div class = "element"><img class = "item" src = {std}></img></div>
        <div class = "element"><img class = "item" src = {prim}></img></div>
        <div class = "element"><img class = "item" src = {noods}></img></div>
        </div>
        </div>
      
      {/* Here is where you will add the next section */}
      </div>
    )
}

export default Food;
