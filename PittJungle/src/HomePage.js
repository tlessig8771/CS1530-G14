import React from 'react';
import Navbar from "./Navbar";
import './HomePage.css';
import sush from "./images/teampics/sush.jpeg";
import sher from "./images/teampics/Sher.jfif";
import trent from "./images/teampics/Trent.png";

function HomePage() {
  return (
  <div className = "App">
    <Navbar/>
<div class='some-page-wrapper'>
<div class='row'>
<div class='column'>
  <div class='left-column'>
  <h2 class = "a">The Issue: </h2>
  <p>-------------------------------------------------------------</p>
    <p class = "a">When students are starting college, 
      it is the first time they are on their own. 
      Students tend to focus their time on academics, 
      which although is important, can be detrimental to their 
      overall college experience. We hope our product can bridge 
      the gap between academics and leisure by introducing students 
      to dining options other than university dining halls, 
      as well as other local events and attractions. </p>
  </div>
</div>
<div class='column'>
  <div class='right-column'>
  <h2 class = "b">Our Mission: </h2>
  <p>-------------------------------------------------------------</p>
    <p class = "b">Our team will put together a product called PittJungle. 
      It will mainly be used as a navigation tool for Pitt students 
      to find local events, eateries, academic recommendations 
      and activities on and around campus. It will allow students to
       create groups and communities with people who have similar interests. 
       This will help new students create a life outside of class which is vital 
       for a college lifestyle.</p>

  </div>
</div>
</div>
</div>

    <h2 class = "team">The Team: </h2> 
    <p>----------------------------------------------------------------------------------------------------------------------------------------</p>
    <div class='team-wrapper'>
<div class='row'>
<div class='column'>
  <div class='x'>
    Sush Bansod
    <img class = "teampic" src = {sush}/>
    Project Manager
  </div>
</div>
<div class='column'>
  <div class='x'>
  Sherryl Augustine
  <img class = "teampic" src = {sher}/>
  Front End Developer
  </div>
</div>
<div class='column'>
  <div class='x'>
    Trent
    <img class = "teampic" src = {trent}/>
    Reccomender System
  </div>
</div>
<div class='column'>
  <div class='x'>
    Luiza
    <img/>
    Back-End Developer
  </div>
</div>
<div class='column'>
  <div class='x'>
   David
   <img/>
   Back-End Developer
  </div>
</div>
</div>
</div>
  </div>
  );
}
  
export default HomePage;
