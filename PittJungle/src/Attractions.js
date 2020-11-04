import React from 'react'
import Navbar from './Navbar'
import './Format.css'

import Cathy from './images/attractions/Cathy.jpg'
import Phipps from './images/attractions/Phipps.jpg'
import Randyland from './images/attractions/Randyland.jpg'
import Soldiers from './images/attractions/Soldiers.jpg'
import Warhol from './images/attractions/Warhol.jpeg'
import ScienceCenter from './images/attractions/ScienceCenter.jpeg'
import Mattress from './images/attractions/Mattress.jpeg'
import Aviary from './images/attractions/Aviary.jpg'
import Heinz from './images/attractions/Heinz.jpeg'
import PNC from './images/attractions/PNC.jpeg'
import PPG from './images/attractions/PPG.jpeg'
import ArtMuseum from './images/attractions/ArtMuseum.jpeg'
import Zoo from './images/attractions/Zoo.jpeg'
import Ohiopyle from './images/attractions/Ohiopyle.jpeg'
import HeinzHistory from './images/attractions/HeinzHistory.jpeg'
import Aquarium from './images/attractions/Aquarium.jpg'
import EscapeRoom from './images/attractions/EscapeRoom.png'
import Peterson from "./images/attractions/Peterson.jpg"

function Attractions() {
return (
<div class = "Attractions">
<Navbar/>
<h2 class= "Heading">Welcome to Pitt!</h2>

<p>--------------------------------------------------------------------
--------------------------------------------------------------------</p>
<div class= "sec1">
<h3>Art, History and Science</h3>
<div class = "row">
<div class = "element"><img class = "item" src = {ArtMuseum}></img><p>Carnegie Museum of Art</p></div>
<div class = "element"><img class = "item" src = {HeinzHistory}></img></div>
<div class = "element"><img class = "item" src = {Randyland}></img></div>
<div class = "element"><img class = "item" src = {Soldiers}></img></div>
<div class = "element"><img class = "item" src = {Warhol}></img></div>
<div class = "element"><img class = "item" src = {ScienceCenter}></img></div>
<div class = "element"><img class = "item" src = {Mattress}></img></div>
</div>
</div>

<div class= "sec2">
<h3>Nature</h3>
<div class = "row">
<div class = "element"><img class = "item" src = {Aviary}></img></div>
<div class = "element"><img class = "item" src = {Phipps}></img></div>
<div class = "element"><img class = "item" src = {Zoo}></img></div>
<div class = "element"><img class = "item" src = {Aquarium}></img></div>
</div>
</div>


<div class= "sec3">
<h3>Sports and Adventure</h3>
<div class = "row">
<div class = "element"><img class = "item" src = {PPG}></img></div>
<div class = "element"><img class = "item" src = {Heinz}></img></div>
<div class = "element"><img class = "item" src = {Ohiopyle}></img></div>
<div class = "element"><img class = "item" src = {EscapeRoom}></img></div>
<div class = "element"><img class = "item" src = {Peterson}></img></div>
<div class = "element"><img class = "item" src = {PNC}></img></div>
</div>
</div>

</div>
)
}

export default Attractions;